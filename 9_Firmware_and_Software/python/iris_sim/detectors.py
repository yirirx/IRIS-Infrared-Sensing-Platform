"""Detection scores used in the initial simulation."""
import numpy as np

def energy_score(samples):
    x = np.asarray(samples, dtype=float)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("samples must be a non-empty one-dimensional array")
    return float(np.mean(x**2))

def matched_filter_score(samples, reference):
    x = np.asarray(samples, dtype=float)
    s = np.asarray(reference, dtype=float)
    if x.ndim != 1 or s.ndim != 1 or x.shape != s.shape:
        raise ValueError("samples and reference must be 1-D arrays of equal shape")
    norm = float(np.linalg.norm(s))
    if norm == 0:
        raise ValueError("reference must not be all zeros")
    return float(np.dot(x, s) / norm)
