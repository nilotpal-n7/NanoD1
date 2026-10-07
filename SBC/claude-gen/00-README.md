# Nano-D1 — Reference Documentation

Learning-grade RISC-V SBC. Sophgo SG2002, **66 × 38 mm**, 4-layer, WiFi, **I²S audio**, Debian from microSD.

> **Scope change:** Ethernet has been removed. The four EPHY pads (62–65) now carry an I²S bus to a MAX98357A amplifier and an INMP441 microphone. Anything in this set still describing Ethernet as present is stale — `02-netmap` §5.2 is the authority on the new block, and the old Ethernet section is preserved as `02-netmap` §9 for reference.

**Read "LLM_INSTRUCTIONS.txt" in root directory.**

**Read `06-corrections-log.md` before trusting any board-specific claim.** It lists facts that were stated wrongly and later disproved. Several are things a fresh session would confidently repeat.

---

## Where things live

```
NanoD1\
├── NanoD1.PrjPcb                    ← the Altium project
├── NanoD1.PcbDoc                    ← board layout
├── NanoD1.BomDoc
├── Constraints.xml                  ← design rules (Constraint Manager)
│
├── Schematics\                      ← 8 sheets
│     NanoD1_Power.SchDoc
│     NanoD1_Decoupling.SchDoc
│     NanoD1_Storage.SchDoc
│     NanoD1_USB.SchDoc
│     NanoD1_Audio.SchDoc          ← was NanoD1_Ethernet, not yet redrawn
│     NanoD1_Wireless.SchDoc
│     NanoD1_Clk_Reset.SchDoc
│     NanoD1_IO.SchDoc
│
├── Libraries\
│     NanoD1.SchLib                  ← 10 built symbols, SG2002 split A–G
│     NanoD1.PcbLib                  ← 13 footprints
│
├── Project Outputs for NanoD1\      ← DRC reports, netlist, status
│
└── SBC\
    ├── claude-gen\                  ← THIS DOCUMENTATION SET
    ├── cadence-imports\             ← vendor reference, read-only
    ├── sophgo-hardware\             ← HDK: pinout, layout guide, ref design
    └── sophgo-doc\                  ← TRM, software manuals
```

