import torch
import torchani
import ase

model = torchani.models.ANIdr()
ase_mol = ase.io.read('/red/roitberg/nick_analysis/2023-12-23-005238.631380_0.1ns_frame5580_atoms2282068_3147562_5732.pdb', format='.pdb')

