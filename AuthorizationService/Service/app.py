from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt)
from dotenv import load_dotenv
import os, pathlib
import datetime
import db_util as db

load_dotenv()

app = Flask(__name__)

# hent keys
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, "keys/private_key.pem"), "r") as f:  # burde nok lægge path i .env, men ikke vigtigt
    PRIVATE_KEY = f.read()

with open(os.path.join(script_dir, "keys/public_key.pem"), "r") as f:
    PUBLIC_KEY = f.read()

#config for jwt gen
app.config["JWT_ALGORITHM"] = "RS256"
app.config["JWT_PRIVATE_KEY"] = PRIVATE_KEY
app.config["JWT_PUBLIC_KEY"] = PUBLIC_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=30)

jwt = JWTManager(app)

@app.route("/getAuthToken", methods=["POST"])
def getAuthToken():
    reqUsername = request.json.get("username")
    reqPassword = request.json.get("password")

    if (not reqUsername or not reqPassword):
        return jsonify({"error": "no username or password"}), 400

    user = db.fetch_user_by_username(reqUsername)

    if (not user):
        return jsonify({"error": "no user match"}), 401

    
    if (user["password"] != reqPassword):
        return jsonify({"error": "wrong password 🐟🐟🐟🦈"}), 401

    access_token = create_access_token(
        identity=user["username"], 
        additional_claims={
            "role": user["role"],
            "department": user["department"]
            }
        )
    return jsonify(access_token=access_token)

@app.route("/getPublicKey", methods=["GET"])
def getPublicKey ():
    return {"key": PUBLIC_KEY}


@app.route("/admin", methods=["GET"])
@jwt_required()
def superSecretMicroService():
    claims = get_jwt()
    
    return jsonify(claims)



@app.route('/', methods=['GET'])
def test():
    return "hello there"

@app.route('/test', methods=['GET'])
def test2():
    return "hello there"

app.run(host='0.0.0.0', debug=True, port=5004)

