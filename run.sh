#!/bin/bash

# Run the Python scripts in order
python3 source/collect.py
python3 source/to.py
python3 source/rename.py
python3 source/reshape.py
python3 source/combine.py
python3 source/flat.py
python3 source/train_valid.py
python3 source/virial.py
rm -r combined_flat_data/ data/ output_steps/
# Create the 01.train folder
mkdir -p 01.train

# Write the input.json file
cat > 01.train/input.json << EOF
{
{
    "_comment": " model parameters",
    "model": {
	"type_map":	["H", "C"],
	"descriptor" :{
	    "type":		"se_e2_a",
	    "sel":		[4, 1],
	    "rcut_smth":	0.50,
	    "rcut":		6.00,
	    "neuron":		[10, 20, 40],
	    "resnet_dt":	false,
	    "axis_neuron":	4,
	    "seed":		1,
	    "_comment":		" that's all"
	},
	"fitting_net" : {
	    "neuron":		[100, 100, 100],
	    "resnet_dt":	true,
	    "seed":		1,
	    "_comment":		" that's all"
	},
	"_comment":	" that's all"
    },

    "learning_rate" :{
	"type":		"exp",
	"decay_steps":	5000,
	"start_lr":	0.001,	
	"stop_lr":	3.51e-8,
	"_comment":	"that's all"
    },

    "loss" :{
	"type":		"ener",
	"start_pref_e":	0.02,
	"limit_pref_e":	1,
	"start_pref_f":	1000,
	"limit_pref_f":	1,
	"start_pref_v":	0,
	"limit_pref_v":	0,
	"_comment":	" that's all"
    },

    "training" : {
	"training_data": {
	    "systems":		["../00.data/training_data"],
	    "batch_size":	"auto",
	    "_comment":		"that's all"
	},
	"validation_data":{
	    "systems":		["../00.data/validation_data"],
	    "batch_size":	"auto",
	    "numb_btch":	1,
	    "_comment":		"that's all"
	},
	"numb_steps":	10000,
	"seed":		10,
	"disp_file":	"lcurve.out",
	"disp_freq":	1000,
	"save_freq":	10000,
	"_comment":	"that's all"
    },    

    "_comment":		"that's all"
}

}
EOF
mkdir -p 02.lmp
cat > 02.lmp/conf.lmp << EOF
{
5 atoms
2 atom types
   0.0000000000   10.1142592220 xlo xhi
   0.0000000000   10.2631236420 ylo yhi
   0.0000000000   10.2167932840 zlo zhi
   0.0367498770    0.1383306230   -0.0563221690 xy xz yz

Atoms # atomic

     1      1    5.4513900000    4.3269700000    3.5664500000
     2      1    4.0585900000    4.9453900000    4.5274400000
     3      1    5.6173700000    5.7721300000    4.6488800000
     4      1    5.4695700000    4.1304600000    5.3741500000
     5      2    5.1628400000    4.7731400000    4.5439000000
}
EOF
cat > 02.lmp/in.lammps << EOF
{
units metal
atom_style atomic
boundary p p p

# --- Neighbor settings ---
neighbor 2.0 bin
neigh_modify one 5000 delay 0 every 1 check yes

# --- Read atomic configuration (defines box + atoms + types) ---
read_data conf.lmp

# --- Define masses *after* box is read ---
mass 1 15.9994   # O
mass 2 1.00794   # H

# --- Force field (DeepMD) ---
pair_style deepmd graph-compress.pb
pair_coeff * *

# --- Optional: Relax system before MD ---
minimize 1.0e-6 1.0e-8 1000 10000

# --- Velocity and MD setup ---
velocity all create 50.0 23456789
fix 1 all nvt temp 50.0 50.0 0.5
timestep 0.001

# --- Output ---
thermo_style custom step pe ke etotal temp press vol
thermo 100
dump 1 all custom 100 ch4.dump id type x y z

run 5000
}
EOF

echo "All done."
