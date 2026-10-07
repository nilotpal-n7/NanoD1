# 06 — Corrections Log

Every error caught and fixed, with how it was caught. **This is the most important file in the set** — it's what stops a future session confidently restating something we already proved wrong.

Read this before trusting any board-specific claim.

---

## Rail voltages and regulator values

| Item | Wrong | Correct | Source |
|---|---|---|---|
| **VDDC** | 0.90 V | **0.95 V** | Hardware Design Guide: "typical is 0.9 V (SG2002 is 0.95 V)". Reference schematic annotates "Need 0.95V !!!" |
| **VDDC feedback divider** | Reference fits 10k/20k = 0.90 V | **11k8 / 20k = 0.954 V** | Reference netlist R39/R43. Their value is the CV181x one — **do not copy it** |
| **Core current** | ~300 mA | **~1.48 A** (1220 TPU + 258 core) | Reference power-tree block diagram |
| **Core regulator headroom** | assumed adequate | **ETA3414 is 1.5 A max, 1.6 A current limit** — no margin. Foldback to 1.2 A below −25 °C | ETA3414 datasheet |
| **VDDQ** | "may be internal to the SiP" | **External 1.35 V supply**, pins 31–34 | SG2002 datasheet §Recommended Operating Conditions |

## Package and footprint

| Item | Wrong | Correct | Source |
|---|---|---|---|
| **QFN pitch** | 0.4 mm | **0.35 mm** | Datasheet: QFN88, 9×9×0.9 mm |
| **Pad size** | assumed | **0.200 × 0.750 mm** | Cadence padstack filename `r_0d2x0d75` + IPC-2581 export |
| **Thermal pad** | assumed | **6.000 × 6.000 mm** exposed, 7.6 × 7.6 mm mask-covered | `s_6d0x6d0.pad` + IPC-2581 |
| **E-pad via count** | ~20 estimated | **39** — 27 inside the 6×6, 12 in the mask ring | Measured from IPC-2581 export |

## Stackup and impedance

| Item | Wrong | Correct | Source |
|---|---|---|---|
| **Prepreg** | 0.2 mm | **5 mil (0.127 mm)** | Layout guide slide 10 |
| **Dk values** | FR-4 defaults | **Prepreg 4.07, core 4.0, mask 3.5** | Layout guide reference stackup |
| **90 Ω geometry** | 0.20 / 0.20 mm | **0.127 / 0.10 / 0.15 mm** coplanar | Layout guide impedance table |
| **100 Ω geometry** | 0.20 / 0.30 mm | **0.127 / 0.127 / 0.15 mm** coplanar | Same |
| **Antenna 50 Ω** | assumed microstrip | **0.762 mm wide, referenced to L4**, planes cut beneath | Layout guide |
| **`.brd` stackup** | — | **Ignore it.** Uniform 8 mil dielectric = Allegro placeholder, never filled in | IPC-2581 export |

## Straps and boot

| Item | Wrong | Correct | Source |
|---|---|---|---|
| **CPU select default** | assumed RISC-V | **Internal pull-DOWN = Cortex-A53.** R15 must be POPULATED for RISC-V | Datasheet + reference netlist (their R16 is NC) |
| **Boot straps** | assumed populated | **Reference populates NONE** — relies on internal pulls | Reference netlist: R11, R14, R16 all NC |
| **SPI NOR strap polarity** | both pull-up | **Pin 23 pulls DOWN**, pin 22 pulls up | TRM boot chapter |
| **SD boot mode** | assumed a fallback exists | **No SD boot mode exists.** SD0 and eMMC share one controller — "eMMC" strap + card fitted *is* card boot | TRM boot chapter |
| **UART0_TX** | not identified as a strap | **Boot strap.** Pull-down = ROM fail mode | Reference schematic: "Do not Delete!!!" |
| **UART0_RX** | unpulled | Reference pulls it up too | Reference netlist R6 |

