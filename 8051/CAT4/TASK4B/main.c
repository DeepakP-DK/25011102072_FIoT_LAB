#include <reg51.h>

unsigned char scan_key(void) {
    unsigned char row;
    for (row = 0; row < 4; ++row) {
        P2 = (unsigned char)~(1 << row);
        if ((P2 & 0xF0) != 0xF0) {
            if (!(P2 & 0x10)) return row * 4 + 1;
            if (!(P2 & 0x20)) return row * 4 + 2;
            if (!(P2 & 0x40)) return row * 4 + 3;
            if (!(P2 & 0x80)) return row * 4 + 4;
        }
    }
    return 0;
}

void delay_ms(unsigned int ms) {
    unsigned int outer, inner;
    for (outer = 0; outer < ms; ++outer)
        for (inner = 0; inner < 120; ++inner) { }
}

void main(void) {
    unsigned char key;
    P1 = 0xFF;
    while (1) {
        key = scan_key();
        if (key) {
            P1 = (unsigned char)~(1 << ((key - 1) & 0x07));
            delay_ms(20);
            while (scan_key()) { }
            delay_ms(20);
            P1 = 0xFF;
        }
    }
}
