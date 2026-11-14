#include "main.h"
#include <stdio.h>
#include <string.h>

UART_HandleTypeDef huart2;

void ESP8266_SendCmd(char *cmd) {
    HAL_UART_Transmit(&huart2, (uint8_t*)cmd, strlen(cmd), 1000);
}

int main(void) {
    char payload[128];
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_USART2_UART_Init();

    ESP8266_SendCmd("AT+RST\r\n");
    HAL_Delay(2000);
    ESP8266_SendCmd("AT+CWMODE=1\r\n");
    HAL_Delay(1000);

    while (1) {
        sprintf(payload, "{\"temp\":%.1f,\"hum\":%.1f,\"press\":%.1f}", 24.9, 60.4, 1015.4);
        /* Publish telemetry payload */
        HAL_Delay(2000);
    }
}
