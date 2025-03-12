import requests
from flask import jsonify
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any
from info.providerId import startTime

uk_timezone = pytz.timezone('Europe/London')

def get_slots(timeNow: int, reasonId: str, userType: str, providerName: str, page: int, patientId: str) -> Dict[str, Any]:

    startingTime = startTime(timeNow, reasonId, userType)
    startingTime = datetime.datetime.fromisoformat(startingTime).astimezone(uk_timezone)
    timeStart = int(startingTime.timestamp() * 1000)

    end_of_day = startingTime + datetime.timedelta(days=7)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd = int(end_of_day_midnight.timestamp() * 1000)
    
    providerLink=""
    if providerName!="":
        providerLink = f"&providerId={providerName}"
    slot_list = []
    pageNo = 1
    while(page):
        try:
            url = f"https://uk.mydentalhub.online/v31/events?timestamp={timeNow}&startDay={timeStart}&endDay={timeEnd}&patientId={patientId}&payorType=Private&patientType={userType}&reasonId={reasonId}&practiceId=UKSHQ02&firstEventForProvider=false{providerLink}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if len(data)==0:
                    timeStart = timeEnd
                    end_of_day = datetime.datetime.fromtimestamp(timeEnd / 1000)  + datetime.timedelta(days=7)
                    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
                    timeEnd = int(end_of_day_midnight.timestamp() * 1000)
                    continue
                if page==1:
                    page_list = []
                    for event in data:
                        name = ''
                        price = ''
                        deposit = ''
                        starting = event.get("startTime")
                        duration = event.get("duration")
                        starting = datetime.datetime.fromisoformat(starting)
                        date = starting.astimezone(uk_timezone).strftime("%d")
                        month = starting.astimezone(uk_timezone).strftime("%B")
                        year = starting.astimezone(uk_timezone).strftime("%Y")
                        time = starting.astimezone(uk_timezone).strftime("%I:%M %p")

                        uk_end_time = starting.astimezone(uk_timezone) + datetime.timedelta(minutes=duration)
                        end_time = uk_end_time.strftime("%I:%M %p")
                        for i in event.get("resourceEvents", []):
                            name = i.get("resourceName")
                            price = i.get("salesInformation", {}).get("price", {}).get("amount")
                            deposit = i.get("salesInformation", {}).get("deposit", {}).get("amount")
                        page_list.append({
                            "Id": event.get('id'),
                            "Name": name,
                            "Start Time": f"{date} {month} {year}, {time}",
                            "End Time": f"{date} {month} {year}, {end_time}",
                            "Duration": duration,
                            "Price": price,
                            "Deposit Amount": deposit,
                            "value":event
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