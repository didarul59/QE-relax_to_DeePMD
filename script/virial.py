import numpy as np
import os

folders = [
    "./00.data/training_data/set.000/",
    "./00.data/validation_data/set.000/"
]

for data_dir in folders:
    print(f"Processing folder: {data_dir}")

    coords = np.load(os.path.join(data_dir, "coord.npy"))
    forces = np.load(os.path.join(data_dir, "force.npy"))
    box = np.load(os.path.join(data_dir, "box.npy"))  # Usually (N_frames, 3, 3)

    # Reshape coords if flattened: (N_frames, N_atoms*3) -> (N_frames, N_atoms, 3)
    if coords.ndim == 2 and coords.shape[1] % 3 == 0:
        N_atoms = coords.shape[1] // 3
        coords = coords.reshape(coords.shape[0], N_atoms, 3)
    else:
        N_atoms = coords.shape[1]

    # Reshape forces similarly
    if forces.ndim == 2 and forces.shape[1] == N_atoms * 3:
        forces = forces.reshape(forces.shape[0], N_atoms, 3)

    # Check frame counts
    if coords.shape[0] != forces.shape[0]:
        print(f"Warning: coords frames ({coords.shape[0]}) != forces frames ({forces.shape[0]}), truncating to minimum.")
    N_frames = min(coords.shape[0], forces.shape[0])

    virials = np.zeros((N_frames, 3, 3))
    for i in range(N_frames):
        r = coords[i]  # shape (N_atoms, 3)
        f = forces[i]  # shape (N_atoms, 3)
        virials[i] = -np.einsum('ai,aj->ij', r, f)  # Virial tensor (3x3)

    # Flatten virial tensor to shape (N_frames, 9)
    virials_flat = virials.reshape(N_frames, 9)

    # Save flattened virial tensor
    virial_path = os.path.join(data_dir, "virial.npy")
    np.save(virial_path, virials_flat)

    print(f"Virial tensor computed, flattened, and saved at {virial_path}")
    print("Virial tensor shape:", virials_flat.shape)
    print()

