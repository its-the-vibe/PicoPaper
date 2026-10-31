import ubinascii
from secrets import BASIC_AUTH_PASSWORD, BASIC_AUTH_USERNAME
import urequests

auth_string = f"{BASIC_AUTH_USERNAME}:{BASIC_AUTH_PASSWORD}"
# b2a_base64 adds a trailing newline character, so we use .strip() to remove it
auth_encoded = ubinascii.b2a_base64(auth_string.encode('ascii')).decode('ascii').strip()

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_encoded}"
}

def set_ntp_time():
    import ntptime
    ntptime.settime()

def thought_for_the_day(log=print):
    responseText = "no response"
    try:
        response = urequests.get('https://vibe-thoughts.vibechung.workers.dev/api/thought')
        jsonData = response.json()
        responseText = jsonData.get("response")
    except Exception as e:
        log(f"Failed to fetch thought: {e}")        
    finally:
        if 'response' in locals():
            response.close()

    return responseText
