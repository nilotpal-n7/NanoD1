# 02 — Net Map

Sources: SG2002 Datasheet V1.0-alpha · `04_SG2002_PINOUT.xlsx` · Hardware Design Guide EN · reference schematic · vendor support lists.

---

## 1. Complete pin map

Package: QFN88, 9 × 9 × 0.9 mm, **0.35 mm pitch**. Pin pads 0.2 × 0.75 mm. Thermal pad 6.0 × 6.0 mm exposed, 7.6 × 7.6 mm mask-covered region.

| # | Signal | Domain | | # | Signal | Domain |
|---|---|---|---|---|---|---|
| 1 | VSS18A_AUD | GND | | 46 | XTAL_XOUT | — |
| 2 | PAD_AUD_AINL_MIC | AUD 1.8 | | 47 | PWR_GPIO0 | RTC 1.8 |
| 3 | PAD_AUD_AVREF | AUD 1.8 | | 48 | PWR_GPIO1 | RTC 1.8 |
| 4 | PAD_AUD_AOUTR | AUD 1.8 | | 49 | PWR_GPIO2 | RTC 1.8 |
| 5 | **VDD18A_AUD** | 1.8 V | | 50 | **VDDC** | 0.95 V |
| 6 | SD0_CLK | SD0 3.3 | | 51 | SD1_D3 | SD1 3.3 |
| 7 | SD0_CMD | SD0 3.3 | | 52 | SD1_D2 | SD1 3.3 |
| 8 | SD0_D0 | SD0 3.3 | | 53 | SD1_D1 | SD1 3.3 |
| 9 | **VDDC** | 0.95 V | | 54 | SD1_D0 | SD1 3.3 |
| 10 | SD0_D1 | SD0 3.3 | | 55 | SD1_CMD | SD1 3.3 |
| 11 | SD0_D2 | SD0 3.3 | | 56 | SD1_CLK | SD1 3.3 |
| 12 | SD0_D3 | SD0 3.3 | | 57 | **VDDIO_SD1** | 3.3 V |
| 13 | **VDDIO_SD0_EMMC** | 3.3 V | | 58 | PWM0_BUCK | 1.8 V |
| 14 | SD0_CD | SD0 3.3 | | 59 | ADC1 | 1.8 V |
| 15 | SD0_PWR_EN | SD0 3.3 | | 60 | USB_VBUS_DET | 1.8 V |
| 16 | **VDDC** | 0.95 V | | 61 | **VDDC** | 0.95 V |
| 17 | SPK_EN (XGPIOA15) | SD0 3.3 | | 62 | PAD_ETH_TXP → *EPHY_RXN* | ETH 1.8 |
| 18 | UART0_TX ⚑ | SD0 3.3 | | 63 | PAD_ETH_TXM → *EPHY_RXP* | ETH 1.8 |
| 19 | UART0_RX | SD0 3.3 | | 64 | PAD_ETH_RXP → *EPHY_TXN* | ETH 1.8 |
| 20 | EMMC_DAT2 / SPINOR_HOLD_X | SD0 3.3 | | 65 | PAD_ETH_RXM → *EPHY_TXP* | ETH 1.8 |
| 21 | EMMC_CLK / SPINOR_SCK | SD0 3.3 | | 66 | **VDD33A_ETH_USB** | 3.3 V |
| 22 | EMMC_DAT0 / SPINOR_MOSI ⚑ | SD0 3.3 | | 67 | GPIO_RTX / EPHY_RTX ⚑ | 1.8 V |
| 23 | EMMC_DAT3 / SPINOR_WP_X ⚑ | SD0 3.3 | | 68 | **VDD18A_USB_PLL_ETH** | 1.8 V |
| 24 | EMMC_CMD / SPINOR_MISO | SD0 3.3 | | 69 | USB_DP | — |
| 25 | EMMC_DAT1 / SPINOR_CS_X | SD0 3.3 | | 70 | USB_DM | — |
| 26 | JTAG_CPU_TMS | SD0 3.3 | | 71 | **VDDC** | 0.95 V |
| 27 | JTAG_CPU_TCK | SD0 3.3 | | 72 | PAD_MIPIRX4N | MIPI 1.8 |
| 28 | IIC0_SCL | SD0 3.3 | | 73 | PAD_MIPIRX4P | MIPI 1.8 |
| 29 | IIC0_SDA | SD0 3.3 | | 74 | PAD_MIPIRX3N | MIPI 1.8 |
| 30 | AUX0 | SD0 3.3 | | 75 | PAD_MIPIRX3P | MIPI 1.8 |
| 31 | **VDDQ_DRAM** | 1.35 V | | 76 | PAD_MIPIRX2N | MIPI 1.8 |
| 32 | **VDDQ** | 1.35 V | | 77 | PAD_MIPIRX2P | MIPI 1.8 |
| 33 | **VDDQ** | 1.35 V | | 78 | PAD_MIPIRX1N | MIPI 1.8 |
| 34 | **VDDQ_DRAM** | 1.35 V | | 79 | PAD_MIPIRX1P | MIPI 1.8 |
| 35 | GPIO_ZQ / PAD_ZQ | RTC 1.8 | | 80 | PAD_MIPIRX0N | MIPI 1.8 |
| 36 | **VDDIO_RTC** | 1.8 V | | 81 | PAD_MIPIRX0P | MIPI 1.8 |
| 37 | **VDDC_RTC** | **cap only** | | 82 | **VDD18A_MIPI** | 1.8 V |
| 38 | PWR_VBAT_DET | RTC 1.8 | | 83 | PAD_MIPI_TXM2 | MIPI 1.8 |
| 39 | PWR_RSTN | RTC 1.8 | | 84 | PAD_MIPI_TXP2 | MIPI 1.8 |
| 40 | PWR_SEQ1 | RTC 1.8 | | 85 | PAD_MIPI_TXM1 | MIPI 1.8 |
| 41 | PWR_SEQ2 | RTC 1.8 | | 86 | PAD_MIPI_TXP1 | MIPI 1.8 |
| 42 | PWR_PTEST | RTC 1.8 | | 87 | PAD_MIPI_TXM0 | MIPI 1.8 |
| 43 | PWR_WAKEUP0 | RTC 1.8 | | 88 | PAD_MIPI_TXP0 | MIPI 1.8 |
| 44 | PWR_BUTTON1 | RTC 1.8 | | 89 | **E-PAD** | **GND** |
| 45 | XTAL_XIN | RTC 1.8 | | | | |

