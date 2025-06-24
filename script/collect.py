import os

def get_number_of_atoms_from_qe_out(filename):
    with open(filename, 'r') as f:
        for line in f:
            if 'number of atoms/cell' in line:
                return int(line.split('=')[-1].strip())
    raise ValueError("Couldn't find number of atoms in QE output.")

def parse_qe_opt_out(filename):
    n_atoms = get_number_of_atoms_from_qe_out(filename)

    with open(filename, 'r') as f:
        lines = f.readlines()

    snapshots = []
    energy = None
    cell = []
    positions = []
    forces = []
    pressure = None

    in_cell = False
    in_positions = False
    in_forces = False
    in_pressure = False

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if 'CELL_PARAMETERS' in line:
            cell = []
            for j in range(3):
                i += 1
                cell.append([float(x) for x in lines[i].strip().split()])
            in_cell = True

        elif 'ATOMIC_POSITIONS' in line:
            positions = []
            for j in range(n_atoms):
                i += 1
                parts = lines[i].strip().split()
                positions.append([parts[0]] + list(map(float, parts[1:4])))
            in_positions = True

        elif 'Forces acting on atoms' in line:
            forces = []
            i += 2
            for j in range(n_atoms):
                parts = lines[i].strip().split()
                fx, fy, fz = map(lambda v: float(v) * 25.711043, parts[-3:])
                forces.append([fx, fy, fz])
                i += 1
            i -= 1
            in_forces = True

        elif 'P=' in line:
            parts = line.split('P=')
            try:
                pressure = float(parts[1].strip())
            except:
                pressure = None
            in_pressure = True

        elif '!' in line and 'total energy' in line:
            try:
                energy = float(line.split()[-2]) * 13.605698
            except:
                energy = None

        if in_cell and in_positions and in_forces and in_pressure:
            snapshots.append({
                'energy': energy,
                'cell': cell,
                'positions': positions,
                'forces': forces,
                'pressure': pressure
            })
            # Reset for next snapshot
            energy = cell = positions = forces = pressure = None
            in_cell = in_positions = in_forces = in_pressure = False

        i += 1

    return snapshots

def save_snapshots(snapshots, base_dir='output_steps'):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for idx, snap in enumerate(snapshots, start=1):
        step_dir = os.path.join(base_dir, f'step_{idx}')
        os.makedirs(step_dir, exist_ok=True)

        with open(os.path.join(step_dir, 'cell.txt'), 'w') as f:
            for row in snap['cell']:
                f.write(' '.join(f"{x:.10f}" for x in row) + '\n')

        with open(os.path.join(step_dir, 'positions.txt'), 'w') as f:
            for atom in snap['positions']:
                elem, x, y, z = atom
                f.write(f"{elem} {x:.10f} {y:.10f} {z:.10f}\n")

        with open(os.path.join(step_dir, 'energy.txt'), 'w') as f:
            f.write(f"{snap['energy']:.10f}\n")

        with open(os.path.join(step_dir, 'forces_pressure.txt'), 'w') as f:
            for fx, fy, fz in snap['forces']:
                f.write(f"{fx:.10f} {fy:.10f} {fz:.10f}\n")
            f.write(f"Pressure: {snap['pressure']:.10f}\n")

if __name__ == '__main__':
    filename = 'opt.out'
    snapshots = parse_qe_opt_out(filename)
    print(f"Parsed {len(snapshots)} snapshots.")
    save_snapshots(snapshots)
    print("Data saved into folders: output_steps/step_1, step_2, ...")

