from flask import Flask, jsonify, request
import requests
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any
from providerId import providerInfo
from availableSlots import get_slots

# Initialize Flask application
app = Flask(__name__)

uk_timezone = pytz.timezone('Europe/London')

@app.route('/')
def home() -> str:
    return "Welcome to the Flask Backend!"


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


    end_of_day = datetime.datetime.fromtimestamp(timeNow / 1000) + relativedelta(months=6)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd2 = int(end_of_day_midnight.timestamp() * 1000)
    

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
    # userType = "ExistingPatient"
    userType = "NewPatient"
    providerId = providerInfo(timeNow, timeStart, timeEnd, reasonId, userType)

    providerData = {
        "Ayeza Tariq": "AYEZA",
        "Calum McCall": "CALUM",
        "Dr Rebecca Smith": "REB",
        "Muqtadeer Syed": "MS",
        "Edward": "HYG",
        "Meenakshi Venkatesh": "MV",
        "Smile Coordinator": "TCO",
    }
    # providerName = providerData["Ayeza Tariq"]
    providerName = ""
    slotsAvailable = get_slots(timeNow, timeStart, timeEnd2, reasonId, userType, providerName)
    return slotsAvailable


# Start the server if the script is run directly
if __name__ == '__main__':
    app.run(debug=True)
