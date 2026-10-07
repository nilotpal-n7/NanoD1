# 05 — Signoff Checklist

Part A is Sophgo's own 16-item checklist, translated and scoped to this board.
Parts B–D cover what their checklist doesn't — mostly schematic items, several of which are board-killers.

Board: **66 × 38 mm** · 4-layer · SG2002 QFN88 · SPI NOR + microSD · AP6212 WiFi · **I²S audio** · no MIPI, **no Ethernet**.

---

## Part A — Vendor checklist

### Stackup

| # | Requirement | ✓ |
|---|---|---|
| A1 | Prepreg ≤ 5 mil post-lamination (excluding copper). L2/L3 core ≥ 25 mil. **1 oz every layer.** Dk entered as 4.07 / 4.0 / 3.5. | ☐ |

### Differential routing

| # | Rule | Requirement | ✓ |
|---|---|---|---|
| A2 | DDR | 3 vias in the E-pad mask-covered region (7.6 × 7.6 mm). **Copy the reference DDR routing / via / cap layout from beneath the package.** | ☐ |
| A3–A5 | MIPI | — | **N/A** |
| A6 | USB impedance | Fab solves in Polar: surface *Diff Coated Coplanar Strips with GND 1B*, inner *Diff Offset Coplanar Strips 1B1A* | ☐ |
| A7 | USB length match | P/N intra-pair ≤ 10 mil | ☐ |
| A8–A9 | EPHY | — | **N/A — Ethernet removed.** USB is now the only differential pair on the board. |

### Single-ended and shielding

| # | Rule | Requirement | ✓ |
|---|---|---|---|
| A10 | Single-end (SDIO) | Shielding rule applied | ☐ |
| A11 | EMMC / SPI NOR | Shielding rule applied; SPI_CLK individually shielded | ☐ |
| A12 | **Audio** | **Now live — digital I²S on pins 62–65.** Shielding rule applied to `I2S_BCLK`, `I2S_LRCK`, `I2S_DOUT`, `I2S_DIN`. BCLK and LRCK are the aggressors — keep them off the analog rails and off `WIFI_ANT`. Vendor's analog-audio items (AVREF filtering, ground splits at the codec) do **not** apply; see `02-netmap` §5.2. | ☐ |
| A13 | **XTAL** | Per-trace GND shield, 0.25 / 0.25 mm | ☐ |
| A14 | RTC | Shielding rule applied | ☐ |
| A15 | WIFI_ANT | Fab solves *Coated Coplanar Strips with GND 1B*, 50 Ω | ☐ |

### Power

| # | Rule | Requirement | ✓ |
|---|---|---|---|
| A16 | **VDDC** (printed "VDC" — typo in source) | Cap count and positions, via count at SoC and regulator, VDDC/GND via rule at each cap. Channel widths per Rule 2. **Copy the reference layout beneath the package.** | ☐ |
| A17 | **Analog IO power** | Trace widths, cap count and positions, via counts, power/GND via rule at each cap. **Copy the reference layout beneath the package.** | ☐ |

---

## Part B — Schematic items the vendor checklist omits

Every one is sourced from the datasheet, hardware design guide, or reference schematic. These are the ones that stop a board booting.