⚑ = strap, see §3.

### 1.1 There is one ground pin

Pin 1 is audio-local. **Every other return path is the exposed pad (89)** — including 1.5 A of core current and every high-speed interface. The via array in the E-pad is not a thermal feature; it is the ground connection. Under-vent it and you get failures that look like signal integrity problems.

### 1.2 The Ethernet naming inversion

Pin 62 is *named* `PAD_ETH_TXP` and carries the *net* `EPHY_RXN`. All four are crossed — TX↔RX **and** P↔N. The vendor's own pinout file spells both names into one cell (`PAD_ETH_TXP___EPHY_RXN`), and so does TRM Table 3.5.

**Ethernet has since been removed from this design** and pins 62–65 now carry I²S — see §5.2. The inversion no longer affects connectivity, but the pad names persist in the pinout tables and in the fmux function lists, so it still matters when reading vendor documentation. Keep the pin names in the symbol.

---

## 2. Power

### 2.1 Rails

| Rail | Voltage | Pins | Budget | Regulator |
|---|---|---|---|---|
| VDDC | **0.95 V** | 9, 16, 50, 61, 71 | 1220 mA TPU + 258 mA core ≈ **1.5 A** | Sync buck, 2 A |
| VDDQ / VDDQ_DRAM | 1.35 V | 31–34 | 300 mA | Sync buck, 1 A |
| 1.8 V | 1.8 V | 5, 36, 68, 82 | ~150 mA | LDO from 3V3 |
| 3.3 V | 3.3 V | 13, 57, 66 | ~144 mA + WiFi bursts | Sync buck, 1 A, **gated** |
| VDDC_RTC | — | 37 | — | **Cap to GND only. Never drive.** |

Datasheet limits: VDDC 0.81–0.99 · 1.8 V rails 1.62–1.98 · 3.3 V 2.97–3.465 · VDDQ 1.283–1.417 (DDR3L).

**0.95 V is specific to SG2002.** The guide says typical is 0.9 V and *SG2002 is 0.95 V*; the reference schematic carries a "Need 0.95V !!!" note. Check your FB divider arithmetic twice.

### 2.2 Sequencing — four documented ways to damage the chip

**Rule:** 0.95 V and 1.8 V may rise together, or core first. **3.3 V only after 1.8 V is established.** Power-down is the reverse.

