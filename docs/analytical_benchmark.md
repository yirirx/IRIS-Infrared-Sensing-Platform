# Analytical benchmark: matched-filter detector

## Purpose
The simulation now records a theoretical matched-filter benchmark alongside the Monte Carlo estimates. This is a model check, not a physical validation.

## Assumptions
- The received observation is x = a s + n, where s is a known deterministic reference burst.
- Noise samples are independent, zero-mean Gaussian with unit variance (AWGN).
- The score is z = (x · s) / ||s||.
- SNR is defined as the mean clean-signal power over the complete N-sample observation divided by the noise variance.

## Derivation
Under the noise-only hypothesis, the normalized score has distribution z | H0 ~ Normal(0, 1). With a signal present, the score has distribution z | H1 ~ Normal(sqrt(N * gamma), 1), where gamma = 10^(SNR_dB / 10). The threshold eta is still estimated from the finite calibration simulation, so the theoretical benchmark isolates the expected detection probability given that threshold:

- Pfa_theory = 1 - Phi(eta)
- Pd_theory = 1 - Phi(eta - sqrt(N * gamma))

The implementation evaluates these expressions using the complementary error function. Because the calibration threshold is estimated from a finite random sample, theoretical false-alarm probability may differ slightly from the requested target.

## What to compare
For each SNR, compare:
- matched_filter_detection_rate: Monte Carlo estimate;
- matched_filter_ci95_low and matched_filter_ci95_high: its Wilson interval;
- matched_filter_theoretical_detection_probability: analytical benchmark;
- matched_filter_false_alarm_rate_validation: independent validation estimate;
- matched_filter_theoretical_pfa: analytical false-alarm probability implied by the estimated threshold.

The Monte Carlo estimate should fluctuate around the analytical value. With small trial counts, the estimate can differ noticeably; a confidence interval is a useful uncertainty summary, not a guarantee that every finite run will contain the exact theoretical value.

## Limitations
This derivation applies only to the current idealized Gaussian-noise model and known reference waveform. It does not model photodetector shot noise, ambient light, optical propagation, analogue electronics, quantization, timing mismatch, or any physical sensor. Agreement validates an implementation against its mathematical assumptions; it does not validate those assumptions for real hardware.
