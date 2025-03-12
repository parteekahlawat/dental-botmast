import requests
from flask import jsonify
import datetime
import pytz

uk_timezone = pytz.timezone('Europe/London')

def timeSelected(date):
    url = "https://uk.mydentalhub.online/hcportal/v1/internal/log"
    headers = {
    "Content-Type": "application/json"
    }
    payload = {
        "action":"select",
        "category":"timeSelection",
        "hitType":"event",
        "label":{date},
        "value":0
    }
    response = requests.post(url, headers=headers, data = json.dumps(payload))
    return