## Peripherals

| Item | Wrong | Correct | Source |
|---|---|---|---|
| **Crystal** | omitted entirely | **25 MHz mandatory**, <±30 ppm, 4-pin, both case grounds bonded, 1 MΩ across XIN/XOUT | Hardware Design Guide |
| **Crystal pin numbers** | XO on pin 2 | **Pins 1 and 3 are the crystal; 2 and 4 are case ground** | Epson TSX-3225 datasheet |
| **Ethernet RSET** | claimed one exists | **No reference resistor exists.** 5.1 Ω series only, no RC filter | Hardware Design Guide + reference schematic |
| **Ethernet pin naming** | — | **TX/RX and P/N are both crossed.** Pin 62 named `PAD_ETH_TXP` carries `EPHY_RXN` | PINOUT xlsx |
| **Bob Smith network** | 4× 75 Ω + 1 nF as discretes | **Internal to HR911105A.** R30–R33 and C39 deleted | HR911105A symbol |
| **AP6212 supplies** | one rail | **Two: VBAT and VDDIO** | AP6212 datasheet |
| **AP6212 pins 21/23** | tie both to VBAT | **Internal buck: 4.7 µH between them, 10 µF on pin 23. Never tie to a rail** | FriendlyELEC NanoPi NEO Air + Rockchip PX30 reference designs |
| **AP6212 NC pins** | — | **5, 8, 29, 30, 32, 35, 37, 38, 47 must FLOAT** — datasheet says do not ground | AP6212 datasheet |
| **SG2002 pin 3 (AVREF)** | left floating | **Needs 1 µF to ground** even with audio unused | Reference schematic |
| **EPHY run endpoints** | "measure U1-62 → J1-1" | **Not a path.** Every EPHY pair is split by a 5.1 Ω series resistor, so each run is two hops: U1.65→R26→J1.1, U1.64→R27→J1.2, U1.63→R28→J1.3, U1.62→R29→J1.6. SoC-side and connector-side pin order do **not** correspond — U1.62 and J1.1 are different pairs | `NanoD1.PcbDoc` net records |

## Board outline

| Item | Wrong | Correct | Source |
|---|---|---|---|
| **Board size** | 65 × 30 mm → 70 × 35 mm | **75 × 38 mm** | `NanoD1.PcbDoc` outline 0 … 75.00 × 0 … 38.00, relative origin at the board corner |
| **`03-layout-rules` §0, §3.1, §5, §8** | reasoned from 65 × 30, then 70 × 35 | **Corrected twice.** Conclusions survive — the ">38 mm" test in §5 was tripped at every size. Note the short dimension is now 38 mm, *at* the deck's boundary rather than inside it | Same |

The dimension has now changed three times and been missed in the docs twice. **When a board dimension changes, grep every file in this set for the old value before doing anything else.**

## Ethernet removal and the audio pivot

Ethernet was dropped in favour of a digital I²S audio subsystem (mic + Class-D amp). Errors caught while planning that change:

