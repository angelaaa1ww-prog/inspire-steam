from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, sys
import utime
from picozero import Speaker
from time import sleep
from dht import DHT22 
import machine
import time
import urequests
import network
import ujson
import dht

pix_res_x = 128
pix_res_y = 64

speaker = Speaker(15)
dht = DHT22(Pin(14)) 
# ThingSpeak settings
THINGSPEAK_API_KEY = "09WFEQ00LOTOTYJ1"
THINGSPEAK_URL = "http://api.thingspeak.com/update"

# Wi-Fi settings
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# Function to read room temperature and humidity
def read_room_temperature_humidity():
    dht_sensor.measure()
    temperature = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    return temperature, humidity

# Function to send data to ThingSpeak
def send_data_to_thingspeak(temperature, humidity,light):
    data = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": temperature,
        "field2": humidity,
        "field2": light,
    }
    response = urequests.post(THINGSPEAK_URL, data=ujson.dumps(data), headers={"Content-Type": "application/json"})
    response.close()

# Initialize the Wi-Fi connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for the Wi-Fi connection to establish
while not wifi.isconnected():
    time.sleep(1)

print("Connected to Wi-Fi")

def sound_alarm():
    speaker.on()
    sleep(1)
    speaker.off()
    sleep(1)

def init_i2c(scl_pin, sda_pin):
    # Initialize I2C device
    i2c_dev = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    
    if not i2c_addr:
        print('No I2C Display Found')
        sys.exit()
    else:
        print("I2C Address      : {}".format(i2c_addr[0]))
        print("I2C Configuration: {}".format(i2c_dev))
    
    return i2c_dev

def display_logo(oled):
    # Display the Raspberry Pi logo on the OLED
    buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    
    oled.fill(0)
    oled.blit(fb, 96, 0)
    oled.show()

temp  = 0
hum   = 0
light = 30



def display_anima(oled):
    # Display a simple timer animation on the OLED
    start_time = utime.ticks_ms()

    while True:
        elapsed_time = (utime.ticks_diff(utime.ticks_ms(), start_time) // 1000) + 1
        dht.measure()
        temp = dht.temperature()
        hum = dht.humidity()
        
        send_data_to_thingspeak(temp, hum,light)
        print("Data sent to ThingSpeak")
        time.sleep(15)
        if(temp > 50 ):
            sound_alarm()
            
        oled.text("Temp : ", 5, 5)
        oled.text(str(temp), 60, 5)
        oled.text("Hum  :", 5, 15)
        oled.text(str(hum), 60, 15)
        oled.show()
        
        # Clear the specific line by drawing a filled black rectangle
        oled.fill_rect(5, 40, oled.width - 5, 8, 0)

        oled.text("Timer:", 5, 30)
        oled.text(str(elapsed_time) + " sec", 5, 40)
        oled.show()
        utime.sleep_ms(1000)


    

def main():
    i2c_dev = init_i2c(scl_pin=27, sda_pin=26)
    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)
    
    display_logo(oled)
 
    display_anima(oled)
   

if __name__ == '__main__':
    main()
