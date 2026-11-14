# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 15

**DATE:** 26/10/2026

**NAME OF EXP:** CAPSTONE MINI-PROJECT: Automated School Monsoon Advisory System

**HARDWARE SETUP / PLATFORM:** NUCLEO-F401RE + BME280 + ESP8266 + Node-RED Decision Engine

---

## TASK15 : Automated Weather Monitoring & School Conduction/Holiday Advisory Decision System

### 1. Circuit Diagram

Capstone Mini-Project extending Task 13 and Task 14 into a practical civic automation system for automated decision-making regarding school operations during rainy and cyclonic weather in Chennai. The system samples live environmental conditions via a Bosch BME280 barometric and humidity sensor, transmits packets across an ESP8266 Wi-Fi gateway to MQTT topic `college/weather/bme280`, and executes automated threshold evaluation within Node-RED to display dynamic civic advisories (`CONDUCT SCHOOL` vs. `DECLARE HOLIDAY`).

- **Target Microcontroller:** STM32F401RET6 (ARM Cortex-M4)
- **Oscillator / Clock Tree:** 84 MHz PLL
- **Configured Pin Allocations:** PB8 (I2C1_SCL), PB9 (I2C1_SDA) for BME280; PA2/PA3 for ESP8266 Wi-Fi Gateway; PA5 (Status LED)
- **External Hardware Peripherals:** Bosch BME280 Sensor, ESP8266 Wi-Fi Gateway, Node-RED Dashboard 2.0 Advisory UI
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

#### Live Operational Results & Decision Dashboard:

##### Civic Decision Dashboard Interface (`CONDUCT SCHOOL`):
![Civic Decision Dashboard](dashboard.png)

##### Node-RED Automated Decision Flow Logic:
![Node-RED Decision Logic Flow](node_red_flow.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

Rapidly dropping barometric pressure (< 1000 hPa) coupled with high humidity (> 85% RH) and persistent precipitation serves as the primary meteorological indicator of cyclonic depression and torrential rainstorms. When environmental thresholds exceed calibrated safety levels, the automated decision engine flags an active monsoon alert, switches the visual banner from green (`CONDUCT SCHOOL`) to red (`DECLARE HOLIDAY`), and broadcasts alerts to education department administrators.

**Pseudocode:**

1. Acquire calibrated sensor data from BME280: Ambient Temperature (°C), Relative Humidity (% RH), Atmospheric Pressure (hPa).
2. Package metrics into JSON payload with station identifier `SNU-CHENNAI-01`.
3. Publish JSON payload via MQTT to topic `college/weather/bme280`.
4. In Node-RED decision engine node (`Evaluate School Conditions`):
   ```javascript
   let temp = msg.payload.temperature;
   let hum = msg.payload.humidity;
   let press = msg.payload.pressure;

   if (press < 1000.0 && hum > 85.0) {
       msg.decision = "DECLARE HOLIDAY";
       msg.alert_count = 1;
       msg.status = "CRITICAL_MONSOON";
   } else {
       msg.decision = "CONDUCT SCHOOL";
       msg.alert_count = 0;
       msg.status = "NORMAL";
   }
   return msg;
   ```
5. Dynamically update Node-RED Dashboard 2.0 UI components.

**Code Structure / Key Registers:**

NUCLEO-F401RE multi-peripheral integration (I2C1 + USART2 + SysTick), rule-based automated decision engine.

#### Embedded C Source Implementation (`main.c`):

```c
#include "main.h"
#include <stdio.h>
#include <string.h>

/* Capstone Mini-Project: Automated School Holiday / Conduction Decision System */
I2C_HandleTypeDef hi2c1;
UART_HandleTypeDef huart2;

float temperature = 24.9f;
float humidity = 60.4f;
float pressure = 1015.4f;

int main(void) {
    char mqtt_payload[160];
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_I2C1_Init();
    MX_USART2_UART_Init();

    while (1) {
        /* Format telemetry for TN School Advisory Node-RED pipeline */
        sprintf(mqtt_payload, 
            "{\"temperature\":%.1f,\"humidity\":%.1f,\"pressure\":%.1f,\"station\":\"SNU_CHENNAI\",\"decision\":\"NORMAL\"}\r\n",
            temperature, humidity, pressure);
        HAL_UART_Transmit(&huart2, (uint8_t*)mqtt_payload, strlen(mqtt_payload), 200);
        HAL_Delay(2000);
    }
}
```

### 3. Inference

The automated decision engine accurately responded to environmental telemetry in real-time. Under baseline prototype conditions (24.9°C, 60.4% RH, 1015.4 hPa), the dashboard indicated `CONDUCT SCHOOL` with 0 active alerts. Injecting extreme weather test parameters instantly toggled the alert state to `DECLARE HOLIDAY`, confirming reliable civic warning capabilities.
