#!/usr/bin/env python3

def parse_input(filename='input.txt'):
    """Parse the input file and return shapes dict and regions list."""
    with open(filename, 'r') as f:
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
            shapes[shape_id] = {
                'lines': shape_lines,
                'cells': cell_count
            }
        else:
            i += 1

    # Parse regions
    regions = []
    i = 0
    while i < len(lines):
        if 'x' in lines[i] and ':' in lines[i]:
            parts = lines[i].split(': ')
            dims = parts[0].split('x')
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].split()))

            regions.append({
                'width': width,
                'height': height,
                'counts': counts
            })
        i += 1

    return shapes, regions