| # | Item | Requirement | ✓ |
|---|---|---|---|
| B1 | **VDDC = 0.95 V** | Not 0.9 V. Re-derive the FB divider before fab. | ☐ |
| B2 | **Core sized for ~1.5 A** | 1220 mA TPU + 258 mA core. 2 A regulator, inductor rated to match. | ☐ |
| B3 | **UART0_TX (18) pull-up** | 4.7 kΩ to 3.3 V. Pull-down = ROM fail mode. | ☐ |
| B4 | **PWR_VBAT_DET (38) divider** | 30 kΩ / 10 kΩ from 5 V → 1.25 V, 1%. Chip will not start without it. | ☐ |
| B5 | **Boot straps (22, 23)** | 4.7 kΩ each, fitted as reworkable 0402 jumpers | ☐ |
| B6 | **GPIO_RTX / EPHY_RTX (67) strap** | **Survives the Ethernet removal.** Despite the name it is an ordinary 1.8 V GPIO (group G12) carrying `CPU_SEL`; EPHY_RTX is only its alternate function. Pull-up to **VDDIO_RTC 1.8 V** = C906 RISC-V. Not 3.3 V. | ☐ |
| B7 | **USB series R ≤ 5.1 Ω** | At the **connector** end. ESD < 5 pF parasitic. | ☐ |
| B8 | **USB-C CC resistors** | 5.1 kΩ on CC1 **and** CC2 — two separate resistors | ☐ |
| B9 | ~~EPHY series R~~ | **N/A — Ethernet removed.** Replaced by B18–B22 below. | — |
| B10 | **25 MHz crystal** | < ±30 ppm, 4-pin SMD, both GND pins bonded. **1 MΩ across XIN/XOUT not omitted.** NP0/C0G load caps. | ☐ |
| B11 | **VDDC_RTC (37)** | Cap to GND only. **Not driven from any supply.** | ☐ |
| B12 | **Power sequencing** | Core ≤ 1.8 V, then 3.3 V only after 1.8 V established. 3.3 V enable gated by PWR_SEQ2 (41). Down = reverse. | ☐ |
| B13 | **No peripheral before its IO domain** | SD card and WiFi on the SEQ2-gated 3.3 V rail | ☐ |
| B14 | **PWM0_BUCK network NC** | Footprints placed, not populated | ☐ |
| B15 | **X5R or X7R only** | Y5V explicitly prohibited | ☐ |
| B16 | **Flash from validated list** | W25Q128JVSIQ **(1T)** or listed equivalent. Suffix matters. | ☐ |
| B17 | **WiFi from validated list** | AP6212 — only SDIO option with a mainline driver | ☐ |

### Audio — added with the I²S pivot

Sources: SG2002 Datasheet Table 2-12, MAX98357A datasheet Table 5 / Figure 4, INMP441 datasheet, `04_SG2002_PINOUT.xlsx` sheet 6. Full reasoning in `02-netmap` §5.2.

| # | Item | Requirement | ✓ |
|---|---|---|---|
| B18 | **Mic runs on VDD1V8** | INMP441 VIH = 0.7 × VDD. At 3.3 V that is 2.31 V, which a 1.8 V pad can never reach. **Not a preference — a hard constraint.** | ☐ |
| B19 | **INMP441, not ICS-43434** | ICS-43434 VOH = 0.65 × VDD = 1.17 V, *below* the SoC's 1.26 V VIH. INMP441 gives 1.62 V. | ☐ |
| B20 | **SD_MODE = 300 kΩ to pin 48** | 300 kΩ pull-up at 1.8 V selects (L/2 + R/2) mono downmix and keeps GPIO shutdown. 69.8 kΩ = right channel; direct high = left. Getting this resistor wrong silently changes the channel. | ☐ |
| B21 | **GAIN_SLOT 100 kΩ to GND, DNP** | Unconnected = 9 dB. Populated through 100 kΩ = 15 dB. Direct to GND = 12 dB. Backwards from intuition — check the footprint is DNP in the BOM. | ☐ |
| B22 | **100 kΩ pull-down on `I2S_DIN`** | Pads 62–65 sit outside the IO blocks; do not assume an internal pull. Stops the SoC input floating when the mic is unpopulated. | ☐ |
| B23 | **22 Ω series footprints on BCLK and LRCK** | Near the SoC, **DNP** by default. Insurance against ringing into two loads. | ☐ |
| B24 | **Amp on VDD3V3, not VBUS_5V** | 5 V only exists while USB-C is plugged, and is the noisiest rail. 3.3 V also satisfies Maxim's *VDD > VDDIO* condition, so SD_MODE needs no series limiter. | ☐ |
| B25 | **DS = 1 in the pinmux** | Table 2-12: IOH 4.0 mA (DS=0) → 4.7 mA (DS=1). The SoC → amp margin is only +100 mV worst case. | ☐ |
| B26 | **C59 stays** | 1 µF on `AUD_AVREF` (pin 3). Required by the reference schematic even though the analog audio block is now unused. | ☐ |

---

## Part C — Layout items beyond the vendor list

