# 03 — Layout Rules

Source: `08_SG2002_4L_PCB38x38mm2_Layout指南.pptx` v0.2 + Hardware Design Guide EN.

---

## 0. Applicability

The deck is scoped to **QFN + DDR SiP, board size ≤ 38 × 38 mm²**. It names CV1810C/CV1811C/CV1812C in the body while the cover says SG2002 — same QFN88 family, consistent with the reference schematic labelling the part `CV181xC_QFN88`.

**Your board is 66 × 38 mm.** The long dimension exceeds 38 mm, and two rules have explicit wider variants keyed on that (§5). Take the wider numbers.

> **Dimension history.** This file was written against 65 × 30 mm, corrected to 70 × 35 mm, and the board is now **66 × 38 mm** — outline in `NanoD1.PcbDoc` spans 0 … 66.00 × 0 … 38.00 with the relative origin set at the board corner. Every rule conclusion below survives all three changes; the ">38 mm" test in §5 was tripped at 65 mm and is tripped harder now. **When a board dimension changes, grep every file in this set for the old value before doing anything else** — this has now been missed three times. See `06-corrections-log.md`.
>
> **Ethernet was removed from this design.** §3's EPHY rows, §3.1 and §3.2's EPHY line no longer apply and are marked superseded. Pins 62–65 now carry I²S — see `02-netmap.md` §5.2.

The deck labels the DDR rail "DDR3_1.5V" because the CV181xC parts it also covers use 1.5 V DDR3. **On SG2002 that rail is DDR3L at 1.35 V.** Layout rules apply unchanged; only the label differs.

---

## 1. Stackup

| Constraint | Requirement |
|---|---|
| Layers | 4 |
| Total thickness | 1.0 mm −10% … 1.6 mm +10% |
| Copper, **every layer** | **1 oz** |
| L1/L2 and L3/L4 prepreg | **≤ 5 mil (0.127 mm)** post-lamination, excluding copper |
| L2/L3 core | **≥ 25 mil (0.635 mm)** |

### Reference stackup — enter these exact values

Total **63.8 mil ≈ 1.62 mm**:

| Element | Material | Thickness | Dk |
|---|---|---|---|
| Solder mask | | 0.8 mil | **3.5** |
| **L1 Top** | copper + plating | 1.25 mil | |
| | **Prepreg** | **5 mil** | **4.07** |
| **L2 Inner 1** | 1 oz foil | 1.25 mil | |
| | **Core** | **47.2 mil** | **4.0** |
| **L3 Inner 2** | 1 oz foil | 1.25 mil | |
| | **Prepreg** | **5 mil** | **4.07** |
| **L4 Bottom** | copper + plating | 1.25 mil | |
| Solder mask | | 0.8 mil | **3.5** |

**The Dk values are the critical part.** Altium's impedance solver will not reproduce the vendor's 98 Ω / 92.5 Ω results on default FR-4 constants. Enter 4.07 / 4.0 / 3.5. Leave the defaults and your trace widths will be wrong with nothing to flag it.

### Layer roles

```
L1  Signal fanout + GND pour     1 oz
L2  GND — solid, unbroken        1 oz
L3  Power shapes (see §4)        1 oz
L4  Power distribution + signal  1 oz
```

**1 oz on inner layers is not the default.** Most 4-layer quotes assume 0.5 oz inner. Specify it or you won't hit the impedances. At 0.127 mm outer dielectric with 1 oz copper you're at the edge of standard capability (5 mil min trace/space) — confirm with your fab before ordering.

---

## 2. Impedance

These are **coplanar-with-ground** structures, not plain microstrip. Ask your fab to solve these exact Polar structures:

- Surface (L1/L4): *Differential Coated Coplanar Strips with Ground, 1B*
- Inner (L2/L3): *Differential Offset Coplanar Strips, 1B1A*
- Antenna: *Coated Coplanar Strips with Ground, 1B*

### Surface — Option 1 (pair-to-pair GND shielding)

