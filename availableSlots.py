import requests
from flask import jsonify
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any


def get_slots(timeNow: int, timeStart: int, timeEnd: int, reasonId: str, userType: str, providerName: str, page: int) -> Dict[str, Any]:
    providerLink=""
    if providerName!="":
        providerLink = f"&providerId={providerName}"
    slot_list = []
    pageNo = 1
    while(page):
        url = f"https://uk.mydentalhub.online/v31/events?timestamp={timeNow}&startDay={timeStart}&endDay={timeEnd}&patientId=0fa43773-b8bd-4b1a-8c5a-2f0580f03673&payorType=Private&patientType={userType}&reasonId={reasonId}&practiceId=UKSHQ02&firstEventForProvider=false{providerLink}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # weekData = data[:7]
                # return jsonify(weekData)
                page_list = []
                for event in data:
                    name = ''
                    price = ''
                    deposit = ''
                    for i in event.get("resourceEvents", []):
                        name = i.get("resourceName")
                        price = i.get("salesInformation", {}).get("price", {}).get("amount")
                        deposit = i.get("salesInformation", {}).get("deposit", {}).get("amount")
                    page_list.append({
                        "Id": i.get('id'),
                        "Name": name,
                        "Start Time": i.get("startTime"),
                        "Duration": i.get("duration"),
                        "Price": price,
                        "Deposit Amount": deposit,
                    })
                slot_list.append({
                    "Page":pageNo,
                    "Slot List":page_list
                })
            else:
                slot_list.append({"error": "Failed to fetch data", "status_code": response.status_code, "Page":pageNo})
            
            timeStart = timeEnd
            end_of_day = datetime.datetime.fromtimestamp(timeEnd / 1000)  + datetime.timedelta(days=7)
            end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
            timeEnd = int(end_of_day_midnight.timestamp() * 1000)
            page = page-1
            pageNo = pageNo+1
        
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500
        
    return slot_list