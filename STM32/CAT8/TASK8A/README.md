# EXPERIMENT DETAILS

**EXP:** CAT 8 - TASK 8A

**DATE:** 

**NAME OF EXP:** STM32 GPIO Bring-Up & Basic Output Control

**HARDWARE SETUP / PLATFORM:** STM32 Blue Pill Board (STM32F103C8T6 @ 72 MHz) + Keil MDK-ARM (HAL)

---

## TASK 8A : STM32 GPIO Bring-Up & Basic Output Control

### 1. Aim
To configure GPIO Port C Pin 13 of the STM32F103C8T6 microcontroller as a digital push-pull output and toggle the onboard user LED at 1 Hz using the Cortex-M SysTick timebase.

### 2. Components Required
- 1x STM32F103C8T6 Blue Pill Development Board (ARM Cortex-M3)
- 1x ST-LINK V2 In-Circuit Debugger / Programmer
- Onboard User SMD LED (connected to PC13 through 510 Ohm to 3.3V)
- 8.0 MHz External Crystal (HSE) on Blue Pill
- Micro-USB Cable & Jumper Wires

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function | Direction / Logic |
|---|---|---|---|
| PC13 | Onboard SMD User LED | Indicator Output | Active-LOW (0 = ON, 1 = OFF) |
| PA13 (SWDIO) | ST-LINK V2 SWDIO Pin | Serial Wire Data Input/Output | Debug Interface |
| PA14 (SWCLK) | ST-LINK V2 SWCLK Pin | Serial Wire Clock Line | Debug Interface |
| +3.3V & GND | ST-LINK +3.3V & GND | Target Operating Power | Regulated 3.3V Rail |
| BOOT0 / BOOT1 | Jumpers tied to GND | Flash Memory Boot Selection | Normal Operation |

### 5. Working Principle
The STM32F103C8T6 contains a 32-bit ARM Cortex-M3 core operating at up to 72 MHz. The onboard user LED on PC13 is wired in active-LOW configuration (anode tied through 510 Ohm to +3.3V). Calling `HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET)` sinks current and turns ON the LED. Calling `HAL_Delay(500)` utilizes the 1ms Cortex-M SysTick hardware counter to generate non-drifting millisecond delays.

### 6. Algorithm / Pseudocode
1. Call `HAL_Init()` to initialize Flash interface, Systick timer, and NVIC priority grouping.
2. Configure System Clock to 72 MHz using HSE (8 MHz) and PLL multiplication (x9).
3. Enable GPIOC clock gate: `__HAL_RCC_GPIOC_CLK_ENABLE()`.
4. Configure PC13 as `GPIO_MODE_OUTPUT_PP`, `GPIO_NOPULL`, `GPIO_SPEED_FREQ_LOW`.
5. In the `while (1)` super-loop:
   a. Toggle PC13: `HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);`.
   b. Delay 500ms: `HAL_Delay(500);`.
6. Repeat indefinitely.

### 7. Core Logic / Code Base
Standard STM32 HAL GPIO APIs: `HAL_GPIO_TogglePin()` and `HAL_Delay()` driven by the 1ms SysTick interrupt handler.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
```c
#include "main.h"

void SystemClock_Config(void);
static void MX_GPIO_Init(void);

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();

    while (1) {
        HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
        HAL_Delay(500);
    }
}

static void MX_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    __HAL_RCC_GPIOC_CLK_ENABLE();

    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
    GPIO_InitStruct.Pin = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
}
```

### 8. Expected Output
The onboard green LED on PC13 blinks symmetrically at exactly 1.0 Hz (500ms ON, 500ms OFF).

### 9. Observation
Oscilloscope frequency measurement at PC13: 1.000 Hz, 50.0% duty cycle, 3.30V logic high.

### 10. Inference
Successfully initialized the STM32F103 hardware platform and validated HAL GPIO output and SysTick timing.
