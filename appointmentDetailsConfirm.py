import requests
from flask import jsonify
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any

uk_timezone = pytz.timezone('Europe/London')

def appointmentDetails(url, payload, selectedDate, eventList):
    headers = {
    "Content-Type": "application/json"
    }
    value = json.loads(payload["value"])
    value["duration"] = eventList["duration"]
    value["reason"] = eventList["reasonExternalId"]
    value["appointmentType"] = eventList["windowType"]
    value["startTime"] = selectedDate
    value["insuranceType"] = "private"
    value["sources"]["scheduledEventsProposed"] = eventList
    
    payload["value"] = json.dumps(value)
    
    response = requests.put(url, headers=headers, json=payload)
    
    return response.json()