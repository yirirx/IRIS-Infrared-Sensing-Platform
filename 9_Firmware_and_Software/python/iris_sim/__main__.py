"""Command-line entry point for IRIS simulation experiments."""
import argparse
from .experiment import run_experiment


def main():
    parser = argparse.ArgumentParser(description="Run reproducible IRIS IR-detection simulations")
    parser.add_argument("--output", default="5_Simulations/results", help="output directory")
    parser.add_argument("--seed", type=int, default=20261014, help="random seed")
    parser.add_argument("--trials", type=int, default=1000, help="signal-present trials per SNR")
    parser.add_argument("--calibration-trials", type=int, default=5000, help="noise-only threshold-calibration records")
    parser.add_argument("--validation-trials", type=int, default=5000, help="independent noise-only validation records")
    parser.add_argument("--target-false-alarm", type=float, default=0.05, help="target false-alarm probability")
    parser.add_argument("--roc-snr", type=float, default=-24, help="SNR point for empirical ROC curve")
    parser.add_argument("--ambient-amplitude", type=float, default=0.0,
                        help="sinusoidal interference amplitude in arbitrary signal units (0 disables)")
    parser.add_argument("--ambient-frequency", type=float, default=50.0,
                        help="sinusoidal interference frequency in Hz (below 50 kHz)")
    args = parser.parse_args()
    rows = run_experiment(args.output, seed=args.seed, trials=args.trials,
                          calibration_trials=args.calibration_trials,
                          validation_trials=args.validation_trials,
                          target_false_alarm=args.target_false_alarm,
                          roc_snr_db=args.roc_snr,
                          ambient_amplitude=args.ambient_amplitude,
                          ambient_frequency_hz=args.ambient_frequency)
    print(f"Wrote {len(rows)} SNR points to {args.output}")
    print("Outputs are simulations, not physical measurements.")


if __name__ == "__main__":
    main()
