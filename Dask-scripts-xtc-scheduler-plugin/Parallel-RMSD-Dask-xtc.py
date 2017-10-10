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
from distributed.diagnostics.plugin import SchedulerPlugin
from MDAnalysis import Writer
import pandas as pd

def submitCustomProfiler(profname,dask_scheduler):
    prof = MyProfiler(profname)
    dask_scheduler.add_plugin(prof)

def removeCustomProfiler(dask_scheduler):
    dask_scheduler.remove_plugin(dask_scheduler.plugins[-1])

class MyProfiler(SchedulerPlugin):
    def __init__(self,profname):
        self.profile = profname

    def transition(self,key,start,finish,*args,**kargs):
        if start == 'processing' and finish == 'memory':
            with open(self.profile,'a') as ProFile:
                ProFile.write('{}\n'.format([key,start,finish,kargs['worker'],kargs['thread'],kargs['startstops']]))

Scheduler_IP = sys.argv[1]
#SLURM_JOBID = sys.argv[2]
print (Scheduler_IP)
print (type (Scheduler_IP))
c = Client(Scheduler_IP)
print (mda.__version__)

DCD1 = os.path.abspath(os.path.normpath(os.path.join(os.getcwd(),'files/1ake_007-nowater-core-dt240ps.dcd')))
PSF = os.path.abspath(os.path.normpath(os.path.join(os.getcwd(),'files/adk4AKE.psf')))
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
    task_start = time.time()
    clone = mda.Universe(topology, trajectory)
    g = clone.atoms[index]

    print("block_rmsd", start, stop, step)

    bsize = stop-start
    results = np.zeros([bsize,2])
    t_comp = np.zeros(bsize)
    t_IO = np.zeros(bsize)

    start1 = time.time()
    start0 = start1
    for iframe, ts in enumerate(clone.trajectory[start:stop:step]):
        start2 = time.time()
        results[iframe, :] = ts.time, rmsd(g, xref0)
        t_comp[iframe] = time.time()-start2
        t_IO[iframe] = start2-start1
        start1 = time.time()

    t_all_frame = time.time()-start0
    t_comp_final = np.mean(t_comp)
    t_IO_final = np.mean(t_comp)
    task_end = time.time()

    return results, t_comp_final, t_IO_final, t_all_frame, task_start, task_end

def com_parallel_dask_distributed(ag, index, n_blocks):
    topology, trajectory = ag.universe.filename, ag.universe.trajectory.filename
    ref0 = ag.universe.select_atoms("protein")
    xref0 = ref0.positions-ref0.center_of_mass()
    bsize = int(np.ceil(ag.universe.trajectory.n_frames / float(n_blocks)))
    print("setting up {} blocks with {} frames each".format(n_blocks, bsize))

    blocks = []
    t_comp = []
    t_IO = []
    t_all_frame = []
    block_rmsd_start = []
    block_rmsd_end = []

    for iblock in range(n_blocks):
        start, stop, step = iblock*bsize, (iblock+1)*bsize, 1
        print("dask setting up block trajectory[{}:{}]".format(start, stop))

        out = delayed(block_rmsd, pure=True)(index, topology, trajectory, xref0, start=start, stop=stop, step=step)

        blocks.append (out[0])
        t_comp.append (out[1])
        t_IO.append (out[2])
        t_all_frame.append (out[3])
        block_rmsd_start.append(out[4])
        block_rmsd_end.append(out[5])

    total = delayed(np.vstack)(blocks)
    t_comp = delayed(np.vstack)(t_comp)
    t_IO = delayed(np.vstack)(t_IO)
    t_all_frame = delayed(np.vstack)(t_all_frame)

    return total, t_comp, t_IO, t_all_frame, block_rmsd_start, block_rmsd_end


with open('data.txt', mode='a') as file:
    traj_size = [600]
    for k in traj_size: # we have 3 trajectory sizes
        # Creating the universe for doing benchmark
        u1 = mda.Universe(PSF, DCD1)
    
        longXTC = os.path.abspath(os.path.normpath(os.path.join(os.getcwd(),'files/newtraj.xtc')))

        # Doing benchmarks
        ii=1
        block_size = [1 6 12 18 24 30 36 42 48 54 60 66 72]
        for i in block_size:      # changing blocks
            for j in range(1,6):    # changing files (5 files per block size)
                # Create a new filei
                c.run_on_scheduler(submitCustomProfiler,os.path.abspath(os.path.normpath(os.path.join(os.getcwd(),'files/XTC_{}_{}_{}.txt'.format(k,i,j)))))
                longXTC1 = os.path.abspath(os.path.normpath(os.path.join(os.getcwd(),'files/newtraj{}.xtc'.format(ii))))
                copyfile(longXTC, longXTC1)
                # Provide the path to my file to all processes
                my_path = os.path.normpath(os.path.join(os.getcwd(), longXTC1))
                longXTC1 = os.path.abspath(my_path)
                # Define a new universe with the new trajectory
                u = mda.Universe(PSF, longXTC1)
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
                output_time = (np.tile([i,j],(i,1)),) + output[1:4]
                output_time_f = np.hstack(output_time)
                pd.DataFrame(output_time_f).to_csv(file)
                c.run_on_scheduler(removeCustomProfiler)
                np.save('files/XTC{}_{}_{}.npz.npy'.format(k,i,j),[output[4],output[5]])
                # Deleting all files
                os.remove(os.path.abspath(os.path.normpath(os.path.join(os.getcwd(),'files/newtraj{}.xtc'.format(ii)))))
                ii = ii+1
