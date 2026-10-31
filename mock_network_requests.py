

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