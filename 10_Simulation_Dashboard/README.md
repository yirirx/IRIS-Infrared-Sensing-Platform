# IRIS Simulation Dashboard

A self-contained browser dashboard for exploring the simplified IRIS burst-detection experiment. It uses vanilla HTML, CSS, and JavaScript; no external packages or build step are required.

## Open the dashboard

- Open `index.html` in a modern desktop or mobile browser.
- Or, after GitHub Pages is enabled for this repository, visit the Pages URL for this project.
- The dashboard performs a separate browser-side Monte Carlo simulation; it does not execute the Python package in the repository.

## Controls

- **SNR:** changes the simulated signal power relative to noise variance.
- **Target false alarm:** calibrates detector thresholds from noise-only samples.
- **Trial count:** controls the number of signal-present trials.
- **Noise variance scale:** scales noise and signal consistently at a given SNR.
- **Detector view:** displays either detector or both.
- **Run experiment:** recalculates thresholds, independent false-alarm validation, detection probabilities, confidence intervals, sweep, and ROC.
- **Export CSV:** downloads summary metrics for the current run.

## Model boundaries

The page models a known sinusoidal burst with additive white Gaussian noise. It is an educational, idealized simulation—not a calibrated optical link or a physical receiver. It does not estimate detection distance or establish hardware sensitivity. Browser-side random numbers are seeded for repeatability, but this implementation is a separate model from the Python CLI; do not expect identical numerical outputs between them.

## Provenance

Dashboard version: 0.1. Baseline seed is derived from the selected settings. Threshold calibration and validation use separate noise-only sample sets. Detection confidence intervals use the Wilson score interval.
