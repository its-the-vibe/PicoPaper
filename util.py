import machine
import time


def current_time_str():
    rtc = machine.RTC()
    rtc_datetime = rtc.datetime()
    month_name = (
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    )[rtc_datetime[1] - 1]
    hour = rtc_datetime[4]
    hour_12 = hour % 12 or 12
    ampm = "AM" if hour < 12 else "PM"
    current_time = "%s %d, %04d %d:%02d %s UTC" % (
        month_name,
        rtc_datetime[2],
        rtc_datetime[0],
        hour_12,
        rtc_datetime[5],
        ampm,
    )
    return current_time

en_pin = machine.Pin(25, machine.Pin.OUT)

def read_battery_voltage():
    en_pin.high()
    time.sleep_ms(10)
    vsys_pin = machine.ADC(29)
    vsys_value = vsys_pin.read_u16()
    en_pin.low()

    lvoltage = vsys_value * (3.3 / 65535) * 3
    return lvoltage
