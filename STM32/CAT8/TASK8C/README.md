# EXPERIMENT DETAILS

**EXP:** CAT 8 - TASK 8C

**DATE:** 

**NAME OF EXP:** STM32 Multi-LED Sequence & Pattern Generator

**HARDWARE SETUP / PLATFORM:** STM32 Blue Pill Board (STM32F103C8T6 @ 72 MHz) + Keil MDK-ARM (HAL)

---

## TASK 8C : STM32 Multi-LED Sequence & Pattern Generator

### 1. Aim
To interface four external LEDs to Port A (PA0 - PA3) of the STM32F103 and implement a high-speed ping-pong chasing light pattern with 150ms step transitions.

### 2. Components Required
- 1x STM32F103C8T6 Blue Pill Board
- 4x 5mm Colored User LEDs (Red, Yellow, Green, Blue)
- 4x 330 Ohm Current-Limiting Resistors
- ST-LINK V2 Debugger
- Solderless Breadboard & Jumpers

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function | Direction / Logic |
|---|---|---|---|
| PA0 (Pin 10) | 330 Ω Resistor -> Red LED Anode | Chaser Channel 1 | Active-HIGH Output |
| PA1 (Pin 11) | 330 Ω Resistor -> Yellow LED Anode | Chaser Channel 2 | Active-HIGH Output |
| PA2 (Pin 12) | 330 Ω Resistor -> Green LED Anode | Chaser Channel 3 | Active-HIGH Output |
| PA3 (Pin 13) | 330 Ω Resistor -> Blue LED Anode | Chaser Channel 4 | Active-HIGH Output |
| LED Cathodes | Common System Ground (GND) | Current Return Path | 0V Reference |

### 5. Working Principle
Pins PA0 to PA3 are configured as push-pull outputs in high-speed mode. An array stores the pin bitmasks: `uint16_t leds[4] = {GPIO_PIN_0, GPIO_PIN_1, GPIO_PIN_2, GPIO_PIN_3}`. The firmware drives each pin HIGH sequentially for 150ms before resetting it, scanning forward from PA0 to PA3, and then reverses back from PA2 to PA1 to produce a continuous fluid ping-pong scanner.

### 6. Algorithm / Pseudocode
1. Configure PA0 - PA3 as `GPIO_MODE_OUTPUT_PP`, `GPIO_NOPULL`, `GPIO_SPEED_FREQ_HIGH`.
2. Define LED pin array: `leds[4] = {GPIO_PIN_0, GPIO_PIN_1, GPIO_PIN_2, GPIO_PIN_3};`.
3. Inside loop:
   a. Forward Sweep: For `i = 0` to `3`:
      - Set pin HIGH: `HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_SET);`.
      - Delay 150ms: `HAL_Delay(150);`.
      - Set pin LOW: `HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_RESET);`.
   b. Reverse Sweep: For `i = 2` down to `1`:
      - Set pin HIGH, delay 150ms, set pin LOW.
4. Repeat indefinitely.

### 7. Core Logic / Code Base
Atomic bit manipulation using STM32 GPIO Bit Set/Reset Register (BSRR) via HAL wrapper functions.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
```c
#include "main.h"

void SystemClock_Config(void);
static void MX_GPIO_Init(void);

int main(void) {
    uint16_t leds[4] = {GPIO_PIN_0, GPIO_PIN_1, GPIO_PIN_2, GPIO_PIN_3};
    int i;
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();

    while (1) {
        for (i = 0; i < 4; i++) {
            HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_SET);
            HAL_Delay(150);
            HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_RESET);
        }
        for (i = 2; i > 0; i--) {
            HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_SET);
            HAL_Delay(150);
            HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_RESET);
        }
    }
}
```

### 8. Expected Output
The 4 LEDs illuminate in a continuous chasing motion (1 -> 2 -> 3 -> 4 -> 3 -> 2 -> 1) with uniform brightness.

### 9. Observation
Step duration verified: 150.0 ms per channel. Total loop cycle period: 900.0 ms.

### 10. Inference
Demonstrated multi-channel parallel GPIO output control and array-driven state sequencing on ARM Cortex-M3.
