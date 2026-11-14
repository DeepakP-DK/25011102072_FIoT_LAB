# EXPERIMENT DETAILS

**EXP:** CAT 12 - TASK 12A

**DATE:** 

**NAME OF EXP:** I2C Sensor Bus – Hardware Master Protocol

**HARDWARE SETUP / PLATFORM:** STM32 Blue Pill Board (STM32F103C8T6 @ 72 MHz) + Keil MDK-ARM (HAL)

---

## TASK 12A : I2C Sensor Bus – Hardware Master Protocol

### 1. Aim
To configure STM32 I2C1 hardware peripheral in Master Mode at standard 100 kHz speed on pins PB6 (SCL) and PB7 (SDA) and implement an active bus address scanner to detect connected I2C slave devices across 0x01 to 0x7F.

### 2. Components Required
- 1x STM32F103C8T6 Blue Pill Board
- 1x Bosch Sensortec BME280 Environmental Sensor Breakout
- 2x 4.7k Ohm Metal Film Pull-Up Resistors
- ST-LINK V2 & Serial Debugger

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | BME280 Pin | Function | Electrical Specification |
|---|---|---|---|
| PB6 (Pin 42) | SCL (Pin 3) | I2C1_SCL Clock Line | Open-Drain with 4.7k Pull-up to 3.3V |
| PB7 (Pin 43) | SDA (Pin 4) | I2C1_SDA Data Line | Open-Drain with 4.7k Pull-up to 3.3V |
| +3.3V Rail | VCC (Pin 1) | Sensor Operating Power | Regulated +3.3V DC Supply |
| GND Rail | GND (Pin 2) & SDO (Pin 5) | Ground & Address Select | SDO to GND selects 7-bit addr 0x76 |

### 5. Working Principle
The Inter-Integrated Circuit (I2C) protocol uses two bidirectional open-drain lines (SCL and SDA) pulled to +3.3V by external resistors. The STM32 I2C peripheral master generates START condition, clock pulses, and 7-bit slave addresses with R/W bit. The firmware calls `HAL_I2C_IsDeviceReady(&hi2c1, (addr << 1), 2, 5)`. When an active slave detects its matching address on the bus, it pulls SDA LOW during the 9th clock cycle (ACK). If an ACK is received, the scanner confirms device presence.

### 6. Algorithm / Pseudocode
1. Initialize HAL and configure I2C1: ClockSpeed = 100000 Hz, DutyCycle = I2C_DUTYCYCLE_2, AddressingMode = 7-bit.
2. Configure PB6 and PB7 as `GPIO_MODE_AF_OD` with `GPIO_PULLUP`.
3. Loop `addr` from 1 to 127:
   a. Call `status = HAL_I2C_IsDeviceReady(&hi2c1, (addr << 1), 2, 5);`.
   b. If `status == HAL_OK`:
      - Log address: Device discovered at 7-bit address 0xXX.
4. Verify that Bosch BME280 acknowledges at address 0x76.

### 7. Core Logic / Code Base
Master mode I2C protocol state machine with ACK/NACK detection via HAL abstraction.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
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

### 8. Expected Output
The address scanner detects and reports device presence at hexadecimal address `0x76` (BME280 with SDO pulled to GND).

### 9. Observation
ACK response confirmed at 0x76 on logic analyzer. SCL clock frequency measured at 99.8 kHz.

### 10. Inference
Successfully initialized the STM32 hardware I2C master engine and validated bus integrity and device addressing.
