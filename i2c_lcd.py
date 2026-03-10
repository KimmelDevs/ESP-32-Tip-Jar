import utime
from lcd_api import LcdApi
from machine import I2C

MASK_RS = 0x01
MASK_RW = 0x02
MASK_E  = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4

class I2cLcd(LcdApi):

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = True          # ← fix is here
        self.i2c.writeto(self.i2c_addr, bytearray([0]))
        utime.sleep_ms(20)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(5)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        utime.sleep_ms(1)
        self.hal_write_command(self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES)
        super().__init__(num_lines, num_columns)

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.i2c.writeto(self.i2c_addr, bytearray([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([byte]))

    def hal_backlight_on(self):
        self.backlight = True
        self.i2c.writeto(self.i2c_addr, bytearray([1 << SHIFT_BACKLIGHT]))

    def hal_backlight_off(self):
        self.backlight = False
        self.i2c.writeto(self.i2c_addr, bytearray([0]))

    def hal_write_command(self, cmd):
        byte = ((self.backlight) << SHIFT_BACKLIGHT)
        upper_nibble = byte | (((cmd >> 4) & 0x0f) << SHIFT_DATA)
        lower_nibble = byte | ((cmd & 0x0f) << SHIFT_DATA)
        self.i2c.writeto(self.i2c_addr, bytearray([upper_nibble | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([upper_nibble]))
        self.i2c.writeto(self.i2c_addr, bytearray([lower_nibble | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([lower_nibble]))
        if cmd <= 3:
            utime.sleep_ms(5)

    def hal_write_data(self, data):
        byte = (MASK_RS | ((self.backlight) << SHIFT_BACKLIGHT))
        upper_nibble = byte | (((data >> 4) & 0x0f) << SHIFT_DATA)
        lower_nibble = byte | ((data & 0x0f) << SHIFT_DATA)
        self.i2c.writeto(self.i2c_addr, bytearray([upper_nibble | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([upper_nibble]))
        self.i2c.writeto(self.i2c_addr, bytearray([lower_nibble | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytearray([lower_nibble]))