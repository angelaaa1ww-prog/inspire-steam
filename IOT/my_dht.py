# Name : Angela Amani
# Date : 4/03/2026
# Program to the working of a DHT22 sensor

from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import framebuf
import utime
from my_dht import DHTSensor  # GP22 sensor

# OLED resolution
pix_res_x = 128
pix_res_y = 64

# ----- DHT22 Setup -----
sensor = DHTSensor(22)  # GP22

# ----- Potentiometer Setup -----
pot = ADC(Pin(28))  # Use the correct pin your potentiometer is connected to
# Note: ADC values range from 0–65535

# ----- OLED Setup -----
i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
devices = i2c_dev.scan()
if not devices:
    print("No I2C display found")
    raise Exception("OLED not detected")
print("OLED I2C address:", hex(devices[0]))

oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)

# ----- Logo buffer -----
logo_buffer = bytearray(
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80"
    b"\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00"
    b"\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@"
    b"\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00"
    b"\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00"
)
fb = framebuf.FrameBuffer(logo_buffer, 32, 32, framebuf.MONO_HLSB)

# Display logo once at startup
oled.fill(0)
oled.blit(fb, 96, 0)
oled.show()
utime.sleep(2)

# Start timer
start_time = utime.ticks_ms()

# ----- Main Loop -----
while True:
    # --- DHT22 Reading ---
    temp, hum = sensor.read()

    if temp is not None:
        print("Temperature:", temp, "C")
        print("Humidity:", hum, "%")
    else:
        print("Sensor Error")

    # --- Potentiometer Reading ---
    pot_value = pot.read_u16()  # 0–65535
    print("Potentiometer value:", pot_value)

    # --- Display on OLED ---
    oled.fill(0)

    # DHT22
    if temp is not None:
        oled.text("Temp: {}C".format(temp), 0, 0)
        oled.text("Hum : {}%".format(hum), 0, 10)
    else:
        oled.text("Sensor Error", 0, 0)

    # Potentiometer
    oled.text("Pot: {}".format(pot_value), 0, 25)

    # Timer
    elapsed = utime.ticks_diff(utime.ticks_ms(), start_time) // 1000
    oled.text("Timer: {}s".format(elapsed), 0, 50)

    oled.show()
    utime.sleep(2)