| Item | Wrong | Correct | Source |
|---|---|---|---|
| **Ethernet remove list** | "delete R30–R33 (75 Ω Bob Smith) and C39 (1 nF 2 kV)" | **Those parts do not exist.** Deleted long ago — the Bob Smith network is internal to the HR911105A. Actual removal list is 9 parts: J1, R26–R29, R34, R35, R36, DA1 | `NanoD1.PcbDoc`; this log, Peripherals |
| **I²S pin selection** | "pick any three spare GPIO — pins 48, 49 or 72–87 — and configure them in the device tree" | **I²S is a hardware pinmux function on specific pads, not assignable to arbitrary GPIO.** Pins 48/49 have no I²S function at all | `04_SG2002_PINOUT.xlsx` sheet 1 |
| **Which pads carry I²S** | — | **The four EPHY pads themselves, at fmux function 7.** 63 → IIS2_BCLK, 62 → IIS2_LRCK, 64 → IIS2_DO, 65 → IIS2_DI. Exactly the four signals needed on exactly the four pads Ethernet vacates; zero extra pins consumed | Same |
| **MAX98357A gain** | "100 kΩ to GND = 9 dB" | **100 kΩ to GND = 15 dB.** Direct to GND = 12 dB. **Unconnected = 9 dB** | MAX98357A datasheet, Gain Selection |
| **MAX98357A SD_MODE** | treated as a simple enable | **It selects the output channel.** Internal 100 kΩ ±8% pulldown, three trip points: direct-high = Left, 69.8 kΩ = Right, **300 kΩ = (L/2 + R/2)**, low = shutdown. Values are for VDDIO = 1.8 V | MAX98357A Table 5, Table 6, Figure 4 |
| **ETH GPIO drive strength** | *I inferred* that pads 62–65 have no drive control, because TRM Table 3.5 leaves their IOGroup blank | **They have a DS bit.** IOH 4.0 mA (DS=0) / 4.7 mA (DS=1); IOL 8.8 / 10.2 mA. Set DS = 1 | SG2002 Datasheet **Table 2-12** |
| **Digital mic choice** | *I recommended* ICS-43434 on size and procurability | **Use INMP441.** ICS-43434 VOH = 0.65 × VDD = 1.17 V at 1.8 V, *below* the SoC's VIH of 1.26 V — it clears only the Schmitt VT+ max (1.14 V) by 30 mV, and its VOH is "guaranteed by design", not tested. INMP441 gives 0.9 × VDD = 1.62 V at 0.25 mA | ICS-43434 & INMP441 datasheets vs Datasheet Table 2-12 |
| **Mic supply rail** | "1.8 V or 3.3 V" | **1.8 V, mandatory.** Mic VIH is 0.7 × VDD; at 3.3 V that is 2.31 V, which a 1.8 V pad can never reach | INMP441 datasheet + Table 2-12 |
| **EPHY pads as GPIO** | assumed the pinmux alone is enough | **The EPHY must be told to release them** via a documented register sequence starting `0x03009804[0] = 1'b1`. Without it the pins are dead and the board looks broken | `04_SG2002_PINOUT.xlsx` sheet 6 |
| **Pin 67** | listed as "EPHY_RTX" and assumed Ethernet-related | **`GPIO_RTX___EPHY_RTX`, an ordinary 1.8 V GPIO in group G12.** EPHY_RTX is its alternate function. It carries `CPU_SEL` and is unaffected by dropping Ethernet | SG2002 TRM Table 3.5 |
| **USBLC6-2SC6 wiring** | D1 pins 4 and 6 as drawn | **D+ and D− were crossed through the ESD array.** Pins 1 & 6 are one internal line (I/O1), 3 & 4 the other (I/O2). As drawn, connector D+ reached the SoC as D−. Swap the nets on pins 4 and 6 | ST USBLC6-2SC6 datasheet Figure 1 + `NanoD1.PcbDoc` net trace |

## Footprint defects found by DRC

| Footprint | Defect | Fix |
|---|---|---|
| **C0402** | pads 0.640 × 0.900 mm on a **0.660 mm pitch** — 0.240 mm overlap. Every 0402 capacitor was a dead short across its own terminals (45 short-circuit violations) | Replaced with manufacturer footprints |
| **C0805** | 1.85 × 1.40 on 1.05 pitch — **0.80 mm overlap**. The 22 µF bulk caps | Replaced |
| **IND2520** | 2.14 × 1.63 on 1.73 pitch — **0.41 mm overlap** | Replaced with `FP-DFE252010C-MFG` |
| **C0603, R0402** | 0.100 mm pad gap against a 0.15 mm clearance rule — legal-but-tight, not shorts | Replaced |
| **QFN88-9x9-0.35** | signal pads **1.250 mm long instead of 0.750**, so each corner pad collided with the perpendicular pad on the adjacent edge — 4 hard shorts including **VDD3V3 ↔ CPU_SEL** | Pads set to 0.200 × 0.750, each edge moved 0.25 mm outward to keep the toe fixed |
| **AP6212-12x12** | silk outline 0.076 mm from its own pad masks against a 0.1 mm rule (45 violations) | Outline moved from ±6.4 to ±6.5 mm |
| **DM3AT microSD** | Keep-Out area fills overlapping the socket's own pads by up to 0.25 mm | Open — see Still unverified |

