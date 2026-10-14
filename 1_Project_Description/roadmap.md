# Roadmap

## Milestone 0 — Simulation foundation (initial)
- [x] Requirements and architecture documentation.
- [x] Modulated burst generation, detector scores, and Monte Carlo runner.
- [x] Automated tests and CI workflow.

## Milestone 1 — Scientifically defensible simulation (in progress)
- [x] Hold noise variance fixed and vary signal power to define SNR consistently.
- [x] Calibrate thresholds on noise-only samples and validate on independent samples.
- [x] Report Wilson 95% confidence intervals for detection and false-alarm probabilities.
- [x] Record seed, threshold, trial counts, and explicit simulation-only labels.
- [ ] Add ROC curves and compare results against analytical predictions.
- [ ] Study timing mismatch, burst duration, and non-Gaussian/ambient-light interference.

## Milestone 2 — Receiver architecture and circuit
- [x] Identify manufacturer-documented candidate architectures and datasheets.
- [ ] Confirm exact order codes, carrier frequency, and current datasheet revisions.
- [ ] Select either a demodulated digital receiver or a photodiode + transimpedance amplifier.
- [ ] Calculate the emitter driver and power budget from verified datasheet conditions.
- [ ] Simulate and review the analogue front end if a raw waveform is required.
- [ ] Publish a reviewed schematic and bill of materials.

## Milestone 3 — Bench prototype
- [ ] Assemble a low-power, non-eye-directed test setup.
- [ ] Capture raw data with instrument settings and test geometry recorded.
- [ ] Repeat tests across distance and ambient-light conditions.
- [ ] Compare measured data with a revised, receiver-specific model.

## Milestone 4 — Research report
- [ ] State the research question, methods, assumptions, uncertainty, and limitations.
- [ ] Publish reproducible scripts, raw measurements, and a clear simulation/measurement distinction.
