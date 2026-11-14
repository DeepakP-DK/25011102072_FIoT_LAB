#include "main.h"

void SystemClock_Config(void);
static void MX_GPIO_Init(void);

int main(void) {
    uint16_t leds[4] = {GPIO_PIN_0, GPIO_PIN_1, GPIO_PIN_2, GPIO_PIN_3};
    int i;
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();

    while (1) {
        for (i = 0; i < 4; i++) {
            HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_SET);
            HAL_Delay(150);
            HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_RESET);
        }
        for (i = 2; i > 0; i--) {
            HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_SET);
            HAL_Delay(150);
            HAL_GPIO_WritePin(GPIOA, leds[i], GPIO_PIN_RESET);
        }
    }
}
