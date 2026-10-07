# 07 — Current State

Snapshot for picking up in a new session. Update this at the end of each working session.

**Last updated:** all four copper layers poured — L2 GND, L3 four power shapes, L1 and L4 GND fill. VDD1V35 rescued from 149 mΩ to 47 mΩ. DRC = 6, all cosmetic silk. Fab outputs not started.

---

## Where the project stands

| Phase | Status |
|---|---|
| Architecture and part selection | **Done** — Ethernet dropped, digital I²S audio in its place |
| Vendor documentation mined | **Done** |
| Altium library | **Done** — manufacturer footprints throughout |
| Schematic capture | **Done.** Compiles clean |
| Netlist | **Current** — 143 components, 105 nets, **no single-pin nets** |
| PCB stackup | **Done** — 4L, 1 oz every layer, Dk entered, impedance profiles solved |
| Design rules | **Done.** Power Width minimums corrected (`03-layout-rules` §3.0) |
| Placement | **Done** — 143 components, all inside 66 × 38, all top side |
| Routing | **Done** |
| **Pours** | **Done — all four layers** |
| **DRC** | **6 violations, all Silk To Solder Mask.** Every other rule 0 |
| Outputs | **Not started** |

---

## Board

**66 × 38 mm**, 4 layers, 1.62 mm, relative origin at the board corner.

Clearance rules actually in the board: **0.254 mm general**, **0.1 mm scoped `InComponent('U1')`**. (`01-design-brief` §5 still says 0.15 mm general — that line is stale.)

Vias are uniformly **0.3 hole / 0.6 pad**, enforced by a Routing Via rule with min = max = preferred.

---

## Copper — measured from the PcbDoc, not assumed

| Layer | Contents | Poured |
|---|---|---|
| **L1 Top** | signal + GND fill | **1230 mm²**, 11 islands, all tied in, 0 shorts |
| **L2 MID1** | GND plane | **2441 mm²**, 439 contours |
| **L3 MID2** | four power shapes, **no signal-only regions left that split anything** | **1313 mm²** |
| **L4 Bottom** | signal + GND fill | **1688 mm²**, 7 islands, all tied in, 0 shorts |

### L3 MID2 breakdown

| Net | Area | Pieces | Tie-in vias | Widest |
|---|---|---|---|---|
| VDD3V3 | 565 mm² | 1 | 13 | 9.8 mm |
| VDD1V8 | 429 mm² | 1 | 3 | 12.6 mm |
| VDDC | 218 mm² | 1 | 9 | 3.9 mm |
| VDD1V35 | 101 mm² | 1 | 2 | 5.7 mm |

**Zero shorts between the four pours.** They tile the board without overlapping: VDD3V3 x 0.6–21.0 · VDDC x 21.5–37.5 · VDD1V35 x 33.8–52.2 y 8.0–15.2 · VDD1V8 x 52.5–65.4.

The VDDC polygon is an **L-shape**, not a rectangle — full width x 21.5–37.5 below y 8.4 to reach the buck (TP4, C48, L2, R46), pulled back to x 33.6 above it so VDD1V35 has a lane. Vertices: `21.5,3.0 → 37.5,3.0 → 37.5,8.4 → 33.6,8.4 → 33.6,25.5 → 21.5,25.5`.

`WL_HOST_WAKE` (16 segments) and `GPIO_AUX0` (5) are still routed on MID2. Neither splits a pour any more. `03-layout-rules` §1 wants MID2 power-only — tidy if convenient, not urgent.

---

## Power rails — measured resistance

| Rail | Source → load | Resistance | Drop |
|---|---|---|---|
| **VDD1V35** | inductor L3 (47.60, 5.50) → U1-31 | **47.3 mΩ** | 14 mV at 0.3 A, 1.1 % |

Was 149 mΩ. See `06-corrections-log` for how. Breakdown: inductor → east via 4.2 mΩ (a 0.80 mm run on **Bottom**), pour across MID2 ~5 mΩ, west via → U1 38.2 mΩ. **The west leg is now the biggest single item on this rail** if anyone wants to keep going.

VDD3V3 (239 mm of conductor, 0.15/0.80 mm) and VDD1V8 (196 mm, 0.15/0.50 mm) were not resistance-modelled — too branchy for the graph reconstruction to trust. Both are at or near their spec widths and both now have plane behind them.

---

## Open DRC — 6, all cosmetic

| Where | What |
|---|---|
| Arc (17.525, 17.725) vs pad R4-1 | pin-1 marker over pad |
| Arc (19.415, 6.295) vs pad R9-1 | pin-1 marker over pad |
| **Pad C17-1 vs text "C12"** | **worth fixing** — C12's designator moved onto C17's pads during the bulk-cap relocation. Not just cosmetic: the silkscreen now mislabels a part |
| **Pad C17-2 vs text "C12"** | same, 0.027 mm |
| Pad C24-1 vs silk track at x 28.775 | 0.075 mm |
| Pad C7-1 vs silk track at x 28.975 | 0.075 mm |

