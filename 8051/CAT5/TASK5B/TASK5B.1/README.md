# EXPERIMENT DETAILS

**EXP:** CAT 5 - TASK 5B.1

**DATE:** 

**NAME OF EXP:** Display Interfacing – Static 7-Segment Display

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 5B.1 : Display Interfacing – Static 7-Segment Display

### 1. Aim
To interface a Common Anode 7-segment display to Port 2 of the 8051 and implement an automated single-digit decimal counter from 0 to 9 with 1-second intervals.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x 0.56-inch Common Anode 7-Segment Display (Red)
- 7x 220 Ohm Current-Limiting Resistors
- 11.0592 MHz Crystal Oscillator + 2x 22pF Capacitors
- +5V DC Regulated Power Supply

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | 7-Segment Pin | Segment Controlled | Logic Level to Illuminate |
|---|---|---|---|
| P2.0 (Pin 21) | Pin 7 | Segment a (Top) | Active-LOW (0) |
| P2.1 (Pin 22) | Pin 6 | Segment b (Top-Right) | Active-LOW (0) |
| P2.2 (Pin 23) | Pin 4 | Segment c (Bottom-Right) | Active-LOW (0) |
| P2.3 (Pin 24) | Pin 2 | Segment d (Bottom) | Active-LOW (0) |
| P2.4 (Pin 25) | Pin 1 | Segment e (Bottom-Left) | Active-LOW (0) |
| P2.5 (Pin 26) | Pin 9 | Segment f (Top-Left) | Active-LOW (0) |
| P2.6 (Pin 27) | Pin 10 | Segment g (Middle) | Active-LOW (0) |
| Display CA (Pins 3, 8) | +5.0V Rail | Common Anode Terminal | Connected to +5.0V |

### 5. Working Principle
In Common Anode 7-segment displays, all internal LED anodes share a common terminal wired to +5.0V. Individual segments illuminate when their respective cathodes are connected to ground through current-limiting resistors. Driving a Port 2 pin LOW (0) causes current to sink into the 8051 output buffer, lighting the corresponding segment. A look-up table in ROM stores pre-calculated hexadecimal codes for digits 0-9: {0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8, 0x80, 0x90}.

### 6. Algorithm / Pseudocode
1. Store segment lookup codes in code memory: `unsigned char code seg_code[10] = {...};`.
2. Define software delay function `delay_ms(unsigned int ms)`.
3. Inside `main()`:
   a. For `digit = 0` to `9`:
      i. Output segment byte to Port 2: `P2 = seg_code[digit];`.
      ii. Delay 1000ms: `delay_ms(1000);`.
   b. Wrap digit back to 0 and repeat continuously.

### 7. Core Logic / Pseudocode / Code Base
Port 2 is mapped at SFR address 0xA0. Common anode codes are computed by setting active segment bits to 0 and inactive segments to 1 (e.g. Numeral '0' activates segments a,b,c,d,e,f -> bits 0..5 = 0, bit 6 = 1, bit 7 = 1 -> 11000000b = 0xC0).

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

/* Common Anode segment codes for numerals 0 - 9 (a=bit0 ... g=bit6) */
unsigned char code seg_code[10] = {
    0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8, 0x80, 0x90
};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned char digit = 0;
    while (1) {
        for (digit = 0; digit < 10; digit++) {
            P2 = seg_code[digit];
            delay_ms(1000);
        }
    }
}
```

### 8. Expected Output
Display smoothly advances through decimal numerals 0, 1, 2, ..., 9 once per second and loops continuously.

### 9. Observation
Each numeral rendered with uniform brightness and crisp contrast. Current per illuminated segment: 9.8 mA.

### 10. Inference
Successfully verified active-LOW common anode decoding and static 7-segment hardware interfacing.
