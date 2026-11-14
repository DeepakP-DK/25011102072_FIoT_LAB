#include <reg51.h>

sbit SW = P3^2;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned char count = 0;
    SW = 1;       /* Configure P3.2 as input */
    P1 = 0xFF;    /* Turn OFF all active-low LEDs */

    while (1) {
        if (SW == 0) {            /* Falling edge detected */
            delay_ms(20);         /* 20ms debounce delay */
            if (SW == 0) {        /* Confirmed valid press */
                count = (count + 1) & 0x0F;
                P1 = ~(count);    /* Display 4-bit count */
                while (SW == 0);  /* Wait for key release */
                delay_ms(20);     /* Release debounce */
            }
        }
    }
}
