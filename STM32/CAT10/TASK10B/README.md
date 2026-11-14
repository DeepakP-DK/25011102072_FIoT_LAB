# EXPERIMENT DETAILS

**EXP:** CAT 10 - TASK 10B

**DATE:** 

**NAME OF EXP:** Timer Actuation – Servo Motor Angle Positioner

**HARDWARE SETUP / PLATFORM:** STM32 Blue Pill Board (STM32F103C8T6 @ 72 MHz) + Keil MDK-ARM (HAL)

---

## TASK 10B : Timer Actuation – Servo Motor Angle Positioner

### 1. Aim
To configure STM32 Timer TIM2 Channel 2 (PA1) to generate a 50 Hz PWM servo control signal (20ms frame) and position an SG90 micro-servo arm sequentially at 0°, 90°, and 180°.

### 2. Components Required
- 1x STM32F103C8T6 Blue Pill Board
- 1x TowerPro SG90 9g Micro-Servo Motor
- 1x External 5V 2A Regulated DC Power Supply
- 1x 100uF Electrolytic Capacitor (Power Rail Decoupling)
- Common Ground Bus & Jumper Wires

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Servo Lead | Function | Specification |
|---|---|---|---|
| PA1 (Pin 11) | Orange / Yellow Wire | TIM2_CH2 PWM Control Pulse | 50 Hz (1.0ms - 2.0ms pulse) |
| Ext +5V Rail | Red Wire | Servo Motor Power | High-current +5.0V supply |
| Common Ground | Brown Wire & MCU GND | Electrical Return Path | Common 0V Reference |

### 5. Working Principle
Standard RC analog servos require a 50 Hz PWM control signal (20ms period). The angular position is determined by the HIGH pulse duration: 1.0ms = 0°, 1.5ms = 90° (neutral center), 2.0ms = 180°. TIM2 is clocked at 72 MHz. Prescaler PSC = 71 yields a 1.0 MHz timer clock (1 us per tick). ARR = 19999 sets the period to 20,000 us (20ms = 50 Hz). Setting CCR2 to 1000 yields 1.0ms; CCR2 = 1500 yields 1.5ms; CCR2 = 2000 yields 2.0ms.

### 6. Algorithm / Pseudocode
1. Configure TIM2 with Prescaler = 71, Period = 19999 (50 Hz).
2. Configure Channel 2 in PWM Mode 1.
3. Start PWM: `HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_2);`.
4. In `while (1)` loop:
   a. Position 0°: `__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 1000); HAL_Delay(1000);`.
   b. Position 90°: `__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 1500); HAL_Delay(1000);`.
   c. Position 180°: `__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 2000); HAL_Delay(1000);`.
5. Repeat continuously.

### 7. Core Logic / Code Base
Timer PWM pulse mapping conforming to standard RC servo pulse specifications.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
```c
#include "main.h"

TIM_HandleTypeDef htim2;

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_TIM2_Init();

    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_2);

    while (1) {
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 1000); /* 0 deg */
        HAL_Delay(1000);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 1500); /* 90 deg */
        HAL_Delay(1000);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 2000); /* 180 deg */
        HAL_Delay(1000);
    }
}
```

### 8. Expected Output
The servo horn steps crisply to 0°, holds for 1s, rotates to 90°, holds for 1s, and rotates to 180° before repeating without mechanical jitter.

### 9. Observation
Pulse widths verified on DSO: 1.000 ms, 1.500 ms, 2.000 ms at 50.00 Hz.

### 10. Inference
Precision microsecond timer compare registers enable accurate, repeatable electromechanical actuation.
