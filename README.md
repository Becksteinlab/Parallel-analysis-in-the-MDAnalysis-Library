# Parallel-analysis-in-the-MDAnalysis-Library
We present a benchmark suite that can be used to evaluate performance for parallel map-reduce type analysis and use it to investigate the performance of MDAnalysis with the Dask library for task-graph based computing. A range of commonly used MD file formats (CHARMM/NAMD DCD, Gromacs XTC, Amber NetCDF) and different trajectory sizes are tested on different high-performance computing (HPC) resources. Benchmarks are performed both on a single node and across multiple nodes.

# Topology & Trajectory used for the benchmark can be downloaded from the following links:
download_files = ["https://www.dropbox.com/sh/ln0klc9j7mhvxkg/AAAL5eP1vrn0tK-67qVDnKeua/Trajectories/equilibrium/adk4AKE.psf",
                 "https://www.dropbox.com/sh/ln0klc9j7mhvxkg/AABSaNJ0fRFgY1UfxIH_jWtka/Trajectories/equilibrium/1ake_007-nowater-core-dt240ps.dcd"]


# Here are the citation and link to the draft of our report (The report is a bit long but it contains all of our data):
Khoshlessan, Mahzad; Beckstein, Oliver (2017): Parallel analysis in the MDAnalysis Library: Benchmark of Trajectory File Formats. figshare.
https://doi.org/10.6084/m9.figshare.4695742 


