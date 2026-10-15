# Simplified ambient-light flicker interference model

## Purpose
IRIS includes a small utility to add a sinusoidal disturbance to a sampled waveform. It enables controlled software stress tests before interference is integrated into the primary detection experiment.

## Model
For samples at times t[n] = n / fs, the utility adds

i[n] = A cos(2 pi f t[n] + phi)

to the input x[n], producing y[n] = x[n] + i[n]. Here A is an arbitrary amplitude in the same units as the input waveform, f is the chosen interference frequency, fs is the sample rate, and phi is a specified phase.

## Why use this model?
It is a transparent first approximation for periodic interference. It lets us test whether software handles a nuisance component and explore sensitivity to its amplitude and frequency.

## Important limitations
- The amplitude is not derived from illuminance, optical power, photodiode responsivity, or receiver gain.
- Real ambient-light effects can include a DC component, mains-related flicker, switching-lighting harmonics, shot noise, saturation, and analogue-front-end behavior.
- The utility does not model those effects and does not claim that any selected frequency or amplitude represents a particular real environment.
- The primary Monte Carlo experiment currently uses its original AWGN-only model. This helper is not yet connected to threshold calibration or detector performance sweeps.

## Next experiment
Integrate the disturbance into noise-only calibration, independent false-alarm validation, and signal-present trials consistently. Compare detectors at the same stated interference conditions and clearly label the outputs as simulation. Do not compare thresholds calibrated under different conditions as though they were directly equivalent.
