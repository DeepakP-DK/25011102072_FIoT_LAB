#include "main.h"

TIM_HandleTypeDef htim2;

void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_TIM2_Init(void);

int main(void) {
    uint16_t duty = 0;
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_TIM2_Init();

    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);

    while (1) {
        for (duty = 0; duty < 1000; duty += 15) {
            __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, duty);
            HAL_Delay(15);
        }
        for (duty = 1000; duty > 0; duty -= 15) {
            __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, duty);
            HAL_Delay(15);
        }
    }
}
