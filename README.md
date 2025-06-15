# QE_to_DeePMD

This repository provides a full pipeline to convert Quantum ESPRESSO (QE) VC-Relax output into DeepMD-kit training data. This basic process helps those who have started learning DeepMD from QE, as training data can be hard to find for beginners.


## 🚀 Working Process

1. Download the zip file from this repository.  
2. Copy your Quantum ESPRESSO VC-Relax output file into the `QE_to_DeepMD` folder.  
3. Rename the VC-Relax output file as `opt.out`.  
4. Run the `run.sh` script to process the data.  
5. Modify the `input.json` file inside the `01.train` folder according to your system before training.  
6. You’re good to go!  

---
 
