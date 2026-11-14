# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 6

**DATE:** 24/08/2026

**NAME OF EXP:** Matrix Keypad Scanning & User Input Interfacing

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51) + Keil C51

---

## TASK6A : 4x4 Matrix Keypad Scanning with 7-Segment Key Code Display

### 1. Circuit Diagram

Interfacing a 4x4 matrix keypad to Port 1. Rows are driven LOW sequentially while columns are read to determine active key closures. The identified key number (0-F) is decoded and displayed in real-time on a 7-segment display.

- **Target Microcontroller:** AT89C51
- **Oscillator / Clock Tree:** 11.0592 MHz Crystal
- **Configured Pin Allocations:** P1.0 - P1.3 (Rows R1-R4); P1.4 - P1.7 (Cols C1-C4); P2.0 - P2.6 to 7-Segment display
- **External Hardware Peripherals:** 4x4 Membrane Keypad, Common Anode 7-Segment Display, 10k Pull-up Resistors
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

Rows R1-R4 are configured as outputs and columns C1-C4 as inputs with pull-ups. The MCU asserts LOW on row 0 while leaving rows 1-3 HIGH, then tests column inputs for a LOW level. If a column is LOW, debounce delay verifies closure, and key code is calculated as (row * 4) + col.

**Pseudocode:**

1. Initialize rows = 0xF0 on Port 1.
2. In keypad_scan():
   a. For row = 0 to 3:
      i. Set current row LOW and all other rows HIGH.
      ii. Read columns P1.4 - P1.7.
      iii. If column is 0, delay 20ms for debounce.
      iv. If still 0, return key_map[row][col].
3. In main(), continuously scan keypad and update Port 2 with seg_code[key].

**Code Structure / Key Registers:**

keypad_scan() row-column matrix scanning function with 2D lookup table.

#### Embedded C Source Implementation (`main.c`):

```c
#include <reg51.h>

#define KEYPAD P1
#define DISPLAY P2

unsigned char code seg_code[16] = {
    0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8,
    0x80, 0x90, 0x88, 0x83, 0xC6, 0xA1, 0x86, 0x8E
};

unsigned char code key_map[4][4] = {
    {0x1, 0x2, 0x3, 0xA},
    {0x4, 0x5, 0x6, 0xB},
    {0x7, 0x8, 0x9, 0xC},
    {0xE, 0x0, 0xF, 0xD}
};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

unsigned char keypad_scan(void) {
    unsigned char r, c;
    for (r = 0; r < 4; r++) {
        KEYPAD = ~(1 << r) | 0xF0; /* Drive one row low, keep cols high */
        if ((KEYPAD & 0xF0) != 0xF0) {
            delay_ms(20); /* Debounce */
            for (c = 0; c < 4; c++) {
                if (!(KEYPAD & (0x10 << c))) {
                    while (!(KEYPAD & (0x10 << c))); /* Wait release */
                    return key_map[r][c];
                }
            }
        }
    }
    return 0xFF; /* No key pressed */
}

void main(void) {
    unsigned char key;
    DISPLAY = 0xFF;
    while (1) {
        key = keypad_scan();
        if (key != 0xFF) {
            DISPLAY = seg_code[key];
        }
    }
}
```

### 3. Inference

Matrix scanning accurately resolved all 16 keys. Pressing any button immediately reflected the corresponding hexadecimal character on the display without ghost keys.
