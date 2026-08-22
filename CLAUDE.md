# CLAUDE.md

This file is the persistent memory for this repository. Claude Code has no memory
across sessions — this file is the substitute. Read it in full before doing any
analysis, editing any notebook, or answering questions about the data.

---

## 1. How Claude Should Use This File (Memory Protocol)

**At the start of every session:**
- Read this entire file before touching any notebook, script, or CSV.
- Treat Section 5 ("Established Analytical Conventions") as settled unless the user
  explicitly asks to revisit a decision. Do not silently re-derive or second-guess
  choices logged there.

**During the session, when something new is learned** — a bug, a naming
inconsistency, a statistical decision, a modeling choice, a correction to a prior
assumption — add an entry to Section 7 ("Session Log") in this exact format:

```
- [YYYY-MM-DD] **Topic**: What was found. Why it matters. What to do about it going forward.
```

Rules for the log:
- One entry per learning. Keep each entry to 2–3 sentences — this is a reference log,
  not a narrative.
- Never delete or silently edit a past entry. If new evidence contradicts an old
  entry, add a new entry that explicitly says so (`Correction to 2026-05-02 entry: ...`)
  and leave the original in place. The user prefers transparent correction over quiet
  revision.
- Distinguish a durable decision (belongs in Section 5 once it stabilizes) from a
  one-off session note (stays in Section 7). If a Section 7 entry represents a
  standing convention that will apply to all future work, propose moving it into
  Section 5 and ask before doing so.
- Do not log routine execution details (ran a cell, fixed a typo, imported a
  package). Log things a future session would otherwise get wrong by guessing.

**Never store in this file:** raw data values, participant/animal identifiers beyond
what's already in the data dictionary, or anything not related to the analysis
pipeline itself.

---

## 2. Project Outline

**Research question:** How does amyloid pathology disrupt hippocampal CA1 function?
Comparing App^NL-G-F knock-in (NLGF) mice to wild-type (WT) littermates via in vivo
electrophysiology.

**Scope:** Spatial coding, theta oscillatory dynamics, theta-gamma phase-amplitude
coupling (PAC), and phase precession, recorded in two behavioral environments (open
field, linear track).

**Scale:** ~1,800 neurons across ~17 animals.

**Confound to always control for:** A second experimenter, Ruth, collected part of
the data. `Experimenter` (Loukia vs. Ruth) and `Age_weeks` are collinear (r = 0.76) —
see Section 5 for how this is handled statistically. Never include both as
simultaneous fixed effects in one model.

**Output target:** Manuscript for *Neuron* (Cell Press), ~7,000-word cap (excludes
STAR Methods and abstract), 8 main figures + 6 supplementary figures. See
`neuron_manuscript_outline.md` for the current word-budget-by-section structure.

---

## 3. Repository Structure

| File | Purpose |
|---|---|
| `ephys_openField_analysis.ipynb` | Open-field spatial firing analysis (rate maps, spatial info, coherence, sparsity, stability) |
| `ephys_PAC_comodulograms.ipynb` | Theta-gamma phase-amplitude coupling, comodulograms (pactools / DAR method) |
| `ephys_LT_PhasePrecession.ipynb` | Linear-track phase precession analysis |
| `ephys_phase_circular_analysis.ipynb` | Circular statistics on theta phase locking (pycircstat2, custom Watson U² fix) |
| `ephys_LinearTrack_analysis.ipynb` | Linear-track firing analysis (non-phase-precession metrics) |
| `ephys_confound_testing_glmm.ipynb` | Confound modeling (Experimenter / Age_weeks), core GLMM pipeline |
| `ephys_PAC_single_trials.ipynb` | Per-trial PAC/oscillatory-event metrics (normality checks, GEE) — separate from the comodulogram notebook |
| `ephys_openField_qc.ipynb` | Open-field QC: per-mouse summary tables, missingness/duplicate/outlier checks, Excel→Parquet caching |
| `neuron_manuscript_outline.md` | Section-by-section word allocation and figure mapping for the *Neuron* submission |
| `concatenated_trials.csv` | Per-cell/per-trial master dataset (1,838 rows × 36 cols) — spatial coding, theta modulation, PAC-adjacent per-cell metrics |
| `concatenated_phase_precession.csv` | Phase precession fits, per cell/direction (330 rows × 15 cols) — currently pseudoreplicated at the trial level, not animal-resolved |
| `concatenated_lfp_stats.csv` | Session-level LFP/PAC summary stats (34 rows × 21 cols) |
| `AllFiguresTogether.pdf` | Current compiled figure set (8 main + 6 supplementary) |

