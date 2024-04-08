from rdkit import Chem
from rdkit.Chem import Draw
import pandas as pd

mol_data = pd.read_parquet('molecule_data.pq')
ala_smiles = mol_data[mol_data['name'] == 'Alanine']['smiles'][0]
# 'CC(C(=O)O)N'
ala_mol = Chem.MolFromSmiles(ala_smiles)
img = Draw.MolToImage(ala_mol)
Draw.MolToFile(ala_mol, 'alanine_std.png')
