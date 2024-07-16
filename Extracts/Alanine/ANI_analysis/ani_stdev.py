import torch
import torchani
from torchani.io import read_xyz

ani_structures = read_xyz('reordered_ani_alanines.xyz')
#print(ani_structures)

model = torchani.models.ANIdr()


