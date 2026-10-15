# IRIS — Infrared Sensing & Signal Processing Platform

![Status](https://img.shields.io/badge/status-reproducible%20simulation-blue) ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB) ![License](https://img.shields.io/badge/license-MIT-green)

**IRIS** is an open engineering project investigating detection of a known modulated infrared-like burst in noise. It begins with a reproducible signal-processing simulation and lays out a responsible path toward a receiver-specific physical prototype.

> **Scope:** current performance results are simulations using an idealized additive white Gaussian noise (AWGN) model. No circuit has been built or measured, and no optical range, sensitivity, medical utility, or real-world performance is claimed.

## Research question
At a fixed target false-alarm probability, how does detection probability change with SNR for an energy detector versus a matched filter detecting a known burst?

## Interactive simulation dashboard

**[Open the IRIS Simulation Control Room source](10_Simulation_Dashboard/index.html)** — adjust SNR, false-alarm target, trial count, and noise scale; run a browser-side Monte Carlo experiment; inspect waveform, detection sweep, ROC, confidence intervals, and export a CSV. It can be run locally by opening the HTML file. To publish a live website, follow the one-time [GitHub Pages setup instructions](10_Simulation_Dashboard/README.md).

The dashboard is a standalone educational model in the browser, separate from the Python CLI. It is not a physical receiver measurement.

## Simulation results

![Detection probability versus SNR](5_Simulations/results/detection_sweep.svg)

![Empirical ROC at -24 dB](5_Simulations/results/roc_curve.svg)

Baseline: 1,000 signal-present trials per SNR; 5,000 noise-only records for threshold calibration; 5,000 independent noise-only records for false-alarm validation; seed \`20261014\`; target false-alarm probability 5%.

- At -27 dB, simulated detection was 5.4% for energy detection and 63.2% for matched-filter detection (1,000 trials each).
- Independently validated false-alarm rates were 5.32% and 5.28%, respectively.
- These depend on the idealized model, reference waveform, thresholds, and SNR convention. They are not hardware performance claims.

Model note: [ambient-flicker interference assumptions and limitations](docs/ambient_interference_model.md).

Raw data: [metrics.csv](5_Simulations/results/metrics.csv) · [downsampled ROC coordinates (21 display points)](5_Simulations/results/roc_curve.csv) · [experiment protocol](5_Simulations/experiment_plan.md) · [validation notes](docs/test_results.md). Re-running the CLI exports the full 101-point ROC sweep.

## Implemented
- Deterministic on/off-keyed burst generation.
- Fixed-variance AWGN channel model and explicit SNR convention.
- Energy and matched-filter detector scores.
- A standalone sinusoidal ambient-flicker interference utility for controlled stress tests (not yet integrated into the primary Monte Carlo experiment).
- Independent noise-only threshold calibration and false-alarm validation.
- Monte Carlo estimates with Wilson 95% confidence intervals.
- Empirical ROC curve at a configurable SNR.
- CSV metrics, plots, automated tests, and GitHub Actions.
- Preliminary receiver architecture study with manufacturer datasheet references.

## Quick start

Requires Python 3.10+.

\`\`\`bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
python -m iris_sim --output 5_Simulations/results --trials 1000 --seed 20261014
\`\`\`

Optional parameters:

\`\`\`bash
python -m iris_sim --trials 2000 --calibration-trials 10000 --validation-trials 10000 --target-false-alarm 0.01 --roc-snr -24
\`\`\`

The ROC SNR must be included in the sweep; the default includes -24 dB. Outputs: \`metrics.csv\`, \`roc_curve.csv\`, \`waveform.png\`, \`detection_sweep.png\`, and \`roc_curve.png\`.

## Architecture

\`\`\`mermaid
flowchart TD
    A[Reference burst and settings] --> B[Scale signal power for SNR]
    B --> C[Add fixed-variance AWGN]
    C --> D[Energy score]
    C --> E[Matched-filter score]
    F[Noise-only calibration set] --> G[Detector thresholds]
    G --> D
    G --> E
    H[Independent noise-only validation] --> I[False-alarm rates + confidence intervals]
    D --> J[Detection rates + confidence intervals]
    E --> J
    I --> K[CSV, plots, reproducible report]
    J --> K
\`\`\`

## Hardware direction — not yet built
Two architectures are under consideration:
1. **Simple digital demo:** compatible integrated IR receiver plus 940 nm emitter. Easier to prototype, but the demodulated output cannot validate raw analogue waveform samples directly.
2. **Waveform-focused research prototype:** BPW34 photodiode, designed transimpedance amplifier, and ADC/oscilloscope capture. More flexible but requires careful analogue design.

Candidate manufacturer documents:
- [Vishay TSSP940 receiver](https://www.vishay.com/docs/82843/tssp940.pdf)
- [Vishay BPW34 photodiode](https://www.vishay.com/docs/81521/bpw34.pdf)
- [Vishay TSAL6200 emitter](https://www.vishay.com/docs/81010/tsal6200.pdf)

These are candidates, not a finalized bill of materials. Verify exact variants, carrier compatibility, current limits, voltage levels, and safety requirements before buying or assembling.

## Roadmap
- [x] Reproducible burst and AWGN simulation.
- [x] Independent threshold calibration and false-alarm validation.
- [x] Wilson 95% intervals and empirical ROC export.
- [ ] Compare Monte Carlo results with analytical predictions.
- [x] Add a standalone sinusoidal ambient-flicker interference utility with parameter validation.
- [ ] Integrate interference into the Monte Carlo experiment and compare detector robustness under matched calibration conditions.
- [ ] Add timing mismatch.
- [ ] Select receiver architecture and design a reviewed circuit.
- [ ] Build a safe low-power bench prototype and record raw measurements.
- [ ] Validate the model against measurements.

## Scientific integrity and safety
Confidence intervals quantify Monte Carlo sampling uncertainty, not uncertainty in a physical receiver. The model omits optical geometry, photodiode responsivity and shot noise, analogue-front-end bandwidth/noise, ADC quantization, ambient-light interference, and component tolerances. Do not infer detection range or medical applicability from this simulation.

IR may be invisible and still pose an eye hazard. Any future hardware work must follow manufacturer safety guidance and use a low-power, non-eye-directed setup.

## License
MIT; see [LICENSE](LICENSE).
