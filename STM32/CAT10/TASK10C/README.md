# EXPERIMENT DETAILS

**EXP:** CAT 10 - TASK 10C

**DATE:** 

**NAME OF EXP:** Timer Multi-Channel Actuation – Dual Motor Drive

**HARDWARE SETUP / PLATFORM:** STM32 Blue Pill Board (STM32F103C8T6 @ 72 MHz) + Keil MDK-ARM (HAL)

---

## TASK 10C : Timer Multi-Channel Actuation – Dual Motor Drive

### 1. Aim
To configure STM32 Timer TIM2 in multi-channel PWM mode on Channel 3 (PA2) and Channel 4 (PA3) to control dual DC motors via an L298N driver for differential robotic steering.

### 2. Components Required
- 1x STM32F103C8T6 Blue Pill Board
- 1x L298N Dual Full-Bridge Motor Driver Module
- 2x 12V DC Geared Motors
- External 12V 2A DC Power Supply
- Common Ground Bus & Wires

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | L298N Terminal | Function | Description |
|---|---|---|---|
| PA2 (Pin 12) | ENA (Enable A) | TIM2_CH3 PWM Output | Left Motor Speed Control |
| PA3 (Pin 13) | ENB (Enable B) | TIM2_CH4 PWM Output | Right Motor Speed Control |
| PB0, PB1 | IN1, IN2 | Direction Control A | Sets Left Motor Forward/Reverse |
| PB10, PB11 | IN3, IN4 | Direction Control B | Sets Right Motor Forward/Reverse |
| Ext +12V / GND | Power Terminals | Motor Power Rail | High-voltage motor supply |

### 5. Working Principle
Multi-channel timers allow synchronous phase-aligned PWM output across multiple physical pins from a single hardware counter timebase. TIM2 Channel 3 and Channel 4 generate 10 kHz PWM to drive the enable inputs of the L298N H-bridge. Differential speed combinations (e.g. Left=75%, Right=75% for straight; Left=40%, Right=80% for turning) allow skid-steering robotic vehicle navigation.

### 6. Algorithm / Pseudocode
1. Initialize TIM2 with Prescaler = 7, Period = 999 (10 kHz PWM carrier).
2. Configure Channel 3 and Channel 4 in PWM Mode 1.
3. Start PWM on both channels: `HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3)` and `TIM_CHANNEL_4`.
4. In loop, cycle through drive states:
   a. Straight: CCR3 = 750, CCR4 = 750 (delay 2s).
   b. Left Turn: CCR3 = 400, CCR4 = 800 (delay 2s).
   c. Right Turn: CCR3 = 800, CCR4 = 400 (delay 2s).

### 7. Core Logic / Pseudocode / Code Base
Synchronized multi-channel compare register updates for robotic drive kinematics.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
```c
#include "main.h"

TIM_HandleTypeDef htim2;

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_TIM2_Init();

    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3);
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_4);

    while (1) {
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_3, 750);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_4, 750);
        HAL_Delay(2000);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_3, 400);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_4, 800);
        HAL_Delay(2000);
    }
}
```

### 8. Expected Output
Both DC motors rotate smoothly with dynamically controlled differential speeds matching programmed steering states.

### 9. Observation
10 kHz PWM eliminated audible motor whine completely while providing linear torque response.

### 10. Inference
Multi-channel hardware timers provide synchronized, phase-coherent control for complex multi-actuator robotics.