Failure modes from the datasheet:

1. Up: VDD3 > 2 V while VDD18 < 1.62 V → **damages the 3 V circuit**
2. Down: VDD3 < 2 V while VDD18 already below 1.62 V
3. Up: VDD18 > 0.7 V while VDD09 < 0.5 V → **eFuse misoperation**
4. Down: VDD09 < 0.5 V while VDD18 > 0.7 V → same

(3) and (4) are worse than they sound: no smoke, just scrambled secure-boot state you won't notice for days.

**Implementation** — plug-in application, no coin cell. Core, 1.8 V and VDDQ free-run; **only the 3.3 V regulator's enable is gated by `PWR_SEQ2` (pin 41)**. This is the reference topology; use it rather than a load switch.

Also from the guide: *peripherals must not power up before the IO domain of the pin they connect to*, or current backfeeds through the IO ESD diodes. That's why the SD card and WiFi module hang off the gated 3.3 V rail, not an always-on one.

### 2.3 PWR_VBAT_DET (pin 38)

**30 kΩ / 10 kΩ divider from 5 V → 1.25 V.** Both 1%. Shutdown threshold 1.0 V.
The reference schematic annotates this "Must be connect". **The chip will not start without it.**

### 2.4 PWM0_BUCK (pin 58)

Reserved for dynamic VDDC scaling — the SoC PWMs its own core voltage after boot. Reference leaves the injection network **NC**. Place the footprints, don't populate.

### 2.5 Decoupling

Per rail: bulk at the regulator, 100 nF per power pin at the chip, each with its own via. **X5R or X7R only — the guide explicitly prohibits Y5V.** Exact cap counts and positions in `03-layout-rules.md` §4.

MLCC derating: a 10 µF 0402 X5R at 6.3 V gives ~4 µF at 3.3 V bias. Use 0603 where the value matters.

---

## 3. Straps — all four

| Net | Pin | Setting | If wrong |
|---|---|---|---|
| **UART0_TX** | 18 | **4.7 kΩ pull-up to 3.3 V** | Pull-down = ROM fail mode. Schematic: "Do not Delete!!!" |
| **SPINOR_MOSI** (EMMC_DAT0) | 22 | 4.7 kΩ, boot-device bit | Wrong boot source |
| **SPINOR_WP_X** (EMMC_DAT3) | 23 | 4.7 kΩ, boot-device bit | Wrong boot source |
| **EPHY_RTX** | 67 | **PU to VDDIO_RTC (1.8 V) = C906 RISC-V**; PD = Cortex-A53 | Boots the wrong architecture |

Boot device is latched from pins 22/23: eMMC = both high, SPI NAND = both low, SPI NOR = the mixed combination. Read the exact table off `SG2002_38板_4L_SCH.pdf` — it's legible in the PDF, garbled in text extraction.

Note pin 67 pulls to **1.8 V**, not 3.3 V. Wrong domain is a real risk here.

**Fit all four as 0402 jumper positions**, not fixed resistors.

⚠️ The strap table lists NOR / NAND / eMMC but not SD. On this family the ROM conventionally falls back to SD0 when the selected device has no valid image — that's how the reference boards boot from card. Confirm in the TRM boot chapter before committing.

---

## 4. The IO voltage problem

Spare GPIO on this chip is overwhelmingly **1.8 V**, and it shapes your header.

The 3.3 V domain (VDDIO_SD0_EMMC) has 22 pins. After SD0 (8), SPI NOR (6) and UART0 (2), **six remain**: 17, 26, 27, 28, 29, 30 — i.e. I²C0, JTAG TMS/TCK, SPK_EN, AUX0.

Everything else spare is 1.8 V: the 16 unused MIPI pins (72–81, 83–88 as XGPIOC[2..17]), PWR_GPIO0–2 (47–49), ADC1 (59), WAKEUP0/BUTTON1 (43/44), and the two audio pins (2, 4).

**After the Ethernet removal**, pins 48 and 49 left the Ethernet-LED role and became genuinely spare; pin 48 is now the amplifier SD_MODE control. Pins 2 and 4 remain spare — note they can also carry I²S (pin 2 → IIS1_BCLK / IIS2_BCLK, pin 4 → IIS1_DI / IIS2_DO / IIS1_DO) and their Audio GPIO drive is stronger than the ETH pads (IOH 11.3 mA min, VOH 1.4 V, absolute VIH 1.2 V — Datasheet Table 2-11).

