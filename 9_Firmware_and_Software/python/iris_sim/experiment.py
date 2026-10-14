"""Reproducible Monte Carlo experiments for IR burst detection."""
import csv
from pathlib import Path
import numpy as np
from .detectors import energy_score, matched_filter_score
from .signal_model import make_burst


def wilson_interval(successes, trials, z=1.96):
    """Two-sided Wilson score interval for a binomial proportion."""
    if trials <= 0 or not 0 <= successes <= trials:
        raise ValueError("require trials > 0 and 0 <= successes <= trials")
    p = successes / trials
    z2 = z * z
    denominator = 1 + z2 / trials
    centre = (p + z2 / (2 * trials)) / denominator
    half = z * np.sqrt(p * (1 - p) / trials + z2 / (4 * trials**2)) / denominator
    return max(0.0, centre - half), min(1.0, centre + half)


def _score_noise(rng, count, reference, batch_size=256):
    """Score noise-only records in batches so memory use stays bounded."""
    energy_scores, matched_scores = [], []
    norm = float(np.linalg.norm(reference))
    remaining = count
    while remaining:
        n = min(batch_size, remaining)
        noise = rng.normal(0.0, 1.0, size=(n, reference.size))
        energy_scores.extend(np.mean(noise**2, axis=1).tolist())
        matched_scores.extend((noise @ reference / norm).tolist())
        remaining -= n
    return np.asarray(energy_scores), np.asarray(matched_scores)


def _roc_points(noise_scores, signal_scores, points=101):
    """Empirical ROC coordinates with threshold sweep; includes endpoints."""
    combined = np.concatenate([noise_scores, signal_scores])
    thresholds = np.quantile(combined, np.linspace(0.0, 1.0, points))
    pfa = np.array([np.mean(noise_scores > t) for t in thresholds])
    pd = np.array([np.mean(signal_scores > t) for t in thresholds])
    order = np.argsort(pfa)
    return pfa[order], pd[order]


def run_experiment(output_dir, seed=20261014, trials=1000, snr_values=None,
                   calibration_trials=5000, validation_trials=5000,
                   target_false_alarm=0.05, roc_snr_db=-24):
    """Run fixed-noise-variance SNR sweep with independent threshold calibration.

    SNR is mean(clean_signal**2) / noise_variance over the complete observation
    window. Thresholds are calibrated on noise-only records and assessed on an
    independent noise-only validation set. The channel is AWGN only.
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
    ref_power = float(np.mean(reference**2))
    if ref_power <= 0:
        raise ValueError("reference signal must have nonzero power")

    energy_cal, matched_cal = _score_noise(rng, calibration_trials, reference)
    energy_threshold = float(np.quantile(energy_cal, 1-target_false_alarm, method="higher"))
    matched_threshold = float(np.quantile(matched_cal, 1-target_false_alarm, method="higher"))
    energy_val, matched_val = _score_noise(rng, validation_trials, reference)
    energy_false = int(np.count_nonzero(energy_val > energy_threshold))
    matched_false = int(np.count_nonzero(matched_val > matched_threshold))
    energy_pfa_ci = wilson_interval(energy_false, validation_trials)
    matched_pfa_ci = wilson_interval(matched_false, validation_trials)

    rows = []
    example_received = None
    roc_signal_energy = roc_signal_matched = None
    for snr_db in snr_values:
        signal_power = 10.0 ** (float(snr_db) / 10.0)
        clean = reference * np.sqrt(signal_power / ref_power)
        energy_hits = matched_hits = 0
        signal_energy_scores, signal_matched_scores = [], []
        for _ in range(trials):
            received = clean + rng.normal(0.0, 1.0, size=reference.size)
            e_score = energy_score(received)
            m_score = matched_filter_score(received, reference)
            energy_hits += e_score > energy_threshold
            matched_hits += m_score > matched_threshold
            if float(snr_db) == float(roc_snr_db):
                signal_energy_scores.append(e_score)
                signal_matched_scores.append(m_score)
            if example_received is None:
                example_received = received.copy()
        e_ci = wilson_interval(energy_hits, trials)
        m_ci = wilson_interval(matched_hits, trials)
        rows.append({
            "snr_db": float(snr_db), "trials": trials,
            "energy_detection_rate": energy_hits / trials,
            "energy_ci95_low": e_ci[0], "energy_ci95_high": e_ci[1],
            "matched_filter_detection_rate": matched_hits / trials,
            "matched_filter_ci95_low": m_ci[0], "matched_filter_ci95_high": m_ci[1],
            "energy_false_alarm_rate_validation": energy_false / validation_trials,
            "energy_false_alarm_ci95_low": energy_pfa_ci[0], "energy_false_alarm_ci95_high": energy_pfa_ci[1],
            "matched_filter_false_alarm_rate_validation": matched_false / validation_trials,
            "matched_filter_false_alarm_ci95_low": matched_pfa_ci[0], "matched_filter_false_alarm_ci95_high": matched_pfa_ci[1],
            "target_false_alarm_rate": target_false_alarm,
            "energy_threshold": energy_threshold, "matched_filter_threshold": matched_threshold,
            "calibration_trials": calibration_trials, "validation_trials": validation_trials,
            "seed": seed, "noise_model": "unit-variance AWGN", "result_type": "simulation_not_measurement",
        })

        if float(snr_db) == float(roc_snr_db):
            roc_signal_energy = np.asarray(signal_energy_scores)
            roc_signal_matched = np.asarray(signal_matched_scores)

    fields = list(rows[0].keys())
    with (output_dir / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    if roc_signal_energy is not None and len(roc_signal_energy):
        epfa, epd = _roc_points(energy_val, roc_signal_energy)
        mpfa, mpd = _roc_points(matched_val, roc_signal_matched)
        with (output_dir / "roc_curve.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["energy_false_alarm_rate", "energy_detection_probability",
                             "matched_filter_false_alarm_rate", "matched_filter_detection_probability",
                             "roc_snr_db", "result_type"])
            for i in range(max(len(epfa), len(mpfa))):
                writer.writerow([epfa[i], epd[i], mpfa[i], mpd[i], roc_snr_db, "simulation_not_measurement"])
        _plot_roc(output_dir / "roc_curve.png", epfa, epd, mpfa, mpd, roc_snr_db)
    else:
        (output_dir / "roc_curve.csv").write_text(
            "ROC not generated: roc_snr_db must be included in snr_values.\n", encoding="utf-8"
        )
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


def _plot_roc(path, energy_pfa, energy_pd, matched_pfa, matched_pd, snr_db):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axis = plt.subplots(figsize=(7, 6))
    axis.plot(energy_pfa, energy_pd, label="Energy detector")
    axis.plot(matched_pfa, matched_pd, label="Matched filter")
    axis.plot([0, 1], [0, 1], linestyle="--", linewidth=1, label="No-discrimination reference")
    axis.set(xlabel="False-alarm probability", ylabel="Detection probability", xlim=(0, 1), ylim=(0, 1),
             title=f"Empirical ROC at SNR = {snr_db} dB (simulation)")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
