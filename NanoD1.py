#!/usr/bin/env python3
"""
NanoD1.py  -  Gerber zip to realistic board renders.

    python NanoD1.py NanoD1.zip
    python NanoD1.py NanoD1.zip -t blue -d 600

Renders every layer separately with an explicit colour, forces them
all onto one common bounding box, and stacks them itself.  Nothing
depends on gerbonara's compositing.

STACKING, bottom of the image upward
    1  substrate      solid rectangle in the mask colour
    2  copper         dimmed - traces showing through the mask
    3  mask openings  pad colour - where mask is absent, bare metal
    4  silkscreen     ink
    5  drill holes    punched through
    6  board edge     thin dark line

INSTALL
    pip install gerbonara
    pip install cairosvg      # optional, PNG output only
"""

import argparse
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

# ----------------------------------------------------------------------
#   substrate  board colour where mask sits on plain laminate
#   copper     copper seen through the mask - a darker substrate
#   pad        exposed metal in mask openings
#   silk       silkscreen ink
#   hole       drilled holes
# ----------------------------------------------------------------------
THEMES = {
    # 'copper' is deliberately well separated from 'substrate'.  A real
    # board shows very little contrast between copper-under-mask and bare
    # laminate, which looks realistic and reads terribly.  These are tuned
    # for legibility - use --realistic if you want the subtle version.
    'black':  dict(substrate='#161616', copper='#4a4238', pad='#d9b45b',
                   silk='#f2f2f0', hole='#000000'),
    'blue':   dict(substrate='#0b3268', copper='#1e63b8', pad='#d9b45b',
                   silk='#ffffff', hole='#04152b'),
    'green':  dict(substrate='#0a4a2c', copper='#178a53', pad='#d9b45b',
                   silk='#ffffff', hole='#031f12'),
    'red':    dict(substrate='#75121c', copper='#bd2a38', pad='#d9b45b',
                   silk='#ffffff', hole='#2e0709'),
    'purple': dict(substrate='#3b2952', copper='#6b4d94', pad='#d9b45b',
                   silk='#ececec', hole='#170f20'),
    'white':  dict(substrate='#f0eee9', copper='#c2bbac', pad='#c9a13f',
                   silk='#1a1a1a', hole='#6e6e6a'),
    'yellow': dict(substrate='#c9a227', copper='#8a6f14', pad='#d9b45b',
                   silk='#1a1a1a', hole='#4a3a0c'),
}

# Subtle, photo-accurate alternative: copper barely differs from the board.
REALISTIC = {
    'black':  '#221f1b', 'blue':  '#0e3a75', 'green': '#0c5433',
    'red':    '#82161f', 'purple':'#432f5c', 'white': '#e3ded2',
    'yellow': '#b8931f',
}

HASL_PAD = '#c6c8cc'          # --finish hasl

PATTERNS = [
    ('drill',    [r'-plated\.txt$', r'-nonplated\.txt$', r'\.drl$',
                  r'drill.*\.txt$', r'\.xln$', r'\.exc$']),
    ('top_cu',   [r'\.gtl$', r'f[_.]?cu\.gbr$', r'top[_-]?copper']),
    ('bot_cu',   [r'\.gbl$', r'b[_.]?cu\.gbr$', r'bottom[_-]?copper']),
    ('top_mask', [r'\.gts$', r'f[_.]?mask\.gbr$', r'top[_-]?mask']),
    ('bot_mask', [r'\.gbs$', r'b[_.]?mask\.gbr$', r'bottom[_-]?mask']),
    ('top_silk', [r'\.gto$', r'f[_.]?silks', r'top[_-]?silk']),
    ('bot_silk', [r'\.gbo$', r'b[_.]?silks', r'bottom[_-]?silk']),
    # .GM1 ahead of .GM: Altium puts only the outer edge in .GM, while
    # Mechanical 1 also carries internal cut-outs.  Take the one with holes.
    # Altium splits these: .GM holds the outer board profile, Mechanical 1
    # (.GM1) holds internal cut-outs.  Render both or the window vanishes.
    ('outline',  [r'\.gm1$', r'\.gko$', r'\.gml$', r'edge[_.]?cuts',
                  r'outline']),
    ('outline2', [r'\.gm$', r'\.gbr$']),
]

JUNK = re.compile(
    r'(status\s*report|\.rep$|\.drr$|\.apr$|\.apr_lib$|\.extrep$|\.rul$'
    r'|\.ldp$|\.net$|\.drc$|\.html?$|\.cam$|\.pdf$|\.gd1$|\.gg1$|readme'
    r'|\.g[1-9]$|\.gp[1-9]$|\.gtp$|\.gbp$|\.gm[2-9]$|\.gm[1-9][0-9]$|\.[1-9]$)',
    re.I)