**Consequences:**
- A 2 × 20 header works, but most of it is 1.8 V. A 3.3 V sensor plugged into the wrong half damages something.
- Split the header into clearly-marked 3.3 V and 1.8 V sections. Silkscreen the domain on **both** sides.
- **Dropping SPI NOR frees six more 3.3 V pins.** SPI NOR is your secondary boot path only — this is a real trade.
- Unused EPHY pins can be repurposed as GPIO, also at 1.8 V.

---

## 5. Interfaces

### 5.1 Crystal — 25 MHz (pins 45/46) — MANDATORY

- 25 MHz, **deviation < ±30 ppm**
- **4-pin SMD, both GND pins bonded to board ground** (ESD immunity)
- Load caps per crystal spec, **NP0/C0G**
- **The 1 MΩ across XIN/XOUT cannot be omitted** — stated explicitly in the guide
- Routing: fully ground-shielded, no high-speed signals underneath, everything else kept away

Reference: 25 MHz / 12.5 pF with 12 pF load caps.

### 5.2 I²S audio (pins 62–65) — replaces Ethernet

**Ethernet was removed from this design.** The four EPHY pads carry an I²S bus instead. Everything below is sourced; the superseded Ethernet section is preserved at the end of this file as §9 for reference.

#### The pin map

`04_SG2002_PINOUT.xlsx` sheet *1. 管腳信息表(QFN)* gives each pad's function-select table. **Function 7 on all four EPHY pads is a complete IIS2 bus** — the exact four signals needed, on the exact four pads Ethernet vacates. No other pins are consumed.

| Pin | Pad name | fmux 7 | Net | Goes to |
|---|---|---|---|---|
| 63 | `PAD_ETH_TXM___EPHY_RXP` | **IIS2_BCLK** | `I2S_BCLK` | amp BCLK + mic SCK |
| 62 | `PAD_ETH_TXP___EPHY_RXN` | **IIS2_LRCK** | `I2S_LRCK` | amp LRCLK + mic WS |
| 64 | `PAD_ETH_RXP___EPHY_TXN` | **IIS2_DO** | `I2S_DOUT` | amp DIN |
| 65 | `PAD_ETH_RXM___EPHY_TXP` | **IIS2_DI** | `I2S_DIN` | mic SD |

`IIS2_DO` / `IIS2_DI` are named from the SoC's point of view: DO is SoC output.

I2S2 is a real peripheral, not a mux artefact — SG2002 TRM gives it base `0x04120000–0x0412FFFF`, its own soft reset (`reg_soft_reset_x_i2s2`), its own APB gate (`clk_apb_i2s2`), dedicated DMA request lines, and an interrupt. The AIAO subsystem selects `3'b110 = From IO I2S2_*` for the external-pad path.

**Pins 48 and 49 (PWR_GPIO1/2) are freed** by dropping the Ethernet LEDs. Pin 48 now drives the amplifier's SD_MODE; 49 is spare.

#### Handing the pads to the pinmux — bring-up, not hardware

These pads sit outside the normal IO blocks (TRM Table 3.5 lists an IOGroup for every pad **except** 62–65). The EPHY must be told to release them. `04_SG2002_PINOUT.xlsx` sheet *6. 如何把 MIPI Audio ETH 切入GPIO* gives the sequence:

```
0x03009804[0]    = 1'b1        rg_ephy_apb_rw_sel = 1, use apb interface
0x03009808[4:0]  = 5'b00001    rg_ephy_pll_stable_cnt = 1  (10 us)
0x03009800[2]    = 0x0905      rg_ephy_dig_rst_n = 1, reset release
wait 10 us
0x0300907C[12:8] = 5'b00101    page_sel_mode0 = page 5
0x03009078[11:0] = 0xF00       set to gpio from top
0x03009074[10:9 2:1] = 0x606   ephy rxp & rxm input + output enable
0x03009070[10:9 2:1] = 0x606
```

**Without this, the pins are dead and the board looks broken.** Put it in the bring-up notes, not just the device tree.

#### Electrical — why the parts were chosen

SG2002 Datasheet **Table 2-12, ETH GPIO Electrical Parameters**, at VDD18A = 1.8 V:

| | Value |
|---|---|
| VIH | ≥ 0.7 × VDD18A = **1.26 V** |
| VIL | ≤ 0.3 × VDD18A = 0.54 V |
| Schmitt VT+ / VT− | 0.84–1.14 / 0.66–1.01 V |
| VOH | ≥ VDD18A − 0.4 = **1.40 V** |
| VOL | ≤ 0.40 V |
| IOH | 4.0 mA (DS=0) / **4.7 mA (DS=1)** min |
| IOL | 8.8 / 10.2 mA min |

**Set DS = 1** in the pinmux. These pads do have a drive-strength control despite sitting outside the IO blocks.

Three interfaces, three margins:

| Direction | Driver min | Receiver threshold | Margin |
|---|---|---|---|
| SoC → MAX98357A | VOH 1.40 V | VIH **1.30 V absolute** | +100 mV |
| SoC → INMP441 | VOH 1.40 V | VIH 0.7 × 1.8 = 1.26 V | +140 mV |
| INMP441 → SoC | VOH 0.9 × VDD = **1.62 V** @ 0.25 mA | VIH 1.26 V | +360 mV |

The SoC→amp 100 mV is worst-case-against-worst-case at 4.0–7.4 mA; the real load is ~30 pF at 3.072 MHz, far below that, so the practical margin is much wider.

**Use the INMP441, not the ICS-43434.** ICS-43434's VOH is 0.65 × VDD = 1.17 V, which is *below* the SoC's 1.26 V VIH — it clears only the Schmitt VT+ max (1.14 V) by 30 mV, and its VOH is "guaranteed by design", not tested. INMP441 gives 1.62 V.

**The mic must run at 1.8 V.** Its VIH is 0.7 × VDD; at 3.3 V that becomes 2.31 V, which a 1.8 V pad can never reach. This is a constraint, not a preference.

#### Circuits

**U9 — MAX98357A**, TQFN 3 × 3 mm (not the 1.345 × 1.435 mm WLP at 0.4 mm pitch)

| Pin | Connection |
|---|---|
| VDD | `VDD3V3` + 10 µF 0805 + 100 nF 0402, caps as close as the layout allows |
| GND | GND |
| BCLK / LRCLK / DIN | `I2S_BCLK` / `I2S_LRCK` / `I2S_DOUT` |
| GAIN_SLOT | 100 kΩ 0402 to GND, **DNP** → 9 dB. Populate → 15 dB |
| SD_MODE | **300 kΩ** 0402 to pin 48 (1.8 V GPIO) → (L/2 + R/2) mono downmix, GPIO-shutdownable |
| OUTP / OUTN | 2-pin JST-PH to speaker |

SD_MODE is a channel selector, not just an enable. It has an internal 100 kΩ ±8% pulldown and three trip points (datasheet Table 5, Figure 4):

| SD_MODE | Channel |
|---|---|
| Direct logic-high (> B2, 1.4 V typ) | Left |
| 69.8 kΩ pull-up at 1.8 V | Right |
| **300 kΩ pull-up at 1.8 V** | **(L/2 + R/2)** |
| Low (< B0, 0.16 V typ) | Shutdown |

Gain is the opposite of what you'd guess: GAIN_SLOT **unconnected = 9 dB**, direct to GND = 12 dB, **to GND through 100 kΩ = 15 dB**.

VDD3V3 rather than VBUS_5V: 5 V only exists while USB-C is plugged and it's the noisiest rail on the board. 3.3 V into 8 Ω is ample for a status/voice speaker, and it satisfies Maxim's *VDD > VDDIO* condition so SD_MODE needs no series limiter.

**U10 — INMP441**

| Pin | Connection |
|---|---|
| VDD | **`VDD1V8`** + 100 nF 0402 at the pin |
| GND | GND |
| L/R | GND → left channel |
| SCK / WS / SD | `I2S_BCLK` / `I2S_LRCK` / `I2S_DIN` |

Plus a **100 kΩ pull-down on `I2S_DIN`** so the SoC input doesn't float when the mic is unpopulated or held in reset — these pads sit outside the IO blocks and internal pulls should not be assumed.

**22 Ω series footprints on `I2S_BCLK` and `I2S_LRCK`** near the SoC, DNP by default. Insurance against ringing into two loads on repurposed PHY pads.

#### What going digital deletes

`02_SOPHGO_Audio_Hardware,_Structural_Design_and_Device_Selection_Instruction` §2.1.1 and §2.2.1 require a discrete audio ground joined to SOC GND through a 0 Ω resistor, placed well away from the noisy VDDC/TPU ground region, with GND-wrapped analog routing and DC isolation capacitors. **None of that applies to an I²S bus.** The whole analog-audio ground island is avoided.

