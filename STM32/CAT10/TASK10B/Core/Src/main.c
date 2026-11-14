#include "main.h"

TIM_HandleTypeDef htim2;

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_TIM2_Init();

    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_2);

    while (1) {
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 1000); /* 0 deg */
        HAL_Delay(1000);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 1500); /* 90 deg */
        HAL_Delay(1000);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_2, 2000); /* 180 deg */
        HAL_Delay(1000);
    }
}
