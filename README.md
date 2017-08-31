# Parallel analysis in the MDAnalysis Library

We present a benchmark suite that can be used to evaluate performance for
parallel map-reduce type analysis and use it to investigate the performance of
[MDAnalysis][] with the [Dask][] library for task-graph based computing 
[(Khoslessan et al, 2017)][KhoshlessanScipy2017].

A range of commonly used MD file formats (CHARMM/NAMD DCD, Gromacs XTC, Amber NetCDF) and different
trajectory sizes are tested on different high-performance computing (HPC)
resources. Benchmarks are performed both on a single node and across multiple
nodes.

For space reasons, not all data could be shown in the SciPy 2017 conference proceedings
paper. For a full analysis see the Technical Report [(Khoshlessan and Beckstein, 2017)][Khoshlessan2017].
The report is available on figshare at DOI [10.6084/m9.figshare.4695742][].


## Supplementary information for SciPy 2017 paper
This repository should be considered part of the Supplementary information to the SciPy 2017 Proceedings
paper [(Khoslessan et al, 2017)][KhoshlessanScipy2017].

### Benchmarking code

The repository contain the code to benchmark parallelization of [MDAnalysis][]:
* RMSD calculation with MDAnalysis with Dask for XTC, DCD, NCDF
* RMSD calculation with MDAnalysis with MPI

### Data files

The data files consist of a topology file `adk4AKE.psf` (in CHARMM PSF format; N = 3341 atoms) 
and a trajectory `1ake_007-nowater-core-dt240ps.dcd` (DCD format) of length 1.004 μs with 
4187 frames; both are freely available under the CC-BY license from figshare at DOI [10.6084/m9.figshare.5108170][] 

Files in XTC and NetCDF formats are generated from the DCD.

## Tested libraries

* [MDAnalysis][] 0.15.0
* [Dask][] 0.12.0 (also 0.13.0)
* [Distributed][] 1.14.3 (also 1.15.1)
* [NumPy][] 1.11.2 (also 1.12.0)

## Comments and Questions

Please raise issues in the [issue tracker][] or ask on the
[MDAnalysis developer mailing list][].


## References

[KhoshlessanScipy2017]: #KhoshlessanScipy2017
<a name="KhoshlessanScipy2017">M. Khoshlessan, I. Paraskevakos, S. Jha, and O. Beckstein (2017)</a>. 
[_Parallel analysis in MDAnalysis using the Dask parallel computing library_](http://conference.scipy.org/proceedings/scipy2017/mahzad_khoslessan.html).
In S. Benthall and S. Rostrup, editors, Proceedings of the 16th Python in Science Conference, Austin, TX, 2017. SciPy. 
   
[Khoshlessan2017]: #Khoshlessan2017
<a name="Khoshlessan2017">Khoshlessan, Mahzad; Beckstein, Oliver (2017)</a>: _Parallel analysis in the MDAnalysis Library: Benchmark of
Trajectory File Formats._ Technical report, Arizona State University, Tempe, AZ, 2017. figshare. doi:[10.6084/m9.figshare.4695742][]


[MDAnalysis]: http://mdanalysis.org
[Dask]: http://dask.pydata.org
[Distributed]: https://distributed.readthedocs.io/
[NumPy]: http://numpy.scipy.org/
[issue tracker]: https://github.com/Becksteinlab/Parallel-analysis-in-the-MDAnalysis-Library/issues
[MDAnalysis developer mailing list]: http://developers.mdanalysis.org/
[10.6084/m9.figshare.4695742]: https://doi.org/10.6084/m9.figshare.4695742
[10.6084/m9.figshare.5108170]: https://doi.org/10.6084/m9.figshare.5108170


[adk4AKE.psf]:    https://www.dropbox.com/sh/ln0klc9j7mhvxkg/AAAL5eP1vrn0tK-67qVDnKeua/Trajectories/equilibrium/adk4AKE.psf
[1ake_007-nowater-core-dt240ps.dcd]: https://www.dropbox.com/sh/ln0klc9j7mhvxkg/AABSaNJ0fRFgY1UfxIH_jWtka/Trajectories/equilibrium/1ake_007-nowater-core-dt240ps.dcd
