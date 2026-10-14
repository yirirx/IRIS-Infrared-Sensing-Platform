# Hardware Status and Design Gate

**Status: pre-design. No circuit has been built or electrically validated.**

## Architecture candidates
- **Low-complexity demonstrator:** 940 nm emitter + compatible integrated demodulating IR receiver + microcontroller GPIO.
- **Waveform research demonstrator:** 940 nm emitter + BPW34 photodiode + transimpedance amplifier + ADC/oscilloscope capture.

These architectures serve different experimental goals. Do not combine their claims: a demodulated digital output cannot validate the same raw waveform assumptions as an analogue photodiode receiver.

## Required design work before assembly
1. Confirm exact component order codes and revisions from manufacturer datasheets.
2. Choose carrier frequency compatible with the receiver.
3. Calculate LED current limiting/driver values for supply and pulse duty cycle; check average and peak ratings.
4. Check logic-level compatibility and decoupling requirements.
5. For BPW34, design and simulate the transimpedance amplifier and check stability, bandwidth, noise, and ADC input range.
6. Define an indoor, low-power, non-eye-directed test setup and review IR eye-safety guidance.
7. Create the schematic and bill of materials with datasheet citations.
8. Define test distances, alignment, ambient-light conditions, repetitions, and measurement uncertainty.

## Evidence policy
Only mark hardware milestones complete after a dated schematic, build photographs, instrument settings, raw data, and repeatable results are added to the repository. Do not describe the device as built, calibrated, medical, or long-range before the evidence exists.