def classify(files):
    """Role-outer, pattern-inner, so pattern priority wins over filename order."""
    cand = [f for f in sorted(files) if not JUNK.search(f.name.lower())]
    found, taken = {}, set()
    for role, pats in PATTERNS:
        if role == 'drill':
            found[role] = []
            for pat in pats:
                hits = [f for f in cand if f not in taken and re.search(pat, f.name.lower())]
                for hit in hits:
                    found[role].append(hit)
                    taken.add(hit)
        else:
            for pat in pats:
                hit = next((f for f in cand
                            if f not in taken and re.search(pat, f.name.lower())),
                           None)
                if hit:
                    found[role] = hit
                    taken.add(hit)
                    break
    return found, [f for f in cand if f not in taken]


def extract(zip_path, dest):
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dest)
    flat = Path(dest) / '_flat'
    flat.mkdir(exist_ok=True)
    out = []
    for p in Path(dest).rglob('*'):
        if p.is_file() and flat not in p.parents:
            t = flat / p.name
            if not t.exists():
                shutil.copy2(p, t)
            out.append(t)
    return flat, out


def load(path, is_drill=False):
    from gerbonara import GerberFile, ExcellonFile
    return (ExcellonFile.open(str(path)) if is_drill
            else GerberFile.open(str(path)))


def union_bounds(objs):
    x0 = y0 = float('inf')
    x1 = y1 = float('-inf')
    flat_objs = []
    for o in objs:
        if isinstance(o, list):
            flat_objs.extend(o)
        else:
            flat_objs.append(o)
    for o in flat_objs:
        try:
            (a, b), (c, d) = o.bounding_box()
        except Exception:
            continue
        x0, y0 = min(x0, a), min(y0, b)
        x1, y1 = max(x1, c), max(y1, d)
    return None if x0 == float('inf') else ((x0, y0), (x1, y1))


def apply_aspect(x, y, w, h, aspect):
    if not aspect: return x, y, w, h
    try:
        num, den = map(float, aspect.replace(':', ' ').replace('/', ' ').split())
        target_ar = num / den
    except:
        return x, y, w, h
    current_ar = w / h
    if current_ar < target_ar:
        pw, ph = h * target_ar, h
    else:
        pw, ph = w, w / target_ar
    return x + w/2 - pw/2, y + h/2 - ph/2, pw, ph


INNER = re.compile(r'<svg[^>]*>(.*)</svg>', re.S | re.I)
VIEWBOX = re.compile(r'viewBox\s*=\s*"([^"]+)"', re.I)


DEBUG = False


def layer_svg(obj, fg, bounds, label='', bg='none'):
    """Render one layer with gerbonara.

    gerbonara paints CLEAR-polarity regions - the knockouts that form
    thermal reliefs and trace clearances inside a copper pour - as
    separate elements filled with the bg colour.  Pass bg='none' and
    those knockouts become invisible, so a ground pour renders as one
    solid sheet.  That was the bottom-layer bug.

    We render with sentinel colours, then swap them for the real ones,
    so we can count exactly how many knockouts were produced.
    """
    FG_SENTINEL = '#ff00ff'
    BG_SENTINEL = '#00ff00'

    kw = dict(fg=FG_SENTINEL, bg=BG_SENTINEL)
    if bounds:
        kw['force_bounds'] = bounds

    try:
        raw = str(obj.to_svg(**kw))
    except TypeError:
        try:
            raw = str(obj.to_svg(fg=FG_SENTINEL, bg=BG_SENTINEL))
        except Exception as e:
            print(f"      [!] {label}: {e}")
            return None, None, 0
    except Exception as e:
        print(f"      [!] {label}: {e}")
        return None, None, 0

    m = INNER.search(raw)
    if not m:
        print(f"      [!] {label}: no <svg> wrapper")
        return None, None, 0
    inner = m.group(1)
    v = VIEWBOX.search(raw)

    n_fg = inner.count(FG_SENTINEL)
    n_bg = inner.count(BG_SENTINEL)

    inner = inner.replace(FG_SENTINEL, fg)
    inner = inner.replace(BG_SENTINEL, bg)

    if DEBUG:
        print(f"        {label}: {n_fg} solid, {n_bg} knockout, "
              f"{len(inner)} chars")
    elif n_bg:
        print(f"      {label}: {n_fg} solid + {n_bg} knockouts")

    return inner, (v.group(1) if v else None), n_bg


