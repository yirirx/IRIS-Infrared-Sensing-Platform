# Changelog

## 0.2.0 — Scientific validation and receiver trade study
- Fixed the simulation SNR convention: hold AWGN variance fixed and scale clean-signal power.
- Added independent threshold calibration and false-alarm validation sets.
- Added Wilson 95% confidence intervals and provenance fields.
- Extended the default SNR sweep to -36 through 0 dB to expose the transition region.
- Added manufacturer-datasheet-based candidate receiver architectures and a hardware design gate.
- No physical hardware claims; circuit design and measurements remain future milestones.

## 0.1.0 — Initial scaffold
- Added requirements, architecture, roadmap, burst generation, detector scores, and Monte Carlo sweep.
- Added automated tests and GitHub Actions.
