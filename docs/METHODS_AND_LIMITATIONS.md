# Methods and limitations of the retained files

The published article is the authority for the reported experimental setup and computational protocol. This repository organisation fixes documentation and access; it does not revise the published article or constitute an independent scientific audit of its entire workflow.

## Published and source-output discrepancy

The retained Lupeol final MM/GBSA output gives −10.75 kcal/mol; the article's narrative and Table 8 give −9.33. The three other endpoint means match. Table 8 headings print kJ/mol, while the narrative and source headers state kcal/mol. The published PDF and source outputs are preserved without edits or conversion. See [the comparison record](../data/PUBLISHED_SOURCE_COMPARISON.json). Identifying the correct Lupeol output version and resolving publication labelling requires author verification; file validation does not settle that question.

## What can be checked here

- Four final MM/GBSA output files include component means, propagated uncertainty, sample SD and SEM, with 501 complex frames stated in their headers. The source files distinguish the sample SD from propagated SD; they should not be interchanged.
- The ORCA input files specify B3LYP, D3, def2-SVP and geometry optimisation. Retained orbital energies, coordinates and cube grids support inspection of the saved DFT results; complete standard-output logs are not bundled.
- GROMACS/Grace trajectory series retain their original numeric values and metadata. Some retained time axes extend slightly beyond the article's nominal 125 ns; inspect the actual bounds reported by `inspect_data.py` before trimming or relabelling them.
- Files named `*_covar.xpm` identify themselves as **Covariance**, with an `nm^2` legend. They must not be presented automatically as dimensionless normalised DCCM matrices. The corresponding source grids are retained without relabelling or numerical conversion.

## What this deposit does not establish

An endpoint energy estimate is not a measured affinity, inhibitor potency or anti-virulence outcome. A low RMSD or an occupied PCA basin alone does not demonstrate pharmacological action. Isolated-ligand frontier orbitals and electrostatic potentials do not establish receptor charge transfer. The article's computational candidate descriptions need to be distinguished from experimental confirmation.

Full trajectories, starting configurations and complete production inputs are not deposited. Consequently, this cleanup cannot independently certify atom selections, periodic-boundary processing, simulation integration, convergence, screening-library completeness or ligand chemical identities. The published numerical results are preserved rather than silently recalculated. Current repository checks verify file integrity, parsability, source consistency and access.
