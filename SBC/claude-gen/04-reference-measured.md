# 04 — Measured Reference Layout

Extracted from `SG2002_QFN88_38_20230301_4L_V1.3` via IPC-2581, FABRICATION mode.
All coordinates are **millimetres relative to the SoC centre** at absolute (18.300, 8.200).
Positive X = right, positive Y = up, viewed from the top.

This replaces every inference I made from the layout-guide screenshots. These are measured numbers.

---

## 1. Confirmed footprint geometry

Straight from the package definition, so this is authoritative for building your Altium footprint:

| Element | Value |
|---|---|
| Package name | `QFN88_9D0X9D0_0D35_E` |
| Pin count | 89 (88 signal + E-pad) |
| Signal pad | **0.200 × 0.750 mm** rectangular |
| Thermal pad (pin 89) | **6.000 × 6.000 mm** square |
| Pitch | 0.35 mm |

Standard via drill sizes used on the board: **0.3 mm** and **0.4 mm / 0.5 mm** circles.

---

## 2. The E-pad via array — actual counts

I previously guessed "about 20 vias" from a screenshot. The real numbers:

| Region | GND vias |
|---|---|
| Inside the exposed 6 × 6 mm pad | **27** |
| In the 6.0 → 7.6 mm solder-mask ring | **12** |
| **Total ground vias at the E-pad** | **39** |

Nearly twice my estimate. Given the E-pad is this chip's only real ground connection and carries 1.5 A of core return, don't economise here.

The array is **not a uniform grid**. Distinct X positions span −3.65 to +3.85 and Y from −3.65 to +3.65, at irregular spacing — the vias are woven around the power vias and escape traces rather than stamped on a lattice.

---

## 3. VDDQ — the 3-via cluster, located exactly

The layout guide said "3 vias in the E-pad solder-mask-covered region." Here they are:

```
(−1.050, −3.600)
(−0.400, −3.600)
(+0.250, −3.600)
```

All three at **Y = −3.600**, i.e. in the mask-covered ring between the 6 × 6 exposed pad and the 7.6 × 7.6 boundary, on the **bottom edge** of the package. Spacing is roughly 0.65 mm.

Two more VDDQ vias sit just inside the pad at (−0.850, −2.950) and (+0.150, −2.950) — that's the pin-out cluster feeding up from below.

**Why the bottom edge:** VDDQ is pins 31–34, dead centre of the package's bottom side. The pinout forces the position, exactly as predicted.

---

## 4. VDDC — 13 via positions

```
(−3.600, −1.600)   (−2.900, −1.600)   (+2.950, −2.300)   (+3.600, −1.925)
(−3.600, +0.500)   (−2.900, +0.500)   (+2.950, −1.300)   (+3.600, −1.250)
(+2.150, +3.650)                      (+2.950, +0.600)   (+3.650, +1.600)
                                      (+2.950, +1.600)   (+3.850, −2.700)
```

Clustered on the **left and right edges** — matching VDDC pins 9, 16 (left side) and 50, 61, 71 (right side). Each pin gets a via at the pin plus a second via ~0.7 mm further out, forming short pairs that carry current down to the L3 pour.

Other rails inside the pad footprint: **IOVDD** 5 vias, **SPI_VCC** 2 vias.

---

## 5. Decoupling — measured positions

**30 of the 40 parts within 8 mm of the SoC are on the BOTTOM side.** The design guide's insistence that bottom-side caps under the chip are critical is not rhetorical — it's where nearly all of them live.

### Ring 1 — under the package body (2.5–3.0 mm)

| Ref | Value | Offset (x, y) |
|---|---|---|
| C29 | 100 nF | (−2.500, +0.500) |
| C15 | 100 nF | (+0.150, −2.550) |
| C9 | 100 nF | (−2.500, +1.500) |
| C30 | 100 nF | (−2.500, −1.600) |
| C32 | 100 nF | (+2.550, +1.600) |
| C28 | 1 µF | (+2.550, +0.600) |
| C13 | 1 µF | (−0.850, −2.550) |
| C26 | 1 µF | (+2.550, −1.300) |

The package half-width is 4.5 mm, so **every one of these sits underneath the chip body**, on the bottom side, at ~2.5 mm from centre. That is the tightest ring physically possible while clearing the E-pad.

### Ring 2 — at the package edge (4.3–4.8 mm)

C16, C22, C23, C10, C31, C19 (100 nF and 1 µF) · C21 2.2 µF · C12 4.7 µF

### Ring 3 — beyond the package (4.9–6.2 mm)

C24 4.7 µF (+2.550, −2.300) · C68 4.7 µF · C25 4.7 µF · **C67 10 µF 0603** at (−3.900, −4.700)

**The cascade is real and it is tight.** 100 nF and 1 µF under the body, 4.7 µF at the edge, 10 µF beyond. The bulk cap sits 6.1 mm out — near the regulator, not the chip, exactly as the guide describes.

