import glob

# Path to the directory containing the .xyz files
xyz_dir = '/red/roitberg/nick_analysis/Ala_df/XYZs'

# New file to contain all concatenated .xyz files
all_xyz_filename = '/red/roitberg/nick_analysis/Ala_df/XYZs/all_alanines.xyz'

# Open the new file in write mode
with open(all_xyz_filename, 'w') as all_xyz_file:
    # Iterate over all .xyz files sorted alphabetically
    for xyz_file in sorted(glob.glob(f"{xyz_dir}/ala_*.xyz")):
        print(xyz_file, 'appending to end')
        # Open and read the current .xyz file
        with open(xyz_file, 'r') as file:
            contents = file.read()
            # Write the contents to the all-in-one .xyz file
            all_xyz_file.write(contents)
            # Optionally, write a newline for separation (may not be needed)
            all_xyz_file.write('\n')

