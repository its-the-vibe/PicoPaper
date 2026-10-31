from machine import Pin
from utime import sleep

sleep(0.01) # Wait for USB to connect
print("Hello, Pi Pico!")

led = Pin("LED", Pin.OUT)
while True:
  led.toggle()
  sleep(1)

