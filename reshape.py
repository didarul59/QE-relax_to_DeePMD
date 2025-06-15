import numpy as np
import os

# ✅ Set your target directory
source_dir = './data/'  # <-- Update if needed

# Change into the target directory
os.chdir(source_dir)

# Get all set directories: set.000, set.001, ...
set_dirs = sorted([d for d in os.listdir() if d.startswith("set.") and os.path.isdir(d)])

for d in set_dirs:
    print(f"Processing {d}...")
    for fname in ["coord.npy", "force.npy", "box.npy"]:
        path = os.path.join(d, fname)
        if not os.path.exists(path):
            print(f"  {fname} not found, skipping.")
            continue

        data = np.load(path)

        # Reshape based on file type
        if fname in ["coord.npy", "force.npy"]:
            if data.shape == (3, 14):  # fallback fix
                data = data.T
            if data.ndim == 2:
                data = data.reshape(1, -1, 3)  # (atoms, 3) → (1, atoms, 3)
        elif fname == "box.npy":
            if data.ndim == 2:
                data = data.reshape(1, 3, 3)   # (3, 3) → (1, 3, 3)

        # Save reshaped data back
        np.save(path, data)
        print(f"  {fname} reshaped to {data.shape}")