| Target | W | S | D (trace→GND) | Solved |
|---|---|---|---|---|
| 100 Ω ±5% | 5 mil (0.127) | 5 mil (0.127) | 6 mil (0.15) | 98.0 Ω |
| 90 Ω ±5% | 5 mil (0.127) | 4 mil (0.10) | 6 mil (0.15) | 92.5 Ω |

### Surface — Option 2 (relaxed ground spacing, Ds = Dg = 3W)

| Target | W | S | Ds | Dg | Solved |
|---|---|---|---|---|---|
| 100 Ω | 5 mil | 5 mil | 12 mil | 12 mil | 100.0 Ω |
| 100 Ω | 4 mil | 4 mil | 12 mil | 12 mil | 101.2 Ω |

### Inner (L2/L3)

| Target | W | S | D | Solved |
|---|---|---|---|---|
| 100 Ω | 5 mil | 10 mil | 12 mil | 98.9 Ω |
| 100 Ω | 4 mil | 7 mil | 8 mil | 99.1 Ω |
| 90 Ω | 5 mil | 7 mil | 6 mil | 90.3 Ω |
| 90 Ω | 4 mil | 5 mil | 6 mil | 90.3 Ω |

### Antenna, 50 Ω single-ended

| Layer | W | D1 | D2 | Solved | Note |
|---|---|---|---|---|---|
| Top | **30 mil (0.762 mm)** | 6 mil | 12 mil | 50.9 Ω | **References L4**, not L2 |

Two things people get wrong here: the trace is much wider than intuition suggests, and **all planes directly beneath it must be cut away**. Referencing to the far layer is what buys the width.

---

## 3. Routing rules

All widths in mm.

| Signal | Layer | Zo | W / S / D | Shielding |
|---|---|---|---|---|
| **USB DP/DM** | Top/Bot | 90 Ω | 0.125 / 0.10 / 0.15 | Lane-to-lane GND shield, **stitching vias ≤ 7.5 mm** |
| ~~EPHY, run ≤ 40 mm~~ | ~~Top only~~ | ~~100 Ω~~ | ~~0.125 / 0.125 / 0.15~~ | **Superseded — Ethernet removed** |
| ~~EPHY, run > 40 mm~~ | ~~Top~~ | ~~*none*~~ | ~~0.125 / 0.125 / 0.125~~ | **Superseded — see §3.1** |
| **I²S audio** (pins 62–65) | Top/Bot | *none* | W ≥ 0.15, spacing 0.15 | Single-ended, no impedance control. Reference the plane. Keep BCLK away from the antenna feed |
| **SDIO** — fanout | Top/Bot | — | W ≥ 0.10, spacing 0.10 | No GND trace; reference the plane |
| **SDIO** — main run | Top/Bot | — | W ≥ 0.10, spacing 0.15 | Same |
| **SPI NOR** — fanout | Top | — | W ≥ 0.10, spacing 0.10 | Same |
| **SPI NOR** — main | Top | — | W ≥ 0.10, spacing 0.15 | Same, but **SPI_CLK individually shielded** |
| **XTAL_IN / XTAL_OUT** | Top | — | **0.25 / 0.25** | **Per-trace GND shielding** |
| **WIFI_ANT** | Top | 50 Ω | 0.75 / 0.15 / 0.30 | Per-trace shield, **planes cut beneath** |
| **RTC** | Top | — | as SDIO | Shielding rule |
| Audio | Top | — | W ≥ 0.10, D = 0.10 | Per-trace shield over dedicated audio GND |

**The crystal traces are 0.25 mm — double everything else on the board** — and get per-trace shielding. Easy to route at default width and never notice.

### 3.0 Power width rules — the Min value must fit the pad

**Measured from `NanoD1.PcbDoc`: every SG2002 signal pad is 0.200 × 0.750 mm.** SOT23-5 regulator pads are 0.600 mm, the L2 inductor pads 0.800 mm, 0805 caps 0.700 mm.

A Width rule's **Minimum** is a hard floor — Altium will not let a trace get thinner anywhere, including where it enters a pad. Five power classes were set with a Min *wider than the pad*, which makes those nets physically unroutable into U1:

