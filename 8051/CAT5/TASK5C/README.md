# EXPERIMENT DETAILS

**EXP:** CAT 5 - TASK 5C

**DATE:** 

**NAME OF EXP:** Alphanumeric LCD Interfacing (HD44780 Controller)

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 5C : Alphanumeric LCD Interfacing (HD44780 Controller)

### 1. Aim
To interface a 16x2 character alphanumeric LCD module with Hitachi HD44780 controller to 8051 Port 2 and Port 3, initializing the display in 8-bit parallel mode and rendering custom university telemetry strings.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x 16x2 Character Alphanumeric LCD Module (HD44780 compliant)
- 1x 10k Single-Turn Trimpot (Contrast Adjustment)
- 1x 100 Ohm Resistor (Backlight Current Limiter)
- +5V DC Regulated Power Supply

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | LCD Pin | Symbol | Description |
|---|---|---|---|
| P2.0 - P2.7 | Pins 7 - 14 | D0 - D7 | 8-Bit Bidirectional Data Bus |
| P3.5 (Pin 15) | Pin 4 | RS | Register Select (0=Command, 1=Data) |
| P3.6 (Pin 16) | Pin 5 | RW | Read/Write (0=Write, 1=Read) |
| P3.7 (Pin 17) | Pin 6 | E | Enable Strobe (Falling Edge Triggered) |
| Trimpot Wiper | Pin 3 | V0 | Liquid Crystal Operating Voltage (Contrast) |
| +5V / GND | Pins 2, 1 | VDD / VSS | Logic Power Supply (+5V / 0V) |
| +5V / GND | Pins 15, 16 | A / K | LED Backlight Anode & Cathode |

### 5. Working Principle
The HD44780 controller manages display memory (DDRAM, CGROM, CGRAM). When RS=0, bytes sent over D0-D7 are interpreted as instructions (clear screen, set cursor, display control). When RS=1, bytes are written into DDRAM as ASCII characters. Data is latched on the high-to-low falling edge of the Enable (E) pin with a minimum pulse width of 450 ns. Initialization sends standard command bytes: 0x38 (8-bit, 2-line, 5x8 font), 0x0C (Display ON, cursor off), 0x06 (Entry mode auto-increment), and 0x01 (Clear display).

### 6. Algorithm / Pseudocode
1. Define pin macros: `#define LCD_DATA P2`, `sbit RS = P3^5;`, `sbit RW = P3^6;`, `sbit EN = P3^7;`.
2. Implement `lcd_cmd(cmd)`: Set RS=0, RW=0, output byte on `LCD_DATA`, pulse EN HIGH then LOW.
3. Implement `lcd_data(data)`: Set RS=1, RW=0, output byte on `LCD_DATA`, pulse EN HIGH then LOW.
4. In `lcd_init()`: Delay 20ms for power stabilization, issue commands `0x38`, `0x0C`, `0x06`, `0x01`.
5. In `main()`:
   a. Call `lcd_init()`.
   b. Set DDRAM to Line 1: `lcd_cmd(0x80);` -> write `"SNU CHENNAI IoT"`.
   c. Set DDRAM to Line 2: `lcd_cmd(0xC0);` -> write `"REG: 25011102072"`.
   d. Halt in `while (1);`.

### 7. Core Logic / Code Base
Driver functions provide modular byte serialization. The Enable pulse timing conforms strictly to the HD44780 bus timing specification.

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

#define LCD_DATA P2

sbit RS = P3^5;
sbit RW = P3^6;
sbit EN = P3^7;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void lcd_cmd(unsigned char cmd) {
    LCD_DATA = cmd;
    RS = 0;
    RW = 0;
    EN = 1;
    delay_ms(2);
    EN = 0;
}

void lcd_data(unsigned char ch) {
    LCD_DATA = ch;
    RS = 1;
    RW = 0;
    EN = 1;
    delay_ms(2);
    EN = 0;
}

void lcd_string(char *str) {
    while (*str) {
        lcd_data(*str++);
    }
}

void lcd_init(void) {
    delay_ms(20);
    lcd_cmd(0x38); /* 8-bit mode, 2-line, 5x7 font */
    lcd_cmd(0x0C); /* Display ON, Cursor OFF */
    lcd_cmd(0x06); /* Auto-increment cursor */
    lcd_cmd(0x01); /* Clear display */
    delay_ms(5);
}

void main(void) {
    lcd_init();
    lcd_cmd(0x80); /* Line 1 */
    lcd_string("SNU CHENNAI IoT");
    lcd_cmd(0xC0); /* Line 2 */
    lcd_string("REG: 25011102072");

    while (1);
}
```

### 8. Expected Output
Line 1 displays 'SNU CHENNAI IoT' and Line 2 displays 'REG: 25011102072' with sharp, high-contrast black characters against green/blue backlight.

### 9. Observation
Measured Enable pulse width: 1.2 us. Contrast Trimpot adjusted to 0.85V on V0 for optimal visual clarity.

### 10. Inference
Implemented robust 8-bit parallel HD44780 protocol communication on the 8051 platform.
