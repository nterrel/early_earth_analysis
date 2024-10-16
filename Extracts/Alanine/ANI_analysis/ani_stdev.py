import torch
import torchani
import typing as tp
from analysis_utils import ANI1x_NR_Model, read_xyz, write_xyz

model = ANI1x_NR_Model(use_repulsion=True)
print(model)
ani_structures = read_xyz('reordered_ani_alanines.xyz')
# print(ani_structures)

exit()