JLC clips silk over pads, so none of these stop a build. Move the **C12 designator** anyway.

---

## Pick-and-place — two real problems

Generated file: `Project Outputs for NanoD1\Pick Place for NanoD1.csv`, 143 rows, all TopLayer.

1. **DNP parts are not marked.** Every row reads `Variation = Fitted`, including **R13, R14, R56, R58, R59**, which are meant to be unfitted. Handed to JLC as-is, they get populated. Fix with an Altium **Variant** before generating the assembly output.

2. **Eight components have Center ≠ Ref.** JLC must use **Center-X / Center-Y**, never Ref-X / Ref-Y:

| Ref | dx | dy |
|---|---|---|
| J5B | −11.43 | 0 |
| J5A | −11.43 | 0 |
| J4 | +10.16 | 0 |
| J3 | 0 | −3.81 |
| J2 | 0 | −2.18 |
| E1 | 0 | −0.76 |
| U2 | +0.56 | +0.07 |
| J6 | 0 | +0.55 |

An 11.43 mm error on both 10-pin headers is a scrapped board, not a rework.

3. **89 of 143 heights read 0.0000 mm.** Blocks 3D collision checking and gives the assembler nothing.

---

## Antenna — signoff C9, still open, now with numbers

`WIFI_ANT` is on **Top**, 0.762 mm wide, from (46.60, 26.37) to (46.52, 35.48). The `SE50_ANT` profile solved it as a microstrip over the L2 plane.

It is **not** an isolated microstrip. Ground copper was already this close to the trace edge *before* any pour:

| y | nearest Top GND from trace edge |
|---|---|
| 26.5 | **0.02 mm** |
| 28.5 | 0.27 mm |
| 30.5 | 0.12 mm |
| 32.5 | 1.07 mm |
| 34.5 | 0.62 mm |

So its impedance is already off 50 Ω. A **polygon pour cutout** now holds the L1 GND fill back — `44.5,25.5 → 48.6,25.5 → 48.6,36.5 → 44.5,36.5` — giving 1.67–1.77 mm along the run and 0.67 mm at the feed. That stops it getting worse; it does not fix what's there.

At ~9 mm of trace into a u.FL connector the cost is a fraction of a dB, not a dead radio. Decide whether to clean up the feed or accept and document.

---

## Known voids in the L2 plane

| Area | Location | Note |
|---|---|---|
| **34.6 mm²** | x 2.0 … 11.9, y 17.0 … 28.0 | Under U2 microSD. **SD0 return currents from U1 cross this.** Still not addressed |
| 9.0 mm² | x 10.8 … 17.7, y 28.9 … 30.7 | slot above the microSD |
| 4.8 mm² ×2 | x 32.2 … 37.9, y 31.2 … 33.7 | near J2 USB-C — **USB return path** |

---

## Next actions, in order

1. **Fix the pick-and-place** — Variant for the five DNP parts, and make sure whatever goes to JLC uses Center-X/Y. This is the only item on the list that can scrap a board
2. **Move the C12 designator** off C17's pads
3. **Inspect the three L2 voids**, especially the microSD one — stitch across or document why not
4. **Stitching vias** ≤ 7.5 mm along the USB shield
5. **Antenna feed** — decide C9: clean up or accept and document
6. **Delete the 221 redundant GND traces on L2**, repour, re-run DRC
7. **Component heights** — 89 of 143 still blank
8. **Via-in-pad decision** — 185 instances (160 excluding U1's thermal pad). Resin plugging or not; note it in the Draftsman drawing either way. Do not rework them
9. **Fab outputs** — Gerber X2, NC drill, BOM with LCSC numbers, CPL. Nothing started
10. **Rebuild `nano-d1-board.html`** — it predates all four pours

---

## Files in this set

| File | Contents |
|---|---|
| `00-README` | Project structure, navigation, vendor sources |
| `01-design-brief` | Scope, aesthetic, Altium workflow, milestones. **§5 clearance line is stale — see above** |
| `02-netmap` | All 88 pins, power tree, straps, per-interface circuits including §5.2 I²S audio. §9 preserves the superseded Ethernet section |
| `03-layout-rules` | Stackup with Dk, impedance geometries, §3.0 power width rules, routing rules, floorplan |
| `04-reference-measured` | Via coordinates, cap cascade, stencil notes |
| `05-signoff-checklist` | Pre-release check, bring-up order |
| **`06-corrections-log`** | **Every error found and fixed — read first** |
| `07-current-state` | This file |
| `bom-corrected.csv` | 141 rows |
| `altium-sg2002-symbol.csv` | 88-pin Symbol Wizard import |
| `SG2002_Part{A,B,C,E,F,G}.csv` · `SG2002_PartD_Audio.csv` | Per-part CSVs for the split symbol |
| `nano-d1-sheets.html` | Schematic viewer, 8 sheets |
| `nano-d1-schematic.html` | PCB-oriented block view |
| `nano-d1-board.html` | Real geometry from the PcbDoc. **Stale — predates all four pours** |
