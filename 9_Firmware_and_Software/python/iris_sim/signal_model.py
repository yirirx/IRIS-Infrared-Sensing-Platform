"""Reference signal generation for the first IRIS simulation milestone."""
import numpy as np

def make_burst(sample_rate_hz=100_000, carrier_hz=5_000, duration_s=0.02,
               burst_start_s=0.005, burst_duration_s=0.008, amplitude=1.0):
    """Return time and an on/off-keyed sinusoidal burst (illustrative units)."""
    if sample_rate_hz <= 0 or carrier_hz <= 0 or duration_s <= 0:
        raise ValueError("sample rate, carrier frequency, and duration must be positive")
    if carrier_hz >= sample_rate_hz / 2:
        raise ValueError("carrier frequency must be below Nyquist frequency")
    if burst_start_s < 0 or burst_duration_s <= 0:
        raise ValueError("burst start must be non-negative and duration positive")
    n = int(round(sample_rate_hz * duration_s))
    t = np.arange(n, dtype=float) / sample_rate_hz
    gate = (t >= burst_start_s) & (t < burst_start_s + burst_duration_s)
    signal = np.zeros(n, dtype=float)
    signal[gate] = amplitude * np.sin(2 * np.pi * carrier_hz * t[gate])
    return t, signal
