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
├── structure_from_rg2.py    # contain the class which is the rg2_structure info from RG2
├── rg2_data_processing.py   # main script, will create folders and copy .vasp structures to each sub directory, and record other info
├── tools.py    # some tools for initializing rg2_structure class
├── gen_incar_and_hs_kpoints.py    # for band structure calculation use
├── elements_map.json    # contain elements map for POTCAR gerneration use
└── rg2_data_info_dict.json    # record the structure info here, will be automatically generated
```

####TODOS:

More to come...
### NOT FINISHED, TBC...