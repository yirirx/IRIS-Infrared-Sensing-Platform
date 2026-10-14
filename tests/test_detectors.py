import numpy as np
import pytest
from iris_sim.detectors import energy_score,matched_filter_score

def test_energy_score(): assert energy_score(np.array([-1.,1.]))==pytest.approx(1.)
def test_matched_filter_alignment():
    ref=np.array([0.,1.,0.,-1.]); assert matched_filter_score(ref,ref)>matched_filter_score(-ref,ref)
def test_shape_mismatch():
    with pytest.raises(ValueError): matched_filter_score(np.ones(3),np.ones(4))
