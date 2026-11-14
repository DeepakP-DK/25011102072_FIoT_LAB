#include <reg51.h>

unsigned char code half_step[8] = {
    0x08, 0x0C, 0x04, 0x06, 0x02, 0x03, 0x01, 0x09
};

sbit DIR_SW   = P3^2;
sbit SPEED_SW = P3^3;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    char step;
    unsigned int step_delay;

    DIR_SW = 1;
    SPEED_SW = 1;

    while (1) {
        step_delay = (SPEED_SW == 1) ? 5 : 15;

        if (DIR_SW == 1) {
            for (step = 0; step < 8; step++) {
                P2 = half_step[step];
                delay_ms(step_delay);
            }
        } else {
            for (step = 7; step >= 0; step--) {
                P2 = half_step[step];
                delay_ms(step_delay);
            }
        }
    }
}
