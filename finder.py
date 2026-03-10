from machine import I2C, Pin
import time

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
time.sleep(1)
devices = i2c.scan()

if devices:
    for d in devices:
        print("Found at:", hex(d))
else:
    print("Nothing found - check wiring!")