**One suggestion:** `SBC\` sits inside the Altium project folder, so the vendor repos get swept into any project backup or archive. Moving `SBC\` up one level beside `NanoD1\` would keep the project folder to just your design.

---

## Which file answers what

| Question | File |
|---|---|
| What is this board, what's in scope, how do I set up Altium | `01-design-brief` |
| What does SG2002 pin *n* connect to? What voltage is that rail? | `02-netmap` |
| How wide is this trace? What's the stackup? Where do parts go? | `03-layout-rules` |
| Where exactly do the vias and decoupling caps go around the SoC? | `04-reference-measured` |
| Have I forgotten anything before ordering? | `05-signoff-checklist` |
| Is this fact actually true, or was it corrected? | **`06-corrections-log`** |
| What's done, what's next? | `07-current-state` |

---

## By project phase

**Schematic capture — done.** `02-netmap` was the source. `altium-sg2002-symbol.csv` and `symbol-parts\*.csv` built the SG2002 symbol.

**Placement and routing — current.** `03-layout-rules` §3 for widths and shielding, §8 for the floorplan. `04-reference-measured` for the via array, cap cascade and L3 pour vertices.

**Before fabrication.** `05-signoff-checklist`, all four parts. `bom-corrected.csv` for values and part numbers.

**Bring-up.** `05-signoff-checklist` final section, plus the pin-resistance table in `02-netmap` §6.

---

## The interactive viewers

| File | Use |
|---|---|
| `nano-d1-sheets.html` | Schematic, 8 tabbed sheets, real symbols, cross-sheet net flags. **Sheet 05 is now the I²S audio block** |
| `nano-d1-schematic.html` | PCB-oriented — floorplan placement, nets coloured by copper layer, stackup rail. **Amp / mic / speaker / audio-passives zones replace the Ethernet front end and RJ45** |
| **`nano-d1-board.html`** | **The real board.** Parsed straight from `NanoD1.PcbDoc` — true dimensions, every pad, track, via and pour. 2D layer view with net tracing and top/bottom flip, exploded 3D stack, and a live track-width audit that re-reads the pad geometry. **Rebuild after any significant PCB change** |

Both were rebuilt for the audio pivot and the 66 × 38 resize. `.bak-eth` copies of the pre-pivot versions sit alongside them.

**Resolved since:** the 1.8 V header came back as **J5A + J5B**, 10 pins each, and J4 is a 9-pin 3.3 V header. Both block diagrams still draw the old single 20-pin J5 — they are schematic-intent views, not the layout.

Neither was ever authoritative over the Altium files — they were the design reference, and the Altium project is the source of truth.

---

## Vendor sources

`github.com/sophgo/sophgo-hardware` → `SG200X/04_SG2002/`

| File | What it gave us |
|---|---|
| `04_SG2002_PINOUT.xlsx` | The 88-pin table |
| `02_..._Hardware_Design_User_Guide_EN` | Circuit requirements, crystal spec, ~~EPHY rules~~ |
| `SG2002 Datasheet (.docx)` | **Table 2-11 Audio GPIO, Table 2-12 ETH GPIO electricals.** The TRM has no electrical characteristics at all — it is a register manual |
| `04_SG2002_PINOUT.xlsx` sheet 6 | The register sequence that releases pads 62–65 from the EPHY block |
| `08_..._4L_PCB..._Layout指南.pptx` | Stackup, impedance, routing rules, power layout |
| `07_SG2002_38_4L_SCH&PCB` | Reference schematic and PCB |
| `09_..._Impedance_Analysis_Reference_Table.xlsx` | Per-pin resistance to GND — a bring-up tool, not a stackup tool |
| `10_Sophgo_WiFi_Support_List` | Validated modules — chose AP6212 |
| `12_Sophgo_Flash_Support_List` | Validated flash — chose W25Q128JVSIQ(1T) |

`SG200X/02_SG200X_Common_HW_DOC/`

| File | What it gave us |
|---|---|
| `02_SOPHGO_Audio_Hardware,_Structural_Design_and_Device_Selection_Instruction` | Speaker spec, mic/speaker placement, amp routing rules — and the AEC caveat on I²S amplifiers |
| EMI troubleshooting, SMT precautions | General |

`components-doc\` holds the part datasheets: MAX98357A, INMP441, ICS-43434 (rejected), AP6212, W25Q128JV, USBLC6-2, and the SG2002 TRM PDF.

**Format warning:** the vendor CAD is Cadence. `.OLB`/`.DSN` import via Altium's OrCAD importer. `.dra`/`.psm`/`.pad` do not — those footprints were rebuilt in the IPC wizard. The `.brd` needed DB Doctor to upres from 16.6 before anything could read it.

---

## Using this in a new chat

Upload the seven markdown files, `bom-corrected.csv`, the seven part CSVs, and your current `NanoD1.NET`. Not the datasheets — their content is already extracted here, and they'd consume the knowledge budget.

Suggested project instructions:

```
Nano-D1: learning-grade RISC-V SBC, Sophgo SG2002, 66 × 38 mm 4-layer.
WiFi + I2S audio. No Ethernet — it was removed and the EPHY pads
now carry I2S.
I'm a senior PCB designer using Altium. Step-by-step, no information dumps.

Read 06-corrections-log.md before stating any board fact. It lists errors
already found and corrected — do not restate anything it disproves.

Cite which file a fact came from. If it isn't in a file, say so rather
than reconstructing.
```

At the end of each session, regenerate `07-current-state.md`, and `06-corrections-log.md` if anything new was disproved.

---

## Honest status

A first spin has roughly even odds of booting. That's normal for a board of this complexity. Order two, keep a bring-up log, and put test points on every rail — TP1 through TP8 are already in the design for exactly that.

Twelve items remain unverified and are listed at the end of `06-corrections-log` — including thermal-pad stencil segmentation, core-buck current headroom, whether the AP6212 needs its LPO clock for WiFi-only operation, and several new ones from the audio pivot.

The audio block is **drawn, placed and routed**, and **all four copper layers are now poured** — L2 GND, four power shapes on L3, GND fill on L1 and L4. DRC is 6 violations, all cosmetic silkscreen.

What remains before fab: the pick-and-place is **not safe to send yet** (DNP parts unmarked, and eight components need Center-X/Y rather than Ref-X/Y), plus the L2 voids, the antenna feed decision, stitching vias, component heights and the Gerber/BOM set. `07-current-state` has the ordered list, `05-signoff-checklist` items P1–P9 have the detail.
