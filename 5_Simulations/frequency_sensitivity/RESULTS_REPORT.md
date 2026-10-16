# IRIS frequency-sensitivity study — results

## Execution and provenance
The frequency-sensitivity experiment completed successfully in the automated robustness workflow, including the automated test suite and artifact commit. [Workflow run](https://github.com/yirirx/IRIS-Infrared-Sensing-Platform/actions/runs/38916092677).

The experiment uses six ideal sinusoidal disturbance frequencies (250, 500, 1,000, 2,500, 5,000, and 10,000 Hz), three arbitrary amplitudes (0.0, 0.2, 0.4), 5,000 clean noise-only calibration trials, 5,000 noise-only validation trials per condition, and 1,000 signal-present trials per SNR. The primary endpoint is independently validated noise-only false-alarm rate. Thresholds are calibrated under clean AWGN and then held fixed while interference is introduced. This is a simulation, not a physical measurement.

## Main observations

### Energy detector
At disturbance amplitude 0.2, the observed false-alarm rate ranges from 15.5% to 16.68% across the tested frequencies. At amplitude 0.4, it ranges from 78.12% to 80.30%. Thus, within this model and tested frequency range, amplitude has a much larger effect than the selected frequency on the energy detector's false-alarm rate.

### Matched filter
At amplitudes 0.2 and 0.4, the matched-filter false-alarm rate stays close to the 5% target for most tested frequencies, but rises sharply at 5,000 Hz: 36.06% at amplitude 0.2 and 43.06% at amplitude 0.4. This demonstrates that the matched filter is not generally immune to sinusoidal interference; susceptibility depends on how the disturbance aligns with the reference waveform and score statistic.

### Illustrative comparison

| Frequency | Amplitude | Energy detector Pfa | Matched-filter Pfa |
|---:|---:|---:|---:|
| 250 Hz | 0.2 | 16.68% | 4.80% |
| 1,000 Hz | 0.2 | 15.50% | 5.42% |
| 5,000 Hz | 0.2 | 15.78% | 36.06% |
| 5,000 Hz | 0.4 | 79.30% | 43.06% |
| 10,000 Hz | 0.4 | 80.18% | 4.48% |

Wilson 95% confidence intervals are included in the CSV. Because each frequency uses a distinct deterministic seed, small differences between frequencies also include Monte Carlo variation.

## Interpretation
1. The energy detector is sensitive to added disturbance energy when its threshold is calibrated in clean noise.
2. The matched filter is more resistant at several tested frequencies, but the 5 kHz result is a clear counterexample to a blanket robustness claim.
3. Detection probability must be considered together with false-alarm probability; a detector that triggers frequently on noise-only records is not necessarily detecting the wanted signal more effectively.
4. These findings apply only to this particular reference waveform, sampling/model settings, disturbance model, and thresholding procedure.

## Limitations and next work
The disturbance is an ideal sinusoid with arbitrary amplitude units and randomized phase. The model omits calibrated ambient illumination, photodiode response and shot noise, DC offset, saturation, analogue filtering, ADC effects, and hardware tolerances. The next useful study is a controlled frequency/phase sweep using a documented reference waveform, followed by comparison against analytical expectations and, eventually, bench measurements. No physical range or receiver performance can be inferred from these results.
