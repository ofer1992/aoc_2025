#!/usr/bin/env python3

from utils import parse_input

shapes, regions = parse_input()

print("=== SHAPES ===")
for shape_id in sorted(shapes.keys()):
    print(f"Shape {shape_id}: {shapes[shape_id]['cells']} cells")

print(f"\n=== TOTAL REGIONS: {len(regions)} ===\n")

# Check 1: Regions with insufficient total cells
print("CHECK 1: Regions with insufficient total cells")
insufficient_cells = []
for idx, region in enumerate(regions):
    grid_cells = region['width'] * region['height']
    total_present_cells = sum(region['counts'][j] * shapes[j]['cells'] for j in range(len(region['counts'])))

    if total_present_cells > grid_cells:
        insufficient_cells.append(idx)

print(f"Impossible (not enough cells): {len(insufficient_cells)}")
print(f"Possibly solvable: {len(regions) - len(insufficient_cells)}")

# Check 2: Regions with sufficient 3x3 blocks (naive approach)
print("\nCHECK 2: Regions with sufficient 3x3 blocks")
sufficient_blocks = []
for idx, region in enumerate(regions):
    blocks = (region['width'] // 3) * (region['height'] // 3)
    total_shapes = sum(region['counts'])

    if blocks >= total_shapes:
        sufficient_blocks.append(idx)

print(f"Enough 3x3 blocks: {len(sufficient_blocks)}")

# Check overlap: regions that pass both checks
print("\nOVERLAP ANALYSIS:")
pass_both = set(range(len(regions))) - set(insufficient_cells)
trivial_fillable = set(sufficient_blocks)
both = pass_both & trivial_fillable

print(f"Pass CHECK 1 (enough cells): {len(pass_both)}")
print(f"Pass CHECK 2 (enough blocks): {len(trivial_fillable)}")
print(f"Pass BOTH checks: {len(both)}")

# Find regions that pass CHECK 2 but fail CHECK 1 (the discrepancy)
fail_1_pass_2 = trivial_fillable - pass_both
if fail_1_pass_2:
    print(f"\n!!! DISCREPANCY: {len(fail_1_pass_2)} regions pass CHECK 2 but fail CHECK 1")
    print("First few examples:")
    for idx in list(fail_1_pass_2)[:3]:
        r = regions[idx]
        grid_cells = r['width'] * r['height']
        total_present_cells = sum(r['counts'][j] * shapes[j]['cells'] for j in range(len(r['counts'])))
        blocks = (r['width'] // 3) * (r['height'] // 3)
        total_shapes = sum(r['counts'])
        print(f"  Region {idx+1} ({r['width']}x{r['height']}): "
              f"grid={grid_cells}, need={total_present_cells}, "
              f"blocks={blocks}, shapes={total_shapes}")
