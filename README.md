# IRIS — Infrared Sensing & Signal Processing Platform

> An open engineering project exploring modulated infrared sensing, noisy-signal detection, and a staged path from reproducible simulation to a low-cost physical prototype.

![Status](https://img.shields.io/badge/status-early%20simulation-blue) ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB) ![License](https://img.shields.io/badge/license-MIT-green)

**This is an original, staged project.** Milestone 0.1 contains a software simulation. No physical prototype, measured range, or hardware performance is claimed yet.

## Goals
- Generate a modulated carrier burst and simulate attenuation/noise.
- Compare energy and matched-filter detection.
- Produce repeatable plots and CSV metrics.
- Document requirements, design decisions, testing, and a responsible hardware path.

## Repository map
- `1_Project_Description/` — requirements, roadmap, design decisions
- `2_System_Architecture/` — block diagram and signal flow
- `3_Sensor_and_Power/` — sensor evaluation and power-budget template
- `4_Schematics_and_Hardware/` — hardware status and preliminary BOM
- `5_Simulations/` — experiment plan and generated results
- `6_Application_Notes/` — detection theory and limitations
- `7_Component_Datasheets/` — component-document register
- `8_Utils/` — evidence and plotting conventions
- `9_Firmware_and_Software/` — Python simulation package
- `docs/`, `tests/`, `.github/workflows/` — reports, unit tests, CI

## Quick start
Requires Python 3.10+.
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m iris_sim --output 5_Simulations/results
pytest
```

The simulation creates `waveform.png`, `detection_sweep.png`, and `metrics.csv` in the selected output directory.

## First simulation
The model generates an on/off-keyed sinusoidal burst, applies scalar gain and additive Gaussian noise, then evaluates an energy score and a matched-filter score. It sweeps SNR and estimates detection and false-alarm rates using repeatable random trials.

This is **not** a calibrated optical propagation model. It does not yet include lens geometry, photodiode responsivity, analogue-front-end bandwidth, saturation, ADC quantization, or measured ambient-light interference. Simulated results must not be presented as hardware measurements or detection range.

## Engineering principles
1. Reproducible experiments and documented parameters.
2. Clear separation of simulation, bench tests, and field measurements.
3. Traceability from requirements to tests.
4. Hardware selection only after requirements and datasheets are reviewed.
5. Original implementation; the organization is inspired by open engineering repositories, not copied from them.

## Safety
IR sources may present eye-safety risks depending on wavelength, optical power, and optics. Before any physical build, review manufacturer safety guidance and use an appropriately rated, low-power setup.

## License
MIT; see [LICENSE](LICENSE).