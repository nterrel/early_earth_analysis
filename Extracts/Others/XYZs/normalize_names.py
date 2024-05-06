import os

def normalize_and_rename(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xyz"):
            # Keep the 'all_' prefix but ensure the rest of the name is in lowercase
            if 'all_' in filename:
                # Strip everything after 'all_' and process it
                prefix, name_part = filename.split('all_', 1)
                new_name = 'all_' + name_part.replace('_', ' ').rstrip('.xyz').lower() + '.xyz'
            else:
                # If 'all_' is not in the filename, just normalize it
                new_name = filename.replace('_', ' ').rstrip('.xyz').lower() + '.xyz'
            
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
            print(f"Renamed '{filename}' to '{new_name}'")

directory = '/red/roitberg/nick_analysis/Extracts/Others/XYZs'
normalize_and_rename(directory)
