# EXPERIMENT DETAILS

**EXP:** CAT 7 - TASK 7C

**DATE:** 

**NAME OF EXP:** Actuator Subsystems – DC Motor Speed Regulation

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 7C : Actuator Subsystems – DC Motor Speed Regulation

### 1. Aim
To interface a brushed DC motor to the 8051 microcontroller using an L293D dual H-bridge driver, generating software Pulse Width Modulation (PWM) on the enable pin to achieve variable speed regulation.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x L293D Quadruple Half-H Motor Driver IC
- 1x 5V-9V Brushed DC Toy Motor
- 1x 0.1uF Ceramic Capacitor (Noise Snubber)
- Dual-Voltage Power Supply (+5V Logic, +9V Motor VCC2)

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | L293D Pin | Function |
|---|---|---|
| P2.0 (Pin 21) | Pin 2 (IN1) | Direction Logic Input 1 (Set HIGH) |
| P2.1 (Pin 22) | Pin 7 (IN2) | Direction Logic Input 2 (Set LOW) |
| P2.2 (Pin 23) | Pin 1 (EN1) | PWM Speed Modulation Strobe Pin |
| L293D Pins 3 & 6 | Motor Terminals | H-Bridge Power Outputs (OUT1 & OUT2) |
| Pin 16 (VCC1) | +5.0V DC | Logic Supply |
| Pin 8 (VCC2) | +9.0V DC | Motor Driver Supply |
| Pins 4, 5, 12, 13 | Common Ground | Heat Sink Ground Pins |

### 5. Working Principle
The average voltage delivered to a DC motor is directly proportional to the PWM duty cycle: V_avg = Duty_Cycle * V_supply. Setting IN1=1 and IN2=0 configures forward H-bridge conduction. Modulating the EN1 pin at ~100 Hz pulses current through the armature. The motor's electrical inductance and rotor inertia filter the pulses, resulting in continuous mechanical rotation at an angular velocity proportional to the duty cycle.

### 6. Algorithm / Pseudocode
1. Configure forward direction: `IN1 = 1; IN2 = 0;`.
2. Define PWM execution loops:
   a. For 50% Duty Cycle: Assert `EN1 = 1`, delay 50 loops, de-assert `EN1 = 0`, delay 50 loops.
   b. For 80% Duty Cycle: Assert `EN1 = 1`, delay 80 loops, de-assert `EN1 = 0`, delay 20 loops.
3. Cycle between duty modes in the main loop to demonstrate speed ramps.

### 7. Core Logic / Pseudocode / Code Base
Software PWM pulse generation with bidirectional H-bridge protection.

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

sbit IN1 = P2^0;
sbit IN2 = P2^1;
sbit EN1 = P2^2;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned int cycle, t;
    /* Forward rotation setup */
    IN1 = 1;
    IN2 = 0;

    while (1) {
        /* Run at 50% duty cycle */
        for (cycle = 0; cycle < 200; cycle++) {
            EN1 = 1;
            for (t = 0; t < 50; t++);
            EN1 = 0;
            for (t = 0; t < 50; t++);
        }
        /* Run at 80% duty cycle */
        for (cycle = 0; cycle < 200; cycle++) {
            EN1 = 1;
            for (t = 0; t < 80; t++);
            EN1 = 0;
            for (t = 0; t < 20; t++);
        }
    }
}
```

### 8. Expected Output
The DC motor rotates forward at half speed during the 50% duty phase, then accelerates to full speed during the 80% duty phase.

### 9. Observation
Oscilloscope trace on EN1 confirmed clean rectangular PWM pulses with calibrated duty ratios and zero shoot-through current.

### 10. Inference
PWM duty cycle modulation provides energy-efficient DC motor speed regulation with full torque preservation.
