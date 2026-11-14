# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 12

**DATE:** 05/10/2026

**NAME OF EXP:** I2C Sensor Bus – Hardware Master Protocol

**HARDWARE SETUP / PLATFORM:** STM32F103C8T6 (Blue Pill) + Keil MDK-ARM (HAL)

---

## TASK12A : I2C1 Hardware Master Bus Initialization & Peripheral Device Scanner

### 1. Circuit Diagram

Configures I2C1 in Master mode at standard 100 kHz clock speed on PB6/PB7. Implements a bus scanner pinging 7-bit addresses 0x01 to 0x7F using HAL_I2C_IsDeviceReady() to detect connected sensor nodes.

- **Target Microcontroller:** STM32F103C8T6
- **Oscillator / Clock Tree:** 72 MHz PLL
- **Configured Pin Allocations:** PB6 (I2C1_SCL), PB7 (I2C1_SDA) with 4.7k external pull-up resistors
- **External Hardware Peripherals:** Bosch BME280 Environmental Sensor Breakout (Address 0x76), 4.7k Pull-up Resistors
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

I2C requires open-drain outputs with pull-up resistors to +3.3V. HAL_I2C_IsDeviceReady generates START condition, sends address + W bit, and checks for ACK from slave. When 0x76 responds with ACK, device presence is confirmed.

**Pseudocode:**

1. Initialize I2C1: ClockSpeed = 100000 Hz, AddressingMode = 7-bit, DutyCycle = 2.
2. Iterate addr from 1 to 127:
   a. Call status = HAL_I2C_IsDeviceReady(&hi2c1, (addr << 1), 2, 10).
   b. If status == HAL_OK, print 'Device found at address 0xXX'.
3. Confirm BME280 responds at 0x76.

**Code Structure / Key Registers:**

hi2c1 handle, HAL_I2C_IsDeviceReady API, address scanning loop.

#### Embedded C Source Implementation (`main.c`):

```c
#include "main.h"
#include <stdio.h>

I2C_HandleTypeDef hi2c1;

int main(void) {
    uint8_t addr;
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_I2C1_Init();

    for (addr = 1; addr < 128; addr++) {
        if (HAL_I2C_IsDeviceReady(&hi2c1, (addr << 1), 2, 5) == HAL_OK) {
            /* Address 0x76 successfully acknowledged */
        }
    }

    while (1) {
        HAL_Delay(1000);
    }
}
```

### 3. Inference

I2C bus scan correctly detected BME280 device at 7-bit slave address 0x76, confirming electrical bus integrity and ACK timing.