The pattern in the first three: the pad length was entered as roughly the body length and the pitch as something smaller. **Check the edge-to-edge gap, not the pad size, on every hand-built chip footprint.**

## Tooling and file format

| Item | Wrong | Correct |
|---|---|---|
| **Vendor CAD files** | "Altium symbol and footprint published" | **Cadence only.** `.OLB`/`.DSN` import via OrCAD; `.dra`/`.psm`/`.pad` do not |
| **Allegro version** | — | Altium imports up to **17.4**. Files are 16.6, extracta was 24.1 — needed DB Doctor to upres |
| **OrCAD import setting** | "convert off-page connectors to Ports" | **Wrong for a flat design** — broke cross-sheet connectivity, 145 nets became 77 |

## Schematic errors found by review

| Item | Found by |
|---|---|
| **Fake bus nets** (`SD0_BUS`, `SPI_BUS`, `XGPIOC_1V8`, J5 `GPIO`) would have shorted 16 pins together | User review of the viewer |
| **GND renamed to `USB_VBUS_DET`** — stray net label shorted the entire ground net | Compiler message |
| **U8 pin 2 not on GND** — LDO ground floating, missed by compiler because Power pins don't error | Netlist diff |
| **14 component value errors** — R44, R45, R48, R49 (feedback dividers), R16, R17 (VBAT divider), R50, R51, L1, L3, C17, C18, C21, C22, C43, C50–C53 | BOM audit against design intent |
| **U4 rotation direction** — clockwise moves top to right, not left | User correction |

---

## Still unverified

| Item | Status |
|---|---|
| Thermal-pad **stencil segmentation** | Not in any vendor document. Target 50–70% coverage, window-pane array. Confirm with assembler. |
| **Core buck current headroom** | ETA3414 at 1.48 A of 1.5 A. Reference ships it. Consider a 2 A+ part if the NPU will be loaded. |
| **AP6212 LPO** | Routed to SoC pin 88, but whether WiFi-only needs it is unconfirmed. |
| **Crystal load caps** | 18 pF assumes 3 pF stray. Tune on the bench. |
| **microSD Keep-Out fills** | Four Keep-Out area fills in `FP-DM3AT-SF-PEJM5_40-MFG` overlap the socket's own pads. Deleting them clears 6 DRC violations but discards the routing exclusion around the eject spring and shell rails. Decision deferred — get the Hirose recommended-PCB-layout figure and redraw them shrunk, or move them to Mechanical 15. |
| **SoC → MAX98357A logic margin** | VOH 1.40 V min vs VIH 1.30 V = 100 mV worst case, but that VOH is specified at 4.0–7.4 mA and the real load is ~30 pF at 3.072 MHz. Set DS = 1 and keep the 22 Ω series footprints. Verify on the bench. |
| **I²S amp vs AEC** | Sophgo audio guide §3.2 warns an I²S amplifier degrades acoustic echo cancellation because the reference is sampled before conversion. Irrelevant for playback and recording; matters if full-duplex voice is ever wanted. |
| **INMP441 acoustic hole** | Bottom-port. Hole diameter and pad-ring rules must come off the recommended land pattern before placement. Mic must face away from the speaker (audio guide §4.1). |
| **`bom-corrected.csv` coverage** | 118 rows against 138 components. Missing U1, U2, U4, J1, J2, J3, J4, Y1, SW1, SW2, E1, TP1–TP8 — every connector, the SoC, the WiFi module, the crystal and the switches. Cannot be handed to an assembler as-is. |
| **Component heights** | 85 of 138 parts report Height = 0.00 mm in the pick-and-place. Breaks 3D clearance checks and gives the assembler nothing. |
| **LED comment convention** | LED1/LED2 use the MPN as Comment; FB2/FB5 use the value. Pick one before the BOM pass. |
| **J5 removal** | The 20-pin GPIO header was deleted (139 → 138 components) and P4 renamed J4. `03-layout-rules` §8 and `02-netmap` §5.8 still assume spare GPIO exits on both long edges. Confirm intent. |

