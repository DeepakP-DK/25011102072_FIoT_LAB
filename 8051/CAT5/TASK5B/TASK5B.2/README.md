# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 5

**DATE:** 17/08/2026

**NAME OF EXP:** Display Interfacing – Multiplexed 7-Segment Displays

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51) + Keil C51

---

## TASK5B.2 : Dual-Digit Multiplexed 00-99 Display with Persistence of Vision (POV)

### 1. Circuit Diagram

Demonstrates time-division multiplexing across two Common Cathode display digits sharing a common segment data bus on Port 2. Transistor switches on P1.0 and P1.1 selectively energize individual digit cathodes at 100 Hz refresh rate to produce a flicker-free dual-digit display using Persistence of Vision.

- **Target Microcontroller:** AT89C51
- **Oscillator / Clock Tree:** 11.0592 MHz Crystal
- **Configured Pin Allocations:** P2.0 - P2.6 as segment data bus; P1.0 (Digit 1 enable / Tens), P1.1 (Digit 2 enable / Units)
- **External Hardware Peripherals:** Dual-digit Common Cathode 7-segment display, 2x BC547 NPN driver transistors, Resistors
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

Human eye retains visual impressions for ~1/25th of a second (POV). By alternately enabling Digit 1 and Digit 2 for 5ms each, the total frame rate is 100 Hz (well above flicker threshold). While Digit 1 is enabled, the tens segment code is driven on P2. Then Digit 1 is disabled, units code placed on P2, and Digit 2 enabled.

**Pseudocode:**

1. Split current number (0-99) into tens = val / 10 and units = val % 10.
2. Enable Digit 1 (P1.0 = 1, P1.1 = 0), output seg_code[tens] on P2, delay 5ms.
3. Blank display (P1.0 = 0, P1.1 = 0) to prevent ghosting.
4. Enable Digit 2 (P1.0 = 0, P1.1 = 1), output seg_code[units] on P2, delay 5ms.
5. Repeat 100 times to hold count for 1 second, then increment value.

**Code Structure / Key Registers:**

Time-multiplexing scanning algorithm with anti-ghosting blanking interval.

#### Embedded C Source Implementation (`main.c`):

```c
#include <reg51.h>

/* Common Cathode segment codes for numerals 0-9 */
unsigned char code seg_code[10] = {
    0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F
};

sbit DIGIT1_EN = P1^0; /* Tens digit driver */
sbit DIGIT2_EN = P1^1; /* Units digit driver */

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void display_number(unsigned char num) {
    unsigned char tens = num / 10;
    unsigned char units = num % 10;
    unsigned int k;

    for (k = 0; k < 50; k++) { /* Refresh display for ~500ms */
        /* Display Tens Digit */
        DIGIT1_EN = 1; DIGIT2_EN = 0;
        P2 = seg_code[tens];
        delay_ms(5);
        DIGIT1_EN = 0; DIGIT2_EN = 0; /* Blanking */

        /* Display Units Digit */
        DIGIT1_EN = 0; DIGIT2_EN = 1;
        P2 = seg_code[units];
        delay_ms(5);
        DIGIT1_EN = 0; DIGIT2_EN = 0; /* Blanking */
    }
}

void main(void) {
    unsigned char count = 0;
    while (1) {
        display_number(count);
        count = (count + 1) % 100;
    }
}
```

### 3. Inference

Multiplexing reduced required MCU pins from 16 down to 9 (7 segment + 2 digit enables). Both digits appeared steadily lit simultaneously without visible flicker or ghosting.
