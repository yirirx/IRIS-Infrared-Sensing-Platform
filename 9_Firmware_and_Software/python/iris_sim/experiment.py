"""Monte Carlo experiment with independent threshold calibration and validation."""
import csv
from pathlib import Path
import numpy as np
from .detectors import energy_score, matched_filter_score
from .signal_model import make_burst


def wilson_interval(successes, trials, z=1.96):
    """Return a two-sided Wilson score interval for a binomial proportion."""
    if trials <= 0 or not 0 <= successes <= trials:
        raise ValueError("require trials > 0 and 0 <= successes <= trials")
    p = successes / trials
    z2 = z * z
    denom = 1 + z2 / trials
    centre = (p + z2 / (2 * trials)) / denom
    half = z * np.sqrt(p * (1 - p) / trials + z2 / (4 * trials**2)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def _noise_scores(rng, count, sample_count, reference, batch_size=256):
    """Generate noise-only detector scores in batches to bound memory use."""
    energy, matched = [], []
    ref_norm = float(np.linalg.norm(reference))
    remaining = count
    while remaining:
        batch = min(batch_size, remaining)
        noise = rng.normal(0.0, 1.0, size=(batch, sample_count))
        energy.extend(np.mean(noise * noise, axis=1).tolist())
        matched.extend((noise @ reference / ref_norm).tolist())
        remaining -= batch
    return np.asarray(energy), np.asarray(matched)


def run_experiment(
    output_dir,
    seed=20261014,
    trials=1000,
    snr_values=None,
    calibration_trials=5000,
    validation_trials=5000,
    target_false_alarm=0.05,
):
    """Run a fixed-noise-variance SNR sweep with independent calibration.

    SNR is defined as mean(clean_signal**2) / noise_variance across the full
    observation window. Thresholds are calibrated once from noise-only data,
    then evaluated on separate noise-only validation trials. The simulated
    channel is AWGN only; it is not a calibrated optical or hardware model.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    if trials < 1 or calibration_trials < 100 or validation_trials < 100:
        raise ValueError("trials must be positive; calibration/validation need at least 100")
    if not 0.0 < target_false_alarm < 1.0:
        raise ValueError("target_false_alarm must be between 0 and 1")
    snr_values = list(range(-36, 1, 3)) if snr_values is None else list(snr_values)
    if not snr_values:
        raise ValueError("snr_values must not be empty")

    rng = np.random.default_rng(seed)
    time_s, reference = make_burst()
    energy_cal, matched_cal = _noise_scores(rng, calibration_trials, reference.size, reference)
    energy_threshold = float(np.quantile(energy_cal, 1 - target_false_alarm, method="higher"))
    matched_threshold = float(np.quantile(matched_cal, 1 - target_false_alarm, method="higher"))
    energy_val, matched_val = _noise_scores(rng, validation_trials, reference.size, reference)
    energy_false = int(np.count_nonzero(energy_val > energy_threshold))
    matched_false = int(np.count_nonzero(matched_val > matched_threshold))
    energy_pfa_ci = wilson_interval(energy_false, validation_trials)
    matched_pfa_ci = wilson_interval(matched_false, validation_trials)

    reference_power = float(np.mean(reference**2))
    rows = []
    example_received = None
    for snr_db in snr_values:
        signal_power = 10 ** (float(snr_db) / 10.0)
        clean = reference * np.sqrt(signal_power / reference_power)
        energy_hits = matched_hits = 0
        for _ in range(trials):
            received = clean + rng.normal(0.0, 1.0, size=reference.size)
            energy_hits += energy_score(received) > energy_threshold
            matched_hits += matched_filter_score(received, reference) > matched_threshold
            if example_received is None:
                example_received = received.copy()
        e_ci = wilson_interval(energy_hits, trials)
        m_ci = wilson_interval(matched_hits, trials)
        rows.append({
            "snr_db": float(snr_db),
            "trials": trials,
            "energy_detection_rate": energy_hits / trials,
            "energy_ci95_low": e_ci[0],
            "energy_ci95_high": e_ci[1],
            "matched_filter_detection_rate": matched_hits / trials,
            "matched_filter_ci95_low": m_ci[0],
            "matched_filter_ci95_high": m_ci[1],
            "energy_false_alarm_rate_validation": energy_false / validation_trials,
            "energy_false_alarm_ci95_low": energy_pfa_ci[0],
            "energy_false_alarm_ci95_high": energy_pfa_ci[1],
            "matched_filter_false_alarm_rate_validation": matched_false / validation_trials,
            "matched_filter_false_alarm_ci95_low": matched_pfa_ci[0],
            "matched_filter_false_alarm_ci95_high": matched_pfa_ci[1],
            "target_false_alarm_rate": target_false_alarm,
            "energy_threshold": energy_threshold,
            "matched_filter_threshold": matched_threshold,
            "calibration_trials": calibration_trials,
            "validation_trials": validation_trials,
            "seed": seed,
            "noise_model": "unit-variance AWGN",
            "result_type": "simulation_not_measurement",
        })

    csv_fields = [
        "snr_db", "trials", "energy_detection_rate", "energy_ci95_low", "energy_ci95_high",
        "matched_filter_detection_rate", "matched_filter_ci95_low", "matched_filter_ci95_high",
        "energy_false_alarm_rate_validation", "matched_filter_false_alarm_rate_validation",
        "target_false_alarm_rate", "calibration_trials", "validation_trials", "seed", "noise_model", "result_type",
    ]
    with (output_dir / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows({key: row[key] for key in csv_fields} for row in rows)
    _plot_waveform(output_dir / "waveform.png", time_s, reference, example_received)
    _plot_sweep(output_dir / "detection_sweep.png", rows)
    return rows


def _plot_waveform(path, time_s, reference, received):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    axes[0].plot(time_s * 1000, reference, linewidth=1)
    axes[0].set_title("Reference burst (simulation; arbitrary amplitude)")
    axes[0].set_ylabel("Amplitude (a.u.)")
    axes[1].plot(time_s * 1000, received, linewidth=0.8)
    axes[1].set_title("Received burst with fixed-variance simulated AWGN")
    axes[1].set_xlabel("Time (ms)")
    axes[1].set_ylabel("Amplitude (a.u.)")
    for axis in axes:
        axis.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _plot_sweep(path, rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    x = [row["snr_db"] for row in rows]
    fig, axis = plt.subplots(figsize=(9, 5))
    for key, low, high, label, marker in (
        ("energy_detection_rate", "energy_ci95_low", "energy_ci95_high", "Energy detector", "o"),
        ("matched_filter_detection_rate", "matched_filter_ci95_low", "matched_filter_ci95_high", "Matched filter", "s"),
    ):
        y = np.asarray([row[key] for row in rows])
        lower = y - np.asarray([row[low] for row in rows])
        upper = np.asarray([row[high] for row in rows]) - y
        axis.errorbar(x, y, yerr=np.vstack([lower, upper]), marker=marker, capsize=3, label=label)
    axis.set_xlabel("SNR (dB; mean signal power / noise variance)")
    axis.set_ylabel("Detection probability")
    axis.set_ylim(-0.03, 1.03)
    axis.set_title("Detection probability vs SNR — AWGN simulation")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
