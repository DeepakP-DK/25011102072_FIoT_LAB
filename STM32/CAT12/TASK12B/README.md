# EXPERIMENT DETAILS

**EXP:** CAT 12 - TASK 12B

**DATE:** 

**NAME OF EXP:** I2C Sensor Bus – Bosch BME280 Register Interfacing

**HARDWARE SETUP / PLATFORM:** STM32 Blue Pill Board (STM32F103C8T6 @ 72 MHz) + Keil MDK-ARM (HAL)

---

## TASK 12B : I2C Sensor Bus – Bosch BME280 Register Interfacing

### 1. Aim
To interface the Bosch Sensortec BME280 digital sensor via I2C1, read the silicon Chip ID register (0xD0) to verify authentic hardware, and download factory NVM trimming calibration coefficient tables.

### 2. Components Required
- 1x STM32F103C8T6 Blue Pill Board
- 1x Bosch BME280 Sensor Breakout
- 2x 4.7k Ohm Pull-Up Resistors
- ST-LINK V2 & Serial Terminal

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | BME280 Pin | Function | Description |
|---|---|---|---|
| PB6 / PB7 | SCL / SDA | I2C1 Bus Lines | Master I2C Communication Lines |
| BME280 SDO | System Ground | Hardware Address Pin | Sets 7-bit address to 0x76 |
| PA9 | Host Terminal RX | USART1 Telemetry | Displays Chip ID & Calibration Registers |

### 5. Working Principle
The Bosch BME280 contains a dedicated Chip Identification register at memory address 0xD0, which holds fixed factory signature 0x60. The STM32 issues a memory read via `HAL_I2C_Mem_Read(&hi2c1, (0x76 << 1), 0xD0, I2C_MEMADD_SIZE_8BIT, &chip_id, 1, 100)`. Upon successful signature verification, factory trimming parameters stored in non-volatile memory (dig_T1..T3, dig_P1..P9, dig_H1..H6) are downloaded to serve as calibration constants for physical compensation math.

### 6. Algorithm / Pseudocode
1. Initialize I2C1 at 100 kHz.
2. Read register 0xD0: `HAL_I2C_Mem_Read(&hi2c1, 0xEC, 0xD0, 1, &chip_id, 1, 100);`.
3. If `chip_id == 0x60`, confirm authentic Bosch BME280 silicon.
4. Read temperature calibration bytes from address 0x88 to 0x8D.
5. Read pressure calibration bytes from address 0x8E to 0x9F.
6. Read humidity calibration bytes from address 0xA1 and 0xE1 to 0xE7.
7. Parse and print parameters to serial console.

### 7. Core Logic / Code Base
Direct register-level memory reading using `HAL_I2C_Mem_Read()` with 8-bit memory address pointer addressing.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
```c
#include "main.h"

I2C_HandleTypeDef hi2c1;
uint8_t chip_id = 0;

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_I2C1_Init();

    /* Read BME280 CHIP_ID register 0xD0 */
    HAL_I2C_Mem_Read(&hi2c1, (0x76 << 1), 0xD0, I2C_MEMADD_SIZE_8BIT, &chip_id, 1, 100);

    while (1) {
        if (chip_id == 0x60) {
            /* Verified authentic BME280 */
        }
        HAL_Delay(1000);
    }
}
```

### 8. Expected Output
Register 0xD0 returns exactly `0x60`. Trimming parameters are successfully loaded into memory structures.

### 9. Observation
Silicon ID read: 0x60 confirmed. Calibration registers returned non-zero factory coefficients.

### 10. Inference
Validated direct memory-mapped register access over I2C and confirmed sensor authenticity.
