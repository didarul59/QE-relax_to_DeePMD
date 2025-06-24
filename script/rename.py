import os

# Correct and existing directory
source_dir = './data/'

# Change into the target directory
os.chdir(source_dir)

# Find all numeric directories (e.g., "0", "1", ...)
dirs = sorted([d for d in os.listdir() if os.path.isdir(d) and d.isdigit()])

# Rename them to set.000, set.001, ...
for i, d in enumerate(dirs):
    new_name = f"set.{i:03d}"
    print(f"Renaming {d} → {new_name}")
    os.rename(d, new_name)

