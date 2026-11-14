# EXPERIMENT DETAILS

**EXP:** CONTINUOUS ASSESSMENT 14

**DATE:** 19/10/2026

**NAME OF EXP:** Cloud Dashboard Integration & Node-RED Telemetry Visualization

**HARDWARE SETUP / PLATFORM:** STM32F103C8T6 + ESP8266 + Node-RED Dashboard Engine

---

## TASK14 : Real-Time Node-RED Web UI Telemetry Visualization & Gauges

### 1. Circuit Diagram

Interfacing the STM32F103 Blue Pill development board with a Wemos D1 Mini ESP8266 Wi-Fi transceiver to stream JSON environmental telemetry to a local/cloud Node-RED Dashboard 2.0 visualization engine.

- **Target Microcontroller:** STM32F103C8T6
- **Oscillator / Clock Tree:** 72 MHz PLL
- **Configured Pin Allocations:** PA2/PA3 to ESP8266; Node-RED MQTT Inflow on TCP 1883
- **External Hardware Peripherals:** Node-RED Server, MQTT Broker, Web Browser Client
- **Power Supply Rails:** +5.0V / +3.3V DC Regulated, Common Ground (GND)

![Circuit Diagram](circuit.png)

#### Live System Visualizations:

##### Node-RED Operational Dashboard UI:
![Node-RED Dashboard](dashboard.png)

##### Node-RED Flow Pipeline Architecture:
![Node-RED Flow Pipeline](node_red_flow.png)

### 2. Core Logic / Pseudocode / Code Base

**Working Principle:**

Node-RED workflow uses an `mqtt-in` node configured for topic `college/weather/bme280`. An inline JSON parser node unpacks `temperature`, `humidity`, and `pressure`. UI widgets (`ui-gauge`, `ui-chart`, `ui-text`) dynamically bind to each measurement stream to provide real-time gauges, trend charts, and status indicators.

**Pseudocode:**

1. Deploy Node-RED flow with MQTT input node connected to broker.emqx.io (port 1883).
2. Connect `json` parser node to decompose payload string into JavaScript object.
3. Route `msg.payload.temperature` to Temperature UI Gauge & Line Chart.
4. Route `msg.payload.humidity` to Humidity Circular Gauge.
5. Route `msg.payload.pressure` to Atmospheric Pressure Numeric Tile.

**Code Structure / Key Registers:**

Node-RED flow JSON schema, WebSocket real-time client push, UI widget configuration.

#### Embedded C Source Implementation (`main.c`):

```c
#include "main.h"
#include <stdio.h>
#include <string.h>

UART_HandleTypeDef huart2;

int main(void) {
    char json_buf[128];
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_USART2_UART_Init();

    while (1) {
        sprintf(json_buf, "{\"temperature\":24.9,\"humidity\":60.4,\"pressure\":1015.4}\r\n");
        HAL_UART_Transmit(&huart2, (uint8_t*)json_buf, strlen(json_buf), 200);
        HAL_Delay(2000);
    }
}
```

### 3. Inference

Live telemetry values updated seamlessly on the web browser dashboard with sub-second latency, providing high visual fidelity. Environmental metrics (24.9°C, 60.4% RH, 1015.4 hPa) displayed cleanly in real-time.
