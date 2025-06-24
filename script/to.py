import os
import numpy as np

def parse_cell(filename):
    with open(filename) as f:
        lines = f.readlines()
    cell = np.array([list(map(float, line.split())) for line in lines])
    return cell

def parse_positions(filename):
    elems = []
    coords = []
    with open(filename) as f:
        for line in f:
            parts = line.strip().split()
            elems.append(parts[0])
            coords.append(list(map(float, parts[1:])))
    return elems, np.array(coords)

def parse_forces_pressure(filename):
    forces = []
    pressure = None
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Pressure:"):
            pressure = float(line.split(":")[1].strip())
        else:
            parts = line.split()
            if len(parts) == 3:
                forces.append(list(map(float, parts)))
    return np.array(forces), pressure

def parse_energy(filename):
    with open(filename) as f:
        energy = float(f.read().strip())
    return energy

def convert_to_deepmd_format(output_dir='./output_steps/', deepmd_data_dir='data'):
    if not os.path.exists(deepmd_data_dir):
        os.mkdir(deepmd_data_dir)

    # Sort step folders
    steps = sorted([d for d in os.listdir(output_dir) if d.startswith('step_')],
                   key=lambda x: int(x.split('_')[1]))

    # First step
    first_step_dir = os.path.join(output_dir, steps[0])
    elems, _ = parse_positions(os.path.join(first_step_dir, 'positions.txt'))

    # Save type.raw (e.g., Si O H)
    with open(os.path.join(deepmd_data_dir, 'type.raw'), 'w') as f:
        f.write(' '.join(elems) + '\n')

    # Map elements to integer indices
    unique_elems = sorted(set(elems))
    elem_to_index = {elem: i for i, elem in enumerate(unique_elems)}
    atom_indices = [elem_to_index[elem] for elem in elems]

    # Save symbol.raw (e.g., 0 0 1 1 2 2)
    with open(os.path.join(deepmd_data_dir, 'symbol.raw'), 'w') as f:
        f.write(' '.join(map(str, atom_indices)) + '\n')

    print(f"Element-to-index mapping: {elem_to_index}")

    # Convert each step
    for i, step in enumerate(steps):
        step_dir = os.path.join(output_dir, step)
        elems, coords = parse_positions(os.path.join(step_dir, 'positions.txt'))
        forces, pressure = parse_forces_pressure(os.path.join(step_dir, 'forces_pressure.txt'))
        cell = parse_cell(os.path.join(step_dir, 'cell.txt'))
        energy = parse_energy(os.path.join(step_dir, 'energy.txt'))

        # Create frame directory
        frame_dir = os.path.join(deepmd_data_dir, str(i))
        os.makedirs(frame_dir, exist_ok=True)

    # Save data
        np.save(os.path.join(frame_dir, 'coord.npy'), coords)
        np.save(os.path.join(frame_dir, 'force.npy'), forces)
        np.save(os.path.join(frame_dir, 'box.npy'), cell)
        np.save(os.path.join(frame_dir, 'energy.npy'), np.array([energy]))
        np.save(os.path.join(frame_dir, 'pressure.npy'), np.array([pressure])) 

    print(f"Converted {len(steps)} steps into DeepMD format at '{deepmd_data_dir}'.")

if __name__ == "__main__":
    convert_to_deepmd_format()

