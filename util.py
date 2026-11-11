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


def fuzzy_time_str(hour, minute):
    hour_12 = hour % 12 or 12
    next_hour_12 = (hour + 1) % 12 or 12
    period = "am" if hour < 12 else "pm"
    next_period = "am" if (hour + 1) % 24 < 12 else "pm"

    if minute < 5:
        return "%dish" % hour_12
    if minute < 15:
        return "just after %d%s" % (hour_12, period)
    if minute < 20:
        return "quarter past %d%s" % (hour_12, period)
    if minute < 30:
        return "%dish" % hour_12
    if minute < 35:
        return "Half %d" % hour_12
    if minute < 45:
        return "just after half past %d" % hour_12
    if minute < 50:
        return "quarter to %d%s" % (next_hour_12, next_period)
    return "%dish" % next_hour_12


en_pin = machine.Pin(25, machine.Pin.OUT)

def read_battery_voltage():
    en_pin.high()
    time.sleep_ms(10)
    vsys_pin = machine.ADC(29)
    vsys_value = vsys_pin.read_u16()
    en_pin.low()

    lvoltage = vsys_value * (3.3 / 65535) * 3
    return lvoltage
