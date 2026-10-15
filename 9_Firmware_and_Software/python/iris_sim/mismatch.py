"""Stress test fixed clean-calibrated thresholds after interference appears."""
import argparse
import csv
from pathlib import Path

import numpy as np

from .detectors import energy_score, matched_filter_score
from .experiment import _score_noise, wilson_interval
from .signal_model import make_burst


def run_mismatched_calibration(output_dir, amplitudes=None, snr_values=None,
                              trials=1000, calibration_trials=5000,
                              validation_trials=5000, target_false_alarm=0.05,
                              frequency_hz=1000.0, seed=20261020):
    """Calibrate thresholds in clean AWGN, then test under interference."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    amplitudes = [0.0, 0.1, 0.2, 0.4, 0.8] if amplitudes is None else list(amplitudes)
    snr_values = [-30, -24, -18] if snr_values is None else list(snr_values)
    if not amplitudes or any(not np.isfinite(a) or a < 0 for a in amplitudes):
        raise ValueError("amplitudes must be finite, non-negative, and non-empty")
    if len(set(amplitudes)) != len(amplitudes):
        raise ValueError("amplitudes must be unique")
    if not snr_values or trials < 1 or calibration_trials < 100 or validation_trials < 100:
        raise ValueError("snr_values must be non-empty; trials positive; calibration/validation >= 100")
    if not 0 < target_false_alarm < 1:
        raise ValueError("target_false_alarm must be between 0 and 1")
    if not np.isfinite(frequency_hz) or not 0 <= frequency_hz < 50000:
        raise ValueError("frequency_hz must be in [0, 50000)")

    rng = np.random.default_rng(seed)
    _, reference = make_burst()
    energy_cal, matched_cal = _score_noise(rng, calibration_trials, reference)
    energy_threshold = float(np.quantile(energy_cal, 1-target_false_alarm, method="higher"))
    matched_threshold = float(np.quantile(matched_cal, 1-target_false_alarm, method="higher"))
    ref_power = float(np.mean(reference**2))
    time_s = np.arange(reference.size, dtype=float) / 100000
    rows = []
    for i, amplitude in enumerate(amplitudes):
        e_val, m_val = _score_noise(
            rng, validation_trials, reference, ambient_amplitude=amplitude,
            ambient_frequency_hz=frequency_hz,
        )
        e_false = int(np.count_nonzero(e_val > energy_threshold))
        m_false = int(np.count_nonzero(m_val > matched_threshold))
        e_pfa_ci = wilson_interval(e_false, validation_trials)
        m_pfa_ci = wilson_interval(m_false, validation_trials)
        for snr_db in snr_values:
            clean = reference * np.sqrt((10.0 ** (float(snr_db)/10.0)) / ref_power)
            e_hits = m_hits = 0
            for _ in range(trials):
                received = clean + rng.normal(0.0, 1.0, size=reference.size)
                if amplitude:
                    phase = rng.uniform(0.0, 2*np.pi)
                    received += amplitude * np.cos(2*np.pi*frequency_hz*time_s + phase)
                e_hits += energy_score(received) > energy_threshold
                m_hits += matched_filter_score(received, reference) > matched_threshold
            e_ci = wilson_interval(e_hits, trials)
            m_ci = wilson_interval(m_hits, trials)
            rows.append({
                "calibration_condition": "clean_AWGN_only",
                "test_ambient_amplitude": amplitude,
                "ambient_frequency_hz": frequency_hz,
                "snr_db": float(snr_db),
                "trials": trials,
                "energy_detection_rate": e_hits/trials,
                "energy_ci95_low": e_ci[0], "energy_ci95_high": e_ci[1],
                "matched_filter_detection_rate": m_hits/trials,
                "matched_filter_ci95_low": m_ci[0], "matched_filter_ci95_high": m_ci[1],
                "energy_false_alarm_rate_validation": e_false/validation_trials,
                "energy_false_alarm_ci95_low": e_pfa_ci[0],
                "energy_false_alarm_ci95_high": e_pfa_ci[1],
                "matched_filter_false_alarm_rate_validation": m_false/validation_trials,
                "matched_filter_false_alarm_ci95_low": m_pfa_ci[0],
                "matched_filter_false_alarm_ci95_high": m_pfa_ci[1],
                "target_false_alarm_rate": target_false_alarm,
                "energy_threshold_clean": energy_threshold,
                "matched_filter_threshold_clean": matched_threshold,
                "calibration_trials": calibration_trials,
                "validation_trials": validation_trials,
                "seed": seed,
                "result_type": "simulation_not_measurement",
            })
    path = output_dir / "mismatched_calibration.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    _plot_mismatch(output_dir / "false_alarm_after_environment_change.png", rows)
    return rows


def _plot_mismatch(path, rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    amplitudes = sorted({r["test_ambient_amplitude"] for r in rows})
    fig, axis = plt.subplots(figsize=(9, 5))
    for key, low, high, label, marker in (
        ("energy_false_alarm_rate_validation", "energy_false_alarm_ci95_low",
         "energy_false_alarm_ci95_high", "Energy detector", "o"),
        ("matched_filter_false_alarm_rate_validation", "matched_filter_false_alarm_ci95_low",
         "matched_filter_false_alarm_ci95_high", "Matched filter", "s"),
    ):
        subset = [next(r for r in rows if r["test_ambient_amplitude"] == a) for a in amplitudes]
        y = [r[key] for r in subset]
        lower = [max(0, v-r[low]) for v,r in zip(y,subset)]
        upper = [max(0, r[high]-v) for v,r in zip(y,subset)]
        axis.errorbar(amplitudes,y,yerr=[lower,upper],marker=marker,capsize=3,label=label)
    axis.axhline(rows[0]["target_false_alarm_rate"],linestyle="--",label="Target Pfa")
    axis.set_xlabel("Interference amplitude at test time (arbitrary units)")
    axis.set_ylabel("False-alarm rate with clean-calibrated threshold")
    axis.set_ylim(0,1)
    axis.set_title("Threshold mismatch under environmental change (simulation)")
    axis.grid(True,alpha=0.3)
    axis.legend()
    fig.tight_layout()
    fig.savefig(path,dpi=160)
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description="Test clean-calibrated IRIS thresholds under interference")
    parser.add_argument("--output",default="5_Simulations/mismatched_calibration")
    parser.add_argument("--trials",type=int,default=1000)
    parser.add_argument("--calibration-trials",type=int,default=5000)
    parser.add_argument("--validation-trials",type=int,default=5000)
    parser.add_argument("--seed",type=int,default=20261020)
    args=parser.parse_args()
    rows=run_mismatched_calibration(args.output,trials=args.trials,
        calibration_trials=args.calibration_trials,validation_trials=args.validation_trials,seed=args.seed)
    print(f"Wrote {len(rows)} rows to {Path(args.output)/'mismatched_calibration.csv'}")
    print("Simulation only; thresholds are calibrated under clean AWGN and tested with optional interference.")


if __name__ == "__main__":
    main()