**⚠️ These data files are not in this git repo.** Notebooks load them via
hardcoded absolute paths into a Dropbox directory (e.g.
`.../Dropbox-UCL/Loukia Katsouri/DataProtocolsEquipment/Ephys_Analysis/RobinData/Analysis/...`),
not a repo-relative path. Before editing a load cell, check the path in that
specific notebook rather than assuming it matches another notebook's convention.

---

## 4. Data Dictionary Notes (read before writing any query)

**`concatenated_trials.csv`** — key columns: `mouse_name`, `Experimenter`,
`Age_weeks`, `Genotype`, `cell_type`, `theta_mod_v1/v2/v3`, `spatial_info`,
`coherence`, `field_size`, `spatial_sparsity`, `phase_locking_*`,
`half_split_stability`, `odd_even_stability`, `environment`.

**`concatenated_phase_precession.csv`** — `mouse_name` here is a **string**, not the
integer used elsewhere. `run_direction` is a repeated-measures identifier within a
cell, not a between-animal grouping variable — do not treat direction-level rows as
independent samples.

**`concatenated_lfp_stats.csv`** — session-level, one row per recording session, not
per cell.

**⚠️ Known trap:** `concatenated_lfp_stats.csv` uses the column name `Phenotype`,
while `concatenated_trials.csv` and `concatenated_phase_precession.csv` use
`Genotype`. Same variable, different name. This has caused repeated silent join/merge
errors — always check which file you're in before writing a filter or join key.

---

## 5. Established Analytical Conventions

These are settled decisions. Don't relitigate without an explicit prompt from the
user.

- **Unit of analysis:** GLMMs (animal as random effect) are primary. Neuron-level
  Mann-Whitney U is secondary/robustness. Report consistency between the two, not
  just one.
- **Pseudoreplication:** Cells are nested within animals. Never compare genotypes at
  the cell level without an animal-level random effect or animal-level aggregation.
  `mouse_name = concatenated_data` (i.e. unresolved animal grouping) is a known
  problem in the phase precession pipeline specifically — flag any phase precession
  result built on this as descriptive/preliminary until animal-resolved.
- **Confound handling:** `Experimenter` and `Age_weeks` are collinear (r = 0.76).
  Always fit three separate models — Experimenter alone, Age alone, both together —
  never both as simultaneous fixed effects in a single model used for inference.
- **Multiple comparisons:** BH-FDR correction is applied **per cell type**
  (Pyramidal, Interneuron separately), not pooled — they are biologically independent
  test families.
- **Permutation tests:** Use median-based permutation, not mean-based. There is an
  influential outlier NLGF animal that distorts mean-based tests.
- **GLMM family selection:** Empirical, via DHARMa residual diagnostics and Pearson
  overdispersion ratios — not assumed from theory. E.g. theta modulation index uses a
  log-shifted Gaussian (`theta_mod_v3_log`, shift +0.20) after ruling out Gamma and
  Yeo-Johnson alternatives.
- **`lmer` contrasts:** Defaults to treatment contrasts, which invalidates Type III
  ANOVA when interactions are present. Always set `contr.sum` explicitly before
  fitting.
- **Circular stats bug:** `watson_u2_test` in `pycircstat2` has confirmed bugs (shape
  mismatch for unequal n, negative rank errors). Use the custom drop-in replacement
  based on `scipy.stats.rankdata` — do not call the library function directly.
- **PAC asymmetry index — rejected:** The collaborator-proposed
  `(PAC_fast - PAC_slow) / (PAC_fast + PAC_slow)` is numerically unstable in NLGF
  sessions specifically (denominator → 0 as overall PAC drops). The existing mixed
  model's `Phenotype:gamma_band` interaction term already tests this question without
  the instability. Don't reintroduce the index without discussing this first.
- **Source-verify before citing:** Package docstrings can misstate the actual
  algorithm. `ephysiopy`'s `getAdaptiveMap()` stopping criterion and α parameter both
  differ from its own docstring *and* from the published Skaggs et al. (1996)
  formula. Always check implementation against source code, not documentation, before
  writing a methods description that cites a formula.

---

## 6. Tooling & Environment

- **No build, lint, or test suite.** There's no `requirements.txt`,
  `environment.yml`, or CI config in this repo — work happens by running cells
  in Jupyter directly. R runs inline per-cell through the `rpy2` bridge rather
  than as standalone scripts, so there is no separate R invocation to run.
