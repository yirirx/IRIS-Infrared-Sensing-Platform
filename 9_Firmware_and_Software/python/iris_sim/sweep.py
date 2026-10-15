"""Controlled Monte Carlo sweep over sinusoidal interference amplitude.

Each amplitude gets its own run directory. Threshold calibration and independent
false-alarm validation are repeated under that amplitude's noise distribution.
All outputs are simulations, not physical measurements.
"""
import argparse
import csv
from pathlib import Path

from .experiment import run_experiment


def run_interference_sweep(output_dir, amplitudes=None, frequency_hz=1000.0,
                           snr_values=None, trials=1000, calibration_trials=5000,
                           validation_trials=5000, target_false_alarm=0.05,
                           seed=20261015):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    amplitudes = [0.0, 0.1, 0.2, 0.4, 0.8] if amplitudes is None else list(amplitudes)
    snr_values = [-30, -24, -18] if snr_values is None else list(snr_values)
    if not amplitudes or any(a < 0 for a in amplitudes):
        raise ValueError("amplitudes must be a non-empty list of non-negative values")
    if not snr_values:
        raise ValueError("snr_values must not be empty")

    summary = []
    for index, amplitude in enumerate(amplitudes):
        run_dir = output_dir / f"amplitude_{amplitude:g}"
        rows = run_experiment(
            run_dir,
            seed=seed + index,
            trials=trials,
            snr_values=snr_values,
            calibration_trials=calibration_trials,
            validation_trials=validation_trials,
            target_false_alarm=target_false_alarm,
            roc_snr_db=snr_values[len(snr_values) // 2],
            ambient_amplitude=amplitude,
            ambient_frequency_hz=frequency_hz,
        )
        for row in rows:
            summary.append({
                "ambient_amplitude": amplitude,
                "ambient_frequency_hz": frequency_hz,
                "snr_db": row["snr_db"],
                "trials": row["trials"],
                "energy_detection_rate": row["energy_detection_rate"],
                "energy_ci95_low": row["energy_ci95_low"],
                "energy_ci95_high": row["energy_ci95_high"],
                "matched_filter_detection_rate": row["matched_filter_detection_rate"],
                "matched_filter_ci95_low": row["matched_filter_ci95_low"],
                "matched_filter_ci95_high": row["matched_filter_ci95_high"],
                "energy_false_alarm_rate_validation": row["energy_false_alarm_rate_validation"],
                "matched_filter_false_alarm_rate_validation": row["matched_filter_false_alarm_rate_validation"],
                "target_false_alarm_rate": target_false_alarm,
                "calibration_trials": calibration_trials,
                "validation_trials": validation_trials,
                "seed": seed + index,
                "result_type": "simulation_not_measurement",
            })

    summary_path = output_dir / "interference_sweep.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)
    _plot_sweep_summary(output_dir / "detection_vs_interference.png", summary)
    _plot_false_alarm_summary(output_dir / "false_alarm_vs_interference.png", summary)
    return summary


def _plot_sweep_summary(path, rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    amplitudes = sorted({row["ambient_amplitude"] for row in rows})
    snrs = sorted({row["snr_db"] for row in rows})
    fig, axis = plt.subplots(figsize=(10, 6))
    for snr in snrs:
        for key, label, marker in (
            ("energy_detection_rate", "Energy", "o"),
            ("matched_filter_detection_rate", "Matched filter", "s"),
        ):
            subset = sorted(
                (row for row in rows if row["snr_db"] == snr),
                key=lambda row: row["ambient_amplitude"],
            )
            x = [row["ambient_amplitude"] for row in subset]
            y = [row[key] for row in subset]
            low_key = "energy_ci95_low" if key == "energy_detection_rate" else "matched_filter_ci95_low"
            high_key = "energy_ci95_high" if key == "energy_detection_rate" else "matched_filter_ci95_high"
            lower = [max(0.0, value - row[low_key]) for value, row in zip(y, subset)]
            upper = [max(0.0, row[high_key] - value) for value, row in zip(y, subset)]
            axis.errorbar(
                x, y, yerr=[lower, upper], marker=marker, capsize=3,
                label=f"{label}, SNR {snr:g} dB",
            )
    axis.set_xlabel("Sinusoidal interference amplitude (arbitrary units)")
    axis.set_ylabel("Detection probability")
    axis.set_ylim(-0.03, 1.03)
    axis.set_title("Detection vs interference amplitude (simulation)")
    axis.grid(True, alpha=0.3)
    axis.legend(ncol=2, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _plot_false_alarm_summary(path, rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    amplitudes = sorted({row["ambient_amplitude"] for row in rows})
    fig, axis = plt.subplots(figsize=(9, 5))
    for key, label, marker in (
        ("energy_false_alarm_rate_validation", "Energy detector", "o"),
        ("matched_filter_false_alarm_rate_validation", "Matched filter", "s"),
    ):
        means = []
        for amplitude in amplitudes:
            values = [row[key] for row in rows if row["ambient_amplitude"] == amplitude]
            means.append(sum(values) / len(values))
        axis.plot(amplitudes, means, marker=marker, label=label)
    target = rows[0]["target_false_alarm_rate"]
    axis.axhline(target, linestyle="--", linewidth=1, label=f"Target {target:.1%}")
    axis.set_xlabel("Sinusoidal interference amplitude (arbitrary units)")
    axis.set_ylabel("Independently validated false-alarm rate")
    axis.set_ylim(0, 1)
    axis.set_title("False alarms vs interference amplitude (simulation)")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Run an IRIS ambient-interference robustness sweep")
    parser.add_argument("--output", default="5_Simulations/interference_sweep")
    parser.add_argument("--amplitudes", type=float, nargs="+", default=[0.0, 0.1, 0.2, 0.4, 0.8])
    parser.add_argument("--frequency", type=float, default=1000.0)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--calibration-trials", type=int, default=5000)
    parser.add_argument("--validation-trials", type=int, default=5000)
    parser.add_argument("--target-false-alarm", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20261015)
    args = parser.parse_args()
    rows = run_interference_sweep(
        args.output, amplitudes=args.amplitudes, frequency_hz=args.frequency,
        trials=args.trials, calibration_trials=args.calibration_trials,
        validation_trials=args.validation_trials,
        target_false_alarm=args.target_false_alarm, seed=args.seed,
    )
    print(f"Wrote {len(rows)} summary rows to {Path(args.output) / 'interference_sweep.csv'}")
    print("Outputs are simulations, not physical measurements.")


if __name__ == "__main__":
    main()
