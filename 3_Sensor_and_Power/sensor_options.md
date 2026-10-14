# Sensor Architecture Trade Study — Preliminary

**Status: candidates identified; no final component selection or circuit validation.** The first physical prototype should prioritize a safe, repeatable optical link, not a medical or long-range claim.

## Candidate A — Integrated IR receiver (simplest first bench test)
**Candidate:** Vishay TSSP94038 (verify exact order code and current datasheet before purchase).

- Datasheet: https://www.vishay.com/docs/82843/tssp940.pdf
- Intended for presence sensing, light barriers, and proximity sensing; active-low digital output in response to 940 nm bursts.
- Supply range stated in datasheet: 2.0–3.6 V.
- The emitter burst must use the carrier frequency specified for the selected part.
- Advantage: avoids designing a photodiode transimpedance amplifier for the first build.
- Limitation: outputs a demodulated digital signal, so it cannot provide the raw analogue waveform needed to validate the current matched-filter simulation directly.

**Use case:** first hardware milestone to measure detection versus distance/ambient conditions as a digital pulse detector, with strict separation from the analogue simulation results.

## Candidate B — Photodiode receiver (more research flexibility)
**Candidate:** Vishay BPW34 silicon PIN photodiode.

- Datasheet: https://www.vishay.com/docs/81521/bpw34.pdf
- Manufacturer lists peak sensitivity near 900 nm and spectral response from approximately 430 to 1100 nm.
- Advantage: provides a photodiode current suitable for a designed analogue front end and ADC-based waveform capture.
- Limitation: requires a properly designed transimpedance amplifier, bias/grounding strategy, bandwidth analysis, and careful ambient-light management. It is not a complete receiver circuit by itself.

**Use case:** second-stage research prototype if raw-waveform comparison is a key objective.

## Candidate emitter candidate
**Vishay TSAL6200**, 940 nm IR emitter: https://www.vishay.com/docs/81010/tsal6200.pdf

The datasheet includes electrical and optical limits; do not assume its headline pulse-current capability is a safe continuous operating point. Final drive current and resistor/transistor sizing must be derived from the actual supply, pulse duty cycle, thermal limits, and datasheet conditions.

## Comparison

| Criterion | TSSP94038 module | BPW34 + analogue front end |
|---|---|---|
| First-build complexity | Lower | Higher |
| Raw analogue waveform | No | Yes, after AFE/ADC design |
| Receiver electronics | Integrated | Must be designed and verified |
| Direct comparability to current waveform simulation | Limited; digital output requires a separate event-level model | Better potential fit |
| Recommended role | Quick first optical-link demonstrator | Research-grade waveform prototype |

## Decision
Do not buy or freeze the BOM yet. Confirm exact part variant, carrier frequency, availability, microcontroller voltage compatibility, and intended test geometry. Choose between the two architectures after deciding whether the first physical result is a digital detection demo or a raw-waveform experiment.
