import numpy as np
import pytest
from iris_sim.signal_model import make_burst

def test_signal_shape_and_quiet_region():
    t,s=make_burst(); assert t.shape==s.shape; assert np.any(s!=0); assert np.all(s[t<.004]==0)
def test_nyquist_validation():
    with pytest.raises(ValueError): make_burst(sample_rate_hz=10_000,carrier_hz=6_000)
