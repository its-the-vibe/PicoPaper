import machine
import framebuf
import random
import urequests
import network_requests
import wifi
from secrets import LOGGING_ENDPOINT
from my_config import TOUCH_ENABLED
import util
import lib.updater
import gc
import waveshare
import sys

wifi = wifi.Wifi()
wlanIp = wifi.connect()

rtc = machine.RTC()

def log(message):
    print(message)
    if wifi.is_connected() and LOGGING_ENDPOINT:
        rtc_datetime = rtc.datetime()
        payload = {
            'severity': 'debug',
            'message': message,
            'service': 'PicoPaper',
            'timestamp': '%04d-%02d-%02dT%02d:%02d:%02d.000Z' % (
                rtc_datetime[0],
                rtc_datetime[1],
                rtc_datetime[2],
                rtc_datetime[4],
                rtc_datetime[5],
                rtc_datetime[6],
            ),
        }
        gc.collect()
        try:
            lresp = urequests.post(LOGGING_ENDPOINT, json=payload, headers=network_requests.headers)
            lresp.close()
        except Exception as e:
            print('Failed to send log:', e)


log(f'Connected! IP address: {wlanIp}')

network_requests.set_ntp_time()

log("Checking for updates...")
lib.updater.check_for_updates("its-the-vibe/PicoPaper", log=log)
log("Update check complete.")

current_time = util.current_time_str()
log(f'Current UTC DateTime: {current_time}')

voltage = util.read_battery_voltage()
log(f"Battery Voltage: {voltage:.2f} V")

epd = waveshare.EPD_2in9()
epd.init()

def get_key():
    if(epd.config.digital_read(epd.config.key0) == 0):
        return 1
    elif(epd.config.digital_read(epd.config.key1) == 0):
        return 2
    elif(epd.config.digital_read(epd.config.key2) == 0):
        return 3
    else:
        return 0 

'''
    Because the touch display requires a relatively fast refresh speed, the default 
    needs to use partial refresh, and four gray levels cannot be used in this mode. 
    Here, only four gray level picture refresh demonstration is used
'''
def show_4gray_demo():
    epd.init_4Gray()
    epd.image4Gray.fill_rect(0, 0, 127, 74, epd.black)  
    epd.image4Gray.text('Grey1',10, 33, epd.white)
    epd.image4Gray.fill_rect(0, 74, 127, 74, epd.darkgray)
    epd.image4Gray.text('Grey2',10, 107, epd.grayish)
    epd.image4Gray.fill_rect(0, 148, 127, 74, epd.grayish)
    epd.image4Gray.text('Grey3',10, 181, epd.darkgray)
    epd.image4Gray.fill_rect(0, 222, 127, 74, epd.white)
    epd.image4Gray.text('Grey4',10, 255, epd.black)
    epd.display_4Gray(epd.buffer_4Gray)
    epd.delay_ms(500)

def reset_base():
    epd.image1Gray_Portrait.fill(0xff)
    epd.display_Base(epd.buffer)

landscape_width = waveshare.EPD_HEIGHT
landscape_height = waveshare.EPD_WIDTH
landscape_buffer = bytearray(landscape_width * landscape_height // 8)
landscape = framebuf.FrameBuffer(
    landscape_buffer,
    landscape_width,
    landscape_height,
    framebuf.MONO_HLSB,
)

def write_landscape():
    epd.image1Gray_Portrait.fill(0xff)
    for x in range(landscape_width):
        for y in range(landscape_height):
            pixel = landscape.pixel(x, y)
            epd.image1Gray_Portrait.pixel(y, landscape_width - 1 - x, pixel)

# The landscape buffer is limited to 6 lines of 36 characters
# This will automatically split long lines into multiple lines of 36 characters each
# respecting whole words
def write_landscape_text(text):
    landscape.fill(0xff)  # white background
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= 36:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines[:6]):  # limit to 6 lines
        landscape.text(line, 8, 12 + i * 18, 0x00)  # limit to 36 characters per line
    write_landscape()

def display_debug_text():
    landscape.fill(0xff)  # white background
    landscape.text("First line012345678901234567890", 8, 12, 0x00)
    landscape.text("Second lineABCDEFGHIJKLMNOPQRSTUVXYZabcdefghijklmnopqrstuvwxyz", 8, 30, 0x00)
    landscape.text(wlanIp, 8, 48, 0x00)
    # landscape.text(responseText, 8, 66, 0x00)
    landscape.text(current_time, 8, 84, 0x00)
    landscape.text(f"Battery Voltage: {voltage:.2f} V", 8, 102, 0x00)

    write_landscape()

    epd.display(epd.buffer)

