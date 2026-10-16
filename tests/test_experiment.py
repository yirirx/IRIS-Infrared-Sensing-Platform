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


def test_ambient_interference_is_recorded_and_awgn_theory_is_disabled(tmp_path):
    rows = run_experiment(
        tmp_path, seed=7, trials=120, snr_values=[-24, 0],
        calibration_trials=500, validation_trials=500, roc_snr_db=-24,
        ambient_amplitude=0.2, ambient_frequency_hz=1000,
    )
    assert rows[0]["ambient_interference_amplitude"] == 0.2
    assert rows[0]["ambient_interference_frequency_hz"] == 1000
    assert rows[0]["ambient_interference_phase"] == "randomized_per_record"
    assert np.isnan(rows[0]["matched_filter_theoretical_detection_probability"])


def test_invalid_ambient_frequency_rejected(tmp_path):
    with pytest.raises(ValueError):
        run_experiment(tmp_path, trials=10, calibration_trials=100, validation_trials=100,
                       ambient_amplitude=0.1, ambient_frequency_hz=50000)

def test_interference_sweep_writes_summary(tmp_path):
    from iris_sim.sweep import run_interference_sweep

    rows = run_interference_sweep(
        tmp_path / "sweep", amplitudes=[0.0, 0.2], frequency_hz=1000,
        snr_values=[-24, 0], trials=100, calibration_trials=100,
        validation_trials=100, seed=11,
    )
    assert len(rows) == 4
    assert (tmp_path / "sweep" / "interference_sweep.csv").exists()
    assert (tmp_path / "sweep" / "detection_vs_interference.png").exists()
    assert (tmp_path / "sweep" / "false_alarm_vs_interference.png").exists()
    assert {row["ambient_amplitude"] for row in rows} == {0.0, 0.2}
    assert all(row["result_type"] == "simulation_not_measurement" for row in rows)
    assert "energy_false_alarm_ci95_low" in rows[0]
    assert "matched_filter_false_alarm_ci95_high" in rows[0]


def test_interference_sweep_rejects_duplicate_amplitudes(tmp_path):
    from iris_sim.sweep import run_interference_sweep

    with pytest.raises(ValueError, match="unique"):
        run_interference_sweep(
            tmp_path / "sweep", amplitudes=[0.1, 0.1], snr_values=[-24],
            trials=10, calibration_trials=100, validation_trials=100,
        )


def test_mismatched_calibration_writes_results(tmp_path):
    from iris_sim.mismatch import run_mismatched_calibration

    rows = run_mismatched_calibration(
        tmp_path / "mismatch", amplitudes=[0.0, 0.2], snr_values=[-24],
        trials=50, calibration_trials=100, validation_trials=100, seed=17,
    )
    assert len(rows) == 2
    assert (tmp_path / "mismatch" / "mismatched_calibration.csv").exists()
    assert (tmp_path / "mismatch" / "false_alarm_after_environment_change.png").exists()
    assert rows[0]["calibration_condition"] == "clean_AWGN_only"


def test_seed_stability_writes_summary(tmp_path):
    from iris_sim.seed_stability import run_seed_stability

    rows = run_seed_stability(
        tmp_path / "stability", seeds=[11, 12], amplitudes=[0.0, 0.2],
        snr_values=[-24], trials=30, calibration_trials=100,
        validation_trials=100,
    )
    assert len(rows) == 4
    assert (tmp_path / "stability" / "seed_stability.csv").exists()
    assert (tmp_path / "stability" / "seed_stability.png").exists()
    assert all(row["seed_count"] == 2 for row in rows)


def test_frequency_study_writes_summary(tmp_path):
    from iris_sim.frequency_study import run_frequency_study

    rows = run_frequency_study(
        tmp_path / "frequency", frequencies_hz=[250.0, 1000.0],
        amplitudes=[0.0, 0.2], snr_values=[-24], trials=30,
        calibration_trials=100, validation_trials=100, seed=31,
    )
    assert len(rows) == 4
    assert (tmp_path / "frequency" / "frequency_sensitivity.csv").exists()
    assert (tmp_path / "frequency" / "frequency_sensitivity.png").exists()
    assert all(row["result_type"] == "simulation_not_measurement" for row in rows)
