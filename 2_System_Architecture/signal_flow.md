# Signal Flow
1. Generate a reference carrier burst.
2. Apply scalar gain and additive noise.
3. Calculate energy and matched-filter scores.
4. Compare scores with thresholds calibrated using noise-only samples.
5. Repeat for signal-present and noise-only trials across SNR values.
6. Export detection and false-alarm rates.

Detection rate is the fraction of signal-present trials detected. False-alarm rate is the fraction of noise-only trials incorrectly labelled as signal. Results depend on the model and finite calibration sample size.
