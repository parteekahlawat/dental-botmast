import requests
from flask import jsonify
import datetime
import pytz

uk_timezone = pytz.timezone('Europe/London')

def takeOTP():
    url = "https://uk.mydentalhub.online/hcportal/v1/internal/log"
    headers = {
    "Content-Type": "application/json"
    }
    payload = {
    "dimension1": "uk.mydentalhub.online",
    "dimension2": "uk.mydentalhub.online_Kilmarnock Smile Studio|UKSHQ02_233",
    "dimension3": false,
    "hitType": "pageview",
    "page": "Booking_3/New%20Patient_7/Ready%20for%20Verification_41"
    }
    response = requests.post(url, headers=headers, data = json.dumps(payload))
    return