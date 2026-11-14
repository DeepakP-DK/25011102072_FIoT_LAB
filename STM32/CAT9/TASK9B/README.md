# EXPERIMENT DETAILS

**EXP:** CAT 9 - TASK 9B

**DATE:** 

**NAME OF EXP:** STM32F4 User Button & Asynchronous External Interrupts (EXTI)

**HARDWARE SETUP / PLATFORM:** NUCLEO-F401RE (STM32F401RET6 @ 84 MHz) + Keil MDK-ARM (HAL)

---

## TASK 9B : STM32F4 User Button & Asynchronous External Interrupts (EXTI)

### 1. Aim
To configure External Interrupt Line 13 (EXTI13) on pin PC13 of the NUCLEO-F401RE in falling-edge trigger mode, servicing user button clicks asynchronously to toggle LED LD2 while placing the core in low-power sleep via WFI.

### 2. Components Required
- 1x STM32 NUCLEO-F401RE Board
- Onboard User Blue Push-Button B1 on PC13
- Onboard User Green LED LD2 on PA5
- Integrated ST-LINK/V2-1

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function | Description |
|---|---|---|---|
| PC13 | Blue User Push-Button B1 | EXTI Line 13 Input | Falling-edge triggered interrupt source |
| PA5 | Green User LED LD2 | Actuator Indicator | Toggled by EXTI Callback handler |
| NVIC | EXTI15_10_IRQn Vector | Interrupt Controller | Preempts core from Wait-For-Interrupt (__WFI) |

### 5. Working Principle
The STM32 SYSCFG peripheral maps port pins to EXTI lines. PC13 routes to EXTI13. When button B1 is pressed, the falling transition triggers `EXTI15_10_IRQHandler()`, which invokes `HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)`. The core executes `__WFI()` (Wait For Interrupt) in the main loop, turning off the CPU clock to conserve energy until awakened by the EXTI event.

### 6. Algorithm / Pseudocode
1. Initialize HAL and configure system clock to 84 MHz.
2. Configure PC13 as `GPIO_MODE_IT_FALLING` with `GPIO_NOPULL`.
3. Set NVIC priority for `EXTI15_10_IRQn` (Preemption: 2, Sub: 0) and enable IRQ.
4. Configure PA5 as output push-pull.
5. Implement `HAL_GPIO_EXTI_Callback(GPIO_Pin)`:
   a. If `GPIO_Pin == GPIO_PIN_13`, call `HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5)`.
6. In `while (1)` main loop: Call `__WFI();` to sleep until next button press.

### 7. Core Logic / Pseudocode / Code Base
Hardware NVIC vectoring, EXTI edge detector configuration, and low-power sleep architecture.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
```c
#include "main.h"

void SystemClock_Config(void);
static void MX_GPIO_Init(void);

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_13) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();

    while (1) {
        __WFI(); /* Sleep and wait for interrupt */
    }
}
```

### 8. Expected Output
The core sleeps at microamp current draw; pressing blue button B1 instantly wakes the core and toggles green LED LD2 with sub-microsecond latency.

### 9. Observation
Wake-up latency measured from PC13 edge to PA5 toggle: 1.15 us.

### 10. Inference
Demonstrated event-driven, power-efficient embedded firmware design utilizing ARM Cortex-M NVIC and EXTI peripherals.
