import requests
from flask import jsonify
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any

list_provider = {
    "AYEZA": "AYEZA TARIQ",
    "CALUM": "CALUM MCCALL",
    "REB": "DR REBECCA SMITH",
    "MS": "MUQTADEER SYED",
    "HYG": "EDWARD",
    "MV": "MEENAKSHI VENKATESH",
    "TCO": "SMILE COORDINATOR"
}

def providerInfo(timeNow: int, reasonId: str, userType: str, patientId: str) -> Dict[str, Any]:
    
    end_of_day = datetime.fromtimestamp(timeNow / 1000) + relativedelta(months=6)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd = int(end_of_day_midnight.timestamp() * 1000)
    
    start_of_day_midnight = datetime.fromtimestamp(timeNow / 1000).replace(hour=0, minute=0, second=0, microsecond=0)
    timeStart = int(start_of_day_midnight.timestamp() * 1000)
    
    url = f"https://uk.mydentalhub.online/v31/events?timestamp={timeNow}&startDay={timeStart}&endDay={timeEnd}&eventType=Proposed&patientId={patientId}&payorType=Private&patientType={userType}&reasonId={reasonId}&practiceId=UKSHQ02&firstEventForProvider=true&isShapeChange=true"
    
    providers = []

    try:
        response = requests.get(url)
        # print(response.json())
        if response.status_code == 200:
            data = response.json() 

            for event in data:
                name = ''
                price = ''
                deposit = ''
                for i in event.get("resourceEvents", []):
                    name = i.get("resourceName")
                    price = i.get("salesInformation", {}).get("price", {}).get("amount")
                    deposit = i.get("salesInformation", {}).get("deposit", {}).get("amount")
                providers.append({
                    "Id": event.get('id'),
                    "Name": list_provider[name],
                    "Start Time": event.get("startTime"),
                    "Duration": event.get("duration"),
                    "Price": price,
                    "Deposit Amount": deposit,
                })
                    # Sort providers by startTime
            providers.sort(key=lambda x: datetime.fromisoformat(x["Start Time"].replace("Z", "+00:00")))

            # Get the earliest start time
            first_start_time = providers[0]["Start Time"] if providers else None

            print("First Start Time:", first_start_time)
            return jsonify(providers)
        else:
            return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

def startTime(timeNow: int, reasonId: str, userType: str) -> str:
    
    end_of_day = datetime.fromtimestamp(timeNow / 1000) + relativedelta(months=6)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd = int(end_of_day_midnight.timestamp() * 1000)
    
    start_of_day_midnight = datetime.fromtimestamp(timeNow / 1000).replace(hour=0, minute=0, second=0, microsecond=0)
    timeStart = int(start_of_day_midnight.timestamp() * 1000)
    
    url = f"https://uk.mydentalhub.online/v31/events?timestamp={timeNow}&startDay={timeStart}&endDay={timeEnd}&eventType=Proposed&patientId=5339fe99-9b2a-4706-8932-6035c505ec61&payorType=Private&patientType={userType}&reasonId={reasonId}&practiceId=UKSHQ02&firstEventForProvider=true&isShapeChange=true"
    
    providers = []
    try:
        response = requests.get(url)
        # print(response.json())
        if response.status_code == 200:
            data = response.json() 

            for event in data:
                name = ''
                price = ''
                deposit = ''
                providers.append({
                    "Start Time": event.get("startTime"),
                })
            providers.sort(key=lambda x: datetime.fromisoformat(x["Start Time"].replace("Z", "+00:00")))

            first_start_time = providers[0]["Start Time"] if providers else None

            print("First Start Time:", first_start_time)
            return first_start_time
        else:
            return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), 500
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500