# NLGF Ephys AXONA Data

In vivo electrophysiology analysis of hippocampal CA1 activity in App^NL-G-F
knock-in (NLGF) mice vs. wild-type (WT) littermates, recorded with AXONA
tetrode systems. Covers spatial coding, theta oscillatory dynamics,
theta-gamma phase-amplitude coupling (PAC), and phase precession in two
behavioral environments (open field, linear track). Target output is a
manuscript for *Neuron* (Cell Press).

Scale: ~1,800 neurons across ~17 animals.

## Repository structure

| File | Purpose |
|---|---|
| `ephys_openField_analysis.ipynb` | Open-field spatial firing analysis (rate maps, spatial info, coherence, sparsity, stability) |
| `ephys_PAC_comodulograms.ipynb` | Theta-gamma phase-amplitude coupling, comodulograms (pactools / DAR method) |
| `ephys_LT_PhasePrecession.ipynb` | Linear-track phase precession analysis |
| `ephys_phase_circular_analysis.ipynb` | Circular statistics on theta phase locking (pycircstat2, custom Watson U² fix) |
| `ephys_LinearTrack_analysis.ipynb` | Linear-track firing analysis (non-phase-precession metrics) |
| `ephys_confound_testing_glmm.ipynb` | Confound modeling (Experimenter / Age_weeks), core GLMM pipeline |
| `ephys_PAC_single_trials.ipynb` | Per-trial PAC/oscillatory-event metrics (normality checks, GEE) |
| `ephys_openField_qc.ipynb` | Open-field QC: per-mouse summary tables, missingness/duplicate/outlier checks, Excel→Parquet caching |
| `figure_style.py` | Shared matplotlib/seaborn styling (rcParams, WT/NLGF colors, `set_panel_title`) — import and call `apply_style()` in any new notebook |
| `CLAUDE.md` | Analysis conventions, data dictionary, and session history for AI-assisted work in this repo |

## Data

Data files (`concatenated_trials.csv`, `concatenated_phase_precession.csv`,
`concatenated_lfp_stats.csv`, `AllFiguresTogether.pdf`, and per-notebook
output folders such as `OpenFieldAnalysis/` and `LinearTrackAnalysis/`) are
**not tracked in this repo**. Notebooks load them via hardcoded absolute
paths into a Dropbox directory:

```
.../Dropbox-UCL/Loukia Katsouri/DataProtocolsEquipment/Ephys_Analysis/RobinData/Analysis/...
```

Check the load cell in the specific notebook you're editing before assuming
a path — conventions differ slightly between notebooks (e.g. `OF_concat/`
vs `LT_concat/`).

## Environment

There's no `requirements.txt`, `environment.yml`, or CI config — work
happens by running cells directly in Jupyter.

- **Python**: `ephysiopy`, `pycircstat2`, `pactools`, `pingouin`, `scipy`,
  `numpy`, `seaborn`, `rpy2`.
- **R** (via the `rpy2` bridge, run inline per-cell rather than as standalone
  scripts): `glmmTMB`, `emmeans`, `DHARMa`, `afex`, `lmerTest`, `car`, `brms`,
  `cmdstanr`.
- Several conda envs on this machine (`scripts`, `scripts313`, `RFCenv`) have
  the full Python + rpy2 stack installed; the base conda env does not.

## Conventions

Statistical and plotting conventions (unit of analysis, confound handling,
multiple-comparisons correction, GLMM family selection, circular-stats bug
workarounds, figure styling, etc.) are documented in [`CLAUDE.md`](CLAUDE.md)
and should be treated as settled unless there's a specific reason to revisit
them.
