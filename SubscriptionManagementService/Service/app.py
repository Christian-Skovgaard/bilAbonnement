from flask import Flask, jsonify, request
from bson import ObjectId
from bson.errors import InvalidId
from bson import Regex
import dbUtil as db
import serviceTasks as tasks
import pymongo
import datetime

myclient = pymongo.MongoClient("mongodb://subscription-management-db:27017")
mydb = myclient["subscriptionDB"] # Choose database "car-catalog-db"
mycol = mydb["subscriptions"] # Choose collection

app = Flask(__name__)

@app.post('/subscriptions')
def createSubscription():

    subObj = request.get_json()
    if not subObj: # vi ser om der er body
        return jsonify({"error": "No JSON body provided"}), 400

    required = {
        "startDate",    # skal være str i format yyyy-mm-dd
        "endDate",
        "pickupLocation",
        "associatedCustommerId",
        "associatedRegNr",
        "pricePrMonth"
    }

    if not required.issubset(subObj):  #vi tjekker om alle keys er der
        return jsonify({"error": "Missing fields 🏺🌎🚑"}), 400

    today = datetime.date.today()

    subObj["associatedRegNr"] = subObj["associatedRegNr"].strip(" ") # trimmer for od orden
    subObj["orderDate"] = today.strftime("%Y-%m-%d") # laver datetime om til str
    subObj["active"] = False

    insertObj = db.insertSubscription(subObj)
    
    if not insertObj["success"]: # hvis ikke det er succes at indsætte i db, måske lidt redudant, men du ved...
        return jsonify({"msg": "internal server error when inserting subObj to db"}), 500
    
    subObj["id"] = insertObj["id"]

    # her skal customer service måske også informeres eller updates

    if True:    # today == datetime.datetime.strptime(subObj["startDate"], "%Y-%m-%d").date():  # vi ser om startday er i dag
        subStartResp = tasks.onSubscriptionStart(subObj)    # i så fald kører de tasks som skal kører ved subscription start

        if not subStartResp["success"]:
            return jsonify({"error": f"error on upstart: {subStartResp['err']}"})

    return jsonify({"msg": f"succesfully inserted sub with id: {subObj['id']}"})

@app.put('/subscriptions/<subId>')
def updateSub (subId):
    reqBody = request.get_json()
    if not reqBody:
        return jsonify("no body attached"), 400
    
    try:
        # Convert string ID to ObjectId
        obj_id = ObjectId(subId)
    except InvalidId:
        return jsonify({"error": "Invalid ID format"}), 400


    sub = mycol.find_one({"_id": obj_id})
    if not sub:
        return jsonify("subscription matching ID not found"), 400
    
    result = mycol.update_one({"_id": obj_id}, {"$set": reqBody})

    return jsonify({
        "message": "Update successful",
        "matched_count": result.matched_count,
        "modified_count": result.modified_count
    })

@app.route('/subscriptions', methods=['GET'])
def get_all_subscriptions():
    subs = list(mycol.find())
    
    for sub in subs:    
        sub['_id'] = str(sub['_id'])    # _id skal laves til str for at gå i json
    
    return jsonify(subs), 200

@app.route('/subscriptions/<sub_id>', methods=['GET'])
def get_subscription(sub_id):

    sub = mycol.find_one({"_id": ObjectId(sub_id)})
    if not sub:
        return jsonify({"error": "No subscibtion matching id 🥷🏿"}), 404

    
    sub['_id'] = str(sub['_id'])    # _id skal laves til str for at gå i json

    return jsonify(sub), 200

@app.route('/subscriptions/query', methods=['GET']) # Skal kunne tage højde for, om pris er INDEN FOR monthlyMin og monthlyMax
def search_cars():
    queryParams = request.args # Dict of query parameters
    query = []

    for key, value in queryParams.items():
        if value != "":
            query.append({key: Regex(value, "i")}) # # Lav en liste af objekter til query ud fra query params f.eks.: [{brand : "Toyota"}, {model : "GT86"}]

    if query:
        mongo_filter = {"$and": query} # Request parameters given.
    else:
        mongo_filter = {}  # No request parameters given / empty request parameters like: ?brand=&model=

    cursor = mycol.find(mongo_filter, {"_id": 0}) # Query and remove MongoDB _id (surpress _id)
    subs = list(cursor)
    return jsonify(subs)

@app.route('/test', methods=['GET'])
def test():
    return jsonify("i am alive")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)