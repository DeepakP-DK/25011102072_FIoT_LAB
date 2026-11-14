#include <reg51.h>

void delay_ms(unsigned int ms) {
    unsigned int tick, inner;
    for (tick = 0; tick < ms; ++tick)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    P1 = 0xFF;
    while (1) {
        P1 = 0x00;       /* active-low LED bank: illuminated */
        delay_ms(250);
        P1 = 0xFF;       /* LED bank: extinguished */
        delay_ms(250);
    }
}
