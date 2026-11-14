#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int outer, inner;
    for (outer = 0; outer < ms; ++outer)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    unsigned char value = 0;
    P1 = 0xFF;
    while (1) {
        P1 = (unsigned char)~value;  /* active-low binary LED display */
        delay_ms(500);
        value = (value + 1) & 0x0F;
    }
}
