import numpy as np
from iris_sim.channel import add_noise

def test_seed_reproducibility():
    s=np.ones(100); a=add_noise(s,5,rng=np.random.default_rng(123)); b=add_noise(s,5,rng=np.random.default_rng(123)); assert np.allclose(a,b)
