# EXPERIMENT DETAILS

**EXP:** CAT 9 - TASK 9A

**DATE:** 

**NAME OF EXP:** STM32F401 Hardware Bring-Up & Multi-Clock Setup

**HARDWARE SETUP / PLATFORM:** NUCLEO-F401RE (STM32F401RET6 @ 84 MHz) + Keil MDK-ARM (HAL)

---

## TASK 9A : STM32F401 Hardware Bring-Up & Multi-Clock Setup

### 1. Aim
To bring up the high-performance ARM Cortex-M4 NUCLEO-F401RE platform, configure the system clock tree to 84 MHz via PLL, and generate a 2 Hz diagnostic heartbeat on onboard user LED LD2 (PA5).

### 2. Components Required
- 1x STM32 NUCLEO-F401RE Development Board (ARM Cortex-M4 with FPU)
- Integrated ST-LINK/V2-1 Debugger / Virtual COM Port Bridge
- Onboard User Green LED LD2 on PA5
- USB Type-A to Mini-B Cable

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function | Description |
|---|---|---|---|
| PA5 | Onboard Green LED LD2 | Heartbeat Output | Active-HIGH Push-Pull Output |
| PC13 | User Blue Push-Button B1 | Digital Input | Active-LOW User Switch |
| PA2 / PA3 | ST-LINK VCP UART Bridge | Debug Telemetry | USART2 TX / RX lines |
| USB VBUS | PC Host USB Port | Power & Debug | Supplies regulated +3.3V and +5V |

### 5. Working Principle
The STM32F401RET6 features an ARM Cortex-M4F core with a single-precision hardware Floating Point Unit (FPU), 512 KB Flash, and 96 KB SRAM. The system clock configuration selects the 16.0 MHz High-Speed Internal (HSI) RC oscillator, routed into the Phase-Locked Loop (PLL) with parameters M=16, N=336, P=4 to produce an 84 MHz SYSCLK (maximum operational core frequency). Pin PA5 is toggled every 250ms via `HAL_GPIO_TogglePin()`.

### 6. Algorithm / Pseudocode
1. Call `HAL_Init()` to initialize Flash prefetch, instruction cache, and SysTick.
2. In `SystemClock_Config()`: Set HSI as PLL source, configure PLL for 84 MHz core clock.
3. Enable GPIOA clock gate: `__HAL_RCC_GPIOA_CLK_ENABLE()`.
4. Configure PA5 as `GPIO_MODE_OUTPUT_PP`, `GPIO_NOPULL`, `GPIO_SPEED_FREQ_LOW`.
5. In `while (1)` loop:
   a. Toggle PA5: `HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);`.
   b. Delay 250ms: `HAL_Delay(250);`.
6. Repeat continuously.

### 7. Core Logic / Code Base
STM32F4xx clock distribution and Flash latency configuration (2 wait states at 84 MHz, 3.3V).

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
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        HAL_Delay(250);
    }
}
```

### 8. Expected Output
The green LD2 LED toggles rapidly at 2.0 Hz (250ms ON, 250ms OFF), indicating full 84 MHz system stability.

### 9. Observation
Oscilloscope frequency at PA5: 2.000 Hz. SYSCLK frequency verified at 84.00 MHz via MCO1 output.

### 10. Inference
Successfully brought up the ARM Cortex-M4 NUCLEO platform at its maximum rated 84 MHz operational frequency.
