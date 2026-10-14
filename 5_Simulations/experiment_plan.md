# SIM-001 — Detection versus SNR

## Question
How does detection probability change with signal-to-noise ratio for two detectors under the same simulated assumptions?

## Method
- Generate a reference burst.
- Calibrate thresholds from independent noise-only samples to a nominal 5% false-alarm target.
- Sweep SNR and evaluate signal-present and noise-only trials.
- Use a fixed random seed.

## Outputs
`waveform.png`, `detection_sweep.png`, `metrics.csv`.

## Limitations
The scalar-gain plus Gaussian-noise model is intentionally simplified. It is not a measured optical receiver and does not establish detection range or real-world sensitivity.
