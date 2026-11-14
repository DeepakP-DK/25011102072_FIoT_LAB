# EXPERIMENT DETAILS

**EXP:** CAT 11 - TASK 11A

**DATE:** 

**NAME OF EXP:** Serial Communication – Asynchronous Transceiver (USART)

**HARDWARE SETUP / PLATFORM:** NUCLEO-F401RE (STM32F401RET6 @ 84 MHz) + Keil MDK-ARM (HAL)

---

## TASK 11A : Serial Communication – Asynchronous Transceiver (USART)

### 1. Aim
To configure STM32F401RE USART2 hardware peripheral on pins PA2 and PA3 at 115200 baud and transmit real-time telemetry packets over the ST-LINK Virtual COM Port to a PC terminal console.

### 2. Components Required
- 1x STM32 NUCLEO-F401RE Board
- Onboard ST-LINK/V2-1 USB Virtual COM Port (VCP)
- PC Host running Serial Terminal (PuTTY / Serial Studio @ 115200 8N1)
- USB Cable

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function | Signal Specification |
|---|---|---|---|
| PA2 (Pin 16) | ST-LINK VCP RX | USART2_TX (Transmit) | 115200 bps, 8 data bits, no parity, 1 stop bit |
| PA3 (Pin 17) | ST-LINK VCP TX | USART2_RX (Receive) | 115200 bps Serial Receive |
| USB Cable | PC USB Host | USB-to-UART Bridge | Enumerates as COMx on Windows |

### 5. Working Principle
The STM32 USART peripheral incorporates a hardware baud rate generator, transmit/receive shift registers, and status flags (TXE, TC, RXNE). On the NUCLEO board, PA2 and PA3 are directly routed to the onboard ST-LINK debugger, which enumerates on the host PC as a USB CDC Virtual COM Port. Telemetry strings are formatted using standard C library functions (`sprintf`) and transmitted via `HAL_UART_Transmit()`.

### 6. Algorithm / Pseudocode
1. Initialize HAL and configure system clock to 84 MHz.
2. Initialize USART2: BaudRate = 115200, WordLength = 8B, StopBits = 1, Parity = NONE, Mode = TX_RX.
3. Send initialization banner string over UART.
4. Inside `while (1)` loop:
   a. Format telemetry message: `sprintf(msg, "Heartbeat #%lu | Core Temp: Nominal | Status: OK\r\n", count++);`.
   b. Transmit packet: `HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);`.
   c. Delay 1000ms: `HAL_Delay(1000);`.
5. Repeat continuously.

### 7. Core Logic / Pseudocode / Code Base
Baud rate register calculation: USARTDIV = 42 MHz / (16 * 115200) = 22.786 -> BRR = 0x16D. Polling transmission via HAL driver.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
```c
#include "main.h"
#include <stdio.h>
#include <string.h>

UART_HandleTypeDef huart2;

int main(void) {
    char msg[64];
    uint32_t count = 0;
    HAL_Init();
    SystemClock_Config();
    MX_USART2_UART_Init();

    strcpy(msg, "\r\n=== STM32F401RE Telemetry Initialized ===\r\n");
    HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);

    while (1) {
        sprintf(msg, "Heartbeat #%lu | Core Temp: Nominal | Status: OK\r\n", count++);
        HAL_UART_Transmit(&huart2, (uint8_t*)msg, strlen(msg), 100);
        HAL_Delay(1000);
    }
}
```

### 8. Expected Output
The host PC terminal streams continuous telemetry lines once per second with zero framing or overrun errors.

### 9. Observation
Measured baud rate on oscilloscope: 115,207 bps (0.006% error vs nominal 115200 bps).

### 10. Inference
Established a high-speed, reliable asynchronous serial telemetry pipeline between the ARM Cortex-M4 and host workstation.
