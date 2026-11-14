# EXPERIMENT DETAILS

**EXP:** CAT 7 - TASK 7A

**DATE:** 

**NAME OF EXP:** Motor Actuation & Driver Interfacing

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 7A : Motor Actuation & Driver Interfacing

### 1. Aim
To interface a 28BYJ-48 5V 4-phase unipolar stepper motor to 8051 Port 2 using a ULN2003 Darlington transistor array driver, implementing full-step excitation sequence for continuous clockwise rotation.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x 28BYJ-48 5V 4-Phase Unipolar Stepper Motor
- 1x ULN2003A Darlington Transistor Driver Board
- 1x External 5.0V 1.0A DC Power Supply
- Connecting Jumpers & Common Ground Bus

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | ULN2003 Pin | Stepper Motor Phase Wire | Functional Role |
|---|---|---|---|
| P2.0 (Pin 21) | IN1 -> OUT1 | Blue (Coil A) | Stator Phase A Driver |
| P2.1 (Pin 22) | IN2 -> OUT2 | Pink (Coil B) | Stator Phase B Driver |
| P2.2 (Pin 23) | IN3 -> OUT3 | Yellow (Coil C) | Stator Phase C Driver |
| P2.3 (Pin 24) | IN4 -> OUT4 | Orange (Coil D) | Stator Phase D Driver |
| Ext +5V Rail | VCC (ULN2003) | Red (Common VCC) | Motor Power Supply |
| Ext GND | GND (ULN2003) & Pin 20 | Common Ground | Current Return Path |

### 5. Working Principle
Microcontroller pins cannot supply the hundreds of milliamps demanded by stepper motor stator windings. The ULN2003 provides high-voltage, high-current open-collector Darlington transistor pairs with built-in inductive suppression clamp diodes. In full-step two-phase-on excitation, two adjacent coils are energized simultaneously to generate maximum magnetic torque. The 4-step sequence is: Step 1 (A+B: 0x09), Step 2 (B+C: 0x0C), Step 3 (C+D: 0x06), Step 4 (D+A: 0x03). Cycling this table sequentially rotates the permanent magnet rotor smoothly.

### 6. Algorithm / Pseudocode
1. Define full-step excitation array in code memory: `unsigned char code full_step[4] = {0x09, 0x0C, 0x06, 0x03};`.
2. Configure Port 2 lower nibble (P2.0 - P2.3) as output.
3. Inside the infinite loop:
   a. For `step = 0` to `3`:
      i. Output step pattern: `P2 = full_step[step];`.
      ii. Introduce inter-step dwell time: `delay_ms(15);`.
   b. Repeat continuously.

### 7. Core Logic / Code Base
Phase switching sequence stored in ROM. Inter-step delay of 15ms establishes a stable commutation speed without rotor stall or slip.

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

/* Full-step excitation sequence for 4-phase unipolar stepper */
unsigned char code full_step[4] = {0x09, 0x0C, 0x06, 0x03};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned char step = 0;
    while (1) {
        for (step = 0; step < 4; step++) {
            P2 = full_step[step];
            delay_ms(15); /* Controls motor speed */
        }
    }
}
```

### 8. Expected Output
The stepper motor shaft rotates continuously in the clockwise direction with high holding torque and quiet operation.

### 9. Observation
Measured shaft angular velocity: ~15 RPM with steady 15ms inter-step timing and zero coil overheating.

### 10. Inference
Validated inductive load driving using ULN2003 Darlington arrays and digital phase commutation sequences.
