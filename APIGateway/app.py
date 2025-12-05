from flask import Flask, request, jsonify, Response
import requests
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity, get_jwt)
import os

# Service URLs (internal Docker network)
services = {
    "car-catalog-service": "http://car-catalog-service:5002",
    "customer-support-service": "http://customer-support-service:5003/",
    "authorization-service": "http://authorization-service:5004",
    "customer-managment-service": "temp:5005",
    "subscription-managment-service": "temp:5006",
    "payment-service": "temp:5007",
    "subscription-management-service": "http://subscription-management-service:5008"
}

app = Flask(__name__)
jwt = JWTManager(app)

resp = requests.get("http://authorization-service:5004/getPublicKey")
PUBLIC_KEY = resp.json()["key"]

# jwt auth config
app.config["JWT_ALGORITHM"] = "RS256" # asymetrisk algoritme som kan valideres af public men kun krypteres af private
app.config["JWT_PUBLIC_KEY"] = PUBLIC_KEY # public key kan bruges til at validere tokens, den får vi fra AuthorizationService


@app.route('/getAuthToken', methods=['POST'])
@jwt_required(optional=True)
def getAuthToken():
    url = f"{services['authorization-service']}/getAuthToken"

    response = requests.request(
        method="POST",
        url=url,
        headers=dict(request.headers),
        data=request.get_data() # body hedder i flask data
    )

    data = response.json()

    return response.content

#endpoint der hjælper med at teste om vi for svar
@app.route('/heath', methods=['GET'])
@jwt_required(optional=True)
def test():
    return jsonify(heath="tip top form 🏋️")


@app.route('/<service>/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
@jwt_required()
def lyskryds(service, path):

    if not service in services:
        return jsonify(msg="no service with that name")

    url = f"{services[service]}/{path}"

    serviceResponse = requests.request(
        method=request.method,
        url=url,
        headers=dict(request.headers), # vi omformaterer fordi req-headersne har formatet flak-header, men headers argumentet forventer dict
        params=request.args,
        data=request.get_data(), # IKKE JSON >:(
    )

    clientResponse = Response(
        response=serviceResponse.content, 
        status=serviceResponse.status_code,
        headers=dict(serviceResponse.headers)
        )

    return clientResponse
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)