# layer roles are named top_* / bot_*, but the sides are called
# 'top' and 'bottom'.  Map one to the other or every bottom lookup
# silently misses and the whole side renders empty.
SIDE_PREFIX = {'top': 'top', 'bottom': 'bot'}


def build(side, objs, theme, bounds, copper_opacity=0.92, mirror=False,
          pour_top=False, pour_bot=False, flip=0):
    pfx = SIDE_PREFIX[side]
    parts, vb = [], None

    def add(key, colour, opacity, label, bg='none'):
        nonlocal vb
        o = objs.get(key)
        if not o:
            return
        
        orig = None
        if (key == 'top_cu' and not pour_top) or (key == 'bot_cu' and not pour_bot):
            orig = o.objects
            o.objects = [p for p in orig if type(p).__name__ != 'Region']

        item_list = o if isinstance(o, list) else [o]
        for i, obj in enumerate(item_list):
            lbl = f"{label}-{i}" if isinstance(o, list) else label
            try:
                inner, v, _ = layer_svg(obj, colour, bounds, lbl, bg)
            finally:
                if orig is not None:
                    o.objects = orig
            if inner is None:
                continue
            vb = vb or v
            o = f' opacity="{opacity}"' if opacity < 1.0 else ''
            parts.append(f'<g id="{lbl}"{o}>{inner}</g>')

    # copper: knockouts painted in substrate so reliefs and clearances show
    add(f'{pfx}_cu',    theme['copper'], copper_opacity, f'{side}-copper',
        bg=theme['substrate'])
    add(f'{pfx}_mask',  theme['pad'],    1.0,  f'{side}-pads',
        bg=theme['substrate'])
    add(f'{pfx}_silk',  theme['silk'],   1.0,  f'{side}-silk')
    add('drill',        theme['hole'],   1.0,  'drill')
    # board edge and internal cut-outs live in different files
    add('outline',      '#000000',       0.9,  'cutouts')
    add('outline2',     '#000000',       0.9,  'board-edge')

    if f'{pfx}_cu' not in objs:
        print(f"      [!] no {pfx}_cu layer - this side will be blank")
    if not parts:
        return None
    if not vb and bounds:
        (a, b), (c, d) = bounds
        vb = f'{a} {b} {c - a} {d - b}'
    vb = vb or '0 0 100 100'
    x, y, w, h = (float(t) for t in vb.replace(',', ' ').split())

    body = "\n".join(parts)
    if mirror:
        if flip == 0:
            body = (f'<g transform="translate({2 * x + w} 0) scale(-1 1)">'
                    f'{body}</g>')
        else:
            body = (f'<g transform="translate(0 {2 * y + h}) scale(1 -1)">'
                    f'{body}</g>')

    return x, y, w, h, body, vb


