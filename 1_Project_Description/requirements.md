# Project Requirements — v0.1 (Draft)

## Purpose
Create a documented platform for studying modulated IR sensing and digital signal detection. The initial milestone must run on a typical laptop.

## Functional requirements
| ID | Requirement | Verification |
|---|---|---|
| FR-01 | Generate a repeatable carrier burst | Unit test and plot |
| FR-02 | Apply gain and controllable noise | Unit test |
| FR-03 | Detect a burst using energy detection | SNR sweep |
| FR-04 | Detect a known burst using matched filtering | SNR sweep |
| FR-05 | Export metrics to CSV | Output-file check |
| FR-06 | Reproduce experiments using a seed | Repeat-run comparison |

## Non-functional requirements
- Python 3.10+; readable modules; automated tests.
- Parameters and model limitations must be documented.
- No unverified claims about physical range or hardware performance.

## Out of scope for v0.1
Distance measurement, thermal imaging, medical diagnosis, custom PCB, calibrated photometry, and claims about physical performance.
