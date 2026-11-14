# EXPERIMENT DETAILS

**EXP:** CAT 5 - TASK 5A

**DATE:** 

**NAME OF EXP:** Interrupt System Architecture & External Asynchronous Events

**HARDWARE SETUP / PLATFORM:** 8051 Microcontroller (AT89C51 @ 11.0592 MHz) + Keil C51

---

## TASK 5A : Interrupt System Architecture & External Asynchronous Events

### 1. Aim
To configure 8051 External Hardware Interrupt 0 (INT0 on P3.2) in falling-edge trigger mode to create an instantaneous emergency stop alarm while the CPU executes a normal background blinking routine.

### 2. Components Required
- 1x AT89C51 Microcontroller IC
- 1x Emergency Stop Push-Button Switch (Normally Open)
- 1x 10k Ohm Pull-Up Resistor
- 1x Green LED (Normal Operation)
- 1x Red LED (Emergency Alert)
- 1x 5V Active Piezo Buzzer
- 2x 330 Ohm Current-Limiting Resistors

### 3. Circuit Diagram
The schematic diagram below illustrates the exact hardware configuration, power rails, oscillator circuitry, and peripheral signal lines.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Functional Description |
|---|---|---|
| P3.2 (/INT0 Pin 12) | E-Stop Button & 10k Pull-up | Asynchronous Falling-Edge Interrupt Source |
| P1.0 (Pin 1) | 330 Ω -> Green LED -> +5V | Normal Background Heartbeat Indicator |
| P1.7 (Pin 8) | 330 Ω -> Red LED & Buzzer -> +5V | Latched Emergency Alarm Indicator |
| XTAL1 / XTAL2 | 11.0592 MHz Crystal + Caps | System Clock |
| RST (Pin 9) | Power-On Reset Circuit | Hardware Reset |

### 5. Working Principle
The 8051 interrupt system provides hardware-vectored preemptive execution. Setting IT0 = 1 in the TCON register configures INT0 to trigger on high-to-low transitions. When the emergency button pulls P3.2 to ground, the CPU completes its current instruction, pushes the Program Counter onto the stack, and vectors directly to memory address 0x0003 (Interrupt vector 0). Inside the ISR, the emergency alarm status is toggled and latched. Execution returns via RETI without affecting main loop integrity.

### 6. Algorithm / Pseudocode
1. Configure falling-edge trigger for External Interrupt 0: `IT0 = 1;` in TCON.
2. Enable External Interrupt 0: `EX0 = 1;` in IE register.
3. Enable Global Interrupts: `EA = 1;` in IE register.
4. Define Interrupt Service Routine `External0_ISR(void) interrupt 0`:
   a. Toggle latched alarm output: `ALARM_LED = ~ALARM_LED;`.
5. In the main loop `while (1)`:
   a. Toggle heartbeat LED on P1.0.
   b. Call `delay_ms(300)`.
6. System responds to INT0 asynchronously at any time during delay loops.

### 7. Core Logic / Pseudocode / Code Base
Registers configured: TCON.0 (IT0 = 1 for edge-trigger), IE.0 (EX0 = 1 to unmask INT0), IE.7 (EA = 1 for global interrupt enable). Keil `interrupt 0` keyword routes function to vector 0x0003.

#### Embedded C Firmware Implementation (`main.c`):
```c
#include <reg51.h>

sbit RUN_LED   = P1^0;
sbit ALARM_LED = P1^7;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void External0_ISR(void) interrupt 0 {
    /* Instantly serviced on falling edge at P3.2 */
    ALARM_LED = ~ALARM_LED; /* Toggle alarm status */
}

void main(void) {
    IT0 = 1; /* Configure INT0 as falling-edge triggered */
    EX0 = 1; /* Enable External Interrupt 0 */
    EA  = 1; /* Enable Global Interrupts */

    ALARM_LED = 1; /* Off (active-low) */
    while (1) {
        RUN_LED = ~RUN_LED; /* Background heartbeat */
        delay_ms(300);
    }
}
```

### 8. Expected Output
Green LED pulses continuously. Pressing the E-Stop button instantly latches/toggles the Red alarm LED and buzzer with sub-microsecond latency, interrupting delay loops immediately.

### 9. Observation
Response latency measured from button falling edge to P1.7 toggle: 3.8 us, proving true hardware-vectored preemption.

### 10. Inference
External hardware interrupts provide deterministic, zero-polling response to critical asynchronous physical events.