def render(zip_path, outdir, tasks, dpi, finish,
           copper_opacity=0.92, realistic=False, mirror=False, aspect=None, flip=0, gap=2.5):
    try:
        import gerbonara  # noqa: F401
    except ImportError:
        sys.exit("gerbonara not installed.   pip install gerbonara")

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    stem = Path(zip_path).stem

    with tempfile.TemporaryDirectory() as tmp:
        flat, files = extract(zip_path, tmp)
        found, ignored = classify(files)

        print(f"\n  archive : {zip_path}")
        print(f"  finish  : {finish}\n")
        print("  LAYERS")
        for role, _ in PATTERNS:
            f = found.get(role)
            if role == 'drill' and f:
                print(f"    {role:9s} " + ", ".join(x.name for x in f))
            else:
                print(f"    {role:9s} {f.name if f else '-- none --'}")
        if ignored:
            print("\n  ignored : " + ", ".join(f.name for f in ignored))

        print("\n  parsing ...")
        objs = {}
        for role, path in found.items():
            if role == 'drill':
                objs[role] = []
                for p in path:
                    try:
                        objs[role].append(load(p, is_drill=True))
                    except Exception as e:
                        print(f"    [!] drill: {e}")
            else:
                try:
                    objs[role] = load(path, is_drill=False)
                except Exception as e:
                    print(f"    [!] {role}: {e}")

        for role in ('top_cu', 'bot_cu', 'top_mask', 'bot_mask',
                     'top_silk', 'bot_silk', 'drill', 'outline', 'outline2'):
            o = objs.get(role)
            if not o:
                continue
            if isinstance(o, list):
                total_n = 0
                for obj in o:
                    try: total_n += len(list(obj.objects))
                    except:
                        try: total_n += len(obj)
                        except: pass
                n = total_n
            else:
                try:
                    n = len(list(o.objects))
                except Exception:
                    try:
                        n = len(o)
                    except Exception:
                        n = '?'
            try:
                bb = union_bounds(o) if isinstance(o, list) else o.bounding_box()
                bbs = (f"{bb[1][0]-bb[0][0]:.1f} x {bb[1][1]-bb[0][1]:.1f} mm"
                       if bb else 'no bbox')
            except Exception:
                bbs = 'no bbox'
            print(f"    {role:9s} {n} primitives, {bbs}")

        bounds = union_bounds(objs.values())
        if bounds:
            (a, b), (c, d) = bounds
            print(f"  board   : {c - a:.2f} x {d - b:.2f} mm")

        def save_and_print(doc_str, fname_stem):
            p = outdir / f"{fname_stem}.svg"
            p.write_text(doc_str, encoding='utf-8')
            print(f"      {p}")
            try:
                import cairosvg
                q = outdir / f"{fname_stem}.png"
                cairosvg.svg2png(bytestring=doc_str.encode(), write_to=str(q), dpi=dpi)
                print(f"      {q}   ({dpi} dpi)")
            except ImportError: pass
            except Exception as e: print(f"      [!] png: {e}")

        total_tasks = len(tasks)
        for i, task in enumerate(tasks, 1):
            print(f"\n  [{i}/{total_tasks}] Rendering {task['mode']} ...")
            if task['mode'] == 'single':
                side = task['side']
                thm = task['theme']
                pour = task['pour']
                
                theme_dict = dict(THEMES[thm])
                if finish == 'hasl': theme_dict['pad'] = HASL_PAD
                if realistic: theme_dict['copper'] = REALISTIC[thm]
                
                pt = pour if side == 'top' else False
                pb = pour if side == 'bottom' else False
                
                doc_data = build(side, objs, theme_dict, bounds, copper_opacity,
                            mirror=(mirror and side == 'bottom'),
                            pour_top=pt, pour_bot=pb, flip=flip)
                if not doc_data:
                    print(f"      no layers for {side}")
                    continue
                x, y, w, h, body, vb = doc_data
                vx, vy, vw, vh = apply_aspect(x, y, w, h, aspect)
                doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx} {vy} {vw} {vh}" '
                       f'width="{vw}mm" height="{vh}mm">\n'
                       f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                       f'fill="{theme_dict["substrate"]}"/>\n{body}\n</svg>')
                
                p_str = "pour" if pour else "nopour"
                fname = f"{stem}_{side}_{thm}_{p_str}"
                save_and_print(doc, fname)

            elif task['mode'] == 'combined':
                u = task['upper']
                l = task['lower']
                u_thm = task['theme_upper']
                l_thm = task['theme_lower']
                u_pour = task['pour_upper']
                l_pour = task['pour_lower']
                
                thm_dict_u = dict(THEMES[u_thm])
                thm_dict_l = dict(THEMES[l_thm])
                if finish == 'hasl':
                    thm_dict_u['pad'] = thm_dict_l['pad'] = HASL_PAD
                if realistic:
                    thm_dict_u['copper'] = REALISTIC[u_thm]
                    thm_dict_l['copper'] = REALISTIC[l_thm]
                
                doc_u = build(u, objs, thm_dict_u, bounds, copper_opacity,
                              mirror=(mirror and u == 'bottom'),
                              pour_top=(u_pour if u=='top' else False),
                              pour_bot=(u_pour if u=='bottom' else False),
                              flip=flip)
                doc_l = build(l, objs, thm_dict_l, bounds, copper_opacity,
                              mirror=(mirror and l == 'bottom'),
                              pour_top=(l_pour if l=='top' else False),
                              pour_bot=(l_pour if l=='bottom' else False),
                              flip=flip)
                
                if not doc_u and not doc_l:
                    print(f"      no layers for either side")
                    continue
                x, y, w, h, body_u, _ = doc_u if doc_u else (0,0,0,0,"",None)
                _, _, _, _, body_l, _ = doc_l if doc_l else (0,0,0,0,"",None)
                
                if doc_u and doc_l:
                    margin = gap
                    total_h = h * 2 + margin
                    vx, vy, vw, vh = apply_aspect(x, y, w, total_h, aspect)
                    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx} {vy} {vw} {vh}" '
                           f'width="{vw}mm" height="{vh}mm">\n'
                           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{thm_dict_u["substrate"]}"/>\n'
                           f'{body_u}\n'
                           f'<g transform="translate(0 {h + margin})">\n'
                           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{thm_dict_l["substrate"]}"/>\n'
                           f'{body_l}\n'
                           f'</g>\n</svg>')
                    up_pstr = "pour" if u_pour else "nopour"
                    lp_pstr = "pour" if l_pour else "nopour"
                    fname = f"{stem}_combined_{u}_{u_thm}_{up_pstr}_{l}_{l_thm}_{lp_pstr}"
                    save_and_print(doc, fname)
                else:
                    print("      missing upper or lower layer for combined view")

    print("\n  SVG is vector - open in a browser and zoom in as far as you like.\n")


