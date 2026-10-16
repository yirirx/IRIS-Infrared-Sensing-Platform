"""Frequency sensitivity study for sinusoidal ambient interference."""
import argparse
import csv
import tempfile
from pathlib import Path

import numpy as np

from .mismatch import run_mismatched_calibration


def run_frequency_study(output_dir, frequencies_hz=None, amplitudes=None,
                        snr_values=None, trials=1000, calibration_trials=5000,
                        validation_trials=5000, seed=20261025):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frequencies_hz = [250.0, 500.0, 1000.0, 2500.0, 5000.0, 10000.0] if frequencies_hz is None else list(frequencies_hz)
    amplitudes = [0.0, 0.2, 0.4] if amplitudes is None else list(amplitudes)
    snr_values = [-30, -24, -18] if snr_values is None else list(snr_values)
    if not frequencies_hz or any(not np.isfinite(f) or f < 0 or f >= 50000 for f in frequencies_hz):
        raise ValueError("frequencies must be finite values in [0, 50000)")
    if len(set(frequencies_hz)) != len(frequencies_hz):
        raise ValueError("frequencies must be unique")
    rows = []
    with tempfile.TemporaryDirectory(prefix="iris_frequency_runs_") as temp:
        for fi, frequency in enumerate(frequencies_hz):
            result = run_mismatched_calibration(
                Path(temp) / f"frequency_{frequency:g}",
                amplitudes=amplitudes, snr_values=snr_values, trials=trials,
                calibration_trials=calibration_trials,
                validation_trials=validation_trials,
                frequency_hz=frequency, seed=seed + fi,
            )
            for row in result:
                # False-alarm values are repeated for each SNR because the same
                # noise-only validation set is shared within a frequency/amplitude.
                rows.append(row)

    summary = []
    for frequency in frequencies_hz:
        for amplitude in amplitudes:
            matching = [r for r in rows
                        if float(r["ambient_frequency_hz"]) == float(frequency)
                        and float(r["test_ambient_amplitude"]) == float(amplitude)
                        and float(r["snr_db"]) == float(snr_values[0])]
            if not matching:
                continue
            row = matching[0]
            summary.append({
                "ambient_frequency_hz": float(frequency),
                "test_ambient_amplitude": float(amplitude),
                "energy_false_alarm_rate": float(row["energy_false_alarm_rate_validation"]),
                "energy_false_alarm_ci95_low": float(row["energy_false_alarm_ci95_low"]),
                "energy_false_alarm_ci95_high": float(row["energy_false_alarm_ci95_high"]),
                "matched_filter_false_alarm_rate": float(row["matched_filter_false_alarm_rate_validation"]),
                "matched_filter_false_alarm_ci95_low": float(row["matched_filter_false_alarm_ci95_low"]),
                "matched_filter_false_alarm_ci95_high": float(row["matched_filter_false_alarm_ci95_high"]),
                "target_false_alarm_rate": 0.05,
                "seed": seed + list(frequencies_hz).index(frequency),
                "calibration_condition": "clean_AWGN_only",
                "result_type": "simulation_not_measurement",
            })
    path = output_dir / "frequency_sensitivity.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    _plot_frequency_study(output_dir / "frequency_sensitivity.png", summary)
    return summary


def _plot_frequency_study(path, rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for axis, detector, key in (
        (axes[0], "Energy detector", "energy_false_alarm_rate"),
        (axes[1], "Matched filter", "matched_filter_false_alarm_rate"),
    ):
        for amplitude in sorted({r["test_ambient_amplitude"] for r in rows}):
            subset = sorted((r for r in rows if r["test_ambient_amplitude"] == amplitude),
                            key=lambda r: r["ambient_frequency_hz"])
            axis.plot([r["ambient_frequency_hz"] for r in subset],
                      [r[key] for r in subset], marker="o", label=f"Amplitude {amplitude:g}")
        axis.axhline(0.05, linestyle="--", label="Target Pfa = 5%")
        axis.set_xscale("log")
        axis.set_xlabel("Interference frequency (Hz)")
        axis.set_title(detector)
        axis.grid(True, alpha=0.3)
        axis.legend()
    axes[0].set_ylabel("False-alarm rate (simulation)")
    fig.suptitle("Frequency sensitivity with clean-calibrated thresholds")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Study IRIS detector sensitivity to interference frequency")
    parser.add_argument("--output", default="5_Simulations/frequency_sensitivity")
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--calibration-trials", type=int, default=5000)
    parser.add_argument("--validation-trials", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20261025)
    args = parser.parse_args()
    rows = run_frequency_study(args.output, trials=args.trials,
        calibration_trials=args.calibration_trials,
        validation_trials=args.validation_trials, seed=args.seed)
    print(f"Wrote {len(rows)} frequency/amplitude rows to {Path(args.output) / 'frequency_sensitivity.csv'}")
    print("Simulation only; interference amplitude is in arbitrary units.")


if __name__ == "__main__":
    main()