---

## Design-rule defects found by measuring the PcbDoc

| Item | What was set | What is true | Source |
|---|---|---|---|
| **Power Width rule Minimums** | `PWR_CORE` Min 0.8, `PWR_1V35` 0.5, `PWR_3V3` 0.4, `PWR_1V8` 0.3 mm | **All five exceed the 0.200 mm SG2002 pad, making those nets unroutable into U1.** Min must drop to 0.15 mm; Preferred is what sets the routed width | `NanoD1.PcbDoc` Pads6 — every U1 signal pad measures 0.200 × 0.750 mm |
| **SG2002 pad size** | assumed "wide enough" | **0.200 × 0.750 mm**, thermal pad 6.000 × 6.000 mm | Pads6 |
| **Keep-Out layer id** | I read layer 56 as "Mechanical 16, not keepouts" | **Layer 56 IS the Keep-Out layer.** The 5 fills near the microSD are genuine keepouts. My layer-number mapping was wrong | Altium layer ids: 1 Top, 2–31 Mid, 32 Bottom, 33/34 Overlay, 39–54 Internal Plane, 55 Drill Guide, **56 Keep-Out**, 57–72 Mechanical 1–16, 74 Multi-Layer |
| **Antenna plane cutout** | I said "no keepout objects on layer 40, so the cutout isn't drawn" | Conclusion right, reasoning wrong — layer 40 is Internal Plane 2, not Keep-Out. The cutout still is not drawn; the only keepouts on layer 56 are the five around the microSD | Fills6 |
| **MAX98357A pin numbers** | I invented BCLK=5, LRCLK=6, DIN=7, GAIN=4, SD_MODE=3, OUT=8/9, VDD=2, GND=1 for the HTML viewers | **Wrong on every pin.** Real TQFN-16: DIN 1, GAIN_SLOT 2, GND 3/11/15, SD_MODE 4, N.C. 5/6/12/13, VDD 7/8, OUTP 9, OUTN 10, LRCLK 14, BCLK 16, EP not internally connected | MAX98357A datasheet, Pin Description p.15 |
| **INMP441 pin count** | I drew it as a 6-pin part | **LGA-9.** SCK 1, SD 2, WS 3, L/R 4, GND 5/6/9, VDD 7, **CHIPEN 8**. A low or floating CHIPEN powers the mic down | INMP441 datasheet Table 6, p.8 |
| **INMP441 SD pull-down** | my inference | **Vendor instruction**, not inference: "The SD trace should have a 100 kΩ pulldown resistor" | Same datasheet |
| **`ETH` net class** | `01-design-brief` listed one as planned | **Never created.** Net classes on the board are RF, XTAL, SPINOR, SDIO, PWR_5V, PWR_1V35, PWR_1V8, PWR_3V3, PWR_CORE | Classes6 |
| **Differential pairs** | thought there were 2 Ethernet pairs | **Four** — ETH_RX_MAG, ETH_TX_MAG, ETH_RX_SOC, ETH_TX_SOC — plus 3 USB. All four ETH now deleted | DifferentialPairs6 |
| **E1 ground stub** | — | GND via at (56.025, 33.000) feeds a 0.925 mm stub on **L2** ending at y 33.925. E1 pad 3 spans y **33.950**–35.000. **25 µm short of the pad** | Tracks6 + Pads6 |