def main():
    ap = argparse.ArgumentParser(description="Render a Gerber zip.")
    ap.add_argument('zipfile')
    ap.add_argument('-o', '--out', default='Renders')
    ap.add_argument('-t', '--theme', default=None, choices=sorted(THEMES) + ['all'])
    ap.add_argument('-f', '--finish', default='enig', choices=['enig', 'hasl'])
    ap.add_argument('-d', '--dpi', type=int, default=1200)
    ap.add_argument('-c', '--copper-opacity', type=float, default=0.92,
                    help='0.0 transparent to 1.0 solid (default 0.92)')
    ap.add_argument('-m', '--mirror', action='store_true',
                    help='mirror the bottom view, as seen from below')
    ap.add_argument('--debug', action='store_true',
                    help='report per-layer render details')
    ap.add_argument('--realistic', action='store_true',
                    help='subtle copper contrast, closer to a real photo')
    ap.add_argument('-s', '--side', default='both',
                    choices=['top', 'bottom', 'both', 'combined'])
    ap.add_argument('-p', '--pour', action='store_true',
                    help='render copper pours/fills on both sides (default: false)')
    ap.add_argument('--top-pour', action='store_true',
                    help='render copper pours on top side only')
    ap.add_argument('--bot-pour', action='store_true',
                    help='render copper pours on bottom side only')
    ap.add_argument('--top-theme', default=None, choices=sorted(THEMES),
                    help='override theme for top side')
    ap.add_argument('--bot-theme', default=None, choices=sorted(THEMES),
                    help='override theme for bottom side')
    ap.add_argument('-a', '--aspect', default=None,
                    help='pad to aspect ratio, e.g. "4:5" or "1:1" (default: fit to board)')
    ap.add_argument('--flip', type=int, choices=[0, 1], default=0,
                    help='mirror axis: 0 = horizontal (left-right), 1 = vertical (up-down) (default: 0)')
    ap.add_argument('--gap', type=float, default=1,
                    help='gap between top and bottom in combined view (default: 2.5mm)')
    a = ap.parse_args()
    globals()['DEBUG'] = a.debug
    if not Path(a.zipfile).exists():
        sys.exit(f"no such file: {a.zipfile}")

    import itertools
    tasks = []
    mega_mode = (a.theme is None and a.top_theme is None and a.bot_theme is None)
    
    themes_list = sorted(THEMES.keys())
    sides_list = ['top', 'bottom']
    pours_list = [True, False]
    
    if mega_mode:
        print("\n=== MEGA MODE ACTIVATED: GENERATING ALL PERMUTATIONS ===")
        for side, theme, pour in itertools.product(sides_list, themes_list, pours_list):
            tasks.append({
                'mode': 'single', 'side': side, 'theme': theme, 'pour': pour
            })
        for u_side, l_side, u_thm, l_thm, u_pour, l_pour in itertools.product(
                sides_list, sides_list, themes_list, themes_list, pours_list, pours_list):
            tasks.append({
                'mode': 'combined', 'upper': u_side, 'lower': l_side,
                'theme_upper': u_thm, 'theme_lower': l_thm,
                'pour_upper': u_pour, 'pour_lower': l_pour
            })
    else:
        base_themes = themes_list if a.theme == 'all' else [a.theme or 'black']
        pour_top = a.pour or a.top_pour
        pour_bot = a.pour or a.bot_pour
        for theme in base_themes:
            t_top = a.top_theme if a.top_theme else theme
            t_bot = a.bot_theme if a.bot_theme else theme
            
            if a.side in ('top', 'bottom', 'both'):
                for side in (['top', 'bottom'] if a.side == 'both' else [a.side]):
                    tasks.append({
                        'mode': 'single', 'side': side,
                        'theme': t_top if side == 'top' else t_bot,
                        'pour': pour_top if side == 'top' else pour_bot
                    })
            if a.side == 'combined':
                tasks.append({
                    'mode': 'combined', 'upper': 'top', 'lower': 'bottom',
                    'theme_upper': t_top, 'theme_lower': t_bot,
                    'pour_upper': pour_top, 'pour_lower': pour_bot
                })
                
    render(a.zipfile, a.out, tasks, a.dpi, a.finish,
           a.copper_opacity, a.realistic, a.mirror, a.aspect, a.flip, a.gap)


if __name__ == '__main__':
    main()