| Class | Nets | Old Min | Narrowest pad | **New Min** | Preferred | Max |
|---|---|---|---|---|---|---|
| `PWR_CORE` | VDDC | ~~0.8~~ | 0.200 (U1-71) | **0.15** | 1.5 | 3 |
| `PWR_1V35` | VDD1V35 | ~~0.5~~ | 0.200 (U1-34) | **0.15** | 1.5 | 3 |
| `PWR_3V3` | VDD3V3 | ~~0.4~~ | 0.200 (U1-13) | **0.15** | 0.8 | 3 |
| `PWR_1V8` | VDD1V8, VDD18A_USB, WIFI_VDD | ~~0.3~~ | 0.200 (U1-82) | **0.15** | 0.5 | 2 |
| `PWR_5V` | VBUS_5V | ~~0.4~~ | 0.400 (C43-1) | **0.15** | 0.8 | 2 |

**Only the Minimum changes.** Preferred is what the interactive router actually starts with, so you still route at full width — you are simply *allowed* to neck down at the terminal instead of being blocked.

Three things to hold onto:

- **Keep every neck short.** Get back to full width within about 1 mm of the pad. The vendor's W2 ≥ 1.5 mm requirement in §4 is about the channel, not the last 200 µm.
- **PWR_CORE at 1.5 mm preferred also needs necking at the regulators** — U5/U6/U7 are SOT23-5 with 0.6 mm pads, and L2's pads are 0.8 mm. That is normal, not a mistake.
- **Most of the power on this board is meant to be poured, not traced.** §4 specifies shapes. The width rule only governs the short neck from pad to shape — which is exactly why the Min had to come down.

`nano-d1-board.html` carries this as a live audit: it reads the real pad geometry out of the PcbDoc and flags any rule whose Min exceeds the pad it has to reach.

### 3.1 ~~Ethernet over 40 mm~~ — SUPERSEDED

> **This whole section no longer applies.** Ethernet was removed; there is no differential pair on the board except USB. Retained because the measurement method and the corridor analysis were reused for the I²S routing, and because the ETH pad names persist in vendor documentation.

#### Historical: Ethernet over 40 mm — a different regime

Above 40 mm the vendor **drops impedance control** and switches to guarded traces:

- GND trace between P and N **within** each pair
- GND trace between the TX pair and the RX pair
- 0.125 / 0.125 / 0.125 (Ws / Sg / Wg)
- Return vias at **both** ends: one tying the guard to the **SoC E-pad** at the chip, one tying it to the **transformer GND pin** at the far end

Also: TX/RX ground shielding must reach **all the way to the pin**, not stop at the fanout.

**Measure the run before choosing.** On a 75 mm board with the SoC centred you land near this boundary, and it's the one dimension that changes a rule set.

**Measured, from `NanoD1.PcbDoc`.** Pad-to-pad, board-relative, R26–R29 series resistors not yet placed:

| Pair | SoC pad | J1 pad | Straight | 45° estimate |
|---|---|---|---|---|
| EPHY_TXP | U1.65 | J1.1 | 28.51 | **30.65** |
| EPHY_RXP | U1.63 | J1.3 | 27.80 | 29.30 |
| EPHY_TXN | U1.64 | J1.2 | 25.63 | 27.43 |
| EPHY_RXN | U1.62 | J1.6 | 24.89 | 25.04 |

Worst case **30.65 mm** — under 40 mm, so the §3 controlled-impedance row applies and §3.1 does not. Headroom ≈ 9.3 mm.

**Each EPHY net is two hops, not one.** R26–R29 (5.1 Ω series) split every pair between the SoC and the magjack: U1.65→R26→J1.1, U1.64→R27→J1.2, U1.63→R28→J1.3, U1.62→R29→J1.6. Note the SoC-side and connector-side pin orders do not correspond — U1.62 and J1.1 are different pairs. Parking those four resistors off the direct path is the fastest way to spend the 9.3 mm.

### 3.2 Length matching