#### What still applies (same document)

- **§2.2.4** — amplifier input and output routing must not cross; supply capacitor as close to the amp as possible; **at least 2 vias** on the direct run from amp output to the speaker connector
- **§4.1** — the **mic must face away from the speaker**, or the angle between them maximised, to limit coupling. Mic needs a discrete acoustic cavity and an anti-vibration bushing (enclosure work)
- **§3.3 speaker spec** — SPL ≥ 89 dB, F0 < 1 kHz (target ~600 Hz), THD ≤ 10%, **8 Ω ±15% for 1 W** (4 Ω for 2 W), rear cavity
- **INMP441 is bottom-port** — it needs an acoustic hole through the PCB. Take the diameter and pad-ring rules from the recommended land pattern before placing

#### One caveat worth knowing now

§3.2 of the same guide: *"If an IIS AMP is desired, please be sure to consult SOPHGO for in-depth analysis of its effects on AEC. This is because IIS AMP is only capable of sampling from behind the AMP where the audio signal waves are not directly transmitted and require conversion. This may harm AEC."*

If you later want acoustic echo cancellation — full-duplex voice, a wake-word assistant that listens while playing — an I²S amplifier degrades it. For playback, status chimes and recording, it does not matter.

#### C59 stays

**Keep C59 (1 µF on `AUD_AVREF`, pin 3)** even though the analog audio block is now unused. The reference schematic requires it regardless; see `06-corrections-log`.

### 5.3 USB 2.0 (pins 69/70)

- 90 Ω ±10%, intra-pair skew **within 10 mil** (guide is stricter than the layout deck; use 10)
- Series resistor **≤ 5.1 Ω at the connector end**, not the SoC
- ESD array with **parasitic capacitance < 5 pF** (e.g. USBLC6-2SC6)
- USB-C: **5.1 kΩ to GND on CC1 and CC2 — two separate resistors.** One shared resistor is a classic fatal error.
- `USB_VBUS_DET` (60): low = host, high = device. 1.8 V domain — divide VBUS accordingly.

### 5.4 microSD — SD0 (pins 6–15)

3.3 V fixed. **eMMC is impossible by construction** — SD0 and eMMC share IO power, and SD cards need 3.0 V while eMMC needs 1.8 V. This is also why UHS-I is out: it requires SD0 to swing to 1.8 V.

- 22 Ω series on CLK; 10 kΩ pull-ups on CMD and DAT0–3
- Card detect to `SD0_CD` (14)
- `SD0_PWR_EN` (15) defaults to `XGPIOA[14]`; set mux to function 0 for hardware card power control
- High-speed timing: 52 MHz, 6 ns setup, 2.5 ns hold, **CL ≤ 30 pF** — the load ceiling is the real constraint. Short traces, one via max, no stubs.

### 5.5 WiFi — SD1 (pins 51–56)

**AP6212** (Broadcom BCM43438A0, 12 × 12 × 1.7 mm, 2.4 GHz b/g/n + BT4.1).

From the vendor's validated list, this is the only SDIO module whose driver (`brcmfmac`) is **mainline** — which is the actual risk on this board, not the hardware. Alternates on the list: BL-M8723DS1 (RTL8723DS), BL-M8821CS1 (RTL8821CS, adds 5 GHz), DXS-S1026_R89S (RTL8189FTV). AIC8800D appears but with no module part number — bare chip only, needs an RF design you don't want.

- 22 Ω series on CLK, 10 kΩ pull-ups on CMD and D0–D3
- `WL_REG_ON` and `WL_HOST_WAKE` on spare PWR_GPIO
- Ferrite + 10 µF + 100 nF local to the module
- u.FL connector rather than a PCB antenna — swappable during debug, and the 50 Ω line is trivial

### 5.6 SPI NOR (pins 20–25)

Default mux is already SPINOR (0x1) on all six — no pinmux work needed.

**W25Q128JVSIQ(1T)** — 16 MB, 3.3 V, SOP8. Marked YES / bring-up OK / stress OK on the vendor list. **The (1T) suffix is specified**; don't substitute silently. Same-rated alternates: GD25Q128ESIG, XT25F128FSSIGU, ZB25VQ128.