---

## 6. Other measured parts near the SoC

| Ref | Value | Offset | Note |
|---|---|---|---|
| R20 | 10 kΩ 1% | (+2.200, −6.200) | Top side |
| R18 | 30 kΩ 1% | (+3.200, −6.500) | VBAT divider upper leg — confirms the 30k/10k pair |
| R8 | 1 MΩ | (+5.600, −3.950) | The crystal feedback resistor |
| C17 | 12 pF | (+6.800, −3.150) | Crystal load cap |
| C18 | 12 pF | (+5.200, −5.400) | Crystal load cap |
| C58 | 22 µF 0603 | (+6.850, −2.600) | Regulator bulk |
| R67 | 33 Ω | (−3.675, +6.800) | Series termination |

The crystal cluster (R8, C17, C18) sits **5–7 mm to the lower right** of the SoC — consistent with XTAL on pins 45/46 at the bottom of the right edge.

---

## 7. Stackup in the file — do not use it

The board's cross-section carries **uniform 0.2032 mm (8 mil) dielectric on all three gaps**, total 0.7315 mm, copper 0.0305 mm.

That is Allegro's **default placeholder cross-section**, not a designed stackup. The give-aways: perfectly uniform dielectric, and a 0.73 mm total that contradicts the layout guide's own stackup slide.

**Use the layout guide values instead** — 5 mil prepreg / 47.2 mil core / 5 mil prepreg, Dk 4.07 / 4.0 / 3.5, 1.62 mm total. Those are the fabrication intent; the `.brd` cross-section was never filled in.

Layer names in the file confirm the roles: `TOP · GND · POWER · BOTTOM`. L2 is ground, L3 is power.

---

## 8. What to do with this

**Build the footprint** from §1 — you now have vendor-confirmed pad dimensions.

**Copy §2–§5 directly.** Your board is **66 × 38 mm** and theirs is 38 × 38 mm, so overall placement doesn't transfer — but everything within ~7 mm of the SoC does, because it's driven by the pinout, not the board outline. Place your SoC, then drop the via array and the cap rings at these exact offsets.

**Scale up the via count.** 39 ground vias at the E-pad, not the 20 I estimated.

**Put your decoupling on the bottom side.** Ring 1 at 2.5 mm sits under the package body, which only works from below.

---

## 9. Still open

The IPC-2581 export doesn't carry paste-mask apertures for the thermal pad in a form I can read here, so the stencil segmentation for the 6 × 6 mm pad remains unanswered. That's in `05_SOPHGO_Precautions_for_PCBA_SMT_Manufacturing_EN.docx` — upload it and I'll close the last gap.

If you also want the L3 VDDC pour outline as explicit polygon vertices, say so — the polygon data is in the file, it just needs a targeted extraction.

---

# Appendix — VDDC pour geometry and stencil

---

## 1. The L3 VDDC pour — exact vertices

Extracted from the POWER layer of the reference board. **Millimetres relative to the SoC centre.**
111 raw vertices, simplified to 69 at 0.05 mm tolerance (the discarded points are sub-0.05 mm arc approximations).

```
  #      X        Y            #      X        Y            #      X        Y
  0   +2.800   +3.604        24   +6.100   -0.900        48   -3.650   +0.800
  1   +2.873   +3.427        25   +6.100   -2.050        49   -2.404   +0.800
  2   +3.197   +3.103        26   +5.850   -2.300        50   -2.227   +0.727
  3   +3.226   +3.038        27   +2.150   -2.300        51   -1.973   +0.473
  4   +3.285   +2.796        28   +1.900   -2.050        52   -1.797   +0.400
  5   +3.300   +2.744        29   +1.900   -1.350        53   -1.147   +0.400
  6   +3.300   +2.556        30   +1.842   -1.190        54   +1.135   +0.400
  7   +3.285   +2.505        31   +1.245   -1.075        55   +1.208   +0.365
  8   +3.290   +2.088        32   +1.179   -1.100        56   +1.735   +0.892
  9   +3.550   +1.850        33   -1.296   -1.100        57   +1.700   +0.965
 10   +3.650   +1.850        34   -1.473   -1.173        58   +1.700   +1.235
 11   +3.900   +1.600        35   -2.127   -1.827        59   +1.735   +1.308
 12   +3.900   +1.200        36   -2.303   -1.900        60   +1.735   +1.892
 13   +3.650   +0.950        37   -3.650   -1.900        61   +1.700   +1.965
 14   +3.550   +0.950        38   -3.900   -1.650        62   +1.700   +3.332
 15   +3.300   +0.702        39   -3.900   -1.200        63   +1.725   +3.395
 16   +3.275   +0.539        40   -3.650   -0.950        64   +1.807   +3.765
 17   +3.275   -0.089        41   -3.350   -0.950        65   +1.872   +3.888
 18   +3.300   -0.251        42   -3.100   -0.700        66   +1.950   +3.900
 19   +3.550   -0.500        43   -3.100   -0.300        67   +2.550   +3.900
 20   +4.497   -0.500        44   -3.350   -0.050        68   +2.800   +3.650
 21   +4.673   -0.573        45   -3.650   -0.050
 22   +4.854   -0.650        46   -3.900   +0.200        (closes back to #0)
 23   +5.850   -0.650        47   -3.900   +0.550
```

