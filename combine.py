import numpy as np
import os

data_path = "./data"
sets = sorted([f for f in os.listdir(data_path) if f.startswith('set.')])

all_coords = []
all_boxes = []
all_forces = []
all_energies = []

for s in sets:
    folder = os.path.join(data_path, s)
    
    coords = np.load(os.path.join(folder, "coord.npy"))   # shape (1, 14, 3)
    boxes = np.load(os.path.join(folder, "box.npy"))      # shape (1, 3, 3)
    forces = np.load(os.path.join(folder, "force.npy"))   # shape (1, 14, 3)
    energy = np.load(os.path.join(folder, "energy.npy"))  # shape (1,)
    
    all_coords.append(coords)
    all_boxes.append(boxes)
    all_forces.append(forces)
    all_energies.append(energy)

# Stack along the first dimension (frames)
coords_all = np.concatenate(all_coords, axis=0)   # shape (N, 14, 3)
boxes_all = np.concatenate(all_boxes, axis=0)     # shape (N, 3, 3)
forces_all = np.concatenate(all_forces, axis=0)   # shape (N, 14, 3)
energies_all = np.concatenate(all_energies, axis=0).reshape(-1, 1)  # shape (N,)

# Create a new folder for combined dataset
combined_path = os.path.join(data_path, "combined")
os.makedirs(combined_path, exist_ok=True)

np.save(os.path.join(combined_path, "coord.npy"), coords_all)
np.save(os.path.join(combined_path, "box.npy"), boxes_all)
np.save(os.path.join(combined_path, "force.npy"), forces_all)
np.save(os.path.join(combined_path, "energy.npy"), energies_all)

import shutil

# Copy type.raw and symbol.raw from ./data folder to ./data/combined
for raw_file in ['type.raw', 'symbol.raw']:
    src = os.path.join(data_path, raw_file)
    dst = os.path.join(combined_path, raw_file)
    if os.path.isfile(src):
        shutil.copy(src, dst)
    else:
        raise FileNotFoundError(f"Missing {raw_file} in the data folder. Please ensure it exists.")

