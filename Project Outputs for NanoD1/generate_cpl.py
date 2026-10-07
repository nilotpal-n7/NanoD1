"""
Generate a corrected JLCPCB CPL from Altium's Pick & Place CSV.

Uses Ref-X/Ref-Y (component origin as shown in Altium UI) instead of
Center-X/Y (geometric centroid), which is wrong for asymmetric footprints.

Also prints a report of components where Center and Ref differ significantly.
"""

import csv
import sys
import math
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = SCRIPT_DIR / "Pick Place for NanoD1(Assembly).csv"
OUTPUT_FILE = SCRIPT_DIR / "NanoD1-CPL-JLCPCB-corrected.csv"

# Components to EXCLUDE from CPL (through-hole / test points / DNP)
EXCLUDE_PREFIXES = ("TP",)  # Test points only - headers are already in Pick & Place

# Threshold in mm to flag centroid vs reference discrepancies
DISCREPANCY_THRESHOLD = 0.5


def parse_pick_place(filepath):
    """Parse Altium Pick & Place CSV, skipping the header block."""
    components = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = None
        for row in reader:
            if not row:
                continue
            # Find the header row
            if row[0].strip('"') == "Designator":
                header = [col.strip('"') for col in row]
                continue
            if header is None:
                continue  # Skip preamble lines
            if len(row) < len(header):
                continue
            record = {}
            for i, col in enumerate(header):
                record[col] = row[i].strip('"')
            components.append(record)
    return components


def main():
    if not INPUT_FILE.exists():
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        sys.exit(1)

    components = parse_pick_place(INPUT_FILE)
    print(f"Parsed {len(components)} components from Pick & Place file.\n")

    # Generate corrected CPL
    cpl_rows = []
    discrepancies = []

    for comp in components:
        des = comp["Designator"]

        # Skip excluded components
        if any(des.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
            continue

        center_x = float(comp["Center-X(mm)"])
        center_y = float(comp["Center-Y(mm)"])
        ref_x = float(comp["Ref-X(mm)"])
        ref_y = float(comp["Ref-Y(mm)"])
        rotation = comp["Rotation"]
        layer = "Top" if comp["Layer"] == "TopLayer" else "Bottom"

        # Calculate discrepancy
        dx = abs(center_x - ref_x)
        dy = abs(center_y - ref_y)
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > DISCREPANCY_THRESHOLD:
            discrepancies.append({
                "Designator": des,
                "Comment": comp.get("Comment", ""),
                "Center": f"({center_x:.4f}, {center_y:.4f})",
                "Ref": f"({ref_x:.4f}, {ref_y:.4f})",
                "Delta": f"{dist:.3f} mm",
            })

        # Use Ref-X/Ref-Y for the CPL (matches Altium UI position)
        cpl_rows.append({
            "Designator": des,
            "Mid X": f"{ref_x:.4f}mm",
            "Mid Y": f"{ref_y:.4f}mm",
            "Layer": layer,
            "Rotation": rotation,
        })

    # Write corrected CPL
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        writer.writeheader()
        writer.writerows(cpl_rows)

    print(f"Wrote {len(cpl_rows)} components to: {OUTPUT_FILE.name}\n")

    # Report discrepancies
    if discrepancies:
        print(f"{'='*70}")
        print(f"CENTROID vs REFERENCE DISCREPANCIES (>{DISCREPANCY_THRESHOLD} mm)")
        print(f"{'='*70}")
        print(f"{'Designator':<12} {'Part':<28} {'Center X,Y':<24} {'Ref X,Y':<24} {'Delta':>8}")
        print(f"{'-'*12} {'-'*28} {'-'*24} {'-'*24} {'-'*8}")
        for d in discrepancies:
            print(f"{d['Designator']:<12} {d['Comment']:<28} {d['Center']:<24} {d['Ref']:<24} {d['Delta']:>8}")
        print(f"\nThese components have asymmetric footprints. The Ref coordinates")
        print(f"(used in the corrected CPL) match what Altium shows in the UI.")
        print(f"JLCPCB typically auto-corrects known footprints during review.")
    else:
        print("No significant centroid discrepancies found.")


if __name__ == "__main__":
    main()
