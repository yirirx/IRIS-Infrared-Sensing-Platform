# Design Decisions

## DD-001: Simulation before hardware
Start in software so the detection pipeline can be verified before parts are selected.

## DD-002: Modulated burst detection
Use on/off-keyed carrier bursts and compare energy detection with matched filtering. This creates a clear, measurable signal-processing problem.

## DD-003: Keep the first channel model simple
Use scalar attenuation and additive white Gaussian noise. This is useful for learning, but not a complete optical channel model.

## DD-004: Separate simulated and measured evidence
Simulation outputs must be labelled as simulation. Hardware results require a documented physical setup and repeatable measurements.
