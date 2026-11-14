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