## Board resize #4, and what the first pour showed

| Item | Was | Is | Source |
|---|---|---|---|
| **Board size** | 65 × 30 → 70 × 35 → 75 × 38 | **66 × 38 mm** | `NanoD1.PcbDoc` Board6 outline, 0…66.000 × 0…38.000 |
| **L2 ground plane** | "solid GND, unbroken" — assumed | Was **236 hand-routed tracks**, no pour at all, until the GND pour was placed. `Polygons6` had been 0 bytes for the whole project | Tracks6 / Polygons6 |
| **VDD1V8 + AUD_AVREF on L2** | — | 21 tracks were splitting the plane; moved to L3. AUD_AVREF was then rerouted on L1/L4 | Tracks6 |
| **Polygon connect for exposed pads** | one Relief rule for everything | Relief spokes (0.25 mm) are **wider than U1's 0.200 mm pads**. `PolyConnect_Thermal` now scopes U1 and U9 to Direct, priority above the All rule | Rules6 |
| **Poured-region net** | a child region reads `net = 0xFFFF` | **Not a fault.** Poured regions inherit the net from their parent polygon; only the polygon record carries `NET` | Regions6 / Polygons6 |
| **Region vs polygon** | I advised a pour cutout to fix the U10 clearance | **Wrong** — the offending copper was a Region inside the U10 footprint, and cutouts only affect polygons | Regions6 |
| **U10 sound-port hole** | pad 0.750 / hole 0.750 | Changed to **0.600 / 0.600**. Pad and hole must move together — shrinking only the hole creates an annular sliver that trips the ring rule | Pads6 |
| **INMP441 land pattern** | I suspected the 0.1 mm pad 5 was a defect | **Correct as drawn.** Datasheet Figure 14 lands only 8 pads at 0.40 × 0.60 plus the through hole | INMP441 datasheet p.17 |


## The L3 power-pour session — measurement errors of mine, and what the file actually said

| Item | What I claimed | What is true | Source |
|---|---|---|---|
| **VDDC plane "waist" = 0.30 mm** | I reported the VDDC pour pinched to 0.30 mm against a 1.5 mm requirement and framed it as a redesign-level defect | **Measurement artifact.** I seeded a max-bottleneck path search at a *via centre*, which sits inside its own antipad, so the whole path inherited that 0.15 mm radius. Re-measured correctly the corridor is **1.9 – 8.3 mm wide**, narrowest slice **1.42 mm** at y ≈ 18 over ~1 mm of length | Regions6 rasterised at 0.02 mm + `distance_transform_edt`; seed the search from a ring *outside* the antipad, never at the via centre |
| **A Top-layer GND pour would detune WIFI_ANT** | I told him to hold the L1 pour because pouring beside a 0.762 mm microstrip would drop it off 50 Ω | Premise was wrong. Top GND copper was **already 0.02 – 1.07 mm from the trace edge** along its whole length before any pour. The trace is already an unintended coplanar waveguide. The pour does not create the problem — it is pre-existing, and it is signoff item C9 | Tracks6/Vias6/Pads6 on layer 1, distance transform along the WIFI_ANT centreline |
| **General clearance rule = 0.15 mm** | `01-design-brief` §5 "Baseline rules" says Clearance, general 0.15 mm | The rule actually in the board is **Clearance Constraint (Gap = 0.254 mm) (All),(All)**, with **0.1 mm** scoped `InComponent('U1')`. `01-design-brief` §5 is stale on this line | `Design Rule Check - NanoD1.drc` |
| **"Pour Order 2" is a field** | I told him to set Pour Order 2 in the polygon dialog | There is no numeric priority field. Repour order is the **list order in `Tools → Polygon Pours → Polygon Manager`**, changed with Move Up / Move Down, and it only matters where polygons overlap | Altium UI |
| **Rectangular pads are not circles** | My own clearance checker modelled every pad as a circle of diameter `max(w,h)` and reported 11.4 mm² of pour-to-pad shorts | All six "shorts" were the four buck inductors L1–L4, whose pads are 0.80 × 2.00 mm. Modelled as rectangles the overlap is **0.0000 mm²** and DRC agrees | Pads6 `w`/`h`/`rot` |

