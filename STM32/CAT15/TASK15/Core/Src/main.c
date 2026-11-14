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
