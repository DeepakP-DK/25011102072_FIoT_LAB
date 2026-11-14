# EXPERIMENT DETAILS

**EXP:** CAT 4 - TASK 4A

**DATE:** 

**NAME OF EXP:** Timer Architecture & Hardware Square Wave Generation

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 4A : Timer Architecture & Hardware Square Wave Generation

### 1. Aim
To configure 8051 Hardware Timer 0 in Mode 1 (16-bit timer mode) to generate a precise 1.0 kHz symmetrical square wave on GPIO pin P1.5 using overflow flag polling.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x 11.0592 MHz Quartz Crystal
- 2x 22pF Ceramic Capacitors
- 1x Digital Storage Oscilloscope (DSO) / Frequency Counter
- 1x Diagnostic LED with 1k Ohm Resistor
- +5V DC Regulated Power Supply

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Functional Description |
|---|---|---|
| P1.5 (Pin 6) | DSO Channel 1 Probe & Diagnostic LED | 1 kHz Symmetrical Square Wave Output |
| XTAL1 / XTAL2 (Pins 19, 18) | 11.0592 MHz Crystal & 22pF Caps | System Clock reference for timer ticks |
| RST (Pin 9) | Power-On Reset RC Circuit | Microcontroller hardware reset |
| EA (Pin 31) | Tied to +5.0V | Internal code execution |
| GND (Pin 20) | DSO Ground Alligator Clip | 0V Reference Ground |

### 5. Working Principle
At an oscillator frequency of 11.0592 MHz, 1 machine cycle is 12 / 11.0592 MHz = 1.08507 us. A 1.0 kHz square wave requires a period T = 1.0 ms, meaning each half-period (HIGH and LOW) must last exactly 500 us. The number of timer increments required is N = 500 us / 1.08507 us = 460.8 ≈ 461 counts. In 16-bit Timer Mode 1, the timer overflows when rolling over from 0xFFFF to 0x0000. Therefore, the required initial reload value is M = 65536 - 461 = 65075 = 0xFE33. High byte TH0 = 0xFE, low byte TL0 = 0x33.

### 6. Algorithm / Pseudocode
1. Configure Timer Mode Register `TMOD = 0x01` (Timer 0 in Mode 1: 16-bit timer, internal clocking).
2. Set initial output state: `sbit WAVE_OUT = P1^5; WAVE_OUT = 0;`.
3. Inside the infinite loop:
   a. Load timer registers: `TH0 = 0xFE; TL0 = 0x33;`.
   b. Start Timer 0 by asserting Run bit: `TR0 = 1;`.
   c. Poll the overflow flag: `while (TF0 == 0);`.
   d. Stop Timer 0: `TR0 = 0;`.
   e. Clear the overflow flag in software: `TF0 = 0;`.
   f. Toggle the output pin: `WAVE_OUT = ~WAVE_OUT;`.
4. Repeat continuously.

### 7. Core Logic / Pseudocode / Code Base
Special Function Registers involved: TMOD (0x89) configured as 0x01, TCON (0x88) controlling TR0 and TF0 flags, and TH0/TL0 (0x8C/0x8A) reload registers.

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

sbit WAVE_OUT = P1^5;

void main(void) {
    TMOD = 0x01; /* Timer 0, Mode 1 (16-bit timer) */
    WAVE_OUT = 0;

    while (1) {
        TH0 = 0xFE;  /* Reload value for 500us delay */
        TL0 = 0x33;
        TR0 = 1;     /* Start Timer 0 */
        while (TF0 == 0); /* Wait for overflow */
        TR0 = 0;     /* Stop Timer 0 */
        TF0 = 0;     /* Clear overflow flag */
        WAVE_OUT = ~WAVE_OUT; /* Toggle output pin */
    }
}
```

### 8. Expected Output
A stable 1.002 kHz square wave with exactly 50% duty cycle visible on the DSO screen with peak-to-peak amplitude of 5.0V.

### 9. Observation
DSO measured parameters: Frequency = 1.0016 kHz, Period = 998.4 us, Duty Cycle = 50.0%, Vpp = 4.98V.

### 10. Inference
Hardware Timer 0 in Mode 1 eliminates software instruction overhead, generating highly accurate frequency waveforms.
