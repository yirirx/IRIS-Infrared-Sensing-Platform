"""Simple gain and additive-white-Gaussian-noise channel model."""
import numpy as np

def add_noise(signal, snr_db, gain=1.0, rng=None):
    """Apply scalar gain and Gaussian noise using signal-power SNR in dB."""
    x = np.asarray(signal, dtype=float) * gain
    if x.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    rng = np.random.default_rng() if rng is None else rng
    power = float(np.mean(x**2))
    if power <= 0:
        return x.copy()
    noise_power = power / (10.0 ** (snr_db / 10.0))
    return x + rng.normal(0.0, np.sqrt(noise_power), size=x.shape)
