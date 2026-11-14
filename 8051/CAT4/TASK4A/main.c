#include <reg51.h>

sbit WAVE_OUT = P1^5;

void main(void) {
    TMOD = 0x01; /* Timer 0, Mode 1 (16-bit timer) */
    WAVE_OUT = 0;

    while (1) {
        TH0 = 0xFE;  /* Reload value for 500us delay */
        TL0 = 0x33;
        TR0 = 1;     /* Start Timer 0 */
        while (TF0 == 0); /* Wait for overflow */
        TR0 = 0;     /* Stop Timer 0 */
        TF0 = 0;     /* Clear overflow flag */
        WAVE_OUT = ~WAVE_OUT; /* Toggle output pin */
    }
}
