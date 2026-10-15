# IRIS ambient-interference sweep — initial results

## Execution status
The GitHub Actions workflow completed successfully. It installed the project, ran the automated tests, executed the controlled sweep, and committed the outputs. See the [workflow run](https://github.com/yirirx/IRIS-Infrared-Sensing-Platform/actions/runs/38752835461).

The sweep used five sinusoidal-interference amplitudes (0, 0.1, 0.2, 0.4, 0.8 arbitrary units), a fixed 1 kHz interference frequency, SNR values -30, -24, and -18 dB, 1,000 signal-present trials per SNR/amplitude, 5,000 threshold-calibration records, and 5,000 independent noise-only validation records. Results are labeled simulation, not measurement.

## Selected detection results

| Interference amplitude (a.u.) | SNR (dB) | Energy detector Pd | Matched-filter Pd |
|---:|---:|---:|---:|
| 0.0 | -30 | 0.060 | 0.407 |
| 0.0 | -24 | 0.074 | 0.887 |
| 0.0 | -18 | 0.144 | 1.000 |
| 0.1 | -30 | 0.047 | 0.388 |
| 0.1 | -24 | 0.074 | 0.877 |
| 0.1 | -18 | 0.128 | 1.000 |
| 0.4 | -30 | 0.057 | 0.389 |
| 0.4 | -24 | 0.057 | 0.880 |
| 0.4 | -18 | 0.127 | 1.000 |
| 0.8 | -30 | 0.049 | 0.392 |
| 0.8 | -24 | 0.052 | 0.880 |
| 0.8 | -18 | 0.103 | 1.000 |

Here, Pd is the empirical probability of detection. The underlying CSV contains Wilson 95% confidence intervals for each estimate.

## Independent false-alarm validation

The target false-alarm probability was 0.05. Observed validation rates across the five amplitudes were:

| Amplitude (a.u.) | Energy detector Pfa | Matched-filter Pfa |
|---:|---:|---:|
| 0.0 | 0.0542 | 0.0468 |
| 0.1 | 0.0444 | 0.0442 |
| 0.2 | 0.0552 | 0.0434 |
| 0.4 | 0.0472 | 0.0552 |
| 0.8 | 0.0474 | 0.0540 |

These are finite-sample estimates; use the reported confidence intervals rather than treating small deviations from 0.05 as meaningful by themselves. The same validation estimate is repeated in the summary for each SNR because the noise-only validation set is shared within each amplitude condition.

## Initial interpretation

1. In this simulated setup, the matched filter had substantially higher detection probability than the energy detector at all three reported SNRs.
2. Detection did not change monotonically with interference amplitude in this small sweep. Therefore, these data do not support a simple claim that increasing this sinusoid always degrades detection.
3. At -18 dB, matched-filter detection reached 1.0 in 1,000 trials. This is an observed rate, not proof of perfect detection; the finite-sample confidence interval remains relevant.
4. Energy-detector detection at -30 dB was close to its false-alarm rate, indicating little separation between signal-present and noise-only scores in that condition.
5. The false-alarm estimates are broadly near the 5% target, but each amplitude has only 5,000 validation records. The intervals and repeated-seed checks should be considered before strong claims.

## Important limits

- Interference amplitude is in arbitrary simulation units, not calibrated illuminance or optical power.
- The signal model is a simplified burst plus Gaussian noise and an ideal sinusoid; it does not model photodiode responsivity, shot noise, analogue front-end bandwidth, saturation, ADC quantization, or real optical geometry.
- The matched filter is evaluated against the reference signal known to this simulation. This is a favorable assumption and should be stated when comparing it with non-coherent energy detection.
- Each interference condition has its own calibrated threshold. This measures performance when the detector is calibrated to the prevailing condition; it does not measure the impact of unexpected interference on a threshold calibrated in a clean environment.
- These results are simulation evidence only, not validation of a physical infrared sensing system.

## Next experiment

Run multiple independent seeds for each amplitude and add a second scenario in which thresholds are calibrated with no interference but evaluated after interference is introduced. That separates two questions: performance after environment-specific recalibration, and robustness to an unanticipated environmental change.
