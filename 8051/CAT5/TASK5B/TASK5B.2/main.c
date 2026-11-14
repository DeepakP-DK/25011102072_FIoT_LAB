#include <reg51.h>

/* Common Cathode segment codes for numerals 0-9 */
unsigned char code seg_code[10] = {
    0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F
};

sbit DIGIT1_EN = P1^0; /* Tens digit driver */
sbit DIGIT2_EN = P1^1; /* Units digit driver */

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void display_number(unsigned char num) {
    unsigned char tens = num / 10;
    unsigned char units = num % 10;
    unsigned int k;

    for (k = 0; k < 50; k++) { /* Refresh display for ~500ms */
        /* Display Tens Digit */
        DIGIT1_EN = 1; DIGIT2_EN = 0;
        P2 = seg_code[tens];
        delay_ms(5);
        DIGIT1_EN = 0; DIGIT2_EN = 0; /* Blanking */

        /* Display Units Digit */
        DIGIT1_EN = 0; DIGIT2_EN = 1;
        P2 = seg_code[units];
        delay_ms(5);
        DIGIT1_EN = 0; DIGIT2_EN = 0; /* Blanking */
    }
}

void main(void) {
    unsigned char count = 0;
    while (1) {
        display_number(count);
        count = (count + 1) % 100;
    }
}
