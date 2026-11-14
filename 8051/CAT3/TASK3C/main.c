#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int outer, inner;
    for (outer = 0; outer < ms; ++outer)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    while (1) {
        P1 = 0xF5;       /* P1.1 and P1.3 active-low: 1010 pattern */
        delay_ms(300);
        P1 = 0xFA;       /* P1.0 and P1.2 active-low: 0101 pattern */
        delay_ms(300);
    }
}
