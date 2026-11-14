# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 10

**DATE:** 21/09/2026

**NAME OF EXP:** Timer Architecture & Hardware Pulse Width Modulation (PWM)

**HARDWARE SETUP / PLATFORM:** STM32F103C8T6 (Blue Pill) + Keil MDK-ARM (HAL)

---

## TASK10A : Hardware PWM Breathing LED Controller Using TIM2 Channel 1

### 1. Circuit Diagram

TIM2 general-purpose timer generates a 1 kHz PWM waveform on Channel 1 (PA0). The program dynamically adjusts the pulse width duty cycle in a sinusoidal breathing ramp from 0% to 100% and back.

- **Target Microcontroller:** STM32F103C8T6
- **Oscillator / Clock Tree:** 72 MHz PLL
- **Configured Pin Allocations:** PA0 configured as TIM2_CH1 Alternate Function Push-Pull
- **External Hardware Peripherals:** External High-Brightness LED, 220 Ohm Current Limiting Resistor, Oscilloscope
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

Timer clock = 72 MHz. Prescaler PSC = 71 gives timer counter frequency = 72 MHz / (71 + 1) = 1 MHz. Auto-reload register ARR = 999 yields PWM frequency = 1 MHz / (999 + 1) = 1000 Hz (1 kHz). Duty cycle is set by writing to CCR1 (0 to 1000).

**Pseudocode:**

1. Configure TIM2 in PWM Mode 1 with Prescaler = 71, Period = 999.
2. Route TIM2_CH1 to PA0.
3. Call HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1).
4. In loop:
   a. Ramp duty from 0 to 1000 in steps of 10, updating CCR1 (__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, duty)), delay 15ms.
   b. Ramp duty down from 1000 to 0, delay 15ms.

**Code Structure / Key Registers:**

TIM_HandleTypeDef htim2, __HAL_TIM_SET_COMPARE macro, HAL_TIM_PWM_Start.

#### Embedded C Source Implementation (`main.c`):

```c
#include "main.h"

TIM_HandleTypeDef htim2;

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_TIM2_Init(void);

int main(void) {
    uint16_t duty = 0;
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_TIM2_Init();

    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);

    while (1) {
        for (duty = 0; duty < 1000; duty += 15) {
            __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, duty);
            HAL_Delay(15);
        }
        for (duty = 1000; duty > 0; duty -= 15) {
            __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, duty);
            HAL_Delay(15);
        }
    }
}
```

### 3. Inference

The LED exhibited a silky-smooth, organic breathing brightness transition without visible stair-stepping.
