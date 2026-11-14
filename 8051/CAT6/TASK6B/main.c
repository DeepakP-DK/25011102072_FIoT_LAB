#include <reg51.h>

sbit RELAY_LOCK = P3^3;
sbit BUZZER     = P3^4;

unsigned char code master_pin[4] = {1, 2, 3, 4};
unsigned char input_pin[4];

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

/* Simplified keypad scanner stub */
unsigned char get_key(void) {
    /* Returns simulated digit for testing / Keil verification */
    return 1;
}

void main(void) {
    unsigned char i, matched;
    RELAY_LOCK = 1; /* Inactive (active low) */
    BUZZER = 1;

    while (1) {
        matched = 1;
        for (i = 0; i < 4; i++) {
            input_pin[i] = master_pin[i]; /* Capture valid simulated entry */
        }

        for (i = 0; i < 4; i++) {
            if (input_pin[i] != master_pin[i]) matched = 0;
        }

        if (matched) {
            RELAY_LOCK = 0; /* Unlock door */
            delay_ms(3000);
            RELAY_LOCK = 1; /* Re-lock */
        } else {
            BUZZER = 0; delay_ms(500); BUZZER = 1;
        }
        delay_ms(1000);
    }
}
