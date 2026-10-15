# IRIS ambient-interference robustness experiment protocol

## Research question
How does the amplitude of a simplified periodic interference term affect the empirical detection probability of an energy detector and a matched-filter detector, when each detector's threshold is calibrated for the same target false-alarm probability under the corresponding interference condition?

## Hypothesis (to be tested, not assumed)
Increasing the interference amplitude may change the detection probability of both detectors. The direction and size of that change depend on the reference waveform, interference frequency, randomized phase, SNR, and score statistic. The experiment must report observed results rather than assume which detector performs better.

## Experimental design
- **Independent variable:** sinusoidal interference amplitude, currently defaulting to 0, 0.1, 0.2, 0.4, and 0.8 arbitrary signal units.
- **Fixed interference frequency:** 1 kHz by default.
- **SNR conditions:** -30, -24, and -18 dB by default.
- **Primary outcomes:** detection probability for the energy detector and matched filter.
- **False-alarm outcome:** rate measured on a noise-only validation set that is independent of the threshold-calibration set.
- **Uncertainty:** Wilson 95% confidence intervals for binomial detection and false-alarm proportions.
- **Reproducibility:** explicit random seed is recorded; separate deterministic seeds are used for each amplitude condition.
- **Provenance:** output rows are labeled `simulation_not_measurement`.

## Fairness and interpretation
Each amplitude condition receives its own threshold calibration and independent noise-only validation under the same modeled disturbance distribution as its signal-present trials. This estimates each detector's behavior when calibrated for that environment. It does not answer the different question of how a fixed threshold calibrated in a clean environment behaves after an unexpected interference change; that would require a separate experiment.

The detection plot and false-alarm plot must be read together. If validation false-alarm rates depart materially from the 5% target, detection rates alone are not a fair basis for claiming detector superiority. Confidence intervals quantify Monte Carlo sampling uncertainty, not model error or real-world uncertainty.

## Model assumptions and limits
The disturbance is an ideal sinusoid with independently randomized phase per record, added to unit-variance Gaussian noise. Its amplitude is expressed in arbitrary signal units. It is not calibrated to illuminance, optical power, photodiode response, receiver electronics, or a specific environment. This model does not include realistic DC ambient-light levels, shot noise, saturation, harmonics, analogue filtering, ADC effects, or hardware tolerances.

## Reporting checklist
Before drawing a conclusion:
1. Confirm automated tests pass.
2. Preserve the generated CSV files and plots with the seed and parameter settings.
3. Check that independent false-alarm estimates and their confidence intervals are consistent with the target.
4. Compare detectors at identical SNR and interference settings.
5. State the observed trend, uncertainty, and any conditions where the trend changes.
6. Do not generalize the simulation to a physical infrared receiver without calibrated measurements.

## Current status
This document specifies the experiment and reporting rules. It does not assert a performance result. A conclusion should only be written after the sweep has been executed and its output reviewed.


## Fixed-threshold environmental-change experiment

A complementary scenario calibrates both detector thresholds under clean AWGN only, then holds those thresholds fixed while testing noise-only and signal-present records under increasing sinusoidal interference. This answers a different operational question than the primary sweep, which recalibrates each detector under each interference condition.

The main outcome is the independent false-alarm rate after the environment changes. If it departs from the target, detection probabilities under that fixed threshold should not be compared as if the false-alarm operating point were unchanged. Outputs remain simulation-only, with arbitrary interference units and Wilson 95% intervals.
