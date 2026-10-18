# Internalin H computational screening research

Research data and code accompanying the published article **Targeting a key virulence factor in Listeria monocytogenes: An in silico discovery and pharmacokinetic profiling of novel internalin H inhibitors**.

Ayush Kumar Dewangan, Usha Chouhan and Deedhiti Mistry. *In Silico Research in Biomedicine* **2** (2026), 100153. Published online 17 December 2025. [DOI and publisher article](https://doi.org/10.1016/j.insi.2025.100153) · [Unmodified published PDF](paper/published_paper.pdf).

The study combines virtual screening, pharmacokinetic predictions, reported 125 ns molecular dynamics, endpoint MM/GBSA and isolated-ligand DFT. The repository provides the retained numerical outputs and a reproducible way to inspect them. Computational rankings are not measurements of inhibitor potency or therapeutic efficacy.

## Start here

| Material | Location |
|---|---|
| Published paper and citation | [Paper information](paper/README.md) · [CITATION.cff](CITATION.cff) |
| Numerical trajectory series | [MD data](data/md/) |
| Four endpoint energy outputs | [MM/GBSA data](data/mmgbsa/) |
| ORCA inputs, coordinates and cube grids | [DFT data](data/dft/) |
| Retained interaction records | [Interaction data](data/interactions/) |
| Scientific scope and caveats | [Methods and limitations](docs/METHODS_AND_LIMITATIONS.md) |
| How to inspect and reproduce | [Reproducibility](docs/REPRODUCIBILITY.md) |
| File-by-file provenance | [Retained source map](data/provenance.json) |

## Reported endpoint estimates

| Compound as identified in the article | PubChem CID reported in the study | Published narrative, kcal/mol | Retained output, kcal/mol |
|---|---|---|---|
| Hederagenin analogue | 137633443 | −17.09 | −17.09 |
| Oleanolic acid analogue, control | 44575931 | −10.88 | −10.88 |
| Maslinic acid analogue | 163053220 | −9.65 | −9.65 |
| Lupeol analogue | 70626379 | **−9.33** | **−10.75** |

**Unresolved source discrepancy:** the retained Lupeol final output differs from the paper. The other three endpoint means match. The paper's Table 8 also prints kJ/mol in its column headings, whereas the narrative and retained outputs state kcal/mol. No value has been replaced or converted. See [the explicit comparison record](data/PUBLISHED_SOURCE_COMPARISON.json); the exact Lupeol output version and the unit labelling require author verification.

Hederagenin has the most negative estimate in both records. These are model-based rankings, not measurements of affinity, inhibitor potency or therapeutic efficacy. Complete uncertainty columns remain in the source files. A passing repository check confirms data integrity and disclosure of the known discrepancy; it does not resolve it scientifically.

## Target and software

The structural template is [PDB 1H6U](https://www.rcsb.org/structure/1H6U), the crystallographic fused N-terminal domains of Internalin H. The article reports AutoDock 4.2.6 for focused docking, AutoDock Vina 1.2.3 for screening, GROMACS 2025.3, AMBER99SB-ILDN protein parameters, GAFF ligand parameters and ORCA 5.0.4 with B3LYP-D3/def2-SVP. The retained ORCA inputs use B3LYP, D3 and def2-SVP. See the paper for the complete protocol.

## Run the repository checks

Python 3.10 or later; no external packages are needed for the data and integrity checks.

```sh
python scripts/inspect_data.py
python scripts/validate_repository.py
```

The source notebooks are retained with outputs cleared; their external paths, installations and missing production inputs still need adaptation. This is a curated companion research record, not a fully self-contained simulation workflow. Raw trajectories and full production inputs are not included and remain available from the author on reasonable request.

Duplicate figures, obsolete plotting variants, binary calculation caches, duplicate manuscripts and reviewer correspondence have been removed from the current tree. Earlier commits remain in Git history. No published paper text or numerical source values were revised during this organisation.

## Licence and attribution

The existing [MIT licence](LICENSE) is retained for repository code. The unmodified published PDF carries its own **CC BY-NC-ND 4.0** notice and is not relicensed under MIT; see [paper information](paper/README.md). Cite all three article authors when using the study.

Contact: Ayush Kumar Dewangan, ayushd9275@gmail.com.
