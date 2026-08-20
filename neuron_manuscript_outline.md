# Manuscript Outline — Neuron Research Article
**Target: ≤7,000 words (main text + main figure legends), ≤8 figures, 150-word abstract (separate cap)**
**Mapped to `AllFiguresTogether.pdf` (6 main + 6 supplementary) + 2 pending figures**

---

## Figure inventory (as it stands)

**Main (existing, 6):**
1. Figure1_FiringMetrics — spike-width GMM classification, cell-type composition, peak/mean firing rate
2. Figure2_PlaceFields — spatial info, field size, sparsity, cell stability
3. Figure3_PhaseCoding — phase variance, theta modulation index, preferred phase, phase locking
4. Figure4_PhasePrecession — precessing-cell proportions, slope/rho (preliminary)
5. Figure5_LFP — theta frequency vs. running speed coupling (OF + LT)
6. Figure6_comod — theta-gamma comodulograms, modulation index (OF + LT)

**Main (new, pending, 2):**
7. **AHP (patch-clamp, collaborator)** — decreased slow AHP in NLGF; single-cell mechanistic correlate of the network-level theta/PAC deficits
8. **Amyloid–metric correlations (not yet done)** — plaque load/density vs. PAC, phase-locking, spatial coding metrics; the piece that would tie pathology burden directly to physiology

→ **8 main figures total — at the cap.** Nothing needs to be cut.

**Supplementary (6, legends excluded from word count):**
S1 Behavioural · S2 ClassifierPyrINs · S3 FiringMetricsLT · S4 SpatialShuffle · S5 PlaceCellsLT · S6 comod (LT)

The supplementary set already carries the replication/robustness burden (LT versions of firing metrics, place cells, PAC; classifier validation; spatial shuffle controls) — so the main-text figures are free to each carry one clean story without hedging in-panel.

---

## Abstract — 150 words (separate cap, not counted in 7,000)
- 1 sentence: disease framing (amyloid pathology, CA1 dysfunction)
- 1–2 sentences: approach (in vivo ephys + patch-clamp + histology, NLGF vs WT, OF + LT, ~1,800 units/17 animals)
- 3–4 sentences: key findings — theta-gamma PAC reduction across both bands, phase-locking impairment, decreased slow AHP as a cellular correlate, [plaque correlation result once available]
- 1 sentence: significance — converging network/cellular/pathology evidence for a theta-pacing deficit

---

## Introduction — 750 words (~11%)
- Amyloid pathology and hippocampal circuit dysfunction in AD models (150 words)
- CA1 as a convergence point: theta oscillations, gamma coupling, spatial coding (200 words)
- Gap: prior work isolates single levels (network oscillations *or* cellular physiology *or* pathology burden) rather than linking them (250 words)
- Study overview: multi-level dataset — extracellular ephys, patch-clamp, histology — testing whether a single theta-pacing/CA1 integration deficit explains findings across levels (150 words)

---

## Results — 3,650 words (~52%)

| Subsection | Figure | Words | Content |
|---|---|---|---|
| Cell-type classification & firing properties | Fig 1 | 500 | GMM spike-width classification; composition; peak/mean rate (GLMM, three-model Experimenter/Age check) |
| Spatial coding | Fig 2 | 500 | Spatial info, coherence, field size, sparsity, stability across genotype × cell type |
| Phase-locking / theta coupling | Fig 3 | 550 | Phase variance, theta modulation index, preferred phase — pyramidal impairment |
| Phase precession (preliminary) | Fig 4 | 300 | Descriptive only; flag low NLGF n and `mouse_name`-as-`concatenated_data` pseudoreplication directly in-text |
| Theta–running speed coupling | Fig 5 | 400 | Frequency-speed regression by genotype, OF + LT |
| Theta-gamma PAC | Fig 6 | 600 | Comodulograms; GLMM interaction (uniform reduction, no band×genotype interaction); anomalous slow-gamma/beta peak flagged descriptively |
| **Slow AHP (patch-clamp)** | Fig 7 | 450 | Collaborator's finding: decreased slow AHP in NLGF pyramidal cells; framed as candidate single-cell mechanism (reduced sAHP → altered spike-timing precision → downstream network PAC/phase-locking deficits) |
| **Amyloid–physiology correlations** | Fig 8 | 350 | Placeholder — plaque density/load regressed against PAC, phase-locking, spatial metrics; word count assumes a clean dose-relationship result. *Revisit once data exist — a null or noisy result needs different framing (see note below)* |

