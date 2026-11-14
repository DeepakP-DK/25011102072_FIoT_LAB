#include "main.h"

I2C_HandleTypeDef hi2c1;
uint8_t chip_id = 0;

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_I2C1_Init();

    /* Read BME280 CHIP_ID register 0xD0 */
    HAL_I2C_Mem_Read(&hi2c1, (0x76 << 1), 0xD0, I2C_MEMADD_SIZE_8BIT, &chip_id, 1, 100);

    while (1) {
        if (chip_id == 0x60) {
            /* Verified authentic BME280 */
        }
        HAL_Delay(1000);
    }
}
