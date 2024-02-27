import pandas as pd
import mdtraj as md
from top_loader import load_topology
import timeit

start_timer = timeit.default_timer()

df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df.pq')
topology = load_topology('/red/roitberg/nick_analysis/traj_top_0.0ns.h5')
topology_timer = timeit.default_timer()
print(f'Topology loaded in {topology_timer - start_timer} seconds.')


# Your Alanine-specific dataframe, ensure it's loaded and filtered for Alanine molecules
df = pd.read_parquet('/red/roitberg/nick_analysis/alanine_df_with_dcd.pq')

def extract_coordinates_for_frame(traj_file, topology, frame_num, df):
    frame = md.load_frame(traj_file, index=frame_num, top=topology)
    coord_dict = {}
    # Filter for the current frame
    filtered_df = df[df['local_frame'] == frame_num]
    for index, row in filtered_df.iterrows():
        try:
            coordinates = frame.xyz[0, row['atom_indices']]
            coord_dict[index] = coordinates
        except Exception as e:
            coord_dict[index] = np.nan
    return coord_dict

def main():
    unique_frames = df['local_frame'].unique()
    for frame_num in unique_frames:
        # Assuming 'dcd_file' column exists and is correctly filled
        traj_file = df[df['local_frame'] == frame_num]['dcd_file'].iloc[0]
        coord_dict = extract_coordinates_for_frame(traj_file, topology, frame_num, df)
        for index, coords in coord_dict.items():
            df.at[index, 'coordinates'] = coords

    # Saving the dataframe after coordinate extraction
    df.to_parquet('/red/roitberg/nick_analysis/alanine_coords.pq', key='df', mode='w')

if __name__ == "__main__":
    main()

end_timer = timeit.default_timer()

print(f'Time for entire script: {end_timer - start_timer} seconds.')
