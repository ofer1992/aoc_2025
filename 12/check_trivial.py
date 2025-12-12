#!/usr/bin/env python3

# Parse the input
with open('input.txt', 'r') as f:
    lines = [line.rstrip() for line in f.readlines()]

# Parse shapes (just for counting)
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
        shapes[shape_id] = True
    else:
        i += 1

# Parse regions and check if trivially fillable
trivial_count = 0
i = 0
while i < len(lines):
    if 'x' in lines[i] and ':' in lines[i]:
        parts = lines[i].split(': ')
        dims = parts[0].split('x')
        width, height = int(dims[0]), int(dims[1])

        counts = list(map(int, parts[1].split()))

        # Calculate number of 3x3 blocks
        blocks = (width // 3) * (height // 3)

        # Calculate total shapes required
        total_shapes = sum(counts)

        if blocks >= total_shapes:
            trivial_count += 1
    i += 1

print(f"Regions that can be trivially filled (3x3 blocks): {trivial_count}")
