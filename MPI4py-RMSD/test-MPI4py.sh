#!/bin/bash

#SBATCH -J parallel_RMSD_XTC             # Job name
#SBATCH -o slurm.%j.out                  # STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err                  # STDERR (%j = JobId)
#SBATCH --partition=compute
# #SBATCH --constraint="large_scratch"
#SBATCH --nodes=3                        # Total number of nodes requested (16 cores/node). You may delete this line if wanted
#SBATCH --ntasks-per-node=24             # Total number of mpi tasks requested
#SBATCH --export=ALL
#SBATCH -t 20:00:00                      # wall time (D-HH:MM)
#SBATCH --mail-user=mkhoshle@asu.edu     # email address
#SBATCH --mail-type=all                  # type of mail to send

#The next line is required if the user has more than one project
# #SBATCH -A A-yourproject # <-- Allocation name to charge job against

#module purge
#module load intel 
#module load openmpi_ib
# Private conda environment
#source activate openmpi

hostnodes=`scontrol show hostnames $SLURM_NODELIST`
echo $hostnodes

SCHEDULER=`hostname`
echo SCHEDULER: $SCHEDULER

#export MV2_SHOW_CPU_BINDING=1

my_file=main2
#my_file=test

#6 12 18 24 30 36 42 48 54 60 66 72
for kk in 1 6 12 18 24 30 36 42 48 54 60 66 72; do
    echo "Working on $kk ...."
    mkdir files_striped
    lfs setstripe -c $kk ./files_striped
    cp -a files/. files_striped
    for jj in {1..5}; do
	lfs getstripe ./files_striped
#        mpirun --report-bindings -np $kk $SLURM_SUBMIT_DIR/$my_file.py $jj # 2>error.txt
        mpirun -np $kk $SLURM_SUBMIT_DIR/$my_file.py $jj
    done
    rm -rf files_striped
done


