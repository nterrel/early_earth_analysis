import math
import os

def determine_correct_dcd(frame_time, traj_dir):
    """
    No longer needed in extraction code since i've saved all .dcd paths to the dataframes containing found molecules
    
    This function checks for the correct simulation timestamp across a directory of
     .dcd trajectory files and returns the path to the correct file (or, if not located,
     returns None).
    :param frame_time: Timestamp (rounded down) of the simulation run
    :param traj_dir: Path to the .dcd files to search through
    """
    dcd_files = [f for f in os.listdir(traj_dir) if f.endswith('.dcd')]
    floor_time_str = "{:.1f}ns".format(math.floor(frame_time * 10) / 10)
    for file in dcd_files:
        if floor_time_str in file:
            return os.path.join(traj_dir, file)
    return None