import requests
from flask import jsonify
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any

uk_timezone = pytz.timezone('Europe/London')

def fillDetails(url, payload, fname, lname, dob, mobile, email ):
    headers = {
    "Content-Type": "application/json"
    }
    value = json.loads(payload["value"])
    value["acceptedTermsOfUse"] = True
    value["firstname"] = fname
    value["lastname"] = lname
    value["dateofbirth"] = int((datetime.datetime.fromisoformat(dob).astimezone(uk_timezone)).timestamp()*1000)
    value["mobilenumber"] = mobile
    value["emailaddress"] = email
    
    payload["value"] = json.dumps(value)
    
    response = requests.put(url, headers=headers, json=payload)
    
    return response.json()