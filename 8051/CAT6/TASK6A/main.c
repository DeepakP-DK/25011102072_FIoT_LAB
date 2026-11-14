#include <reg51.h>

#define KEYPAD P1
#define DISPLAY P2

unsigned char code seg_code[16] = {
    0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8,
    0x80, 0x90, 0x88, 0x83, 0xC6, 0xA1, 0x86, 0x8E
};

unsigned char code key_map[4][4] = {
    {0x1, 0x2, 0x3, 0xA},
    {0x4, 0x5, 0x6, 0xB},
    {0x7, 0x8, 0x9, 0xC},
    {0xE, 0x0, 0xF, 0xD}
};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

unsigned char keypad_scan(void) {
    unsigned char r, c;
    for (r = 0; r < 4; r++) {
        KEYPAD = ~(1 << r) | 0xF0; /* Drive one row low, keep cols high */
        if ((KEYPAD & 0xF0) != 0xF0) {
            delay_ms(20); /* Debounce */
            for (c = 0; c < 4; c++) {
                if (!(KEYPAD & (0x10 << c))) {
                    while (!(KEYPAD & (0x10 << c))); /* Wait release */
                    return key_map[r][c];
                }
            }
        }
    }
    return 0xFF; /* No key pressed */
}

void main(void) {
    unsigned char key;
    DISPLAY = 0xFF;
    while (1) {
        key = keypad_scan();
        if (key != 0xFF) {
            DISPLAY = seg_code[key];
        }
    }
}
