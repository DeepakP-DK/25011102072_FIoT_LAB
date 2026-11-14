#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++) {
            /* ~1ms calibrated delay loop at 11.0592 MHz */
        }
    }
}

void main(void) {
    P1 = 0xFF; /* Initialize Port 1 as output */
    while (1) {
        P1 = 0x55; /* Pattern 1: 01010101b */
        delay_ms(500);
        P1 = 0xAA; /* Pattern 2: 10101010b */
        delay_ms(500);
    }
}
