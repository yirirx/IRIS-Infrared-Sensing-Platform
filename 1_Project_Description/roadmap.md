# Project Roadmap

## Milestone 0 — Simulation foundation
- [x] Requirements, architecture, and design decisions.
- [x] Reference burst generation and detector scores.
- [x] Automated tests and CI workflow.

## Milestone 1 — Reproducible statistical experiment
- [x] Define SNR with fixed noise variance and scaled signal power.
- [x] Calibrate thresholds on noise-only records.
- [x] Validate false-alarm rates on an independent noise-only dataset.
- [x] Add Wilson 95% intervals, seed metadata, and CSV outputs.
- [x] Add empirical ROC curve at a chosen SNR.
- [ ] Compare Monte Carlo outcomes with analytical predictions.
- [ ] Study timing/frequency mismatch and non-Gaussian ambient-light interference.

## Milestone 2 — Receiver architecture and circuit
- [x] Identify candidate architectures and link manufacturer datasheets.
- [ ] Verify exact order codes, carrier compatibility, and datasheet revisions.
- [ ] Select digital-demodulated or raw-analogue receiver path.
- [ ] Calculate emitter driver and power budget from verified limits.
- [ ] Design and review a schematic; simulate the analogue front end if selected.

## Milestone 3 — Bench prototype
- [ ] Build a low-power, non-eye-directed setup.
- [ ] Record setup geometry, instruments, settings, and raw data.
- [ ] Repeat tests across distance and ambient-light conditions.
- [ ] Compare measurements with a receiver-specific model.

## Milestone 4 — Research report
- [ ] Document question, methods, assumptions, uncertainty, and limitations.
- [ ] Publish raw measurements only when genuinely collected and traceable.
