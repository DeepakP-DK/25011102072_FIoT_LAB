#include <reg51.h>

/* Common Anode segment codes for numerals 0 - 9 (a=bit0 ... g=bit6) */
unsigned char code seg_code[10] = {
    0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8, 0x80, 0x90
};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned char digit = 0;
    while (1) {
        for (digit = 0; digit < 10; digit++) {
            P2 = seg_code[digit];
            delay_ms(1000);
        }
    }
}
