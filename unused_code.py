alanine_df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df.pq')
# The above df can be obtained with:
    # df = pd.read_parquet('/red/roitberg/prod_analysis/merged_mol.pq')
    # alanine_df = df[df['name'] == 'Alanine']
    # alanine_df.to_parquet('/red/roitberg/nick_analysis/alanine_df.pq')
    # Then load

#print(alanine_df['dcd_file'].unique()) #NOTE: This does detect there are structures from every .dcd file except 0.0ns


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
    floor_time_str = "{:.1f}ns".format(math.floor(floor_time * 10) / 10)
    for file in dcd_files:
        if floor_time_str in file:
            return os.path.join(traj_dir, file)
    return None


def old_determine_correct_dcd(frame_time, traj_dir):
    """
    This function checks for the correct simulation timestamp across a directory of
     .dcd trajectory files and returns the path to the correct file (or, if not located,
     returns None).
    :param frame_time: Timestamp (rounded down) of the simulation run
    :param traj_dir: Path to the .dcd files to search through
    """
    dcd_files = [f for f in os.listdir(traj_dir) if f.endswith('.dcd')]
    frame_time_str = "{:.2f}".format(frame_time)

    for file in dcd_files:
        traj_filename = os.path.basename(file)
        match = re.search(r'_(\d+\.\d+)ns\.dcd$', traj_filename)
        if match:
            time_offset = match.group(1)
            if frame_time_str == time_offset:
                return os.path.join(traj_dir, file)
    return None

# How to separate the merged_mol.pq into 0.1ns chunks so each corresponds to a traj file:
floored_times = [math.floor(time * 10) / 10 for time in df['time'].unique()]
unique_floored_times = set(floored_times)

df['floor_time'] = (df['time'] * 10).floordiv(1) / 10
unique_floor_times = df['floor_time'].unique()
separate_dfs = {floor_time: df[df['floor_time'] == floor_time] for floor_time in unique_floor_times}

# Example of accessing one of the split DataFrames
example_time = unique_floor_times[0]
example_df = separate_dfs[example_time]

for floor_time, df in separate_dfs.items():
    filename = f"df_for_floor_time_{floor_time}.pq"
    df.to_parquet(filename, index=True)     # NOTE: We want to keep the index here, as it tells the # of molecules in that same frame slice 


# To read and return the 



# These were in Richard's code:
        #command = f"python /red/roitberg/extract_slice.py {traj_file} {top_file} --frame_num={frame_num} --atom_indices=\"{atom_indices}\""
        #subprocess.run(command, shell=True)
        # Decided to just copy the entire slice_and_save_frame function, but i think the subprocess library is worth looking into

# Iterate over each row in the alanine dataframe
for index, row in alanine_df.iterrows():
    count += 1
    frame_time = math.floor(row['time'] * 10) / 10
    atom_indices = row['atom_indices']
    
    traj_file = determine_correct_dcd(frame_time, traj_dir)
    print('Trajectory file path:', traj_file)

    if traj_file is None:
        print(f'No .dcd file found for frame time {frame_time}')
    frame_num = row['local_frame']
    print(frame_num)

    slice_and_save_frame(traj_file, top_file, frame_num, atom_indices)
    #command = f"python /red/roitberg/extract_slice.py {traj_file} {top_file} --frame_num={frame_num} --atom_indices=\"{atom_indices}\""
    #subprocess.run(command, shell=True)

    if count > 100:
        break



# OLD main() (Jan 25th at 13:57):
def main():
    for floor_time, df in separate_dfs.items():
        unique_frames = df['local_frame'].unique()
        for frame_num in unique_frames:
            traj_file = df[df['local_frame'] == frame_num]['dcd_file'].iloc[0]
            coord_df = extract_coordinates_for_frame(traj_file, frame_num, df)
            df = df.merge(coord_df, left_index=True, right_index=True, how='left')
            break

        # NOTE: If saving to h5 instead of pq, multi-dim NP array can be saved directly
        #   Trying that last today (1/24/24) since I keep hitting errors 

        df.to_hdf(f"/red/roitberg/nick_analysis/split_parquets/coord_df_{floor_time}.h5", key='df', mode='w')
        break