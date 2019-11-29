#!/bin/bash

#PBS -S /bin/bash
#PBS -o myjob.out
#PBS -e myjob.err
#PBS -l walltime=08:00:00
#PBS -l nodes=1:ppn=24
#PBS -q	normal
#PBS -m e

ulimit -s unlimited
csh
cd $PBS_O_WORKDIR

RELAX_NORMALLY=FALSE
num_relax_times=1

echo 'R' > tmp  # status: Relaxiation
python check_state.py
# Judge if relaxed
while [[ $num_relax_times -le 6 ]]
do
	mpirun -hostfile $PBS_NODEFILE vasp-544-n > LOG
	num_lines=$( grep F OSZICAR | wc -l )
	
	if [ $num_lines -eq 1 ]
	then
        echo $(num_lines)
        # echo 'Relaxed!'
        RELAX_NORMALLY=TRUE
        break
    else
        # echo 'NOT Relaxed!'
        cp CONTCAR POSCAR
        echo $(num_relax_times)
        num_relax_times=$((num_relax_times+1))
    fi
done

if [ $RELAX_NORMALLY ]
then
    cp POSCAR run.sh POTCAR bandStructure/
    cd ./bandStructure/
    python gen_incar_and_hs_kpoints.py
    # qsub -N bs bs.sh # this command doesn't work due to it's not on the mu node
    mpirun -hostfile $PBS_NODEFILE vasp-544-n > LOG
    echo 'Q' > ../tmp # Status: Queuing for band structure calculation
    python ../check_state.py
else
    #record error message and return to the root script
    echo 'ERROR' > tmp # Status: Error
    python check_state.py
fi