| # | Item | Requirement | ✓ |
|---|---|---|---|
| C1 | **E-pad GND via array** | ~20 vias distributed across the pad. Chip's **only** ground return besides pin 1. | ☐ |
| C2 | **Board > 38 mm → wider channels** | VDDC W2 ≥ 1.5 mm, VDDQ W2 ≥ 1.5 mm, **effective after antipads**. The board's short dimension is now **exactly 38 mm** — at the boundary, so apply the wider rule. | ☐ |
| C3 | **VDDC cap cascade** | 0.1 µF at the chip, 1 µF next, 4.7 µF mid, 10 µF **at the regulator** | ☐ |
| C4 | **One via per power pin, at the pin** | 5 for VDDC; likewise each analog rail | ☐ |
| C5 | **One GND via beside every cap** | Not automatable — check by eye | ☐ |
| C6–C7 | ~~EPHY run / shield~~ | **N/A — Ethernet removed.** Replaced by C14–C17 below. | — |
| C8 | **Stitching vias ≤ 7.5 mm** | Along the USB shield. (EPHY half of this item is gone.) | ☐ |
| C9 | **Antenna plane cutout** | All layers cleared beneath. 0.762 mm trace, referenced to **L4**. | ☐ |
| C10 | ~~Ethernet chassis isolation~~ | **N/A — Ethernet removed.** `CHGND` is gone, and with it the isolated chassis island on L2. Confirm no orphan island survives in the L2 pour. | ☐ |
| C11 | **L3 shape plan** | VDDC horseshoe + analog pours + central GND island — planned, not improvised | ☐ |
| C12 | **Header IO domains silkscreened** | 3.3 V and 1.8 V sections marked on **both** sides | ☐ |
| C13 | **No strap pin exposed on the header** | A jumper wire on a strap boots the wrong CPU or device | ☐ |

### Audio layout — added with the I²S pivot

From `02_SOPHGO_Audio_Hardware,_Structural_Design_and_Device_Selection_Instruction` and the INMP441 datasheet. Floorplan in `03-layout-rules` §8.

| # | Item | Requirement | ✓ |
|---|---|---|---|
| C14 | **Amp in / out do not cross** | §2.2.4. Supply capacitor as close to the amp as the layout allows. | ☐ |
| C15 | **≥ 2 vias amp → speaker connector** | §2.2.4, on the direct run to the JST. | ☐ |
| C16 | **Mic faces away from the speaker** | §4.1 — or the angle between them maximised. Needs a discrete acoustic cavity and an anti-vibration bushing (enclosure work). | ☐ |
| C17 | **Acoustic hole under the INMP441** | Bottom-port part. Take the hole diameter and pad-ring rules from the recommended land pattern **before** placing it — this drives a board cut-out, not just a footprint. | ☐ |
| C18 | **No analog audio ground island** | §2.1.1 / §2.2.1's discrete audio ground, 0 Ω bridge and DC isolation caps do **not** apply to a digital bus. If one exists from the old scope, remove it. | ☐ |

---

## Part D — Fab and assembly

| # | Item | Requirement | ✓ |
|---|---|---|---|
| D1 | Stackup called out | 1 oz all layers, ≤ 5 mil prepreg, ≥ 25 mil core. Not the vendor default. | ☐ |
| D2 | Impedance table on Draftsman | With both Polar structure names | ☐ |
| D3 | Castellation note | Edge plating is a manual process — state it | ☐ |
| D4 | Matte black mask + ENIG | Both specified in the order | ☐ |
| D5 | 0.35 mm pitch assembly | Stencil + reflow, or paid assembly. Hand-soldering is not viable. | ☐ |
| D6 | Test points on every rail | 5 V, 3.3 V, 1.8 V, 1.35 V, 0.95 V, plus PAD_ZQ and PWR_SEQ1/2 | ☐ |
| D9 | **Speaker not fitted for first power-on** | Leave the JST unmated until the amp's SD_MODE and gain settings are confirmed. A wrong GAIN_SLOT populate is 15 dB into an 8 Ω driver. | ☐ |
| D7 | Bring-up table printed | `09_SG2002_QFN88_Impedance_Analysis_Reference_Table` | ☐ |
| D8 | Two boards ordered | You will destroy one | ☐ |

