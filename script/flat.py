import numpy as np
import os

# Folder containing original data, relative to current directory
original_folder = 'data/combined/'

# New folder inside current directory (practical/)
new_folder = 'combined_flat_data'

# Make sure the new folder exists
os.makedirs(new_folder, exist_ok=True)

# Load original arrays
coords = np.load(os.path.join(original_folder, 'coord.npy'))    # e.g. (13,14,3)
forces = np.load(os.path.join(original_folder, 'force.npy'))
boxes = np.load(os.path.join(original_folder, 'box.npy'))
energies = np.load(os.path.join(original_folder, 'energy.npy'))
pressure = np.load(os.path.join(original_folder, 'pressure.npy'))
# Flatten coords and forces to shape (frames, atoms * 3)
coords_flat = coords.reshape(coords.shape[0], -1)   # (N, 42) if 14 atoms × 3 coords
forces_flat = forces.reshape(forces.shape[0], -1)
boxes_flat = boxes.reshape(boxes.shape[0], -1)      # (N, 9)
# energies should already be 1D

# Save flattened arrays in new folder
np.save(os.path.join(new_folder, 'coord.npy'), coords_flat)
np.save(os.path.join(new_folder, 'force.npy'), forces_flat)
np.save(os.path.join(new_folder, 'box.npy'), boxes_flat)
np.save(os.path.join(new_folder, 'energy.npy'), energies)
np.save(os.path.join(new_folder, 'pressure.npy'), pressure)
for raw_file in ['type.raw', 'symbol.raw']:
    src_path = os.path.join(original_folder, raw_file)
    dst_path = os.path.join(new_folder, raw_file)
    if os.path.exists(src_path):
        with open(src_path, 'rb') as fin, open(dst_path, 'wb') as fout:
            fout.write(fin.read())
    else:
        print(f"Warning: {raw_file} not found in {original_folder}. Skipping copy.")


print(f"All data flattened and saved in folder: {new_folder}")
