import requests
from flask import jsonify, request
from dotenv import load_dotenv
import dbUtil as db
import datetime
import os

load_dotenv()

def onSubscriptionStart (subObj):
    authToken = getAuthToken()
    
    # Opret task i TaskManagementService
    taskResp = requests.request(
        method="POST",
        url=f"{os.getenv('GATEWAY_URL')}/task-management-service/tasks",
        headers={
            "Authorization": f"Bearer {authToken}",
            "Content-Type": "application/json"
        },
        json={
            "title": f"Ny subscription startet - {subObj['associatedRegNr']}",
            "description": f"Subscription med ID {subObj['id']} er blevet oprettet og startet for bil {subObj['associatedRegNr']}",
            "assignedTo": "Reception",
            "status": "pending"
        }
    )
    
    if "error" in taskResp:
        return {
            "success": False,
            "err": taskResp["error"]
            }
    
    # skrive og resaverer bilen
    carResp = requests.request(
        method="PUT",
        url=f"{os.getenv('GATEWAY_URL')}/car-catalog-service/cars/regNr/{subObj['associatedRegNr']}",
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
    

def onSubscriptionEnd (subObj):
    authToken = getAuthToken()
    
    #skrive til payment servicen
    paymentResp = requests.request( # ikke done!!!
        method="PUT",
        url=f"{os.getenv('GATEWAY_URL')}/payment-service/",
        headers={
            "Authorization": f"Bearer {authToken}",
            "Content-Type": "application/json"
            },
        json={"active": False}
    )


    # skrive og afresaverer bilen
    carResp = requests.request(
        method="PUT",
        url=f"{os.getenv('GATEWAY_URL')}/car-catalog-service/cars/regNr/{subObj['associatedRegNr']}",
        headers={
            "Authorization": f"Bearer {authToken}",
            "Content-Type": "application/json"
            },
        json={"active": False}
    )

    if "error" in carResp:
        return {
            "success": False,
            "err": carResp["error"]
            }
    
    # opdatere aktiv status i db
    dbResp = db.updateSubscriptionOnId(subObj["id"],{"active": False})
    if not dbResp["success"]:
        return {
            "success": False,
            "err": "error updating active status!"
            }
    
    return {"success": True}
    
    
    None

def getAuthToken():
    
    authCredz = {
        "username": os.getenv("AUTH_USERNAME"),
        "password": os.getenv("AUTH_PASSWORD")
    }

    url = f"{os.getenv('GATEWAY_URL')}/getAuthToken"

    response = requests.request(
        method="POST",
        url=url,
        headers={"Content-Type": "application/json"},
        json=authCredz
    ).json()

    key = response["access_token"]

    return key