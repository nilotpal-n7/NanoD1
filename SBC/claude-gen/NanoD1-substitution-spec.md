# Nano-D1 — substitution spec for the unstocked parts

Use this to pick in-stock JLC parts. Every constraint below is derived from the board or a
datasheet, and says what breaks if it's violated. Anything not listed is free to vary.

---

## Inductors L1 – L4

**All four share the same land: two pads 2.00 × 0.80 mm on 2.00 mm centres** (standard
2520 metric / 1008 imperial). Any 2520 power inductor fits with no PCB change. Body up to
2.5 × 2.0 mm; height is unconstrained by the layout — nothing sits above them.

Ripple computed at the ETA3414's 3 MHz switching frequency, Vin = 5 V.

| Ref | Rail | I(dc) | ripple ΔI | I(peak) | **Isat min** | **Irms min** | **DCR max** | L |
|---|---|---|---|---|---|---|---|---|
| **L1** | LX_3V3 → VDD3V3 | 2.0 A | 0.17 A | 2.09 A | **2.8 A** | **2.2 A** | 100 mΩ | 2.2 µH ±20% |
| **L2** | LX_VDDC → VDDC | 1.48 A | 0.26 A | 1.61 A | **2.2 A** | **1.7 A** | 70 mΩ | 1.0 µH ±20% |
| **L3** | LX_1V35 → VDD1V35 | 1.0 A | 0.15 A | 1.08 A | **1.5 A** | **1.2 A** | 120 mΩ | 2.2 µH ±20% |
| **L4** | WL_LDO_IN → WL_LDO_SW | 0.4 A | — | ~0.5 A | **0.8 A** | **0.6 A** | 300 mΩ | 4.7 µH ±20% |

**Isat is the one that matters.** Exceed it and the inductance collapses, current spikes, and the
buck can go into hiccup or destroy itself. Irms is a thermal limit — exceeding it means it runs hot,
not that it fails immediately.

**Prefer shielded** on all four. L2 sits 3.5 mm from U6 and L1 3.5 mm from U5; unshielded
wirewound parts couple into neighbouring feedback nodes.

**Do not go larger than 2520.** L1's nearest neighbour is C45 at 2.2 mm and L3's is R50 at 1.87 mm.
A 3 × 3 mm part needs those moved.

**Why L1 was flagged:** the previously proposed WPN252012H2R2MT guarantees only 1.90 A Irms
against a 2 A rail. If the real 3.3 V load is under 1.5 A it would have been fine — but size it
for the regulator, not for the guess.

---

## Y1 — 25 MHz crystal

Feeds `XTAL_XIN` / `XTAL_XOUT`, the SG2002's main oscillator. **Nothing boots without it.**

| Requirement | Value | Why |
|---|---|---|
| Frequency | **25.000 MHz** | fixed by the SoC |
| Package | **SMD 3225, 4 pad** (3.2 × 2.5 mm) | footprint is fixed |
| **Load capacitance** | **12 pF preferred** | see below |
| ESR | **≤ 60 Ω** | the original is 40 Ω; much higher and the oscillator may not start |
| Stability | **≤ ±30 ppm** | original is ±20 ppm |

### If the CL is not 12 pF, C55 and C56 must change

The loading caps and the crystal are a matched pair:

```
CL = (C55 × C56)/(C55 + C56) + C_stray        with C55 = C56 = C:
CL = C/2 + C_stray            C_stray ≈ 3 pF on this board
```

Current build: C55 = C56 = 18 pF → CL = 9 + 3 = **12 pF**, which is exactly the TSX-3225 spec.

**So: C = 2 × (CL_new − 3 pF)**

| New crystal CL | Set C55 = C56 to |
|---|---|
| 8 pF | 10 pF |
| 10 pF | 15 pF (nearest E12 to 14) |
| **12 pF** | **18 pF — no change** |
| 16 pF | 27 pF (nearest E12 to 26) |
| 18 pF | 30 pF |
| 20 pF | 33 pF (nearest E12 to 34) |

**Pick a 12 pF part and nothing changes.** Any other CL is a schematic edit, not just a BOM swap —
and the wrong loading caps pull the clock off frequency, which breaks USB enumeration and
SD timing before it breaks anything obvious.

The 3 pF stray figure is an assumption carried from `06-corrections-log`, not a measurement.
Tune on the bench at bring-up.

---

## FB2, FB5 — ferrite beads

| Requirement | Value | Why |
|---|---|---|
| Impedance | **600 Ω @ 100 MHz** | matches the design intent |
| Package | **0603** | footprint is fixed |
| Rated current | **≥ 1 A** | FB5 carries WiFi peaks (~400 mA); 1 A gives margin |
| DCR | **≤ 200 mΩ** | at 400 mA that's < 80 mV drop on WIFI_VDD |

FB2 sits on `VDD1V8 → VDD18A_USB` (low current). FB5 on `VDD3V3 → WIFI_VDD` — **FB5 is the one
that needs the current rating.** Same part for both is simplest.

---

## SW1, SW2 — tactile switches

**Recommendation: accept the pre-order.** MOQ 16 at $9.15 total is cheap, and the alternative
is a footprint change.

If you'd rather substitute: the land is Panasonic **EVQ-P2** — SMD J-lead, body 3.5 × 4.7 mm.
Verify the candidate's land pattern against `FP-EVQ-P2002M-MFG` pad-for-pad before committing;
tactile switch footprints are not interchangeable between manufacturers.

---

## E1 — U.FL connector

Stock 1, MOQ 7. It's a 2 × 2 mm 3-pad part — **hand-solder it.** Leave it off the assembly.

If you do want it placed, any IPEX/U.FL clone on the same 3-pad land works; the land is
`HRS-U.FL-R-SMT-3_V`. Check the pad drawing matches before ordering.

---

## U10 — INMP441 microphone

No drop-in substitute. The LGA-9 land with a bottom acoustic port is specific to this part,
and the board has a 0.600 mm hole drilled for it.

**Leave unpopulated this spin.** You lose the microphone; the MAX98357A playback path is
unaffected. Fit it later by hand or on the next spin.

---

## U1 — SG2002

Not in JLC's library. Self-supply. Consider whether you want JLC to place a customer-supplied
part (they do, for a fee and with a minimum) or to hand-place a QFN88 at 0.35 mm pitch yourself —
which `01-design-brief` §1 already warns is not viable without stencil and reflow.

---

## Do not assemble at JLC

`J3, J4, J5A, J5B, J6` are all **through-hole** — 0.90 mm holes for the headers, 1.00 mm for the
JST-PH, 35 joints in total. JLC's Economic PCBA is SMT-only; through-hole means Standard PCBA
with per-joint hand-soldering charges.

Mark all five Do Not Populate and solder them yourself.
