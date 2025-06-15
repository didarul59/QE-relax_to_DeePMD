#!/bin/bash

# Run the Python scripts in order
python3 collect.py
python3 to.py
python3 rename.py
python3 reshape.py
python3 combine.py
python3 flat.py
python3 train_valid.py

# Create the 01.train folder
mkdir -p 01.train

# Write the input.json file
cat > 01.train/input.json << EOF
{
  "_comment": "model parameters",
  "model": {
    "type_map": ["C", "N", "S", "O", "Na"],
    "descriptor": {
      "type": "se_e2_a",
      "sel": [4, 1, 2, 3, 2],
      "rcut_smth": 0.50,
      "rcut": 6.00,
      "neuron": [10, 20, 40],
      "resnet_dt": false,
      "axis_neuron": 4,
      "seed": 1,
      "_comment": "that's all"
    },
    "fitting_net": {
      "neuron": [100, 100, 100],
      "resnet_dt": true,
      "seed": 1,
      "_comment": "that's all"
    },
    "_comment": "that's all"
  },

  "learning_rate": {
    "type": "exp",
    "decay_steps": 5000,
    "start_lr": 0.001,
    "stop_lr": 3.51e-8,
    "_comment": "that's all"
  },

  "loss": {
    "type": "ener",
    "start_pref_e": 0.02,
    "limit_pref_e": 1,
    "start_pref_f": 1000,
    "limit_pref_f": 1,
    "start_pref_v": 0,
    "limit_pref_v": 0,
    "_comment": "that's all"
  },

  "training": {
    "training_data": {
      "systems": ["../00.data/training_data"],
      "batch_size": "auto",
      "_comment": "that's all"
    },
    "validation_data": {
      "systems": ["../00.data/validation_data"],
      "batch_size": "auto",
      "numb_btch": 1,
      "_comment": "that's all"
    },
    "numb_steps": 10000,
    "seed": 10,
    "disp_file": "lcurve.out",
    "disp_freq": 1000,
    "save_freq": 10000,
    "_comment": "that's all"
  },

  "_comment": "that's all"
}
EOF

echo "All done."
