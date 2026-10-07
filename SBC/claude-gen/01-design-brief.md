# 01 — Design Brief

---

## 1. Why SG2002 makes this tractable

| Normally hard | On SG2002 |
|---|---|
| DDR routing — fly-by topology, ±0.5 mm matching, VREF | **Gone.** 256 MB DDR3 is in-package. Zero DDR traces. |
| ~~Ethernet PHY — separate chip, RGMII, 25 MHz xtal, straps~~ | ~~**Gone.** 10/100 EPHY integrated.~~ **Ethernet has since been dropped entirely** — the four EPHY pads now carry I²S audio. See `02-netmap` §5.2. |
| Audio codec — I²C control, analog ground island, AVREF filtering | **Gone.** Digital I²S out to a MAX98357A amp and an INMP441 mic. No analog audio path on the board. |
| BGA fanout — via-in-pad, HDI, blind vias | **Gone.** QFN88, single peripheral row, 4 layers. |

What's left is a power tree, a QFN escape, USB2, SDIO and connectors. That's a board you can finish.

**The catch:** 0.35 mm pitch. Escape routing needs 0.1/0.1 mm rules and hand-soldering is not viable — stencil and reflow, or paid assembly.

---

## 2. Architecture

```
                 ┌──────────────────────────────┐
   USB-C ──5V──▶ │ ESD + reverse protection     │
                 └────────────┬─────────────────┘
                              │ VBUS_5V
     ┌──────────┬─────────────┼──────────────┬─────────────┐
     ▼          ▼             ▼              ▼             ▼
 Buck 3V3    Buck 0V95    Buck 1V35      LDO 1V8    (load path)
   2A          2A            1A          from 3V3
     │           │             │              │
     │           │             │              │   3V3 gated by PWR_SEQ2
     └───────────┴─────────────┴──────────────┴──▶ SG2002 QFN88
                                                    │
        ┌────────┬─────────┬──────────┬─────────┬───┴────┬────────┐
      USB2     SD0       SD1        I2S2     UART0    SPI NOR   GPIO
        │        │         │          │         │        │        │
     USB-C   microSD   AP6212    ┌────┴────┐  4-pin  W25Q128  castellated
                      + antenna  │         │   hdr             2 × 20
                                 ▼         ▼
                            MAX98357A   INMP441
                            (3V3 amp)   (1V8 mic)
                                 │
                              JST-PH → 8 Ω speaker
```

I²S rides the four pads Ethernet vacated (62–65) on fmux function 7. No extra SoC pins were consumed, and pins 48/49 were freed.

Cores: RISC-V C906 @1 GHz **or** Cortex-A53 @1 GHz (strap-selected), plus a 700 MHz C906 and an 8051. 1 TOPS NPU.

---

## 3. Scope — what's simplified

| Simplified | Skipped | Cost |
|---|---|---|
| microSD at 3.3 V fixed | UHS-I voltage switching | ~4× slower card IO |
| Pre-certified WiFi module | RF matching, crystal, certification | ~$3 BOM |
| **No Ethernet at all** | RJ45, magnetics, chassis ground island, 100 Ω pairs | Network is WiFi-only |
| **Digital I²S audio** | Codec, analog ground island, AVREF filtering | AEC quality (see `02-netmap` §5.2) |
| USB-C sink only, no PD | CC negotiation, PD controller | 5 V / 1.5 A ceiling |
| **66 × 38 mm**, 4 layers | 6-layer density | Bigger board |
| No MIPI CSI/DSI | Camera and display paths | Drops those features |
| No EMC pre-compliance | Filtering, shielding margin | Won't pass CE/FCC |

**Do not simplify away:** decoupling, ground integrity, ESD on external ports, power sequencing, test points.

### Why 66 × 38 mm and not 36 × 21 mm

The LicheeRV Nano is 36 × 21 mm and needs 6 layers to achieve it. Upsizing gives room for the QFN escape, the power stage, and the wider power channels the vendor requires above 38 mm. Keep the Nano's *look*, not its density.

**Size history:** 65 × 30 → 70 × 35 → **66 × 38**. Dropping the RJ45 frees 15.25 × 17.94 mm on the right short edge; the audio block needs roughly 15 × 10 of it. **Decision: hold 66 × 38 for now**, revisit shrinking once audio is placed and routed. When this number changes again, grep every file in this set for the old value first — it has already been missed twice.

---

## 4. Aesthetic

The Allwinner D1 / MangoPi MQ-Pro family look, decomposed:

| Element | Spec |
|---|---|
| Soldermask | **Matte black.** Not glossy — matte is what reads in photos. Same price. |
| Finish | **ENIG.** Gold against black is the whole effect. HASL ruins it. |
| Silkscreen | White, 0.8 mm minimum height, 0.15 mm stroke. Below 0.8 mm on black is unreadable. |
| Copper accent | Optional mask opening shaped as a logo, so gold shows through |
| Corners | R2.0 mm, drawn as arcs in the outline |
| Castellations | 0.6 mm half-holes at 2.54 mm pitch, both long edges, plated |
| Mounting | 4 × M2.5 (2.7 mm plated, 6 mm keepout all layers) |
| Discipline | Symmetric decoupling, connectors on a common baseline, passives on one rotation grid |

Edge plating is a manual fab process — put an explicit note in the Draftsman drawing.

**Add a bottom-side silkscreen pinout table** with every GPIO number, function and **voltage domain**. On this board the domain matters (see `02-netmap.md` §4) — most spare IO is 1.8 V.

---

## 5. Altium project setup

