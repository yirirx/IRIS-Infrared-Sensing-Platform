# Modulation and Detection

## Energy detector
For samples `x[n]` in an observation window, the energy score is `mean(x[n] ** 2)`. It is simple but ignores the detailed shape of the expected waveform.

## Matched filter
For a known reference `s[n]`, the correlation score is `dot(x, s) / norm(s)`. With known timing and a known reference, correlation can outperform a generic energy score in additive white Gaussian noise. Performance depends on synchronization, noise assumptions, and threshold selection.

This is an introductory description of the simulation, not a complete optical receiver design.
