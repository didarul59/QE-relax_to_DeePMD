import numpy as np
import os

folder = 'combined_flat_data'

for fname in ['coord.npy', 'force.npy', 'box.npy', 'energy.npy']:
    path = os.path.join(folder, fname)
    if os.path.exists(path):
        data = np.load(path)
        print(f"{fname}: shape = {data.shape}")
    else:
        print(f"{fname} not found in {folder}")
