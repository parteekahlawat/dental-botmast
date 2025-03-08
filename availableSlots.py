import requests
from flask import jsonify
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any


def get_slots(timeNow: int, timeStart: int, timeEnd: int, reasonId: str, userType: str, providerName) -> Dict[str, Any]:
    providerLink=""
    if providerName!="":
        providerLink = f"&providerId={providerName}"
    url = f"https://uk.mydentalhub.online/v31/events?timestamp={timeNow}&startDay={timeStart}&endDay={timeEnd}&patientId=0fa43773-b8bd-4b1a-8c5a-2f0580f03673&payorType=Private&patientType={userType}&reasonId={reasonId}&practiceId=UKSHQ02&firstEventForProvider=false{providerLink}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weekData = data[:7]
            return jsonify(weekData)
        else:
            return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500