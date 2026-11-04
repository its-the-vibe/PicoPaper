# copy to main.py
import lib.updater
from machine import Pin
import network
import time
from secrets import WIFI_SSID, WIFI_PASSWORD

wlan = network.WLAN(network.STA_IF)
led = Pin("LED", Pin.OUT)

wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

while not wlan.isconnected():
    led.toggle()
    time.sleep(1)

led.off()
print("Connected to WiFi")

lib.updater.check_for_updates("its-the-vibe/PicoPaper")

