# Model Limitations and Claim Policy

## What the current model includes
- A deterministic on/off-keyed sinusoidal reference burst.
- Unit-variance additive white Gaussian noise (AWGN).
- Energy and matched-filter scores.
- Empirical threshold calibration, independent noise-only validation, and Monte Carlo confidence intervals.

## What it does not model
- Optical power budget, distance, lens/aperture, beam divergence, or reflection geometry.
- Photodiode responsivity and shot noise.
- Transimpedance-amplifier bandwidth, noise, stability, or saturation.
- ADC quantization, sampling-clock jitter, or receiver timing mismatch.
- Ambient-light interference, sunlight, fluorescent/LED flicker, temperature drift, or component tolerances.
- Actual sensor modules, microcontroller code, or physical measurements.

## Claim policy
Do not claim a detection distance, calibrated sensitivity, medical use, or hardware reliability from this simulation. Those claims require a defined physical setup, actual parts, repeatable measurements, and documented uncertainty. Confidence intervals here quantify Monte Carlo sampling uncertainty only.
