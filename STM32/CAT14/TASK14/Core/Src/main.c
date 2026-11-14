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
