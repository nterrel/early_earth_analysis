def adjust_coordinates(coord, box_size=556.0):
    """Adjust coordinates using periodic boundary conditions."""
    return coord % box_size

def process_xyz_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    adjusted_lines = []
    problem_count = 0
    for i in range(len(lines)):
        if lines[i].startswith("Frame"):
            block = lines[i:i+14]  # Assuming each block is 14 lines including the Frame line
            problem_detected = any(float(line.split()[2]) > box_size for line in block if len(line.split()) == 4)
            if problem_detected:
                problem_count += 1
                for j in range(1, 14):  # Skip the Frame line itself
                    if len(block[j].split()) == 4:
                        _, x, y, z = block[j].split()
                        x, y, z = map(float, [x, y, z])
                        # Adjust coordinates if necessary
                        y = adjust_coordinates(y, box_size=556.0)
                        block[j] = f"{block[j].split()[0]} {x:.6f} {y:.6f} {z:.6f}\n"
            adjusted_lines.extend(block)

    return adjusted_lines, problem_count

# Path to the original and adjusted XYZ files
original_xyz_filename = '/path/to/all_alanines.xyz'
adjusted_xyz_filename = '/path/to/all_alanines_adjusted.xyz'

# Process the original file
adjusted_lines, problem_count = process_xyz_file(original_xyz_filename)

# Write the adjusted lines to a new file
with open(adjusted_xyz_filename, 'w') as f:
    f.writelines(adjusted_lines)

print(f"Total sets with out-of-bounds coordinates adjusted: {problem_count}")

