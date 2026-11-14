#include <reg51.h>

sbit RUN_LED   = P1^0;
sbit ALARM_LED = P1^7;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void External0_ISR(void) interrupt 0 {
    /* Instantly serviced on falling edge at P3.2 */
    ALARM_LED = ~ALARM_LED; /* Toggle alarm status */
}

void main(void) {
    IT0 = 1; /* Configure INT0 as falling-edge triggered */
    EX0 = 1; /* Enable External Interrupt 0 */
    EA  = 1; /* Enable Global Interrupts */

    ALARM_LED = 1; /* Off (active-low) */
    while (1) {
        RUN_LED = ~RUN_LED; /* Background heartbeat */
        delay_ms(300);
    }
}
