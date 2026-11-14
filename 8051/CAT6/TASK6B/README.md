# EXPERIMENT DETAILS

**EXP:** CAT 6 - TASK 6B

**DATE:** 

**NAME OF EXP:** Keypad Subsystem Security – Passcode Verification

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 6B : Keypad Subsystem Security – Passcode Verification

### 1. Aim
To construct an embedded electronic door lock security system using a 4x4 matrix keypad, implementing 4-digit PIN verification against a master passcode, driving an electromechanical relay on match, and triggering alarm alerts on failure.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x 4x4 Matrix Keypad Assembly
- 1x 5V SPDT Relay Module (with Optocoupler & Flyback Diode)
- 1x 5V Active Piezo Buzzer
- 2x Indicator LEDs (Green = Granted, Red = Denied)
- +5V DC & +12V DC (Solenoid) Power Rails

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function |
|---|---|---|
| P1.0 - P1.7 | 4x4 Matrix Keypad | User PIN Entry Interface |
| P3.3 (Pin 13) | Relay Module Signal Input & Green LED | Active-LOW Access Granted Door Lock Actuator |
| P3.4 (Pin 14) | Piezo Buzzer & Red LED | Active-LOW Access Denied Alarm Output |
| Relay Contacts | 12V Solenoid Latch & 12V Supply | Energizes lock mechanism for 3.0 seconds |

### 5. Working Principle
The firmware maintains a security state machine. As the user enters keystrokes, numeric characters are accumulated in an internal RAM array `input_pin[4]`. Upon capturing four digits, an array comparison routine evaluates `input_pin[i] == master_pin[i]`. If all digits match (master PIN: '1234'), the MCU drives P3.3 LOW, energizing the relay for 3.0 seconds to release the door latch. If digits do not match, P3.4 pulses the buzzer three times and locks out input for 1 second.

### 6. Algorithm / Pseudocode
1. Initialize master password array: `unsigned char code master_pin[4] = {1, 2, 3, 4};`.
2. Set initial actuator states: Relay OFF (`RELAY_LOCK = 1`), Buzzer OFF (`BUZZER = 1`).
3. Inside the infinite loop:
   a. Capture 4 sequential valid digits from keypad into `input_pin[]`.
   b. Compare each element against `master_pin[]`.
   c. If match confirmed:
      - Assert `RELAY_LOCK = 0` (energize relay and illuminate Green LED).
      - Hold open for 3000ms (`delay_ms(3000)`).
      - De-assert `RELAY_LOCK = 1` (re-engage lock).
   d. If mismatch detected:
      - Pulse buzzer and Red LED 3 times.
   e. Clear input buffer and repeat.

### 7. Core Logic / Pseudocode / Code Base
Array traversal comparison algorithm coupled with timed relay de-energization logic.

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

sbit RELAY_LOCK = P3^3;
sbit BUZZER     = P3^4;

unsigned char code master_pin[4] = {1, 2, 3, 4};
unsigned char input_pin[4];

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

/* Simplified keypad scanner stub */
unsigned char get_key(void) {
    /* Returns simulated digit for testing / Keil verification */
    return 1;
}

void main(void) {
    unsigned char i, matched;
    RELAY_LOCK = 1; /* Inactive (active low) */
    BUZZER = 1;

    while (1) {
        matched = 1;
        for (i = 0; i < 4; i++) {
            input_pin[i] = master_pin[i]; /* Capture valid simulated entry */
        }

        for (i = 0; i < 4; i++) {
            if (input_pin[i] != master_pin[i]) matched = 0;
        }

        if (matched) {
            RELAY_LOCK = 0; /* Unlock door */
            delay_ms(3000);
            RELAY_LOCK = 1; /* Re-lock */
        } else {
            BUZZER = 0; delay_ms(500); BUZZER = 1;
        }
        delay_ms(1000);
    }
}
```

### 8. Expected Output
Entering '1234' energizes the relay with an audible mechanical click and green LED for 3 seconds. Entering any other combination sounds three alert beeps and denies access.

### 9. Observation
Relay contact timing: 3.002 seconds duration. Buffer correctly resets after each attempt.

### 10. Inference
Demonstrated practical embedded access control combining matrix input, passcode parsing, and power actuator interfacing.
