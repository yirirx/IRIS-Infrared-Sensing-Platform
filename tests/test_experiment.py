import csv
import pytest
from iris_sim.experiment import run_experiment, wilson_interval


def test_wilson_interval_contains_observed_rate():
    low, high = wilson_interval(50, 100)
    assert low < 0.5 < high


def test_wilson_interval_rejects_invalid_counts():
    with pytest.raises(ValueError):
        wilson_interval(101, 100)


def test_experiment_writes_reproducible_outputs(tmp_path):
    out = tmp_path / "run"
    rows = run_experiment(out, seed=42, trials=120, snr_values=[-24, 0],
                          calibration_trials=500, validation_trials=500, roc_snr_db=-24)
    assert len(rows) == 2
    with (out / "metrics.csv").open(newline="", encoding="utf-8") as handle:
        saved = list(csv.DictReader(handle))
    assert len(saved) == 2
    assert saved[0]["result_type"] == "simulation_not_measurement"
    assert 0.0 <= float(saved[0]["matched_filter_theoretical_pfa"]) <= 1.0
    assert 0.0 <= float(saved[0]["matched_filter_theoretical_detection_probability"]) <= 1.0
    assert float(saved[1]["matched_filter_theoretical_detection_probability"]) > float(
        saved[0]["matched_filter_theoretical_detection_probability"]
    )
    assert float(saved[0]["energy_ci95_low"]) <= float(saved[0]["energy_detection_rate"])
    assert (out / "waveform.png").exists()
    assert (out / "detection_sweep.png").exists()
    assert (out / "roc_curve.png").exists()
    with (out / "roc_curve.csv").open(newline="", encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == 101


def test_invalid_false_alarm_rate_rejected(tmp_path):
    with pytest.raises(ValueError):
        run_experiment(tmp_path, trials=10, calibration_trials=100, validation_trials=100,
                       target_false_alarm=1.0)
