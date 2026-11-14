# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 3

**DATE:** 03/08/2026

**NAME OF EXP:** Switch Interfacing & Software Debouncing Techniques

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51) + Keil C51

---

## TASK3A : Debounced Push-Button Counter with LED Status Indication

### 1. Circuit Diagram

A momentary push-button switch is interfaced to P3.2 with an external 10k pull-up resistor. Four LEDs on P1.0 - P1.3 indicate a 4-bit binary counter value (0x0 to 0xF). A 20ms software debounce verification algorithm filters mechanical contact bounce transients before incrementing the counter on each valid switch press.

- **Target Microcontroller:** AT89C51
- **Oscillator / Clock Tree:** 11.0592 MHz Crystal
- **Configured Pin Allocations:** P3.2 (INT0 pin / GPIO) as tactile switch input; P1.0 - P1.3 as 4-bit binary LED counter output
- **External Hardware Peripherals:** Tactile Push Button, 10k Pull-up Resistor, 4x Green LEDs with 330 Ohm resistors
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

Mechanical switch contacts chatter for 5 to 15 milliseconds upon closure. To prevent false multi-triggering, the firmware samples P3.2 upon detecting a LOW state, executes a 20ms delay, and re-samples P3.2. If the pin remains LOW, a confirmed button press event is logged. The code then awaits button release before registering another state change.

**Pseudocode:**

1. Initialize P3.2 as input by writing '1' to P3.2.
2. Initialize Port 1 counter display to 0x00.
3. Loop continuously:
   a. Read P3.2; if P3.2 == 0 (switch pressed):
      i. Execute 20ms debounce delay.
      ii. If P3.2 is still 0:
          Increment counter variable (counter = (counter + 1) & 0x0F).
          Output counter onto P1 (P1 = ~counter for active-low LEDs).
          Wait in while(P3.2 == 0) loop until switch is released.
          Execute 20ms release debounce delay.

**Code Structure / Key Registers:**

sbit SW = P3^2; Port 1 lower nibble mapped to display LEDs. Debounce delay using software loop.

#### Embedded C Source Implementation (`main.c`):

```c
#include <reg51.h>

sbit SW = P3^2;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned char count = 0;
    SW = 1;       /* Configure P3.2 as input */
    P1 = 0xFF;    /* Turn OFF all active-low LEDs */

    while (1) {
        if (SW == 0) {            /* Falling edge detected */
            delay_ms(20);         /* 20ms debounce delay */
            if (SW == 0) {        /* Confirmed valid press */
                count = (count + 1) & 0x0F;
                P1 = ~(count);    /* Display 4-bit count */
                while (SW == 0);  /* Wait for key release */
                delay_ms(20);     /* Release debounce */
            }
        }
    }
}
```

### 3. Inference

Mechanical bounce was completely eliminated. Every single switch press cleanly incremented the binary counter on P1 from 0 to 15 without accidental double-counting, confirming effective debounce logic.
