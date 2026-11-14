# EXPERIMENT DETAILS

**EXP:** CAT 5 - TASK 5B.3

**DATE:** 

**NAME OF EXP:** Display Interfacing – Multiplexed 4-Digit Display

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 5B.3 : Display Interfacing – Multiplexed 4-Digit Display

### 1. Aim
To interface a 4-digit multiplexed Common Cathode 7-segment display module to 8051 Port 0 and Port 2, implementing an interactive Up/Down counter controlled by an external SPST switch.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x 4-Digit Common Cathode 7-Segment Display Module
- 1x 8-Pin 10k Ohm Resistor Network (Pull-up for Port 0)
- 4x S8050 NPN Transistors
- 1x SPST Slide / Toggle Switch
- +5V DC Power Supply

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function |
|---|---|---|
| P0.0 - P0.6 (Pins 39 - 33) | 10k Pull-up Network & Segments a - g | Open-Drain Segment Bus |
| P2.0 - P2.3 (Pins 21 - 24) | Transistors Q1 - Q4 Base Resistors | 4-Digit Active-LOW Selectors |
| P3.3 (Pin 13) | SPST Direction Switch to GND | Direction Selector (1=UP, 0=DOWN) |
| VCC (Pin 40) / GND (Pin 20) | +5.0V DC and Common GND | System Power Supply |

### 5. Working Principle
Port 0 on the 8051 features open-drain output FETs without internal pull-ups, requiring an external 10k pull-up resistor network to achieve valid logic HIGH levels. Digits are parsed mathematically into Thousands, Hundreds, Tens, and Units using integer division and modulo arithmetic. A 4-phase time-multiplexing scanner illuminates one digit at a time for 3.0 ms (12.0 ms full frame time = ~83 Hz refresh rate).

### 6. Algorithm / Pseudocode
1. Read Direction Switch on P3.3: if HIGH -> count UP, if LOW -> count DOWN.
2. Decompose `count` into 4 digits: `d[0] = count / 1000; d[1] = (count/100)%10; d[2] = (count/10)%10; d[3] = count % 10;`.
3. Execute 20 multiplexing cycles (~240ms duration):
   a. For `scan = 0` to `3`:
      i. Activate digit: `P2 = ~(1 << scan);`.
      ii. Output segment data on Port 0: `P0 = seg_code[d[scan]];`.
      iii. Delay 3ms: `delay_ms(3);`.
      iv. Blank display: `P2 = 0xFF;`.
4. Update count variable according to direction state and clamp between 0 and 9999.
5. Repeat continuously.

### 7. Core Logic / Pseudocode / Code Base
Port 0 open-drain pull-up configuration combined with rotating bit-mask `~(1 << scan)` on Port 2 creates an efficient round-robin digit scanner.

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

unsigned char code seg_code[10] = {
    0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F
};

sbit DIR_SW = P3^3; /* 1 = UP, 0 = DOWN */

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned int count = 1234;
    unsigned char digits[4];
    unsigned char scan = 0, cycle = 0;

    DIR_SW = 1; /* Input */

    while (1) {
        digits[0] = count / 1000;
        digits[1] = (count / 100) % 10;
        digits[2] = (count / 10) % 10;
        digits[3] = count % 10;

        for (cycle = 0; cycle < 20; cycle++) {
            for (scan = 0; scan < 4; scan++) {
                P2 = ~(1 << scan);             /* Select active digit */
                P0 = seg_code[digits[scan]];   /* Output segment data */
                delay_ms(3);
                P2 = 0xFF;                     /* Blanking */
            }
        }

        if (DIR_SW == 1) {
            count = (count < 9999) ? count + 1 : 0;
        } else {
            count = (count > 0) ? count - 1 : 9999;
        }
    }
}
```

### 8. Expected Output
The 4-digit display smoothly counts up from 0000 to 9999 when P3.3 is HIGH, and counts down when P3.3 is toggled LOW.

### 9. Observation
Zero ghosting observed across adjacent digits due to calibrated 3ms dwell time and blanking intervals.

### 10. Inference
Validated open-drain bus interfacing and scalable multi-digit scanning algorithms.
