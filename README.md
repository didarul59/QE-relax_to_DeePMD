# QE_to_DeepMD

This repository provides a full pipeline to convert Quantum ESPRESSO (QE) molecular dynamics output into DeepMD-kit training data.

> 🔒 **Private repository — for personal use only**

---

## 📁 Project Structure

QE_to_DeepMD/
├── collect.py # Collect QE MD output
├── to.py # Convert output to NumPy format
├── rename.py # Rename data files
├── reshape.py # Reshape the data
├── combine.py # Combine multiple runs
├── flat.py # Flatten arrays for training
├── shape.py, train_valid.py, etc.
│
├── combined_flat_data/ # Final processed .npy files
├── 00.data/
│ ├── training_data/ # 90% data split
│ └── validation_data/ # 10% data split
│
└── 01.train/
└── input.json # DeepMD training config