### Measured properties

| Property | Value |
|---|---|
| Extents X | −3.900 … +6.100 (**10.000 mm** wide) |
| Extents Y | −2.300 … +3.900 (**6.200 mm** tall) |
| Enclosed area | **24.67 mm²** |
| Vertices (raw / simplified) | 111 / 69 |
| Cutouts | **0** |

### Reading the shape

It is **not** a symmetric horseshoe. The slide made it look like one; the coordinates say otherwise.

- **Left arm** — a narrow finger reaching to X = −3.900 around Y = −1.9 … +0.8, serving VDDC pins 9 and 16 on the left package edge
- **Right arm** — a taller lobe from Y = −0.5 up to Y = +3.9 at X ≈ +3.3 … +3.9, serving pins 50, 61 and 71
- **Bottom bridge** — a narrow waist at Y ≈ −1.100 running from X = −1.296 to +1.179, joining the two arms *underneath* the E-pad
- **Regulator arm** — the pour breaks out to the right at X = +4.5 … +6.1, between Y = −0.650 and −2.300. **That arm is 1.65 mm wide**, comfortably above the ≥1.0 mm W1 minimum

The waist at Y ≈ −1.1 is the interesting bit. The pour ducks *below* the E-pad centre to cross from one side to the other, keeping clear of the dense ground via field above it. The upper boundary at Y = +0.400 (vertices 52–54) is where it stops to leave room for that via array.

### Using it in Altium

1. Place your SoC, note its centre coordinate
2. **Place » Polygon Pour**, then enter vertices numerically as *SoC centre + offset*
3. Set net to VDDC, layer to your L3, Solid pour
4. It has no cutouts — antipads generate automatically from your clearance rules

Since your board is **66 × 38 mm** rather than 38 × 38 mm, the regulator arm (vertices 20–27) is the part to redraw — it points wherever *your* core buck sits. Everything within ±4 mm of centre transfers unchanged, because it's dictated by pin positions.

---

## 2. Paste stencil — what the documents actually say

I checked both sources. Neither gives thermal-pad segmentation.

**`05_SOPHGO_Precautions_for_PCBA_SMT_Manufacturing_EN` is a QA checklist**, not a stencil design guide. What it does specify:

| Item | Requirement |
|---|---|
| **Stencil thickness** | **0.1 mm** |
| **Applied paste thickness** | **0.1 mm**, even thickness and consistency |
| Stencil condition | Flat, uncontaminated, normal-sized apertures |
| Stencil size | Must match your PCB manufacturer's requirement — not universally compatible between fabs |
| PCB finish | **Immersion gold** — confirms ENIG, consistent with the aesthetic spec |
| PCB storage | Vacuum bag; discard boards opened more than 6 months |
| Baking | Required for SoC and DDR flash before SMT |
| **Reflow peak** | **248 °C IC surface temperature, 80 s reflow duration** |
| Depaneling | Do not press the centre of the board when splitting |

**The IPC-2581 export didn't carry it either.** The paste layers (PMT/PMB) contain one feature each — Allegro generates paste from padstack definitions rather than as explicit artwork, and the export didn't expand them. So the reference board's actual aperture pattern isn't recoverable from this file.

### General practice for a 6 × 6 mm thermal pad

Not vendor-specific, so treat as a starting point and confirm with your assembler:

- **Never a single 6 × 6 mm aperture.** Roughly 100% paste coverage over 36 mm² floats the package, causing tilt, opens on the fine-pitch perimeter pins, and solder squeeze-out.
- **Target 50–70% paste coverage** on the thermal pad.
- **Segment into a window-pane array** — a 3 × 3 or 4 × 4 grid of square apertures with gaps between them. A 4 × 4 grid of 1.1 mm squares gives ~54% coverage; 3 × 3 of 1.6 mm gives ~64%.
- **Keep apertures clear of the thermal vias** so paste doesn't wick down the barrels. Your vias should be plugged and capped anyway.
- **Perimeter pins at 0.2 × 0.75 mm** are near 1:1 with the 0.1 mm stencil — check the area ratio with your assembler; you may need a slight aperture reduction or a laser-cut electropolished stencil.

Ask your assembly house to review the stencil design. They do this daily and will have a house rule for QFN thermal pads.

---
