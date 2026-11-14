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
