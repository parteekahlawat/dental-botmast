from flask import Flask, jsonify, request
import requests
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any
from enum import Enum
from providerId import providerInfo
from availableSlots import get_slots
from providerId import startTime
# Initialize Flask application
app = Flask(__name__)

uk_timezone = pytz.timezone('Europe/London')

class ReasonId(Enum):
    COMPOSITE_BONDING_CONSULTATION = "0-28-418"
    COSMETIC_CONSULTATION = "0-33-418"
    TOOTH_WHITENING_CONSULTATION = "0-36-418"
    INVISALIGN_CONSULTATION = "0-42-418"
    ORTHODONTIC_CONSULTATION = "0-44-418"
    HYGIENE_30_MINS = "0-46-418"
    CFAST_CONSULTATION = "0-43-418"
    AIR_POLISH = "0-54-418"
    HYGIENE_40_MINS = "0-47-418"
    TREATMENT_COORDINATOR_IMPLANTS = "0-48-418"
    TREATMENT_COORDINATOR_INVISALIGN = "0-49-418"
    TREATMENT_COORDINATOR_WHITENING = "0-50-418"
    HYGIENE_20_MINS = "0-53-418"
    PRIVATE_EXAM = "0-55-418"

class UserType(Enum):
    NEW_PATIENT = "NewPatient"
    EXISTING_PATIENT = "ExistingPatient"

class ProviderId(Enum):
    AYEZA_TARIQ = "AYEZA"
    CALUM_MCCALL = "CALUM"
    DR_REBECCA_SMITH = "REB"
    MUQTADEER_SYED = "MS"
    EDWARD = "HYG"
    MEENAKSHI_VENKATESH = "MV"
    SMILE_COORDINATOR = "TCO"

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
    
    start_of_day_midnight = local_time.replace(hour=0, minute=0, second=0, microsecond=0)
    timeStart = int(start_of_day_midnight.timestamp() * 1000)


    end_of_day = datetime.datetime.fromtimestamp(timeNow / 1000) + relativedelta(months=6)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd2 = int(end_of_day_midnight.timestamp() * 1000)
    
    
    reasonId = ReasonId.COMPOSITE_BONDING_CONSULTATION.value
    userType = UserType.NEW_PATIENT.value 

    providerId = providerInfo(timeNow, timeStart, timeEnd2, reasonId, userType)

    providerName = ""
    
    page = 4
    
    startingTime = startTime(timeNow, timeStart, timeEnd2, reasonId, userType)
    
    startingTime = datetime.datetime.fromisoformat(startingTime)

    end_of_day = startingTime + datetime.timedelta(days=7)
    end_of_day_midnight = end_of_day.replace(hour=23, minute=59, second=59, microsecond=999999)
    timeEnd = int(end_of_day_midnight.timestamp() * 1000)

    slotsAvailable = get_slots(timeNow, int(startingTime.timestamp() * 1000), timeEnd, reasonId, userType, providerName, page)
    return slotsAvailable


# Start the server if the script is run directly
if __name__ == '__main__':
    app.run(debug=True)
