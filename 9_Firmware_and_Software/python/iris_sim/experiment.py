"""Monte Carlo experiment comparing simple IR burst detectors."""
import csv
from pathlib import Path
import numpy as np
from .channel import add_noise
from .detectors import energy_score, matched_filter_score
from .signal_model import make_burst

def run_experiment(output_dir, seed=20261013, trials=300, snr_values=None):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    if trials < 1:
        raise ValueError("trials must be positive")
    snr_values = list(range(-12, 13, 3)) if snr_values is None else list(snr_values)
    if not snr_values:
        raise ValueError("snr_values must not be empty")
    rng = np.random.default_rng(seed)
    t, ref = make_burst()
    cal_n = max(500, trials)
    noise_cal = [rng.normal(0, 1, ref.size) for _ in range(cal_n)]
    e_thr = float(np.quantile([energy_score(x) for x in noise_cal], .95))
    m_thr = float(np.quantile([matched_filter_score(x, ref) for x in noise_cal], .95))
    rows=[]; example=None
    for snr in snr_values:
        eh=mh=ef=mf=0
        for _ in range(trials):
            received=add_noise(ref, snr, rng=rng)
            eh += energy_score(received) > e_thr
            mh += matched_filter_score(received, ref) > m_thr
            noise_only=rng.normal(0, 1, ref.size)
            ef += energy_score(noise_only) > e_thr
            mf += matched_filter_score(noise_only, ref) > m_thr
            if example is None: example=received
        rows.append({'snr_db':snr,'trials':trials,'energy_detection_rate':eh/trials,
                     'matched_filter_detection_rate':mh/trials,'energy_false_alarm_rate':ef/trials,
                     'matched_filter_false_alarm_rate':mf/trials,'seed':seed})
    with (output_dir/'metrics.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)
    _plot_waveform(output_dir/'waveform.png',t,ref,example)
    _plot_sweep(output_dir/'detection_sweep.png',rows)
    return rows

def _plot_waveform(path,t,ref,received):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,1,figsize=(10,6),sharex=True)
    axes[0].plot(t*1000,ref,linewidth=1); axes[0].set_title('Reference burst (simulation)'); axes[0].set_ylabel('Amplitude (a.u.)')
    axes[1].plot(t*1000,received,linewidth=.8); axes[1].set_title('Received waveform with simulated noise'); axes[1].set_xlabel('Time (ms)'); axes[1].set_ylabel('Amplitude (a.u.)')
    for ax in axes: ax.grid(True,alpha=.25)
    fig.tight_layout(); fig.savefig(path,dpi=160); plt.close(fig)

def _plot_sweep(path,rows):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    x=[r['snr_db'] for r in rows]; fig,ax=plt.subplots(figsize=(9,5))
    ax.plot(x,[r['energy_detection_rate'] for r in rows],'o-',label='Energy detector')
    ax.plot(x,[r['matched_filter_detection_rate'] for r in rows],'s-',label='Matched filter')
    ax.set_xlabel('SNR (dB, simulation parameter)'); ax.set_ylabel('Detection rate'); ax.set_ylim(-.03,1.03)
    ax.set_title('Detection rate versus SNR — simulated trials'); ax.grid(True,alpha=.3); ax.legend()
    fig.tight_layout(); fig.savefig(path,dpi=160); plt.close(fig)
