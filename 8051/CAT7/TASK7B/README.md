# EXPERIMENT DETAILS

**EXP:** CAT 7 - TASK 7B

**DATE:** 

**NAME OF EXP:** Motor Actuation – Direction & Speed Control

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 7B : Motor Actuation – Direction & Speed Control

### 1. Aim
To implement an 8-step half-stepping commutation algorithm for a unipolar stepper motor on 8051 Port 2, incorporating interactive SPST switch controls for bidirectional rotation (CW/CCW) and dynamic speed selection.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x 28BYJ-48 Stepper Motor + ULN2003 Driver Board
- 2x SPST Toggle Switches (Direction and Speed)
- 2x 10k Ohm Pull-Up Resistors
- External 5V 1A DC Power Supply

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function |
|---|---|---|
| P2.0 - P2.3 | ULN2003 Inputs IN1 - IN4 | 4-Phase Stepper Commutation Outputs |
| P3.2 (Pin 12) | Direction Switch & 10k Pull-up | Rotation Direction (1=CW, 0=CCW) |
| P3.3 (Pin 13) | Speed Switch & 10k Pull-up | Commutation Speed (1=Fast 5ms, 0=Slow 15ms) |
| Motor Red Lead | +5.0V External Power Supply | Coil Center-Tap VCC |
| Common Ground | MCU Pin 20 & ULN2003 GND | Common 0V Reference |

### 5. Working Principle
Half-stepping interleaves single-phase and two-phase excitation, doubling the angular resolution to 4096 steps per revolution (for a 64:1 geared 28BYJ-48). The 8-element sequence is: {0x08, 0x0C, 0x04, 0x06, 0x02, 0x03, 0x01, 0x09}. Moving forward through the array produces CW rotation; moving backward produces CCW rotation. The delay between steps dictates commutation speed (5ms = Fast, 15ms = Slow).

### 6. Algorithm / Pseudocode
1. Define 8-element half-step array: `half_step[8] = {0x08, 0x0C, 0x04, 0x06, 0x02, 0x03, 0x01, 0x09};`.
2. Read Speed Switch P3.3: if HIGH -> set `step_delay = 5ms`, else `step_delay = 15ms`.
3. Read Direction Switch P3.2:
   a. If P3.2 == 1 (CW): iterate `step` index from 0 to 7, write `P2 = half_step[step]`, delay `step_delay`.
   b. If P3.2 == 0 (CCW): iterate `step` index from 7 down to 0, write `P2 = half_step[step]`, delay `step_delay`.
4. Repeat continuously.

### 7. Core Logic / Code Base
Bidirectional array indexing logic with runtime conditional speed assignment.

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

unsigned char code half_step[8] = {
    0x08, 0x0C, 0x04, 0x06, 0x02, 0x03, 0x01, 0x09
};

sbit DIR_SW   = P3^2;
sbit SPEED_SW = P3^3;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    char step;
    unsigned int step_delay;

    DIR_SW = 1;
    SPEED_SW = 1;

    while (1) {
        step_delay = (SPEED_SW == 1) ? 5 : 15;

        if (DIR_SW == 1) {
            for (step = 0; step < 8; step++) {
                P2 = half_step[step];
                delay_ms(step_delay);
            }
        } else {
            for (step = 7; step >= 0; step--) {
                P2 = half_step[step];
                delay_ms(step_delay);
            }
        }
    }
}
```

### 8. Expected Output
The stepper motor executes silky-smooth half-stepping rotation, reversing direction instantly when P3.2 is toggled and tripling speed when P3.3 is asserted.

### 9. Observation
Half-stepping significantly reduced mechanical resonance and audible vibration compared to full-stepping.

### 10. Inference
Half-stepping doubles angular positioning precision while providing dynamic speed and direction controllability.
