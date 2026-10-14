"""Command-line entry point for IRIS experiments."""
import argparse
from pathlib import Path
from .experiment import run_experiment

def main():
    parser = argparse.ArgumentParser(description="Run the IRIS simulated IR detection experiment")
    parser.add_argument("--output", default="5_Simulations/results", help="directory for CSV and plots")
    parser.add_argument("--trials", type=int, default=100, help="Monte Carlo trials per SNR")
    parser.add_argument("--seed", type=int, default=20261013, help="random seed")
    args = parser.parse_args()
    rows = run_experiment(Path(args.output), trials=args.trials, seed=args.seed)
    print(f"Wrote simulation outputs for {len(rows)} SNR points to {args.output}")

if __name__ == "__main__":
    main()
