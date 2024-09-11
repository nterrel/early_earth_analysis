import os
import shutil

# TEST ON 1scripts_to_resubmit.txt -- remove the `1` after it works properly
script_list = "1scripts_to_resubmit.txt"

backup_dir = "original_scripts_backup"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def edit_script(script_path):
    # Create a backup copy of the original script
    script_dir, script_name = os.path.split(script_path)
    backup_script_path = os.path.join(backup_dir, f"original_{script_name}")
    shutil.copy(script_path, backup_script_path)

    # Read the contents of a SLURM script for LAMMPS restart
    with open(script_path, 'r') as file:
        lines = file.readlines()

    # Edit script to remove the reservation information
    with open(script_path, 'w') as file:
        for line in lines:
            if "--reservation" in line or "--qos" in line or "--account" in line:
                continue
            elif "--nodes" in line or "--ntasks-per-node" in line:
                continue
            elif "--partition=" in line:
                line = "#SBATCH --partition=gpu\n"
            elif "--ntasks=" in line:
                line = "#SBATCH --ntasks=32\n"
            elif "--cpus-per-task=" in line:
                line = "#SBATCH --cpus-per-task=1\n"
            elif "--gres=" in line:
                line = "#SBATCH --gpus-per-task=a100:1\n"
            elif "--mem=" in line:
                line = "#SBATCH --mem-per-cpu=12gb\n"
            elif "--time=" in line:
                line = "#SBATCH --time=02:00:00\n"
            
            file.write(line + "\n")

with open(script_list, 'r') as list_file:
    script_paths = list_file.readlines()
    for script_path in script_paths:
        script_path = script_path.strip()
        if os.path.exists(script_path):
            edit_script(script_path)
            print(f"New script saved to: {script_path}")
        else:
            print(f"Script not found: {script_path}")

print("Scripts updated successfully, original copies saved.")

