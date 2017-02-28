# Parallel analysis in the MDAnalysis Library

We present a benchmark suite that can be used to evaluate performance for
parallel map-reduce type analysis and use it to investigate the performance of
[MDAnalysis](http://mdanalysis.org) with the [Dask](http://dask.pydata.org)
library for task-graph based computing [(Khoshlessan and Beckstein, 2017)][Khoshlessan2017]. A
range of commonly used MD file formats (CHARMM/NAMD DCD, Gromacs XTC, Amber
NetCDF) and different trajectory sizes are tested on different high-performance
computing (HPC) resources. Benchmarks are performed both on a single node and
across multiple nodes.

The the draft of the report including all data is available on figshare at DOI
[10.6084/m9.figshare.4695742][]; the report will be updated as necessary, which
will be recorded in the history on figshare. 


## Data files

The topology file (PSF format) and the trajectory (DCD) used for the benchmark
can be downloaded from dropbox 

* [adk4AKE.psf][]
* [1ake_007-nowater-core-dt240ps.dcd][]

Files in XTC and NetCDF formats are generated from the DCD.





## References

[Khoshlessan2017]: #Khoshlessan2017
<a name="Khoshlessan2017">Khoshlessan, Mahzad; Beckstein, Oliver
(2017)</a>: _Parallel analysis in the MDAnalysis Library: Benchmark of
Trajectory File Formats._ figshare. doi:[10.6084/m9.figshare.4695742][]


[10.6084/m9.figshare.4695742]: https://doi.org/10.6084/m9.figshare.4695742
[adk4AKE.psf]:    https://www.dropbox.com/sh/ln0klc9j7mhvxkg/AAAL5eP1vrn0tK-67qVDnKeua/Trajectories/equilibrium/adk4AKE.psf
[1ake_007-nowater-core-dt240ps.dcd]: https://www.dropbox.com/sh/ln0klc9j7mhvxkg/AABSaNJ0fRFgY1UfxIH_jWtka/Trajectories/equilibrium/1ake_007-nowater-core-dt240ps.dcd
