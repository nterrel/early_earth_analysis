import pandas as pd
import os

# Define file names
original_formula_15 = 'combined_original_formula.pq'
original_molecule_15 = 'combined_original_molecule.pq'
quenched_formula_15 = 'combined_quenched_formula.pq'
quenched_molecule_15 = 'combined_quenched_molecule.pq'

# Subdirectory with 400 frames
subdir = 'random_400_frames'

original_formula_400 = os.path.join(subdir, 'combined_original_formula.pq')
original_molecule_400 = os.path.join(subdir, 'combined_original_molecule.pq')
quenched_formula_400 = os.path.join(subdir, 'combined_quenched_formula.pq')
quenched_molecule_400 = os.path.join(subdir, 'combined_quenched_molecule.pq')

# Read 15 frame parquet files
df_original_formula_15 = pd.read_parquet(original_formula_15)
df_original_molecule_15 = pd.read_parquet(original_molecule_15)
df_quenched_formula_15 = pd.read_parquet(quenched_formula_15)
df_quenched_molecule_15 = pd.read_parquet(quenched_molecule_15)

# Read 400 frame parquet files
df_original_formula_400 = pd.read_parquet(original_formula_400)
df_original_molecule_400 = pd.read_parquet(original_molecule_400)
df_quenched_formula_400 = pd.read_parquet(quenched_formula_400)
df_quenched_molecule_400 = pd.read_parquet(quenched_molecule_400)

# Concatenate the dataframes for original and quenched
combined_original_formula = pd.concat([df_original_formula_15, df_original_formula_400], ignore_index=True)
combined_original_molecule = pd.concat([df_original_molecule_15, df_original_molecule_400], ignore_index=True)
combined_quenched_formula = pd.concat([df_quenched_formula_15, df_quenched_formula_400], ignore_index=True)
combined_quenched_molecule = pd.concat([df_quenched_molecule_15, df_quenched_molecule_400], ignore_index=True)

# Save the concatenated data as new parquet files
combined_original_formula.to_parquet('combined_415_original_formula.pq')
combined_original_molecule.to_parquet('combined_415_original_molecule.pq')
combined_quenched_formula.to_parquet('combined_415_quenched_formula.pq')
combined_quenched_molecule.to_parquet('combined_415_quenched_molecule.pq')

print("Parquet files successfully concatenated and saved.")

