## Automatically generate vasp inputs files based on RG2 structure

#### Description:
RG2 program (see more info [here](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.97.014104)) can generate crystal
structures based on graph theory. These structures may not be very stable, but are possible phases, so it's very useful 
for phase searching.

Our purpose is to use the RG2 program to generate more crystal structures within certain
space group range (here, we first study cubic crystal system, where space group range is 195-230). And with these structures, 
automatically generate [VASP](https://cms.mpi.univie.ac.at/wiki/index.php/The_VASP_Manual) input files (INCAR, KPOINTS, POSCAR, POTCAR)
and run the calculation.

The calculation contains structure relaxation, and band structure calculation along certain high symmetry path.

#### Folder trees:
```angular2
├── out/    # place the generated structures here
├── rg2_cubic/    # this directory and the child directories will be created by script
|       ├── sg_195/    # sg stands for space group, sort based on space group
|       ├── sg_196/
|       ├── ...
|       └── sg_230/
|
├── scripts/  # place all the scripts that will be copied to each structure directory
|       ├── relax.sh    # main shell script that will be submitted to other nodes, contains relaxation and band structure calculation
|       ├── gen_incar_and_hs_kpoints.py    # for band structure calculation use
|       ├── check_state.py   # Show current job state ((W, R, BS, Q, F, ERROR), easy to trace the job path. See the script for detail
|       └── vasprun2json.py  # record the calculated bands results into .json file
|
├── structure_from_rg2.py    # contain the class which is the rg2_structure info from RG2
├── rg2_data_processing.py   # main script, will create folders and copy .vasp structures to each sub directory, and record other info
├── tools.py    # some tools for initializing rg2_structure class 
├── batch_job_controller.py  # submit batch jobs at a time
├── elements_map.json    # contain elements map for POTCAR gerneration use
└── rg2_data_info_dict.json    # record the structure info here, will be automatically generated
```

### Environments:

Python version: >= 3.0

[Pymatgen](https://pymatgen.org/#getting-pymatgen) version: v2019.11.11(suggested, very old verison may casue bugs)

[VASP](https://cms.mpi.univie.ac.at/marsweb/) version: vasp-544-n (You can set your own version in /scripts/relax.sh)

Portable Batch System (PBS): using PBS for job scheduling 

### Usage Instruction:

More to come...
