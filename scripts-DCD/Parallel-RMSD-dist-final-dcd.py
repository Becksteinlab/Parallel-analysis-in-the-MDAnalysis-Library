#!/usr/bin/env python
from __future__ import print_function, division
import sys
import numpy as np
import MDAnalysis as mda
import dask
from dask.delayed import delayed
from dask import multiprocessing
from dask.multiprocessing import get
from MDAnalysis.analysis.align import rotation_matrix
from MDAnalysis.core.qcprot import CalcRMSDRotationalMatrix
import time
from shutil import copyfile
import glob, os
from dask.distributed import Client
from MDAnalysis import Writer

Scheduler_IP = sys.argv[1]
#SLURM_JOBID = sys.argv[2]
print (Scheduler_IP)
print (type (Scheduler_IP))
#print (Client(Scheduler_IP))
c = Client(Scheduler_IP)
print (mda.__version__) 

DCD1 = os.path.abspath(os.path.normpath(os.path.join(os.getcwd(),'1ake_007-nowater-core-dt240ps.dcd'))) 
PSF = os.path.abspath(os.path.normpath(os.path.join(os.getcwd(),'adk4AKE.psf')))
# Check the files in the directory
filenames = os.listdir(os.getcwd())
print (filenames)

def rmsd(mobile, xref0):
    # """Calculate optimal RMSD for AtomGroup *mobile* onto the coordinates *xref0* centered at the orgin.
    #The coordinates are not changed. No mass weighting.
    # 738 us
    xmobile0 = mobile.positions - mobile.center_of_mass()
    return CalcRMSDRotationalMatrix(xref0.T.astype(np.float64), xmobile0.T.astype(np.float64),mobile.n_atoms, None, None)

def block_rmsd(index, topology, trajectory, xref0, start=None, stop=None, step=None):
    clone = mda.Universe(topology, trajectory)
    g = clone.atoms[index]
    
    print("block_rmsd", start, stop, step)
    
    bsize = stop-start
    results = np.zeros([bsize,2])
    t_comp = np.zeros(bsize)
    
    start1 = time.time()
    for iframe, ts in enumerate(clone.trajectory[start:stop:step]):
        start2 = time.time()
        results[iframe, :] = ts.time, rmsd(g, xref0)
        t_comp[iframe] = time.time()-start2

    t_all_frame = time.time()-start1
    t_comp_final = np.mean(t_comp)    

    return results, t_comp_final, t_all_frame

def com_parallel_dask_distributed(ag, index, n_blocks):
    topology, trajectory = ag.universe.filename, ag.universe.trajectory.filename
    ref0 = ag.universe.select_atoms("protein")  
    xref0 = ref0.positions-ref0.center_of_mass()
    bsize = int(np.ceil(ag.universe.trajectory.n_frames / float(n_blocks)))
    print("setting up {} blocks with {} frames each".format(n_blocks, bsize))

    blocks = []
    t_comp = []
    t_all_frame = []

    for iblock in range(n_blocks):
        start, stop, step = iblock*bsize, (iblock+1)*bsize, 1
        print("dask setting up block trajectory[{}:{}]".format(start, stop))
        
        out = delayed(block_rmsd, pure=True)(index, topology, trajectory, xref0, start=start, stop=stop, step=step)   
        
        blocks.append (out[0])
        t_comp.append (out[1])
        t_all_frame.append (out[2])

    total = delayed(np.vstack)(blocks)
    t_comp_avg = delayed(np.sum)(t_comp)/n_blocks
    t_comp_max = delayed(np.max)(t_comp)
    t_all_frame_avg = delayed(np.sum)(t_all_frame)/n_blocks
    t_all_frame_max = delayed(np.max)(t_all_frame)

    return total, t_comp_avg, t_comp_max, t_all_frame_avg, t_all_frame_max


with open('data.txt', mode='w') as file:
    traj_size = [100,300,600]
    for k in traj_size: # we have 3 trajectory sizes
        # Creating the universe for doing benchmark
        u1 = mda.Universe(PSF, DCD1) 
        longDCD = 'newtraj.dcd'        

        # Creating big trajectory sizes from initial trajectory
        with mda.Writer(longDCD, u1.atoms.n_atoms) as W:
             for i in range (k):
                for ts in u1.trajectory:
                    W.write(u1)        
        u = mda.Universe(PSF, longDCD)


        # Doing benchmarks
        ii=1
        block_size = [1,6,8,12,18,24,30,36,42,48,54,60,66,72]
        for i in block_size:      # changing blocks
            for j in range(1,6):    # changing files (5 files per block size)
                # Create a new file
                longDCD1 = 'newtraj{}.dcd'.format(ii)
                copyfile(longDCD, longDCD1)
                # Provide the path to my file to all processes 
                my_path = os.path.normpath(os.path.join(os.getcwd(), longDCD1))
                print (my_path)
                longDCD1 = os.path.abspath(my_path)
                # Define a new universe with the new trajectory
                u = mda.Universe(PSF, longDCD1)
		print(u)
                print("frames in trajectory ", u.trajectory.n_frames)
                print (len(u.trajectory))
                mobile = u.select_atoms("(resid 1:29 or resid 60:121 or resid 160:214) and name CA")
                index = mobile.indices
                total = com_parallel_dask_distributed(mobile, index, i)
                total = delayed (total)
		start = time.time()
                output = total.compute(get=c.get)
                tot_time = time.time()-start
                file.write("XTC{} {} {} {} {} {} {} {}\n".format(k, i, j, output [1], output [2], output [3], output [4], tot_time))  
                file.flush() 
                # Deleting all files
                os.remove('newtraj{}.xtc'.format(ii))
                ii = ii+1    