## VDD1V35 — a real defect, and how it was found

| Item | Was | Is | Source |
|---|---|---|---|
| **Bulk decoupling placement** | C13 1 µF, C14 4.7 µF, C15 4.7 µF, C16 10 µF sat at x 53.8 – 63.9 — **27 to 38 mm from the U1 pins they decouple** (31–34, at x 26.1–27.2). The rail serpentined out to x 63.9 and back to reach them | Moved to x 23.3 – 26.6, now **2.09 – 4.43 mm** from the pins. C11/C12 (100 nF) were already correct at 0.92 / 2.90 mm | Pads6 |
| **Buck-to-SoC resistance** | **149 mΩ** — 45.4 mm of 0.15 mm trace end to end, no wider section anywhere, against a 1.5 mm preferred width in `03-layout-rules` §3.0 | **47.3 mΩ.** 14 mV at 0.3 A, 1.1 % of 1.35 V | Tracks6 graph, ρ = 1.72e-8, 1 oz = 35 µm |
| **What fixed it** | — | Three things, in order: move the four bulk caps to the load; pour `VDD1V35_L3` on MID2 (101 mm², 5.7 mm widest) to carry the middle 15 mm; move the buck output leg to **Bottom**, where that corridor held exactly one track, at 0.80 mm | — |
| **Why the top layer could not be widened** | — | A shortest-path search over legal L1 routes returned **16.0 mm at 0.15 mm max width**, against 18.1 mm as routed. The pads of L3 (inductor), C49, R48 and C41 box it in. Top layer was a dead end — this is why the leg went to Bottom | L1 clearance map, `distance_transform_edt` |
| **Designator collision** | I used "L3" for both the inner power layer and the 1.35 V buck inductor, and confused the user | **L3 is a component** — the 1.35 V inductor, pin 2 at (47.60, 5.50) = the regulator output, pin 1 at (47.60, 7.50) = LX. The layer is **MID2**. Never write "L3" for the layer in this project | Components6 |

## Signal nets on the power layer

| Item | Detail |
|---|---|
| **What splits a pour** | Three separate pour fragmentations this session were each caused by **one signal track crossing MID2**: `WL_HOST_WAKE` cut 22.7 mm² off the VDDC pour; `HDR18_8` + `HDR18_9` split VDD3V3 into 376 + 183 mm² across a **0.21 mm** gap at (11.46, 27.42). Moving the signal off MID2 merged each one |
| **The stranded VDD3V3 island** | Before the fix, the 183 mm² upper-left piece reached the net **only through J4 pin 8's through-hole barrel**. Not floating — Remove Dead Copper had kept it — but a header pin was carrying a third of the 3.3 V plane |
| **Still on MID2** | `WL_HOST_WAKE` 16 segments, `GPIO_AUX0` 5. Harmless now — neither splits a pour — but MID2 is meant to be power-only per `03-layout-rules` §1 |

## Via-in-pad — a board-wide convention, not a defect

**185 vias sit inside component pads.** 25 of them are U1's thermal pad (pin 89) and are correct. The rest are 0.3 mm vias in 0402/0603 terminals and in test-point pads, used throughout to reach the planes.

This is buildable and JLC will accept it, but **unfilled via-in-pad wicks solder during reflow** and can starve a 0402 joint. Do **not** rework 160 vias. Decide before ordering whether to pay for resin plugging, and put the note in the Draftsman drawing. Logged in `05-signoff-checklist`.
