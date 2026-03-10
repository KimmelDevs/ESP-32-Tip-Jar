from machine import I2C, Pin
from i2c_lcd import I2cLcd
import time

i2c = I2C(0, sda=Pin(22), scl=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

lcd.backlight_on()
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Hello World!")
lcd.move_to(0, 1)
lcd.putstr("ESP32 Ready!")