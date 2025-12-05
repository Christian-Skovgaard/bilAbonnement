from flask import Flask, jsonify, request
import pymongo

myclient = pymongo.MongoClient("mongodb://damage-registration-db:27017")
mydb = myclient["damage-registration-db"] # Choose database "car-catalog-db"
mycol = mydb["cases"] # Choose collection

app = Flask(__name__)

# Get all damageCases
@app.route('/cases', methods=['GET'])
def get_cases():
    cursor = mycol.find({})
    damageCases = []
    for doc in cursor:
        # Convert ObjectId (or other non-JSON types) to string
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        damageCases.append(doc)
    return jsonify(damageCases)

#Search damageCases med regNr
@app.route('/cases/<regnr>/query', methods=['GET'])
def get_cases_by_regnr(regnr):
    queryParams = request.args
    query = [{"regNr": regnr}]
    for key, value in queryParams.items():
        if value != "":
            query.append({key: {"$regex": value, "$options": "i"}})
    mongo_filter = {"$and": query} if query else {}
    cursor = mycol.find(mongo_filter)
    damageCases = []
    for doc in cursor:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        damageCases.append(doc)
    return jsonify(damageCases)

#POST på RegNr
@app.route('/cases/<regNr>', methods=['POST'])
def add_case(regNr):
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
@app.route('/cases/<int:caseId>', methods=['PUT'])
def update_case(caseId):
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