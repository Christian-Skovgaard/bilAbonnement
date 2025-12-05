from flask import Flask, jsonify, request
import pymongo

myclient = pymongo.MongoClient("mongodb://damage-registrations-db:27017")
mydb = myclient["damage-registrations-db"] # Choose database "car-catalog-db"
mycol = mydb["damageCases"] # Choose collection

app = Flask(__name__)

# Get all damageCases
@app.route('/damageCases', methods=['GET'])
def get_damageCases():
    cursor = mycol.find({}, {"_id": 0})
    damageCases = list(cursor)
    return jsonify(damageCases)

#Search damageCases med regNr
@app.route('/damageCases/<regnr>/query', methods=['GET'])
def search_damageCases(regnr):
    # Brug regnr direkte uden at fjerne mellemrum
    queryParams = request.args
    query = [{"regNr": regnr}]  

    # Tilføj yderligere query-parametre som regex
    for key, value in queryParams.items():
        if value != "":
            query.append({key: {"$regex": value, "$options": "i"}})

    mongo_filter = {"$and": query} if query else {}

    cursor = mycol.find(mongo_filter)
    damageCases = list(cursor)
    return jsonify(damageCases)

#POST på RegNr
@app.route('/damageCases/<regNr>', methods=['POST'])
def add_damagecase(regNr):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    data["regNr"] = regNr

    cursor = mycol.insert_one(data)

    return jsonify({
        "message": "Damagecase added",
        "regNr": regNr,
        "inserted_id": str(cursor.inserted_id)
    }), 201




#PUT damageCases med caseId 
@app.route('/damageCases/<int:caseId>', methods=['PUT'])
def update_damageCases(caseId):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    
    data.pop("_id", None)

    cursor = mycol.update_one(
        {"caseId": caseId},
        {"$set": data}
    )

    if cursor.matched_count == 0:
        return jsonify({"error": "Complaint not found"}), 404

    return jsonify({"message": "Complaint updated"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)


