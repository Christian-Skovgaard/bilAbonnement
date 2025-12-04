from flask import Flask, jsonify, request
import dbUtil as db
import serviceTasks as tasks
import pymongo
import datetime

myclient = pymongo.MongoClient("mongodb://subscription-management-db:27017")
mydb = myclient["subscription-db"] # Choose database "car-catalog-db"
mycol = mydb["subscription"] # Choose collection

app = Flask(__name__)

@app.post('/createSubscription')
def createSubscription():

    subObj = request.get_json()

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
    subObj["orderDate"] = today.strftime("%Y-%m-%d"), # laver datetime om til str
    subObj["active"] = False

    insertObj = db.insertSubscription(subObj)


    print(insertObj)
    if not insertObj["success"]: # hvis ikke det er succes at indsætte i db, måske lidt redudant, men du ved...
        return jsonify({"msg": "internal server error when inserting subObj to db"}), 500
    
    subObj["id"] = insertObj["id"]

    print("today", today == datetime.datetime.strptime(subObj["startDate"], "%Y-%m-%d").date())
    if today == datetime.datetime.strptime(subObj["startDate"], "%Y-%m-%d").date():  # vi ser om startday er i dag
        subStartResp = tasks.onSubscriptionStart(subObj)    # i så fald kører de tasks som skal kører ved subscription start
        print(subStartResp)

    return jsonify({"msg": f"succesfully inserted sub with id: {subObj["id"]}"})


@app.route('/dostuff', methods=['GET'])
def stuff():

    data = {
        "yes": "baby"
    }

    resp = db.insertSubscription(data)

    print(resp)

    return jsonify("ok")


@app.route('/test', methods=['GET'])
def test():
    return jsonify("i am alive")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008)