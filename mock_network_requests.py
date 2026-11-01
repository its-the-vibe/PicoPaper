

def set_ntp_time():
    print("Mock: set_ntp_time called")


def thought_for_the_day(log=print):
    print("Mock: thought_for_the_day called")
    return "This is a mock thought for the day"

mock_tube_status = [
    {
        "id": "jubilee",
        "name": "Jubilee",
        "lineStatuses": [
            {
                "statusSeverityDescription": "Good Service"
            }
        ]
    },
    {
        "id": "district",
        "name": "District",
        "lineStatuses": [
            {
                "statusSeverityDescription": "Severe Delays",
                "reason": "District Line: Severe delays due to train cancellations.  "
            }
        ]
    }
]

def tube_status(log=print):
    print("Mock: tube_status called")
    return mock_tube_status

mock_weather = {
    "current_condition": [
        {
            "FeelsLikeC": "9",
            "FeelsLikeF": "48",
            "cloudcover": "92",
            "humidity": "82",
            "observation_time": "10:44 PM",
            "precipInches": "0.0",
            "precipMM": "0.0",
            "pressure": "1032",
            "pressureInches": "30",
            "temp_C": "10",
            "temp_F": "51",
            "uvIndex": "0",
            "visibility": "10",
            "visibilityMiles": "6",
            "weatherCode": "122",
            "weatherDesc": [
                {
                    "value": "Overcast "
                }
            ],
            "weatherIconUrl": [
                {
                    "value": "https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png"
                }
            ],
            "winddir16Point": "E",
            "winddirDegree": "81",
            "windspeedKmph": "4",
            "windspeedMiles": "2"
        }
    ],
    "nearest_area": [
        {
            "areaName": [
                {
                    "value": "Strand"
                }
            ],
            "country": [
                {
                    "value": "United Kingdom"
                }
            ],
            "latitude": "51.508",
            "longitude": "-0.121",
            "population": "0",
            "region": [
                {
                    "value": "Westminster Greater London"
                }
            ],
            "weatherUrl": [
                {
                    "value": "https://www.worldweatheronline.com/v2/weather.aspx?q=51.508,-0.121"
                }
            ]
        }
    ],
    "request": [
        {
            "query": "Lat 51.51 and Lon -0.13",
            "type": "LatLon"
        }
    ],
    "weather": [
        {
            "astronomy": [
                {
                    "moon_illumination": "71",
                    "moon_phase": "Waning Gibbous",
                    "moonrise": "09:01 PM",
                    "moonset": "01:15 PM",
                    "sunrise": "06:52 AM",
                    "sunset": "04:35 PM"
                }
            ],
            "avgtempC": "11",
            "avgtempF": "52",
            "date": "2026-10-31",
            "maxtempC": "15",
            "maxtempF": "59",
            "mintempC": "8",
            "mintempF": "47",
            "sunHour": "10.0",
            "totalSnow_cm": "0.0",
            "uvIndex": "1"
        },
        {
            "astronomy": [
                {
                    "moon_illumination": "60",
                    "moon_phase": "Last Quarter",
                    "moonrise": "10:28 PM",
                    "moonset": "01:43 PM",
                    "sunrise": "06:54 AM",
                    "sunset": "04:33 PM"
                }
            ],
            "avgtempC": "10",
            "avgtempF": "51",
            "date": "2026-11-01",
            "maxtempC": "14",
            "maxtempF": "57",
            "mintempC": "7",
            "mintempF": "45",
            "sunHour": "9.0",
            "totalSnow_cm": "0.0",
            "uvIndex": "1"
        },
        {
            "astronomy": [
                {
                    "moon_illumination": "48",
                    "moon_phase": "Waning Crescent",
                    "moonrise": "11:53 PM",
                    "moonset": "02:03 PM",
                    "sunrise": "06:56 AM",
                    "sunset": "04:31 PM"
                }
            ],
            "avgtempC": "10",
            "avgtempF": "50",
            "date": "2026-11-02",
            "maxtempC": "13",
            "maxtempF": "55",
            "mintempC": "8",
            "mintempF": "46",
            "sunHour": "9.0",
            "totalSnow_cm": "0.0",
            "uvIndex": "1"
        }
    ]
}

def weather(log=print):
    log("Returning mock weather data.")
    return mock_weather
