import requests
from flask import jsonify
import datetime
import pytz
from dateutil.relativedelta import relativedelta
from typing import Dict, Any

uk_timezone = pytz.timezone('Europe/London')

def appointmentCard(stacks):
    print("length :", len(stacks))
    for i in stacks:
        cards = i["cards"][0]
        print(cards["identifier"])
        if cards["identifier"] == "5":  # Ensure cards list is not empty
            print("got card")
            return cards  # Return first matching card
    return {} # Return None if no match found
        
def patientCard(stacks):
    for i in stacks:
        cards = i["cards"][0]
        if cards["identifier"] == "10":  # Ensure cards list is not empty
            return cards  # Return first matching card
    return {} # Return None if no match found

def transitionCard(stacks):
    for i in stacks:
        cards = i["cards"][0]
        if cards["identifier"] == "39":  # Ensure cards list is not empty
            return cards["actions"][0]  # Return first matching card
    return {} # Return None if no match found

def extractId(timeNow):
    url = f"https://uk.mydentalhub.online/v31/organization/233/perspectives?perspective=3&timestamp={timeNow}"
    
    print(url)
    headers = {
    "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    stacks = data.get("stacks", [])
    print(len(stacks))
    
    # here we will extract appointment details
    appointment_details = appointmentCard(stacks)
    appointment_body = appointment_details["body"]
    appointment_url = appointment_details["sourceObjectID"]
    
    patient_details = patientCard(stacks)
    patient_body = patient_details["body"]
    patient_url = patient_details["sourceObjectID"]
    
    transition_details = transitionCard(stacks)
    transition_body = transition_details["requirementsMet"]
    transition_url = transition_details["path"]

    # print(appointment_details)
    details_extracted = {
        "Appointment":{
            "Link":appointment_url,
            "Body":appointment_body
        },
        "Patient":{
            "Link":patient_url,
            "Body":patient_body
        },
        "Transition":{
            "Link":transition_url,
            "Body":transition_body
        }
    }
    return details_extracted
    