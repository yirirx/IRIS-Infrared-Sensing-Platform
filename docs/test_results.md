# Test Results

Local verification on 2026-10-14:
- Unit tests: **6 passed**.
- Simulation: completed with 9 SNR points and 100 trials per point.
- Outputs generated: `waveform.png`, `detection_sweep.png`, and `metrics.csv`.

These are software/simulation checks only. They are not physical hardware measurements. Re-run with:

```bash
python -m pip install -e ".[dev]"
pytest
python -m iris_sim --output 5_Simulations/results --trials 100
```
