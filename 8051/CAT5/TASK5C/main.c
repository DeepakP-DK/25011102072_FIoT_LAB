#include <reg51.h>

#define LCD_DATA P2

sbit RS = P3^5;
sbit RW = P3^6;
sbit EN = P3^7;

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 120; j++);
    }
}

void lcd_cmd(unsigned char cmd) {
    LCD_DATA = cmd;
    RS = 0;
    RW = 0;
    EN = 1;
    delay_ms(2);
    EN = 0;
}

void lcd_data(unsigned char ch) {
    LCD_DATA = ch;
    RS = 1;
    RW = 0;
    EN = 1;
    delay_ms(2);
    EN = 0;
}

void lcd_string(char *str) {
    while (*str) {
        lcd_data(*str++);
    }
}

void lcd_init(void) {
    delay_ms(20);
    lcd_cmd(0x38); /* 8-bit mode, 2-line, 5x7 font */
    lcd_cmd(0x0C); /* Display ON, Cursor OFF */
    lcd_cmd(0x06); /* Auto-increment cursor */
    lcd_cmd(0x01); /* Clear display */
    delay_ms(5);
}

void main(void) {
    lcd_init();
    lcd_cmd(0x80); /* Line 1 */
    lcd_string("SNU CHENNAI IoT");
    lcd_cmd(0xC0); /* Line 2 */
    lcd_string("REG: 25011102072");

    while (1);
}
