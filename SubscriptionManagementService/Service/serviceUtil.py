import requests
from flask import jsonify, request
from dotenv import load_dotenv
import datetime
import os

load_dotenv()

def onSubscriptionStart ():
    authHeader = getAuthHeader()
    
    # skrive og resavere bilen
    # opdatere aktiv status i db
    

    None

def onSubscriptionEnd ():
    #jwt
    # skrive til payment
    # afresavere bilen
    # opdatere aktiv status i db
    
    
    None

def getAuthHeader():
    
    authCredz = {
        "username": os.getenv("AUTH_USERNAME"),
        "password": os.getenv("AUTH_PASSWORD")
    }

    url = f"{os.getenv("LOCAL_GATEWAY_URL")}/getAuthToken"

    response = requests.request(
        method="POST",
        url=url,
        headers={"Content-Type": "application/json"},
        json=authCredz
    ).json()

    key = response["access_token"]

    returnHeader = {"Authorization": f"Bearer {key}"}

    return returnHeader

print(getAuthHeader())