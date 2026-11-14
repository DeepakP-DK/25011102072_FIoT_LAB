#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int outer, inner;
    for (outer = 0; outer < ms; ++outer)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    P1 = 0xFF;
    while (1) {
        P1 = 0xF0;       /* four active-low LEDs ON */
        delay_ms(250);
        P1 = 0xFF;       /* all four LEDs OFF */
        delay_ms(250);
    }
}