---

## Bring-up

**Order matters.** Do not populate the SoC until the power tree is verified.

1. **Power tree alone, SoC not fitted.** Scope all five rails on a slow ramp. Verify sequencing against B12 — core leads or ties with 1.8 V, 3.3 V comes last. Confirm PWR_VBAT_DET sits at 1.25 V.
2. **Populate the SoC.** Before applying power, check pin-to-GND resistances against the table in `02-netmap.md` §6. VDDC pins should read 48–53 Ω; USB_DP/DM ~87 kΩ. A short here is a solder defect, not a design fault.
3. **Confirm the 25 MHz crystal oscillates.** Probe with a low-capacitance probe or watch the current draw.
4. **UART0 console at 115200.** If nothing prints, check B3 first — the UART0_TX strap is the most common cause of a silent board.
5. **microSD boot** → WiFi → **audio**.
6. **Audio last, and only after the EPHY release sequence is written.** Pins 62–65 stay dead until the register writes in `02-netmap` §5.2 run — the pads are held by the EPHY block, not the pinmux. Set DS = 1 in the same pass. Then check for BCLK on pin 63 with a scope *before* concluding anything is broken.

**If DDR init fails:** check VDDQ ripple and PAD_ZQ before anything else. That's the design guide's own first diagnostic.

**If the wrong architecture boots:** GPIO_RTX (67) strap, and confirm it pulls to 1.8 V not 3.3 V.

**If audio is silent:** in this order — (1) the EPHY release sequence ran; (2) BCLK/LRCK present at the amp; (3) SD_MODE resistor is 300 kΩ, not 69.8 kΩ or a direct tie; (4) pin 48 is actually driving high. Do not start by suspecting the speaker.

Keep a written log. A first spin has roughly a 50/50 chance of booting, and the log is what makes rev B quick.

---

## Added after the pour session — check these before ordering

| # | Item | Status |
|---|---|---|
| **P1** | **DNP parts are not marked in the pick-and-place.** All 143 rows read `Variation = Fitted`, including R13, R14, R56, R58, R59. Create an Altium **Variant** and regenerate the assembly output, or JLC populates them | **OPEN — can scrap a build** |
| **P2** | **CPL must use Center-X / Center-Y, not Ref-X / Ref-Y.** Eight parts differ: J5A and J5B by **11.43 mm**, J4 by 10.16, J3 by 3.81, J2 by 2.18, E1 by 0.76, U2 by 0.56, J6 by 0.55 | **OPEN — can scrap a build** |
| **P3** | **Via-in-pad: 185 instances** (160 excluding U1's thermal pad). Unfilled vias in 0402 terminals wick solder during reflow. Decide on resin plugging and note it in the Draftsman drawing. **Do not rework them** | **OPEN — decision, not rework** |
| **P4** | **Antenna feed impedance (see C9).** `WIFI_ANT` on Top already has ground copper 0.02–1.07 mm from its edge, so it is a coplanar waveguide, not the 50 Ω microstrip `SE50_ANT` assumed. An L1 pour cutout at `44.5,25.5 → 48.6,25.5 → 48.6,36.5 → 44.5,36.5` stops it worsening. Accept and document, or rework the feed | **OPEN** |
| **P5** | **C12 designator sits on C17's pads.** Two of the six open DRC violations. Cosmetic to the fab, but the silkscreen mislabels a part for anyone doing rework | **OPEN** |
| **P6** | **Component heights: 89 of 143 read 0.0000 mm** | **OPEN** |
| **P7** | **L2 plane voids** — 34.6 mm² under the microSD carrying SD0 returns, 9.0 mm² above it, two 4.8 mm² slots on the USB return path near J2 | **OPEN** |
| **P8** | **221 redundant GND traces on L2** under the pour. Delete, repour, re-run DRC | **OPEN** |
| **P9** | **Stitching vias ≤ 7.5 mm along the USB shield** | **OPEN** |
| P10 | All four layers poured, no shorts between pours, DRC clean apart from 6 silk violations | **DONE** |
| P11 | VDD1V35 buck-to-SoC resistance 47.3 mΩ (14 mV at 0.3 A) | **DONE** |
