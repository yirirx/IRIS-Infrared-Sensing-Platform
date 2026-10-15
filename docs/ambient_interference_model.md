# Simplified ambient-light flicker interference model

## Purpose
IRIS includes a sinusoidal disturbance model that is integrated as an optional condition in the Monte Carlo experiment. A sweep helper varies its amplitude and exports detection and false-alarm plots for controlled software stress tests.

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
- The Monte Carlo experiment now optionally includes this interference in threshold calibration, independent false-alarm validation, and signal-present trials. The phase is randomized independently for each record. The default remains AWGN-only when the amplitude is zero.

## Next experiment
Run a controlled sweep over several interference amplitudes and frequencies. The amplitude-sweep plot includes Wilson 95% intervals for the detection estimates; these represent Monte Carlo sampling uncertainty only. Calibrate each detector and validate false alarms under the same interference distribution used for signal-present trials. Compare detectors at the same stated conditions and clearly label outputs as simulation. Do not compare thresholds calibrated under different conditions as though they were directly equivalent. The analytical matched-filter benchmark is disabled (written as NaN) when interference is enabled because the AWGN-only derivation no longer applies.
