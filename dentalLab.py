from flask import Flask, jsonify, request
import requests
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any

# Initialize Flask application
app = Flask(__name__)

uk_timezone = pytz.timezone('Europe/London')

@app.route('/')
def home() -> str:
    return "Welcome to the Flask Backend!"


def providerInfo(timeNow: int, timeStart: int, timeEnd: int, reasonId: str) -> Dict[str, Any]:
    """
    Function to fetch provider information.
    """
    end_of_day = datetime.datetime.fromtimestamp(timeNow / 1000) + relativedelta(months=6)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd2 = int(end_of_day_midnight.timestamp() * 1000)
    
    url = f"https://uk.mydentalhub.online/v31/events?timestamp={timeNow}&startDay={timeStart}&endDay={timeEnd2}&eventType=Proposed&patientId=5339fe99-9b2a-4706-8932-6035c505ec61&payorType=Private&patientType=NewPatient&reasonId={reasonId}&practiceId=UKSHQ02&firstEventForProvider=true&isShapeChange=true"
    
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


@app.route('/data')
def get_external_data() -> Dict[str, Any]:
    """
    Fetch external data and return provider data.
    """
    local_time = datetime.datetime.now(uk_timezone)

    timeNow = int(local_time.timestamp() * 1000)

    start_of_day = local_time + datetime.timedelta(days=19)
    start_of_day_midnight = start_of_day.replace(hour=0, minute=0, second=0, microsecond=0)
    timeStart = timeNow

    end_of_day = local_time + datetime.timedelta(days=25)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd = int(end_of_day_midnight.timestamp() * 1000)

    reasonIdData = {
        "Composite Bonding Consultation": "0-28-418",
        "Cosmetic Consultation": "0-33-418",
        "Tooth whitening Consultation": "0-36-418",
        "Invisalign Consultation": "0-42-418",
        "Orthodontic Consultation": "0-44-418",
        "hygiene 30 mins": "0-46-418",
        "Cfast Consultation": "0-43-418",
        "Air Polish": "0-54-418",
        "Hygiene 40 mins": "0-47-418",
        "Treatment Co-Ordinator Implants": "0-48-418",
        "Treatment Co-Ordinator Invisalign": "0-49-418",
        "Treatment Co-Ordinator Whitening": "0-50-418",
        "Hygiene 20 mins": "0-53-418",
        "Private Exam": "0-55-418",
    }

    reasonId = reasonIdData["Composite Bonding Consultation"]
    providerId = providerInfo(timeNow, timeStart, timeEnd, reasonId)

    providerData = {
        "Ayeza Tariq": "AYEZA",
        "Calum McCall": "CALUM",
        "Dr Rebecca Smith": "REB",
        "Muqtadeer Syed": "MS",
        "Edward": "HYG",
        "Meenakshi Venkatesh": "MV",
        "Smile Coordinator": "TCO",
    }

    url = f"https://uk.mydentalhub.online/v31/events?timestamp={timeNow}&startDay={timeStart}&endDay={timeEnd}&patientId=0fa43773-b8bd-4b1a-8c5a-2f0580f03673&payorType=Private&patientType=NewPatient&reasonId=0-28-418&practiceId=UKSHQ02&firstEventForProvider=false"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data", "status_code": response.status_code}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


# Start the server if the script is run directly
if __name__ == '__main__':
    app.run(debug=True)