- **Languages:** Python (Jupyter notebooks) + R via `rpy2` bridge.
- **R packages:** `glmmTMB`, `emmeans`, `DHARMa`, `afex`, `lmerTest`, `car`, `brms`,
  `cmdstanr`.
- **Python packages:** `ephysiopy` (`ephysiopy.common.ratemap`,
  `ephysiopy.common.phasecoding.LFPOscillations`), `pycircstat2` (with custom
  `watson_u2_test` fix), `pactools` (DAR method for PAC comodulograms), `pingouin`,
  `scipy`, `numpy`, `rpy2`.
- **Plotting:** Save outputs as PDF with `pdf.fonttype: 42` for Illustrator
  compatibility. Colors: WT = `#5B8DB8` (steel blue), NLGF = `#E07B54` (orange). WT
  is always ordered first on axes.
- **Key references:** Skaggs et al. (1996, *Hippocampus*) — adaptive binning;
  Guardamagna et al. (2023, *Cell Reports*) — Theta Score for
  phase-precessing/phase-locked classification; Tort et al. (2010) — KL-divergence
  MI; Duprêlatour et al. (2017, *PLOS Comp Bio*) — DAR-based PAC.

---

## 7. Session Log

*(Newest entries at the top. See Section 1 for the format and rules.)*

<!-- Add new entries below this line. -->
- [2026-08-22] **Spatial-cell GLMM result (open field)**: Binomial GLMM
  (`is_spatial ~ Genotype + (1|mouse_name)`, fit separately per cell type)
  shows NLGF Pyramidal cells significantly less likely to be spatial than WT
  (OR=0.347, p=0.020, n=719 cells/17 mice); Interneurons show the same
  direction but are not significant (OR=0.570, p=0.283, n=359 cells/17 mice).
  Not yet cross-checked against the median-based permutation test that
  Section 5 calls for as the robustness comparison — treat the Pyramidal
  result as preliminary until that check is run, since the notebook's own
  permutation-test cell flags an outlier NLGF mouse (1117201, 90% spatial)
  that drives the mean-based version of this same comparison.
- [2026-08-22] **Notebook kernel is missing packages needed to execute it**:
  `ephys_openField_analysis.ipynb` is registered against
  `/Users/loukia/miniconda3/bin/python` (base conda env), which lacks
  `seaborn` and `rpy2` — cells fail on import. The `scripts`, `scripts313`,
  and `RFCenv` conda envs all have both installed and point rpy2 at the same
  system R (`/Library/Frameworks/R.framework/Resources`, where `glmmTMB`
  works despite a TMB version-mismatch warning). Use one of those envs to
  actually run notebook code from the command line; don't assume the base
  env works.

---

## 8. Karpathy's Four Rules for AI-Assisted Analysis

Adapted from Andrej Karpathy's public observations on recurring LLM coding failure
modes (Jan 2026) — silent assumptions, overengineering, scope creep, and vague
success criteria — for a statistical analysis codebase rather than general software.
Source: [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills).

### Rule 1 — Think Before Coding
- Do not silently pick a statistical approach when more than one is defensible (test
  choice, model family, contrast coding, aggregation level). State the assumption and
  the alternative, and ask if it materially changes the conclusion.
- If a request is ambiguous about which dataset, environment, or cell type to use,
  say so and pick the most likely one explicitly rather than guessing quietly.
- If something in the data contradicts an established convention in Section 5, stop
  and flag it — don't quietly work around it.

### Rule 2 — Simplicity First
- Use the minimum statistical machinery that answers the question. Don't add a
  Bayesian model, a new robustness check, or a new package where the existing GLMM
  pipeline already answers it (see the PAC asymmetry index precedent in Section 5).
- No speculative generality — don't build a reusable framework for a one-off plot or
  a single figure's stats.

### Rule 3 — Surgical Changes
- Touch only the notebook, cell, or function the task requires. Don't refactor
  unrelated analysis code, rename columns, or "clean up" a script while doing
  something else.
- If you notice pre-existing dead code or an unrelated bug, mention it — don't fix it
  unless asked.
- Clean up only what your own change made unused or obsolete.

### Rule 4 — Goal-Driven Execution
- Before running an analysis, state what a successful result looks like (e.g. "DHARMa
  residuals pass dispersion test," "no rank-deficiency warning," "effect direction
  matches the neuron-level Mann-Whitney check"). Loop against that criterion rather
  than stopping at the first output.
- For manuscript text, the success criterion is usually: stays within the word
  budget for that subsection (Section 2 outline), states the implementation caveat if
  one exists (Section 5), and doesn't overstate preliminary results (e.g. phase
  precession) as confirmed.
