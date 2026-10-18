# Inspecting the deposited InlH data

Clone or download the repository. Python 3.10 or later is sufficient for the following commands:

```sh
python scripts/inspect_data.py
python scripts/validate_repository.py
```

`inspect_data.py` reads the retained XVG/Grace numeric series, XPM grid dimensions, final MM/GBSA components and frontier-orbital energies. It prints a JSON summary without modifying any source file. Use `--output summary.json` to save the inspection result. The command does not run simulations or download inputs.

`validate_repository.py` checks every manifest checksum, four endpoint estimates, source-file mappings, local Markdown links, notebook outputs and exclusion of raw trajectories and reviewer correspondence. GitHub Actions runs the same check on pushes.

## Source notebooks

The notebooks retain the original scientific source cells with execution outputs and execution counters cleared. They are provenance and starting points for adapting the original Colab workflow. Their external-drive paths, package installations and production inputs require review before execution. No notebook was rerun as part of this cleanup. A complete environment lockfile and full raw trajectories are not supplied, so this deposit does not promise one-command reproduction of the full study.

## Data organisation

`data/md/` contains the original numeric series and PCA/covariance grids. `data/mmgbsa/` contains one final output per system. `data/dft/` contains the retained inputs, coordinates, property files, orbital energies and cube grids. `data/interactions/` contains the saved contact tables. `data/provenance.json` maps original file paths to the single retained copy. `MANIFEST.json` records current file SHA-256 checksums.

See [methods and limitations](METHODS_AND_LIMITATIONS.md) before interpreting the covariance maps or comparing uncertainty columns. The paper PDF is unchanged; the DOI is the permanent article identifier.