class Menu:
    def __init__(self):
        self.options = [
            "Morning Dash",
            "Fuzzy Clock",
            "Demo",
            "Exit",
        ]
        self.current_option = 0

    def show(self):
        self.display_base()
        epd.display_Base(epd.buffer)
        self.update()

    def display_base(self):
        epd.image1Gray_Portrait.fill(0xff)
        # show a box
        epd.image1Gray_Portrait.rect(5, 5, 117, 100, 0x00)
        epd.image1Gray_Portrait.text('Menu', 10, 10, 0x00)
        for i, option in enumerate(self.options):
            epd.image1Gray_Portrait.text(f'  {option}', 10, 30 + i * 20, 0x00)

    def update(self):
        self.display_base()
        epd.image1Gray_Portrait.text("* ", 10, 30 + self.current_option * 20, 0x00)
        epd.display_Partial(epd.buffer)

    def select_next(self):
        self.current_option = (self.current_option + 1) % len(self.options)
        self.update()

    def run(self):
        log("Running menu...")
        self.show()
        while True:
            key = get_key()
            if key == 1:
                self.select_next()
            if key == 2:
                log(f"Selecting current option... {self.current_option}")
                self.handle_selection()

    def handle_selection(self):
        if self.current_option == len(self.options) - 1:  # Exit option
            log("Exiting menu...")
            sys.exit(0)
        if self.current_option == 0:  # Morning Dash
            morning_dash = MorningDash()
            morning_dash.run()
        if self.current_option == 1:  # Fuzzy Clock
            fuzzy_clock = FuzzyClock()
            fuzzy_clock.run()
        if self.current_option == 2:  # Demo option
            demo = Demo()
            demo.run()

        self.show()

# show_4gray_demo()

# def pthread_irq():
#     if(epd.config.digital_read(epd.config.int_pin) == 0):
#         icnt_dev.Touch = 1
#     else:
#         icnt_dev.Touch = 0

def light_sleep():
    log("entering lightsleep")
    log("Turning off Wi-Fi...")
    wifi.disconnect(flash=True)

    epd.sleep()

    machine.lightsleep()


class FuzzyClock:
    def run(self):
        log("Starting fuzzy clock...")
        self.display()

        while True:
            if get_key() == 3:
                return

            wifi.disconnect()
            epd.sleep()
            remaining_seconds = random.randint(10, 20) * 60
            while remaining_seconds > 0:
                machine.lightsleep(min(1000, remaining_seconds * 1000))
                remaining_seconds -= 1
                if get_key() == 3:
                    epd.init()
                    wifi.connect()
                    return

            epd.init()
            self.display()

    def display(self):
        rtc_datetime = rtc.datetime()
        weekdays = (
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday",
        )
        months = (
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        )
        fuzzy_time = util.fuzzy_time_str(rtc_datetime[4], rtc_datetime[5])
        date = "%s, %s %d, %d" % (
            weekdays[rtc_datetime[3]],
            months[rtc_datetime[1] - 1],
            rtc_datetime[2],
            rtc_datetime[0],
        )
        write_landscape_text("%s\n%s" % (fuzzy_time, date))
        epd.display(epd.buffer)


class MorningDash:
    def __init__(self):        
        self.thoughtText = network_requests.thought_for_the_day(log=log)
        self.weather = network_requests.weather(log=log)

        reset_base()

        self.displayFuncs = [
            self.display_thought,
            self.retrieve_and_display_tube_status,
            self.display_weather,
        ]
        self.current_display = 0

    def run(self):
        log("Starting morning dash...")
        self.display_thought()

        while (1):
            key = get_key()

            if key == 1:
                log("Switching display...")
                self.current_display = (self.current_display + 1) % len(self.displayFuncs)
                self.displayFuncs[self.current_display]()

            if rtc.datetime()[4] == 9 or key == 2:
                light_sleep()

            if key == 3:
                log("Exiting morning dash...")
                return

    def display_thought(self):
        write_landscape_text(self.thoughtText)
        epd.display_Partial(epd.buffer)

    def retrieve_and_display_tube_status(self):
        tube_status = network_requests.tube_status(log=log)

        landscape.fill(0xff)  # white background
        landscape.text(util.current_time_str(), 8, 12, 0x00)
        # iterate over all tube lines and display their status
        for line in tube_status:
            landscape.text(f"{line['name']}: {line['lineStatuses'][0]['statusSeverityDescription']}", 8, 30 + tube_status.index(line) * 18, 0x00)

        write_landscape()
        epd.display_Partial(epd.buffer)

    def display_weather(self):
        if self.weather:
            weather_desc = self.weather['current_condition'][0]['weatherDesc'][0]['value']
            temp_C = self.weather['current_condition'][0]['temp_C']
            max_temp_C = self.weather['weather'][0]['maxtempC']
            min_temp_C = self.weather['weather'][0]['mintempC']
            sunrise = self.weather['weather'][0]['astronomy'][0]['sunrise']
            sunset = self.weather['weather'][0]['astronomy'][0]['sunset']

            landscape.fill(0xff)  # white background
            landscape.text(f"Weather: {weather_desc}", 8, 12, 0x00)
            landscape.text(f"Current: {temp_C} C", 8, 30, 0x00)
            landscape.text(f"Min: {min_temp_C} C  Max: {max_temp_C} C", 8, 48, 0x00)
            landscape.text(f"Sunrise: {sunrise}", 8, 66, 0x00)
            landscape.text(f"Sunset: {sunset}", 8, 84, 0x00)
            write_landscape()
            epd.display_Partial(epd.buffer)

class Demo:
    def run(self):
        log("Running demo...")        
        show_4gray_demo()        
        epd.delay_ms(10000)
        display_debug_text()
        epd.delay_ms(10000)
        return


menu = Menu()
menu.run()
