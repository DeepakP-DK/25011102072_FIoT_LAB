#include <reg51.h>

sbit TEST_OUT = P1^0;

void delay_ms(unsigned int ms) {
    unsigned int ms_count, cycles;
    for (ms_count = 0; ms_count < ms; ++ms_count)
        for (cycles = 0; cycles < 120; ++cycles) { }
}

void main(void) {
    TEST_OUT = 0;
    while (1) {
        TEST_OUT = !TEST_OUT;
        delay_ms(100);
    }
}
