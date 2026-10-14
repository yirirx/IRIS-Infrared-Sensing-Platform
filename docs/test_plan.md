# Test Plan

| ID | Test | Expected result |
|---|---|---|
| T-01 | Generate burst | Matching time/signal array shapes and nonzero burst |
| T-02 | Invalid Nyquist parameters | Clear `ValueError` |
| T-03 | Energy score | Non-negative score for real-valued samples |
| T-04 | Matched-filter alignment | Aligned reference scores above inverted reference |
| T-05 | Seed determinism | Same seed gives same noise samples |
| T-06 | Wilson interval | Valid interval contains observed proportion |
| T-07 | Experiment output | CSV and both PNG files are created |
| T-08 | Output provenance | CSV explicitly marks results as simulation, not measurement |
| T-09 | Independent false-alarm validation | False-alarm rate is measured on noise samples not used to set thresholds |

Run `pytest` from the repository root. Monte Carlo tests use reduced trial counts for speed; the documented baseline uses larger trial counts.
