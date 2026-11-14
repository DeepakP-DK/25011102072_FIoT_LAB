#include <reg51.h>

/* Full-step excitation sequence for 4-phase unipolar stepper */
unsigned char code full_step[4] = {0x09, 0x0C, 0x06, 0x03};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void main(void) {
    unsigned char step = 0;
    while (1) {
        for (step = 0; step < 4; step++) {
            P2 = full_step[step];
            delay_ms(15); /* Controls motor speed */
        }
    }
}