- 10 kΩ pull-ups on CS, WP, HOLD; 22 Ω series on SCK
- **SPI_CLK must be individually ground-shielded** per the guide
- Bus under 30 mm. Timing: 13.4 ns min clock (~74 MHz), 3.5 ns setup, 2.6 ns output delay

### 5.7 PAD_ZQ (pin 35)

The bring-up table measures 3.9 MΩ on the reference board — **no external ZQ resistor populated**. Leave unloaded, bring to a test point. The guide's first diagnostic for DDR init failure is *check VDDQ ripple and ZQ resistance*.

### 5.8 Debug, buttons, LEDs

| Net | Pin | Circuit |
|---|---|---|
| UART0 TX/RX | 18, 19 | 4-pin 2.54 header: GND / TX / RX / 3V3. Square pad on pin 1. **Pin 18 carries the strap pull-up.** |
| RESET_N | 39 | Tactile button, 10 kΩ PU, 100 nF |
| BOOT_BTN | spare GPIO | Tactile button, 10 kΩ PU |
| LED_PWR | — | 3V3 + 2 kΩ, green |
| LED_USER | spare GPIO | 1 kΩ, green |

You will use the UART console constantly. Accessible edge, clear silkscreen.

**Freed by dropping Ethernet:** PWR_GPIO1 (48) and PWR_GPIO2 (49), both 1.8 V. Pin 48 now drives the MAX98357A's SD_MODE through 300 kΩ (§5.2). Pin 49 is unallocated.

---

## 6. Bring-up reference — pin resistance to GND

From `09_SG2002_QFN88_Impedance_Analysis_Reference_Table.xlsx`. Red probe on GND, black on pin.

| Pin(s) | Expected |
|---|---|
| VDDC (9, 16, 61, 71) | **48–53 Ω** |
| VDDQ (32, 33) | ~8.5 kΩ |
| VDDQ_DRAM (31, 34) | ~48.7 kΩ |
| VDDIO_SD0_EMMC (13) | ~1.15 MΩ |
| VDDIO_SD1 (57) | ~449 kΩ |
| VDD33A_ETH_USB (66) | ~8.7 kΩ |
| VDD18A_USB_PLL_ETH (68) | ~451 kΩ |
| USB_DP / DM (69, 70) | ~87 kΩ |
| SD0-domain signal IO | ~5 MΩ |

On a dead board this finds a solder short or damaged pin in minutes. Print it.

---

## 9. Superseded — the Ethernet section

Kept verbatim so a future session can see what was replaced and why, and so nothing here gets accidentally re-derived from scratch. **None of it is live.** The four pads now carry I²S; see §5.2.

### Old §5.2 Ethernet (pins 62–65)

- **5.1 Ω or less in series** on each of the four lines — surge immunity and EMI. Not optional.
- **No RC filter on the pairs** — the guide warns it wrecks the eye diagram.
- ESD only if externally exposed; parasitic capacitance matters.
- **There is no reference/RSET resistor.** The internal PHY needs nothing beyond the series resistors.
- Magnetics: integrated-magnetics RJ45 is fine and simpler than the reference's discrete transformer.
- Center tap 75 Ω 1% + 0.1 µF; chassis bridge 1 nF / 2 kV; TVS line-side.
- Chassis-ground island under the RJ45, 1 MΩ ∥ 1 nF bridge, no pour under the magnetics.
- LEDs: `EPHY_LNK_LED` / `EPHY_SPD_LED` are mux options on PWR_GPIO1 (48) / PWR_GPIO2 (49). **1.8 V pins.**

### Parts this required, all now removed

J1 (HR911105A integrated-magnetics RJ45), R26–R29 (5R1 series), R34 (1 M chassis bridge), R35/R36 (1 k LED), DA1 (SMBJ14A). The 1 nF / 2 kV bridge cap was specified but never placed.

Nets that died with it: `EPHY_*`, `ETH_*`, `CHGND`. The isolated chassis island on L2 goes with `CHGND`.

### One fact from this section that is still true

**Auto-MDIX is present** — `sophgo-doc/SG200X/TRM/contents/{en,cn}/network/eth_phy.rst`: *"支持以太网路线交叉线或直连线自动移动翻转功能"*. It made the lane order free. Irrelevant now, but it was verified against the source, so it is recorded rather than re-litigated.

### And one that is not

The naming inversion (§1.2) is **not** superseded — the pad names still read `PAD_ETH_TXP___EPHY_RXN` in every vendor table and in the fmux function lists. It no longer affects connectivity, but it still matters when reading the documentation.
