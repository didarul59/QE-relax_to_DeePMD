import numpy as np
import os

data_dir = './combined_flat_data'  # <-- this matches your folder structure

# Load arrays
coords = np.load(os.path.join(data_dir, 'coord.npy'))
boxes = np.load(os.path.join(data_dir, 'box.npy'))
forces = np.load(os.path.join(data_dir, 'force.npy'))
energies = np.load(os.path.join(data_dir, 'energy.npy'))
pressure = np.load(os.path.join(data_dir, 'pressure.npy'))

total_samples = coords.shape[0]
val_size = int(total_samples * 0.10)
train_size = total_samples - val_size

coords_train, coords_val = coords[:train_size], coords[train_size:]
boxes_train, boxes_val = boxes[:train_size], boxes[train_size:]
forces_train, forces_val = forces[:train_size], forces[train_size:]
energies_train, energies_val = energies[:train_size], energies[train_size:]
pressure_train, pressure_val = pressure[:train_size], pressure[train_size:]

train_dir = os.path.join('./00.data', 'training_data/set.000')
val_dir = os.path.join('./00.data', 'validation_data/set.000')

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

np.save(os.path.join(train_dir, 'coord.npy'), coords_train)
np.save(os.path.join(train_dir, 'box.npy'), boxes_train)
np.save(os.path.join(train_dir, 'force.npy'), forces_train)
np.save(os.path.join(train_dir, 'energy.npy'), energies_train)
np.save(os.path.join(train_dir, 'pressure.npy'), pressure_train)

np.save(os.path.join(val_dir, 'coord.npy'), coords_val)
np.save(os.path.join(val_dir, 'box.npy'), boxes_val)
np.save(os.path.join(val_dir, 'force.npy'), forces_val)
np.save(os.path.join(val_dir, 'energy.npy'), energies_val)
np.save(os.path.join(val_dir, 'pressure.npy'), pressure_val)
import shutil
import os

train_dir1 = os.path.join('./00.data', 'training_data')
val_dir1 = os.path.join('./00.data', 'validation_data')

symbol_src = os.path.join(data_dir, 'symbol.raw')
type_src = os.path.join(data_dir, 'type.raw')

if os.path.exists(symbol_src) and os.path.exists(type_src):
    # Copy symbol.raw content but rename as type.raw
    shutil.copy(symbol_src, os.path.join(train_dir1, 'type.raw'))
    shutil.copy(symbol_src, os.path.join(val_dir1, 'type.raw'))
    
    # Copy type.raw content but rename as symbol.raw
    shutil.copy(type_src, os.path.join(train_dir1, 'symbol.raw'))
    shutil.copy(type_src, os.path.join(val_dir1, 'symbol.raw'))
else:
    if not os.path.exists(symbol_src):
        print(f"Warning: symbol.raw not found in {data_dir}")
    if not os.path.exists(type_src):
        print(f"Warning: type.raw not found in {data_dir}")


print(f"Saved {train_size} training and {val_size} validation samples in:")
print(f" - {train_dir}")
print(f" - {val_dir}")
print("Training set shapes:")
print("coords_train:", coords_train.shape)
print("boxes_train:", boxes_train.shape)
print("forces_train:", forces_train.shape)
print("energies_train:", energies_train.shape)

print("\nValidation set shapes:")
print("coords_val:", coords_val.shape)
print("boxes_val:", boxes_val.shape)
print("forces_val:", forces_val.shape)
print("energies_val:", energies_val.shape)

