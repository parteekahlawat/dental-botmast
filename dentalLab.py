from flask import Flask, jsonify, request
import requests
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any


from info.providerId import providerInfo
from info.availableSlots import get_slots
from info.providerId import startTime
from info.extractId import extractId

from appointmentDetailsConfirm import appointmentDetails
from fillDetail import fillDetails
from enums.enum import ProviderId
from enums.enum import UserType
from enums.enum import ReasonId
# Initialize Flask application
app = Flask(__name__)

uk_timezone = pytz.timezone('Europe/London')



@app.route('/')
def home() -> str:
    return "Welcome to the Flask Backend!"

@app.route('/provider-details', methods=["GET"])
def provider():
    
    local_time = datetime.datetime.now(uk_timezone)
    timeNow = int(local_time.timestamp() * 1000)
    
    reasonId = ReasonId.COMPOSITE_BONDING_CONSULTATION.value
    userType = UserType.NEW_PATIENT.value 
    
    providerId = providerInfo(timeNow, reasonId, userType, patientId="1a669786-3064-4047-a0a3-4df2732a57d9")
    return providerId["providers"]


@app.route('/data', methods = ["GET"])
def get_external_data() -> Dict[str, Any]:

    # arguments added
    page = request.args.get("page", default=1, type=int)
    providerName = request.args.get("providerName", default="", type=str)
    
    # Now time
    local_time = datetime.datetime.now(uk_timezone)
    timeNow = int(local_time.timestamp() * 1000)
    # print(timeNow)
    
    # extracted = extractId(timeNow)

    # patientId = extracted["Patient"]["Body"]["name"]
    patientId = "1a669786-3064-4047-a0a3-4df2732a57d9"

    reasonId = ReasonId.COMPOSITE_BONDING_CONSULTATION.value
    userType = UserType.NEW_PATIENT.value 

    providerId = providerInfo(timeNow, reasonId, userType, patientId)

    slotsAvailable = get_slots(timeNow, reasonId, userType, providerName, page, patientId)
    # return slotsAvailable
    selectedDate = "2025-03-31T13:50:00.000Z"
    
    appointmentUrl = extracted["Appointment"]["Link"]
    appointmentPayload = extracted["Appointment"]["Body"]
    eventScheduled = slotsAvailable["value"]
    appointmentDetails(appointmentUrl, appointmentPayload, selectedDate, eventScheduled)
    
    
    patientUrl = extracted["Patient"]["Link"]
    patientPayload = extracted["Patient"]["Body"]
    fillDetails(patientUrl, patientPayload, fname="", lname="", dob="", mobile="", email="" )
    

    # otp_details_value = {
    # "iso5218Sex": "MALE",
    # "callback": false,
    # "internalPatientId": "a4835efb-c22a-4da8-80fb-52f463da05dd",
    # "codeAlreadyVerified": false,
    # "emailChannel": false,
    # "smsChannel": false,
    # "acceptedTermsOfUse": true,
    # "acceptedMarketingConsent": false,
    # "acceptedTermsOfUseChangeDate": "2025-03-11T12:39:55.582Z",
    # "firstname": "Demo",
    # "lastname": "LastDemo",
    # "dateofbirth": 248054400000,
    # "emailaddress": "demo@demo.com",
    # "mobilenumber": "+447809246818",
    # "hasEnteredVerificationCode":true,
    # "verificationCode":{otp}
    # }
    
    
    
    
    return slotsAvailable


# Start the server if the script is run directly
if __name__ == '__main__':
    app.run(debug=True)
