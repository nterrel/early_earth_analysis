import glob
import os

def concatenate_xyz_files(directory):
    molecule_files = {}
    xyz_files = glob.glob(os.path.join(directory, '*.xyz'))
    
    # Group files by molecule name
    for file in xyz_files:
        molecule_name = os.path.basename(file).split('_')[0]
        
        if molecule_name not in molecule_files:
            molecule_files[molecule_name] = []
        molecule_files[molecule_name].append(file)
    
    # Concatenate files for each molecule
    for molecule, files in molecule_files.items():
        sorted_files = sorted(files, key=lambda x: float(os.path.basename(x).split('_')[1].rstrip('ns.xyz')))
        output_file_path = os.path.join(directory, f"all_{molecule}.xyz")

        with open(output_file_path, 'w') as output_file:
            for file_path in sorted_files:
                with open(file_path, 'r') as input_file:
                    contents = input_file.read()
                    output_file.write(contents)
                    #output_file.write('\n')  # Optional: adds a newline between files for clarity
        
        print(f"Concatenated {len(files)} files into {output_file_path}")

# Specify the directory containing the XYZ files
directory = '/red/roitberg/nick_analysis/XYZs'
concatenate_xyz_files(directory)
