#!/bin/bash

#PBS -S /bin/bash
#PBS -o myjob.out
#PBS -e myjob.err
#PBS -l walltime=04:00:00
#PBS -l nodes=1:ppn=24
#PBS -q	normal
#PBS -m e

echo 'BS' > ../tmp  # Status: Runing Band Structure calculation

ulimit -s unlimited
csh
cd $PBS_O_WORKDIR
mpirun -hostfile $PBS_NODEFILE vasp-544-n > LOG

python vasprun2json.py

if [ -f rg2_raw_data_*.json ]
then
    echo 'F' > ../tmp
else
    echo 'ERROR' > ../tmp
fi

python ../check_state.py