---

## Discussion — 1,350 words (~19%)
- Integration across levels: network (PAC, phase-locking) → cellular (sAHP) → pathology (plaque correlation) as one theta-pacing/CA1 integration story (350 words)
- Biological interpretation of PAC (MEC layer III → fast gamma; CA3 Schaffer collaterals → slow gamma; medial septum as pacemaker not generator) tied to the sAHP finding — intrinsic excitability change as a plausible upstream driver (350 words)
- Relationship between phase-locking/spatial coding deficits and amyloid burden — how directly the correlation figure does or doesn't support causality (200 words)
- Limitations: phase precession pseudoreplication, Experimenter/Age collinearity, cross-sectional design, patch-clamp and imaging from a separate collaborator (different N, different animals — state this explicitly) (300 words)
- Future directions: resolving phase precession with more animals, theta-peak-frequency cross-reference for the PAC anomaly (150 words)

---

## Figure Legends — 950 words (~14%, counted in the 7,000)
- ~120 words average × 8 main figures
- Each: orient (what/where) → panels → stats (test, n, correction) → direction of effect
- Fig 7/8 legends should state data provenance plainly (patch-clamp: collaborator, separate cohort; histology: pending) since these differ methodologically from the extracellular dataset

---

## STAR Methods — *excluded from word count*
Free to be thorough here:
- Animals, surgery, recording (NLGF/WT, environments)
- Spike sorting, GMM cell-type classification criteria
- GLMM specifications: `glmmTMB` model families per metric (Gamma, Negative Binomial, Beta-logit, log-shifted Gaussian, von Mises via `brms`)
- Three-model collinearity approach (Experimenter alone / Age alone / both)
- BH-FDR correction (per cell type, Python `multipletests`)
- Robustness checks: Mann-Whitney U, animal-level permutation tests (20,000 perms, seed=42)
- PAC: `pactools` DAR method, comodulogram construction
- Circular statistics: custom Watson U² (rankdata-based), `pycircstat2` caveat noted
- Key Resources Table (required by Cell Press STAR format)

---

## Running total check
150 (abstract, separate) + 750 (Intro) + 3,650 (Results) + 1,350 (Discussion) + 950 (Legends) = **6,700 words** in the 7,000 cap — leaves ~300-word buffer, useful given two figures are still in progress.

---

## Open decisions to lock before drafting
1. **Amyloid correlation figure is not yet done** — the 350-word Results allocation and Discussion framing above assume a positive dose-relationship. If the result turns out null, weak, or noisy once the data exist, the outline needs a second pass: a null result belongs in Results as a stated non-finding (don't inflate word count trying to explain it away) and shifts Discussion weight toward limitations rather than mechanism. Flag this now so it isn't quietly reframed later.
2. **Patch-clamp AHP figure comes from a different cohort/method** — decide early how prominently to state the N and whether it's the same animals as the extracellular recordings or a separate group; this affects how strongly Fig 7 can be linked causally to Figs 3/6 in the Discussion.
3. **Order of Figs 7–8 relative to 1–6**: current draft puts network-level findings first, then cellular (AHP), then pathology (plaque) — a bottom-up alternative (pathology → cellular → network) is also defensible; worth deciding based on which framing the Introduction sets up.
4. **Phase precession framing**: confirm Discussion explicitly states the pseudoreplication caveat rather than softening it in Results.
5. **PAC anomaly**: decide whether the slow-gamma/beta peak gets a full Results subsection or stays as a Discussion/future-directions note pending the theta-peak-frequency cross-reference analysis.
