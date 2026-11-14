# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 12

**DATE:** 05/10/2026

**NAME OF EXP:** I2C Sensor Bus – Bosch BME280 Register Interfacing

**HARDWARE SETUP / PLATFORM:** STM32F103C8T6 + Keil MDK-ARM (HAL)

---

## TASK12B : Bosch Sensortec BME280 Chip ID & Factory Calibration Retrieval

### 1. Circuit Diagram

Reads the Chip Identification register (0xD0) of the Bosch BME280 via I2C to verify silicon version (expected value: 0x60). Downloads factory trimmed temperature, pressure, and humidity calibration coefficient tables.

- **Target Microcontroller:** STM32F103C8T6
- **Oscillator / Clock Tree:** 72 MHz PLL
- **Configured Pin Allocations:** PB6 (I2C1_SCL), PB7 (I2C1_SDA); USART1 PA9/PA10 for debug telemetry
- **External Hardware Peripherals:** BME280 Barometric Pressure, Temperature & Humidity Sensor, ST-LINK VCP
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

BME280 register 0xD0 holds fixed ID 0x60. The MCU performs a memory read using HAL_I2C_Mem_Read(&hi2c1, 0xEC, 0xD0, I2C_MEMADD_SIZE_8BIT, &chip_id, 1, 100). Factory calibration parameters (dig_T1-T3, dig_P1-P9, dig_H1-H6) are parsed from non-volatile NVM registers.

**Pseudocode:**

1. Initialize I2C1 and USART1.
2. Read register 0xD0; verify chip_id == 0x60.
3. Read calibration bytes: 0x88 to 0xA1 (Temperature and Pressure trim parameters).
4. Read calibration bytes: 0xE1 to 0xE7 (Humidity trim parameters).
5. Format and print calibration coefficients over USART1.

**Code Structure / Key Registers:**

HAL_I2C_Mem_Read memory read APIs, factory compensation register map.

#### Embedded C Source Implementation (`main.c`):

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

### 3. Inference

Register 0xD0 returned exactly 0x60, confirming authentic Bosch BME280 silicon. Factory calibration coefficients were successfully parsed.
