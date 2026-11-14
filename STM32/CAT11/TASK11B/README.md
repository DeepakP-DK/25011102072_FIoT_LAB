# EXPERIMENT DETAILS

**EXP:** CAT 11 - TASK 11B

**DATE:** 

**NAME OF EXP:** Serial Communication – Interrupt-Driven Command Interpreter

**HARDWARE SETUP / PLATFORM:** NUCLEO-F401RE (STM32F401RET6 @ 84 MHz) + Keil MDK-ARM (HAL)

---

## TASK 11B : Serial Communication – Interrupt-Driven Command Interpreter

### 1. Aim
To implement a non-blocking, interrupt-driven Command Line Interface (CLI) shell over USART2, processing incoming character streams via RX interrupts, buffering full commands, and actuating user LED LD2.

### 2. Components Required
- 1x STM32 NUCLEO-F401RE Board
- Onboard ST-LINK VCP
- Host PC Interactive Serial Terminal (PuTTY)
- Green User LED LD2 on PA5

### 3. Circuit Diagram
The schematic diagram below illustrates the complete hardware interfacing, pin assignments, power decoupling rails, and external peripheral connections.

![Circuit Diagram](circuit.png)

### 4. Connections
The following pin-to-pin wiring table details the physical electrical interconnections:

| MCU Pin | Connected Device | Function | Description |
|---|---|---|---|
| PA2 / PA3 | ST-LINK VCP | USART2 TX / RX | Asynchronous Serial Command Bus (115200 bps) |
| PA5 | User LED LD2 | Actuator Target | Toggled by parsed 'ON' / 'OFF' commands |
| NVIC | USART2_IRQn Vector | Interrupt Controller | Serves byte arrivals non-blockingly |

### 5. Working Principle
Polling UART for user keystrokes stalls the CPU and risks byte drops. Instead, the firmware arms the RX interrupt using `HAL_UART_Receive_IT(&huart2, &rx_byte, 1)`. When a byte arrives, the hardware triggers `USART2_IRQHandler()`, invoking `HAL_UART_RxCpltCallback()`. Arriving characters are placed into a circular command buffer. When a carriage return (`\r` or `\n`) is received, the string is null-terminated and a `cmd_ready` flag is set. The main loop evaluates the command string (`ON` -> PA5 HIGH, `OFF` -> PA5 LOW) without blocking background operations.

### 6. Algorithm / Pseudocode
1. Initialize USART2 and GPIO PA5.
2. Arm non-blocking RX interrupt: `HAL_UART_Receive_IT(&huart2, &rx_byte, 1);`.
3. In `HAL_UART_RxCpltCallback(huart)`:
   a. If `rx_byte == '\r'` or `'\n'`, set `cmd_ready = 1`.
   b. Else append `rx_byte` into `rx_buf[rx_idx++]`.
   c. Re-arm interrupt: `HAL_UART_Receive_IT(&huart2, &rx_byte, 1);`.
4. In main loop `while (1)`:
   a. If `cmd_ready == 1`:
      - If `strcmp(rx_buf, "ON") == 0`: Turn ON LD2.
      - If `strcmp(rx_buf, "OFF") == 0`: Turn OFF LD2.
      - Reset `cmd_ready = 0` and `rx_idx = 0`.

### 7. Core Logic / Code Base
Interrupt-driven circular buffering with asynchronous command token dispatching.

#### Embedded C Firmware Implementation (`Core/Src/main.c`):
```c
#include "main.h"
#include <string.h>

UART_HandleTypeDef huart2;
uint8_t rx_byte;
char rx_buf[32];
uint8_t rx_idx = 0;
volatile uint8_t cmd_ready = 0;

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart->Instance == USART2) {
        if (rx_byte == '\r' || rx_byte == '\n') {
            rx_buf[rx_idx] = '\0';
            cmd_ready = 1;
            rx_idx = 0;
        } else if (rx_idx < 31) {
            rx_buf[rx_idx++] = rx_byte;
        }
        HAL_UART_Receive_IT(&huart2, &rx_byte, 1);
    }
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_USART2_UART_Init();
    HAL_UART_Receive_IT(&huart2, &rx_byte, 1);

    while (1) {
        if (cmd_ready) {
            cmd_ready = 0;
            if (strcmp(rx_buf, "ON") == 0) {
                HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
            } else if (strcmp(rx_buf, "OFF") == 0) {
                HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);
            }
        }
    }
}
```

### 8. Expected Output
Typing 'ON' into the terminal turns ON the green LED LD2; typing 'OFF' extinguishes it immediately without interrupting background tasks.

### 9. Observation
Zero CPU cycle wasted polling. Commands processed instantaneously upon Enter keystroke.

### 10. Inference
Interrupt-driven serial communication provides deterministic, responsive human-in-the-loop control for embedded systems.
