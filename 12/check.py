#!/usr/bin/env python3

# Parse the input
with open('input.txt', 'r') as f:
    lines = [line.rstrip() for line in f.readlines()]

# Parse shapes
shapes = {}
i = 0
while i < len(lines):
    if ':' in lines[i] and 'x' not in lines[i]:
        shape_id = int(lines[i].split(':')[0])
        shape_lines = []
        i += 1
        while i < len(lines) and lines[i] and ':' not in lines[i]:
            shape_lines.append(lines[i])
            i += 1
        # Count # cells in this shape
        cell_count = sum(line.count('#') for line in shape_lines)
        shapes[shape_id] = cell_count
    else:
        i += 1

print(f"Shapes and their cell counts:")
for shape_id in sorted(shapes.keys()):
    print(f"  Shape {shape_id}: {shapes[shape_id]} cells")
print()

# Parse regions and check
impossible_regions = []
i = 0
region_num = 0
while i < len(lines):
    if 'x' in lines[i] and ':' in lines[i]:
        parts = lines[i].split(': ')
        dims = parts[0].split('x')
        width, height = int(dims[0]), int(dims[1])
        grid_cells = width * height

        counts = list(map(int, parts[1].split()))

        # Calculate total present cells needed
        total_present_cells = sum(counts[j] * shapes[j] for j in range(len(counts)))

        region_num += 1
        if total_present_cells > grid_cells:
            impossible_regions.append((region_num, width, height, grid_cells, total_present_cells))
            print(f"Region {region_num} ({width}x{height}): IMPOSSIBLE")
            print(f"  Grid cells: {grid_cells}")
            print(f"  Present cells needed: {total_present_cells}")
            print(f"  Deficit: {total_present_cells - grid_cells}")
            print()
    i += 1

print(f"\nTotal regions: {region_num}")
print(f"Impossible regions (not enough space): {len(impossible_regions)}")
