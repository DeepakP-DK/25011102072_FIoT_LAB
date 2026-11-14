# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 8

**DATE:** 07/09/2026

**NAME OF EXP:** STM32 Digital Input & Push-Button Control

**HARDWARE SETUP / PLATFORM:** STM32F103C8T6 (Blue Pill) + Keil MDK-ARM (HAL)

---

## TASK8B : Push-Button Controlled LED Latch on PA0 and PC13

### 1. Circuit Diagram

Interfaces an active-low tactile push button to PA0 using internal pull-up resistor. Pressing the button toggles the operational state of the onboard LED on PC13.

- **Target Microcontroller:** STM32F103C8T6
- **Oscillator / Clock Tree:** 72 MHz PLL
- **Configured Pin Allocations:** PA0 as GPIO Input with Internal Pull-up (PULLUP); PC13 as GPIO Output
- **External Hardware Peripherals:** External Push Button switch to GND on PA0, Onboard LED on PC13
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

Internal pull-up holds PA0 at 3.3V (HIGH) when idle. Pressing the button shorts PA0 to GND (LOW). HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) senses the falling transition. A 20ms HAL_Delay provides debounce filtering.

**Pseudocode:**

1. Configure PA0 as GPIO_MODE_INPUT with GPIO_PULLUP.
2. Configure PC13 as GPIO_MODE_OUTPUT_PP.
3. In while(1) loop:
   a. If HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET:
      i. HAL_Delay(20) debounce.
      ii. If still RESET:
          HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
          while(HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET);
          HAL_Delay(20);

**Code Structure / Key Registers:**

GPIO HAL Input read APIs, software debouncing, and state toggling.

#### Embedded C Source Implementation (`main.c`):

```c
#include "main.h"

void SystemClock_Config(void);
static void MX_GPIO_Init(void);

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();

    while (1) {
        if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET) {
            HAL_Delay(20); /* Debounce */
            if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET) {
                HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
                while (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET);
                HAL_Delay(20);
            }
        }
    }
}
```

### 3. Inference

Single button presses cleanly toggled the LED state with zero chatter false-triggers, proving internal pull-up reliability.
