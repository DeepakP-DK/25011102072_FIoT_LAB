#include <reg51.h>

unsigned char code seg_code[10] = {
    0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F
};

sbit DIR_SW = P3^3; /* 1 = UP, 0 = DOWN */

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned int count = 1234;
    unsigned char digits[4];
    unsigned char scan = 0, cycle = 0;

    DIR_SW = 1; /* Input */

    while (1) {
        digits[0] = count / 1000;
        digits[1] = (count / 100) % 10;
        digits[2] = (count / 10) % 10;
        digits[3] = count % 10;

        for (cycle = 0; cycle < 20; cycle++) {
            for (scan = 0; scan < 4; scan++) {
                P2 = ~(1 << scan);             /* Select active digit */
                P0 = seg_code[digits[scan]];   /* Output segment data */
                delay_ms(3);
                P2 = 0xFF;                     /* Blanking */
            }
        }

        if (DIR_SW == 1) {
            count = (count < 9999) ? count + 1 : 0;
        } else {
            count = (count > 0) ? count - 1 : 9999;
        }
    }
}
