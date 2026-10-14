"""Command-line entry point for IRIS experiments."""
import argparse
from pathlib import Path
from .experiment import run_experiment


def main():
    parser = argparse.ArgumentParser(description="Run the IRIS simulated IR detection experiment")
    parser.add_argument("--output", default="5_Simulations/results", help="directory for CSV and plots")
    parser.add_argument("--trials", type=int, default=1000, help="signal-present Monte Carlo trials per SNR")
    parser.add_argument("--seed", type=int, default=20261014, help="random seed")
    parser.add_argument("--calibration-trials", type=int, default=5000, help="noise-only threshold-calibration windows")
    parser.add_argument("--validation-trials", type=int, default=5000, help="independent noise-only validation windows")
    parser.add_argument("--target-false-alarm", type=float, default=0.05, help="target false-alarm probability")
    args = parser.parse_args()
    rows = run_experiment(
        Path(args.output), trials=args.trials, seed=args.seed,
        calibration_trials=args.calibration_trials,
        validation_trials=args.validation_trials,
        target_false_alarm=args.target_false_alarm,
    )
    print(f"Wrote {len(rows)} SNR points to {args.output}")
    print(f"Thresholds: energy={rows[0]['energy_threshold']:.6f}, matched_filter={rows[0]['matched_filter_threshold']:.6f}")
    print("Outputs are simulations, not physical measurements.")


if __name__ == "__main__":
    main()
