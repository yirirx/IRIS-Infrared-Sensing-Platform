import numpy as np
import pytest
from iris_sim.channel import add_noise, add_ambient_flicker

def test_seed_reproducibility():
    s=np.ones(100); a=add_noise(s,5,rng=np.random.default_rng(123)); b=add_noise(s,5,rng=np.random.default_rng(123)); assert np.allclose(a,b)

def test_ambient_flicker_zero_amplitude_preserves_signal():
    signal = np.linspace(-1, 1, 100)
    result = add_ambient_flicker(signal, 1000, amplitude=0, frequency_hz=50)
    assert np.allclose(result, signal)

def test_ambient_flicker_is_deterministic_and_bounded():
    signal = np.zeros(1000)
    a = add_ambient_flicker(signal, 1000, amplitude=0.3, frequency_hz=50, phase_rad=0.2)
    b = add_ambient_flicker(signal, 1000, amplitude=0.3, frequency_hz=50, phase_rad=0.2)
    assert np.allclose(a, b)
    assert np.isclose(np.max(np.abs(a)), 0.3)

@pytest.mark.parametrize("kwargs", [
    {"sample_rate_hz": 0, "amplitude": 1, "frequency_hz": 10},
    {"sample_rate_hz": 100, "amplitude": -1, "frequency_hz": 10},
    {"sample_rate_hz": 100, "amplitude": 1, "frequency_hz": 50},
])
def test_ambient_flicker_rejects_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        add_ambient_flicker(np.zeros(10), **kwargs)
