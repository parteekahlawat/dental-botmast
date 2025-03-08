import requests
from flask import jsonify
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any

def providerInfo(timeNow: int, timeStart: int, timeEnd: int, reasonId: str, userType: str) -> Dict[str, Any]:

    end_of_day = datetime.datetime.fromtimestamp(timeNow / 1000) + relativedelta(months=6)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd2 = int(end_of_day_midnight.timestamp() * 1000)
    
    url = f"https://uk.mydentalhub.online/v31/events?timestamp={timeNow}&startDay={timeStart}&endDay={timeEnd2}&eventType=Proposed&patientId=5339fe99-9b2a-4706-8932-6035c505ec61&payorType=Private&patientType={userType}&reasonId={reasonId}&practiceId=UKSHQ02&firstEventForProvider=true&isShapeChange=true"
    
    providers = []
    try:
        response = requests.get(url)
        print(response.json())
        if response.status_code == 200:
            data = response.json()  # Assuming the response is in JSON format

            for event in data:
                name = ''
                price = ''
                deposit = ''
                for i in event.get("resourceEvents", []):
                    name = i.get("resourceName")
                    price = i.get("salesInformation", {}).get("price", {}).get("amount")
                    deposit = i.get("salesInformation", {}).get("deposit", {}).get("amount")
                providers.append({
                    "Id": i.get('id'),
                    "Name": name,
                    "Start Time": i.get("startTime"),
                    "Duration": i.get("duration"),
                    "Price": price,
                    "Deposit Amount": deposit,
                })
            return jsonify(providers)
        else:
            return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
