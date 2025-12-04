import requests
from flask import jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()

def onSubscriptionStart ():
    # get jwt
    
    # skrive og resavere bilen
    # opdatere aktiv status i db
    

    None

def onSubscriptionEnd ():
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
        data=authCredz
    )

    return response

print(getAuthHeader())