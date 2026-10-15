"""Repeated-seed stability check for the fixed-threshold mismatch experiment."""
import argparse
import csv
import tempfile
from pathlib import Path

import numpy as np

from .mismatch import run_mismatched_calibration


def run_seed_stability(output_dir, seeds=None, amplitudes=None, snr_values=None,
                       trials=1000, calibration_trials=5000, validation_trials=5000):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    seeds = [20261020, 20261021, 20261022, 20261023, 20261024] if seeds is None else list(seeds)
    amplitudes = [0.0, 0.1, 0.2, 0.4, 0.8] if amplitudes is None else list(amplitudes)
    snr_values = [-30, -24, -18] if snr_values is None else list(snr_values)
    if not seeds or len(set(seeds)) != len(seeds):
        raise ValueError("seeds must be a non-empty list of unique values")
    if any(not isinstance(seed, int) for seed in seeds):
        raise ValueError("seeds must be integers")

    records = []
    with tempfile.TemporaryDirectory(prefix="iris_seed_runs_") as temp:
        for seed in seeds:
            rows = run_mismatched_calibration(
                Path(temp) / f"seed_{seed}", amplitudes=amplitudes,
                snr_values=snr_values, trials=trials,
                calibration_trials=calibration_trials,
                validation_trials=validation_trials, seed=seed,
            )
            for row in rows:
                records.append(row)

    summary = []
    for amplitude in sorted(set(float(a) for a in amplitudes)):
        for detector, key in (
            ("Energy detector", "energy_false_alarm_rate_validation"),
            ("Matched filter", "matched_filter_false_alarm_rate_validation"),
        ):
            values = [
                float(row[key]) for row in records
                if float(row["test_ambient_amplitude"]) == amplitude
                and row["calibration_condition"] == "clean_AWGN_only"
                and float(row["snr_db"]) == float(snr_values[0])
            ]
            summary.append({
                "test_ambient_amplitude": amplitude,
                "detector": detector,
                "target_false_alarm_rate": 0.05,
                "seed_count": len(values),
                "mean_false_alarm_rate": float(np.mean(values)),
                "std_false_alarm_rate_across_seeds": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
                "min_false_alarm_rate": float(np.min(values)),
                "max_false_alarm_rate": float(np.max(values)),
                "seeds": ";".join(str(seed) for seed in seeds),
                "result_type": "simulation_not_measurement",
            })

    path = output_dir / "seed_stability.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    _plot_seed_stability(output_dir / "seed_stability.png", summary)
    return summary


def _plot_seed_stability(path, summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axis = plt.subplots(figsize=(9, 5))
    for detector, marker in (("Energy detector", "o"), ("Matched filter", "s")):
        rows = [r for r in summary if r["detector"] == detector]
        x = [r["test_ambient_amplitude"] for r in rows]
        y = [r["mean_false_alarm_rate"] for r in rows]
        err = [r["std_false_alarm_rate_across_seeds"] for r in rows]
        axis.errorbar(x, y, yerr=err, marker=marker, capsize=3, label=detector)
    axis.axhline(0.05, linestyle="--", label="Target Pfa = 5%")
    axis.set_xlabel("Interference amplitude (arbitrary units)")
    axis.set_ylabel("Mean false-alarm rate across seeds")
    axis.set_ylim(0, 1.05)
    axis.set_title("Seed stability of clean-calibrated thresholds (simulation)")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Check IRIS mismatch results across random seeds")
    parser.add_argument("--output", default="5_Simulations/seed_stability")
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--calibration-trials", type=int, default=5000)
    parser.add_argument("--validation-trials", type=int, default=5000)
    parser.add_argument("--seeds", type=int, nargs="+", default=[20261020, 20261021, 20261022, 20261023, 20261024])
    args = parser.parse_args()
    rows = run_seed_stability(args.output, seeds=args.seeds, trials=args.trials,
                              calibration_trials=args.calibration_trials,
                              validation_trials=args.validation_trials)
    print(f"Wrote {len(rows)} summary rows to {Path(args.output) / 'seed_stability.csv'}")
    print("Summary reports between-seed variation; simulation only.")


if __name__ == "__main__":
    main()
