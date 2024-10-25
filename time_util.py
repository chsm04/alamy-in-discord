import requests
from datetime import datetime

def get_internet_time():
    response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")
    response_json = response.json()
    internet_time = datetime.fromisoformat(response_json["utc_datetime"])
    return internet_time

# 사용 예시
internet_timestamp = get_internet_time().isoformat()
print("인터넷 타임스탬프:", internet_timestamp)