#include "main.h"
#include <stdio.h>

I2C_HandleTypeDef hi2c1;
float temperature, pressure, humidity;

int8_t user_i2c_read(uint8_t reg_addr, uint8_t *reg_data, uint32_t len, void *intf_ptr) {
    uint8_t dev_addr = *(uint8_t*)intf_ptr;
    if (HAL_I2C_Mem_Read(&hi2c1, (dev_addr << 1), reg_addr, I2C_MEMADD_SIZE_8BIT, reg_data, len, 100) == HAL_OK)
        return 0;
    return -1;
}

int8_t user_i2c_write(uint8_t reg_addr, const uint8_t *reg_data, uint32_t len, void *intf_ptr) {
    uint8_t dev_addr = *(uint8_t*)intf_ptr;
    if (HAL_I2C_Mem_Write(&hi2c1, (dev_addr << 1), reg_addr, I2C_MEMADD_SIZE_8BIT, (uint8_t*)reg_data, len, 100) == HAL_OK)
        return 0;
    return -1;
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_I2C1_Init();

    while (1) {
        /* Simulated compensated read cycle */
        temperature = 24.9f;
        pressure = 1015.4f;
        humidity = 60.4f;
        HAL_Delay(1000);
    }
}
