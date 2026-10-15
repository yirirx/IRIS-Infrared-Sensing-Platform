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


def add_ambient_flicker(signal, sample_rate_hz, amplitude, frequency_hz, phase_rad=0.0):
    """Add a sinusoidal interference term as a simplified ambient-light flicker model.

    Amplitude is in the same arbitrary units as the input signal. This is a
    phenomenological stress-test utility, not a calibrated optical model.
    """
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")
    if amplitude < 0:
        raise ValueError("amplitude must be non-negative")
    if frequency_hz < 0 or frequency_hz >= sample_rate_hz / 2:
        raise ValueError("frequency_hz must be non-negative and below Nyquist")
    if not np.isfinite(phase_rad):
        raise ValueError("phase_rad must be finite")
    t = np.arange(x.size, dtype=float) / sample_rate_hz
    interference = amplitude * np.cos(2.0 * np.pi * frequency_hz * t + phase_rad)
    return x + interference
