# Test Plan
| ID | Test | Expected result |
|---|---|---|
| T-01 | Generate burst | Matching array shapes and nonzero burst |
| T-02 | Invalid Nyquist parameters | Clear `ValueError` |
| T-03 | Energy score | Non-negative for real-valued samples |
| T-04 | Matched-filter alignment | Aligned reference scores above inverted reference |
| T-05 | Seed determinism | Same seed gives same noisy samples |
| T-06 | CLI run | CSV and two PNG files are produced |

Run `pytest` from the repository root.
