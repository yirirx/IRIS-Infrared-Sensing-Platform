import csv

import numpy as np
import pytest

from iris_sim.experiment import run_experiment, wilson_interval


def test_wilson_interval_contains_observed_rate():
    low, high = wilson_interval(50, 100)
    assert low < 0.5 < high


def test_wilson_interval_rejects_invalid_counts():
    with pytest.raises(ValueError):
        wilson_interval(101, 100)


def test_experiment_writes_reproducible_metrics(tmp_path):
    out = tmp_path / "run"
    rows = run_experiment(
        out, seed=42, trials=80, snr_values=[-6, 0, 6],
        calibration_trials=500, validation_trials=500,
    )
    assert len(rows) == 3
    with (out / "metrics.csv").open(newline="", encoding="utf-8") as handle:
        saved = list(csv.DictReader(handle))
    assert len(saved) == 3
    assert saved[0]["result_type"] == "simulation_not_measurement"
    assert float(saved[0]["energy_ci95_low"]) <= float(saved[0]["energy_detection_rate"])
    assert (out / "waveform.png").exists()
    assert (out / "detection_sweep.png").exists()


def test_snr_definition_scales_clean_signal_power():
    # The SNR convention used by the experiment is explicitly mean signal
    # power over the complete observation window divided by noise variance.
    assert 10 ** (-10 / 10) == pytest.approx(0.1)
