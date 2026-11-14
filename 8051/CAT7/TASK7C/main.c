#include <reg51.h>

sbit IN1 = P2^0;
sbit IN2 = P2^1;
sbit EN1 = P2^2;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned int cycle, t;
    /* Forward rotation setup */
    IN1 = 1;
    IN2 = 0;

    while (1) {
        /* Run at 50% duty cycle */
        for (cycle = 0; cycle < 200; cycle++) {
            EN1 = 1;
            for (t = 0; t < 50; t++);
            EN1 = 0;
            for (t = 0; t < 50; t++);
        }
        /* Run at 80% duty cycle */
        for (cycle = 0; cycle < 200; cycle++) {
            EN1 = 1;
            for (t = 0; t < 80; t++);
            EN1 = 0;
            for (t = 0; t < 20; t++);
        }
    }
}
