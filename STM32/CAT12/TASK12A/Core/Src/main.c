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
