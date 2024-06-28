import pandas as pd

mol_df = pd.read_parquet('/red/roitberg/nick_analysis/Restart/228k_atoms/test_analyze1/2024-06-07-131408.685273_seg0000of0010_molecule.pq')

print('`mol_df`\n', mol_df)

formula_df = pd.read_parquet('/red/roitberg/nick_analysis/Restart/228k_atoms/test_analyze1/2024-06-07-131408.685273_seg0000of0010_formula.pq')

print('`formula_df`\n', formula_df)

def atom_count(formula):
    import re
    return sum(int(num) if num else 1 for num in re.findall(r'(\d*)[A-Z]', formula))

filtered_formula_df = formula_df[formula_df['index'].apply(atom_count) > 5]

print('`filtered_formula_df`\n', filtered_formula_df)


