# Changelog

## 0.3.0 — ROC analysis and validated Monte Carlo workflow
- Defined SNR by holding noise variance fixed and scaling signal power.
- Separated threshold calibration from false-alarm validation.
- Added Wilson 95% intervals, reproducible metadata, and independent validation rates.
- Added empirical ROC coordinates and ROC plot at a configurable SNR.
- Expanded tests and regenerated result artifacts from the simulation code.
- Explicitly labeled results as simulations, not physical measurements.

## 0.1.0 — Initial scaffold
- Added requirements, architecture, signal generation, detector scores, and initial simulation sweep.
- Added automated tests and continuous integration.