### Structure
```
NanoD1.PrjPcb
├── Schematics/
│   ├── 00_Top.SchDoc          (sheet symbols only)
│   ├── 01_Power.SchDoc
│   ├── 02_SoC_Core.SchDoc     (rails, decoupling, straps, crystal)
│   ├── 03_SoC_IO.SchDoc       (pinmux breakout, header)
│   ├── 04_Storage.SchDoc      (µSD, SPI NOR)
│   ├── 05_USB.SchDoc
│   ├── 06_Audio.SchDoc         (was 06_Ethernet — MAX98357A + INMP441)
│   ├── 07_Wireless.SchDoc
│   └── 08_Connectors.SchDoc   (debug, buttons, LEDs)
├── NanoD1.PcbDoc
├── Libraries/  (NanoD1.SchLib + NanoD1.PcbLib)
└── Outputs/    (NanoD1.OutJob, NanoD1.PcbDwf)
```

Use **hierarchical** sheets. Port mismatches are cheap errors; a mistyped global net label is not.

Draw the SoC symbol **split by function** — one part per power domain, mirroring the reference schematic's U1A–U1G. It makes the domain boundaries visible on the page, which is exactly where mistakes happen on this chip.

### Setup order

1. **Layer Stack Manager** — build the stackup from `03-layout-rules.md` §1, *including the Dk values*. Altium's solver won't match the vendor's impedance table on default FR-4 constants.
2. **Impedance profiles** — `DIFF90_SURF`, `DIFF100_SURF`, `SE50_ANT`. Verify against the vendor table; a mismatch means your Dk is wrong.
3. **Net classes** — `PWR_5V`, `PWR_3V3`, `PWR_1V8`, `PWR_1V35`, `PWR_CORE`, `USB`, **`I2S`**, `SDIO0`, `SDIO1`, `SPINOR`, `XTAL`, `RF`. Delete the old `ETH` class.
4. **Differential pairs** — `Design → Classes` → right-click net class → Create Differential Pairs From Net Class. **USB is now the only differential pair on the board.**
5. **xSignals** — run the wizard for USB only (through ESD and series R). The Ethernet xSignals are gone. The 22 Ω DNP footprints on `I2S_BCLK` / `I2S_LRCK` do fragment those nets, but I²S is not length-tuned, so no xSignal is needed there.
6. **Design rules** — widths keyed to impedance profiles, not hardcoded numbers

### Baseline rules

| Rule | Value |
|---|---|
| Clearance, general | ~~0.15 mm~~ — **the board actually uses 0.254 mm**, see `06-corrections-log` |
| Clearance, QFN escape region | 0.10 mm, scoped `InComponent('U1')` |
| Via | 0.3 mm hole / 0.6 mm pad |
| Min annular ring | 0.13 mm |
| Solder mask expansion | 0.05 mm |
| Silk-to-mask clearance | 0.15 mm |
| Polygon connect | Relief, 4 spokes, 0.25 mm — **except thermal pad, Direct** |

Per-net widths and shielding rules are in `03-layout-rules.md` §3.

### Mechanical

Outline on Mechanical 1 → `Design → Board Shape → Define from selected objects`. Pull STEP models for USB-C, microSD, the JST-PH and headers from the manufacturers. Check clearances in 3D before routing — mechanical collisions caught late are expensive.

**New mechanical item:** the INMP441 is a bottom-port mic and needs an acoustic hole through the board. Take the diameter and pad-ring rules from its recommended land pattern **before** placing it — this is a board cut-out, not just a footprint. The speaker also wants a rear cavity, which is enclosure work.

### Outputs (.OutJob)

Gerber X2 or ODB++ · NC Drill · IPC-2581 backup · ActiveBOM CSV with MPNs · Pick & Place · Draftsman assembly drawing carrying the stackup table, impedance table, castellation note and fab notes · PDF3D.

Use **Variants** for DNP parts so the BOM stays clean.

---

## 6. Software

⚠️ Check current upstream status before planning. Vendor tree is the pragmatic path today.

1. Start from Sipeed's LicheeRV Nano SDK or Sophgo's buildroot. Not from scratch.
2. **U-Boot** — copy the reference board config. DDR init needs no change; it's in-package.
3. **Device tree** — this is where your board differs: pinmux for header pins, SDIO1 WiFi node, **I2S2 node with pins 62–65 on fmux function 7 and DS = 1**, LED/button GPIOs. The EPHY node is gone.
   ⚠️ **The EPHY block must be told to release pads 62–65** before the pinmux can claim them — a fixed register sequence, given in `02-netmap` §5.2. This is not optional and not in the stock device tree. Without it the audio pins are dead and the board looks broken.
4. **Debian rootfs** — debootstrap onto partition 2, vendor kernel and modules into it. Keep a known-good vendor image to diff against.

---

## 7. Milestones

- [ ] **M0** Import the vendor pin table; build the SoC symbol split by domain
- [ ] **M1** Rebuild the QFN88 footprint in the IPC wizard (Cadence source won't import)
- [ ] **M2** Power schematic with hand-checked FB dividers — **core is 0.95 V, size for 1.5 A**
- [ ] **M3** Full schematic, ERC clean, zero suppressed warnings
- [ ] **M4** Stackup, Dk values, impedance profiles, design rules — before placing anything
- [ ] **M5** Placement per the floorplan in `03-layout-rules.md` §8; place the audio block in the ex-RJ45 zone
- [ ] **M6** Route: power shapes → USB → SDIO1 → SDIO0 → SPI NOR → crystal → **I²S** → GPIO
- [ ] **M7** Silkscreen and aesthetic pass; Draftsman with stackup, impedance and castellation notes
- [ ] **M8** Run `05-signoff-checklist.md` end to end
- [ ] **M9** Outputs, BOM, order two boards
- [ ] **M10** Bring-up per `05-signoff-checklist.md`
