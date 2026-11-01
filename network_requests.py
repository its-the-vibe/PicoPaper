import ubinascii
from secrets import BASIC_AUTH_PASSWORD, BASIC_AUTH_USERNAME, TUBE_STATUS_ENDPOINT, TUBE_STATUS_BEARER_TOKEN
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
        log(f"Fetched thought: {responseText}")
    except Exception as e:
        log(f"Failed to fetch thought: {e}")        
    finally:
        if 'response' in locals():
            response.close()

    return responseText

tube_status_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TUBE_STATUS_BEARER_TOKEN}"
}

def tube_status(log=print):
    try:
        response = urequests.get(TUBE_STATUS_ENDPOINT, headers=tube_status_headers) 
        jsonData = response.json()
        return jsonData
    except Exception as e:
        log(f"Failed to fetch tube status: {e}")
        return []
    finally:
        if 'response' in locals():
            response.close()

def weather(log=print):
    try:
        response = urequests.get("https://wttr.in/London?format=j2") 
        jsonData = response.json()
        return jsonData
    except Exception as e:
        log(f"Failed to fetch weather: {e}")
        return None
    finally:
        if 'response' in locals():
            response.close()
