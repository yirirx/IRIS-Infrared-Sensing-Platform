# Simulation Baseline and Validation Record

## Run configuration
- Date: 2026-10-14
- Seed: 20261014
- Signal-present trials per SNR: 1,000
- Noise-only threshold calibration windows: 5,000
- Independent noise-only validation windows: 5,000
- Target false-alarm probability: 0.05
- Noise model: unit-variance additive white Gaussian noise (AWGN)
- SNR: mean clean-signal power over the full observation window divided by noise variance

## Observed simulation results
- Energy detector threshold: 1.052563 (simulation score units)
- Matched-filter threshold: 1.668514 (simulation score units)
- Validated energy-detector false-alarm rate: 0.0532; Wilson 95% interval approximately [0.0473, 0.0598]
- Validated matched-filter false-alarm rate: 0.0528; Wilson 95% interval approximately [0.0469, 0.0593]
- At -36 dB SNR, energy detection was 0.043 and matched-filter detection was 0.158 in 1,000 trials.
- At -27 dB SNR, energy detection was 0.054 and matched-filter detection was 0.632 in 1,000 trials.
- At -12 dB SNR, energy detection was 0.591 and matched-filter detection was 1.000 in 1,000 trials.
- At -6 dB SNR and above in this sweep, both detectors detected all 1,000 signal-present trials.

## Interpretation
These numbers are reproducible simulation output under the stated AWGN model and signal definition. They are not physical receiver measurements and do not predict detection distance. The matched filter integrates across the known burst, so the chosen waveform has substantial processing gain; this is why its detection probability rises earlier in the SNR sweep.

The measured false-alarm rates are close to, but not exactly equal to, the 5% target because thresholds and validation rates are estimated from finite random samples.

## Reproduce
```bash
python -m pip install -e ".[dev]"
pytest
python -m iris_sim --output 5_Simulations/results --trials 1000 --seed 20261014
```
