#include "main.h"

TIM_HandleTypeDef htim2;

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_TIM2_Init();

    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_3);
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_4);

    while (1) {
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_3, 750);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_4, 750);
        HAL_Delay(2000);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_3, 400);
        __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_4, 800);
        HAL_Delay(2000);
    }
}
