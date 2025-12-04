import requests
from flask import jsonify, request
from dotenv import load_dotenv
import dbUtil as db
import datetime
import os

load_dotenv()

def onSubscriptionStart (subObj):
    authToken = getAuthToken()
    
    # skrive og resaverer bilen
    carResp = requests.request(
        method="PUT",
        url=f"{os.getenv("LOCAL_GATEWAY_URL")}/car-catalog-service/cars/regNr/{subObj["associatedRegNr"]}",
        headers={
            "Authorization": f"Bearer {authToken}",
            "Content-Type": "application/json"
            },
        json={"active": True}
    )

    if "error" in carResp:
        return {
            "success": False,
            "err": carResp["error"]
            }
    
    # opdatere aktiv status i db
    dbResp = db.updateSubscriptionOnId(subObj["id"],{"active": True})
    if not dbResp["success"]:
        return {
            "success": False,
            "err": "error updating active status!"
            }
    
    return {"success": True}
    

def onSubscriptionEnd ():
    #jwt
    # skrive til payment
    # afresavere bilen
    # opdatere aktiv status i db
    
    
    None

def getAuthToken():
    
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


carResp = requests.request(
        method="PUT",
        url="http://localhost:5001/car-catalog-service/cars/regNr/XD69420",
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2NDg4OTE4MSwianRpIjoiNDE2MGQwODQtYzI4Yy00NmVlLWI0MmItMDlkYzQ3N2ZhZDNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkJvIiwibmJmIjoxNzY0ODg5MTgxLCJjc3JmIjoiODJiYzVkZDItZmVjOC00NGNiLWFkOTQtZDI3NThjZGE3ZmU1IiwiZXhwIjoxNzcwMDczMTgxLCJyb2xlIjoiYWRtaW4iLCJkZXBhcnRtZW50IjoiS29saW5nIn0.ervCIhnk4iyzZNB4DpuU4IvrtMttntWcdcrvytnUrfauFuGqvPm6_nqH0Ps45gCqhCIUI3YUQti7jk3JTiLsA4L8RFhYOdaFv6LrYjACHINtl6Q1XO5IJTlSAGsuWc3EiWrvpHRfUvDB5-8n6xRNa5qEdwEToZofjcvYrxCuWsZ067rNYVumWR6e9oAOc7IUFHcC_L1vYGwti2SbB8XJAxxkdJc3Zr8YTOD9EBscal1pOOdznRHR4pS3QUUDIpJJxBssINq1wClaS9_8zPYhTW4eMgeq3NDVoqtwaW7y7cwG5BXNIhyicRGD-WD33oAklHr2Ess8wfNrmSs-Ozp-WA",
            "Content-Type": "application/json"
            },
        json={"active": True}
    )

print(carResp.content)