| Signal | Constraint | Limit |
|---|---|---|
| USB DP/DM | P/N intra-pair | **≤ 10 mil** (guide is stricter than the deck's 20 mil) |
| ~~EPHY each pair~~ | ~~P/N intra-pair~~ | ~~≤ 0.5 mm~~ — **superseded, Ethernet removed** |
| I²S BCLK / LRCK / data | none | Single-ended. No matching required |

---

## 4. Power layout

Colour key in the reference figures: **blue = GND · dark red = general copper · bright red/magenta = highlighted rail · yellow = vias.**

### 4.1 VDDC (0.95 V, ~1.5 A)

| Item | Requirement |
|---|---|
| Vias at SoC | **5** — one per VDDC pin (9, 16, 50, 61, 71), placed **at the pin**, spread around the perimeter, not ganged |
| Decoupling | **10 caps** — see cascade below |
| GND vias | **At least one beside every cap.** Called out in red in the source — the vendor's way of saying people break it. |
| Layers | Shapes on L3 and Bottom |
| Channel under the QFN | W1 ≥ **1.0 mm** effective, after deducting antipads |
| Channel entering SoC region | W2 ≥ **1.5 mm** (your board is > 38 mm) |

**The L3 geometry.** VDDC on the inner layer is neither a trace nor a plane — it's a **horseshoe-shaped pour wrapping the SoC**, with a GND island left in the centre under the E-pad. The five vias drop into the arms. W1 is the narrowest neck where the pour passes under the package body.

This tells you the layer strategy: **L3 is a shape layer, not a split plane.** VDDC runs from the regulator on Bottom, vias up into the L3 horseshoe, feeds the pins from there.

**Cap cascade** — graded, not clustered:

| Caps | Value | Position |
|---|---|---|
| C1, C6, C7 | 0402 0.1 µF | Hugging the SoC |
| C2, C3, C5 | 0402 1 µF | Next ring out |
| C4, C8 | 0402 4.7 µF | Mid-field |
| C9, C10 | 0603 10 µF | **At the regulator** |

Bulk at the source, small values at the load. Crowding all ten near the chip — the instinctive move — is not what the reference does.

`L1` and `W2` are measured on **Bottom**: L1 is the regulator-to-SoC run length, W2 the narrowest effective neck entering the SoC region.

"Effective width after deducting antipads" is the phrase people miss. A 1.5 mm shape with via clearances punched through it is not 1.5 mm of copper.

### 4.2 VDDQ / VDDQ_DRAM (1.35 V, ~300 mA)

| Item | Requirement |
|---|---|
| Vias in the E-pad mask-covered region (7.6 × 7.6 mm) | **3**, as a tight cluster at **one edge** |
| Vias in the pin-out region | **6** |
| Vias at SoC on the Bottom main route | **9** (3 × 3 array) |
| Main route width | W1 ≥ 1.5 mm |
| Channel entering SoC | W2 ≥ **1.5 mm** (> 38 mm board) |
| Decoupling | 2 × 0402 0.1 µF, 1 × 0402 1 µF, 2 × 0402 4.7 µF, 1 × 0603 10 µF |
| GND vias | ≥ 1 beside each cap |

These clusters belong at the **bottom edge** of the package — because VDDQ is pins 31–34, dead centre of the bottom edge (§8). The pinout forces the position; it wasn't a layout preference.

One inconsistency in the vendor doc: Rule 3 text references caps "C4/C5/C6/**C7**" but the list defines only C1–C6. Trust the list.

### 4.3 E-pad

Two concentric regions, not the same size:

- **7.6 × 7.6 mm** — copper covered by solder mask
- **6.0 × 6.0 mm** — exposed opening (matches `s_6d0x6d0.pad`)

Both a distributed array and counted clusters are present:

- **GND gets a scattered array** — roughly 20 vias across the pad area
- **Power rails get counted clusters** at defined entry points, in the mask-covered ring where they won't wick solder during reflow

Specify vias in the exposed region as plugged and capped.

### 4.4 Analog IO power (1.8 V and 3.3 V)

| Where | Minimum width |
|---|---|
| Top, under the SoC | W1 ≥ 0.4 mm |
| Top, outside the SoC | W2 ≥ 0.5 mm |
| L3 and Bottom, everywhere | W3 ≥ 0.5 mm |

Plus one via per power pin and ≥ 1 GND via beside every cap. On L3 these rails form **large interlocking pours** fitted around the VDDC horseshoe and the central GND island — plan that layer deliberately at floorplan time.

---

## 5. What changes because the board exceeds 38 mm

| Rule | ≤ 38 × 38 mm | **Yours** |
|---|---|---|
| VDDC channel W2 | ≥ 1.2 mm | **≥ 1.5 mm** |
| VDDQ channel W2 | ≥ 1.0 mm | **≥ 1.5 mm** |

Both trigger when the power run L1 exceeds 10 mm, which on a 75 mm board it will. Budget the copper at floorplan time.

The test is on the **long** dimension: 75 mm > 38 mm. The short dimension is 38 mm, exactly at the deck's boundary rather than inside it — treat it as at the limit, not comfortably within. The conclusion is the same one this section reached at 65 mm and at 70 mm; only the number it was derived from changed.

---

## 6. Altium implementation

| Rule | Mechanism |
|---|---|
| Stackup + Dk | Layer Stack Manager, materials entered explicitly |
| Impedance targets | Impedance tab → `DIFF90_SURF`, `DIFF100_SURF`, `SE50_ANT`. Cross-check against §2 — a mismatch beyond a few percent means your Dk is wrong |
| Per-interface W/S | Width + Differential Pair Routing rules scoped to net classes |
| **Power Min width** | **Set Min to 0.15 mm on every `PWR_*` class — see §3.0. A Min wider than the destination pad blocks routing entirely** |
| Intra-pair skew | Matched Lengths, or Differential Pair Length Tuning, 10 mil |
| Stitching ≤ 7.5 mm | `Tools → Via Stitching/Shielding → Add Shielding to Net` |
| Antenna cutout | Polygon cutout on all layers + Keep-Out on Mechanical 15 |
| One via per power pin | **Manual check** |
| ≥ 1 GND via per cap | **Manual check** |
| Effective width after antipads | **Manual check** — ruler tool after pour |

The last three are the ones that get missed. They're in `05-signoff-checklist.md`.

---

## 7. Copy, don't design

Three of the vendor's sixteen checklist items say the same thing: 建议贴上SOC PKG 下方…走线/VIA/Cap layout — *paste in the routing / via / cap layout from beneath the SoC package.* It applies to DDR, VDDC and analog power.

The Hardware Design Guide is blunt: capacitor values and POWER/GND via layout beneath the chip *"must fully refer to the reference board PCB design."*

Open slides 13–15 and 33–36 and copy the figures literally. This is the one region of the board where copying beats designing.

---

## 8. Ball map and floorplan

The QFN88 is functionally segregated by edge. This dictates SoC rotation and therefore the whole board.

| Edge | Pins | Function |
|---|---|---|
| **Left** | 1–22 | Audio (1–5), **SD0 / microSD** (6–15), UART0 (18–19), start of SPI NOR (20–22) |
| **Bottom** | 23–44 | Rest of SPI NOR (23–25), JTAG (26–27), I²C0 (28–29), **DDR/VDDQ** (31–34), PAD_ZQ (35), **RTC + sequencing** (36–44) |
| **Right** | 45–66 | **Crystal** (45–46), PWR_GPIO (47–49), **SD1 / WiFi** (51–56), ADC/VBUS_DET (58–60), **I²S audio** (62–65, was EPHY) |
| **Top** | 67–88 | GPIO_RTX / CPU_SEL (67), **USB DP/DM** (69–70), MIPI (72–88) |

Three consequences:

**DDR power via clusters belong at the bottom edge** — forced by pins 31–34.

**USB used to compete with Ethernet for the top-right corner.** With Ethernet gone, USB has the corner to itself and the I²S bus — single-ended, no impedance control — can take whatever path is convenient out of the right edge.

**Power regulation belongs along the bottom** — VDDQ, VDDC_RTC, PWR_SEQ1/2 and PWR_VBAT_DET are all bottom-edge pins.

### Recommended floorplan, 66 × 38 mm, SoC at 0°

Roughly to scale: ≈1.2 mm per character horizontally, ≈3.2 mm per row vertically.

```
 38 mm  ┌───────────────────────────────────────────────────────────────┐
   ◉    │                     [USB-C J2]     [D1] [DA1]  [E1 u.FL]   ◉  │
        │   ┌─────────┐                                                 │
 micro  │   │   U2    │       ╔═══════════╗                             │
  SD ◄──┤   │  µSD    │       ║    U1     ║      ┌──────────┐  ┌──────┐ │
 (left  │   │ socket  │       ║  SG2002   ║      │    U4    │  │ audio│ │
 edge)  │   │         │       ║   QFN88   ║      │  AP6212  │  │ U9/U10│
        │   └─────────┘       ╚═══════════╝      └────┬─────┘  └──┬───┘ │
        │                                             │           │ ►JST│
        │  [XTAL]  [1V35] [0V95] [1V8] [3V3]      ░░antenna        │     │
   ◉    │           power along bottom edge        ░░keepout       │  ◉  │
  0 mm  └───────────────────────────────────────────────────────────────┘
        0 mm     UART hdr ○RST ○BOOT      castellations both      75 mm
                                          long edges
```

The right short edge, formerly the RJ45, is now free — **15.25 × 17.94 mm** of it. The amplifier (3 × 3 mm), the mic (4.72 × 3.76 mm), the JST speaker connector (~6 × 5 mm) and their passives need roughly 15 × 10 mm, so the zone has slack. **Decision taken: keep 66 × 38 for now**, revisit shrinking once the audio block is placed and routed.

**This section never carried numeric placement coordinates** — only edge assignments and the sketch above, both ordinal rather than dimensioned. Live coordinates are in `07-current-state.md` and, authoritatively, in the PcbDoc.

| Block | Position | Why |
|---|---|---|
| microSD | Left short edge | SD0 is the entire left package edge |
| Power regulators | Bottom long edge | VDDQ, SEQ, VBAT_DET all bottom-edge pins |
| Crystal | Near pins 45–46 | Right edge, lowest pins. Needs full ground shielding. **Keep the run short — it has drifted twice** |
| WiFi module | Right of the SoC | SD1 is right edge — keeps SDIO short |
| **Audio (U9 amp, U10 mic)** | **Right short edge, ex-RJ45 zone** | I²S is pins 62–65 on the right edge. Amp output to JST needs ≥2 vias |
| **Speaker JST** | **Right or bottom-right edge** | Short, direct run from the amp |
| USB-C | Top long edge, right of centre | USB pins are top edge near the right corner |
| Castellations | Both long edges | Spare GPIO exits top and bottom |

**Do not rotate the SoC for connector aesthetics.** The 40 mm Ethernet cliff that used to force this is gone, but the pinout argument stands on its own: SD0 is the whole left edge, the power pins are the bottom edge, SD1 and I²S are the right edge.

**Two placement rules from the vendor audio guide** (`02_SOPHGO_Audio_Hardware,_Structural_Design_and_Device_Selection_Instruction`):

- **§2.2.4** — amplifier input and output routing must not cross; the supply capacitor sits as close to the amp as the layout allows; the direct run from amp output to the speaker connector carries **at least 2 vias**
- **§4.1** — the **mic must face away from the speaker**, or the angle between them be maximised, to limit acoustic coupling. The INMP441 is bottom-port, so it needs an acoustic hole through the PCB with the pad ring from its recommended land pattern

### Routing order

Power shapes → USB → SDIO1 (WiFi) → SDIO0 (microSD) → SPI NOR → crystal → **I²S audio** → everything else.

I²S moved late in the order: it is single-ended, has no impedance or matching constraint, and at ~3 MHz BCLK it is the most tolerant bus on the board. Route it around the constrained nets, not before them.

Never route GPIO before the constrained nets.
