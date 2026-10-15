# IRIS threshold-mismatch experiment — results

## Status and reproducibility
The automated robustness workflow completed successfully, including the Python test suite and both interference experiments. [Workflow run](https://github.com/yirirx/IRIS-Infrared-Sensing-Platform/actions/runs/38753693319).

This experiment calibrated thresholds on 5,000 noise-only records under clean AWGN, then held those thresholds fixed while testing each ambient-interference amplitude with 5,000 independent noise-only validation records and 1,000 signal-present trials per SNR. The random seed was 20261020. The target false-alarm rate was 5%. All results are simulation, not physical measurements.

## Main result: false alarms after environmental change

| Interference amplitude (arbitrary units) | Energy detector Pfa | Matched-filter Pfa |
|---:|---:|---:|
| 0.0 | 4.78% | 5.02% |
| 0.1 | 7.18% | 5.10% |
| 0.2 | 15.60% | 5.10% |
| 0.4 | 78.80% | 5.26% |
| 0.8 | 100.00% | 5.92% |

Wilson 95% confidence intervals are included in `mismatched_calibration.csv`. At amplitude 0.4, the energy detector's false-alarm interval is approximately 77.65%–79.91%; at amplitude 0.8, every one of the 5,000 noise-only validation records exceeded the clean-calibrated energy threshold. The matched-filter false-alarm estimates remain much closer to the 5% target over these tested conditions.

## Interpretation

1. **The energy detector is highly sensitive to this modeled sinusoidal disturbance when its threshold is not recalibrated.** Its score accumulates signal energy, including disturbance energy, so noise-only records can exceed the clean-calibrated threshold.
2. **The matched filter is more resistant to this specific interference in this particular model.** A sinusoid at the selected frequency contributes less coherently to the reference-waveform correlation. This is not a general guarantee for arbitrary interference frequencies, phases, or waveform shapes.
3. **Do not interpret the energy detector's increased detection rate under strong interference as improved useful detection.** Its false-alarm rate rises sharply, so many noise-only records are incorrectly labeled as signal-present. Detection probability must be interpreted alongside false-alarm probability.
4. The two detectors use different score statistics and clean-calibrated thresholds; this experiment evaluates the effect of environmental mismatch, not an optimally recalibrated comparison at a fixed operating point.

## Limitations
The interference is an ideal sinusoid with arbitrary amplitude units and randomized phase. The model does not represent calibrated ambient illumination, photodiode response, shot noise, saturation, analogue filtering, ADC effects, or real optical geometry. The results support a narrow statement about this simulation only; they do not establish physical infrared receiver performance.

## Next step
Repeat the experiment across multiple independent random seeds, report mean and between-seed variation, and test additional interference frequencies and waveform shapes. That will help determine whether this behavior is stable or specific to the current configuration.
