import network
from machine import Pin
from secrets import WIFI_SSID, WIFI_PASSWORD
import time

class Wifi:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.led = Pin("LED", Pin.OUT)

    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        while not self.wlan.isconnected():
            self.led.toggle()
            time.sleep(1)
        
        self.led.off()
        return self.wlan.ifconfig()[0]

    def is_connected(self):
        return self.wlan.isconnected()

    def disconnect(self):
        self.wlan.disconnect()
        self.wlan.active(False)
