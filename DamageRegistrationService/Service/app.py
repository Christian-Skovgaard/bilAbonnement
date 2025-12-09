from flask import Flask, jsonify, request, abort
import pymongo
from bson.objectid import ObjectId

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

# Find damageCases for regNr
@app.route('/cases/<regnr>', methods=['GET'])
def get_cases_by_regnr(regnr):
    cursor = mycol.find({"regNr" : regnr})
    damageCases = []
    for doc in cursor:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        damageCases.append(doc)
    return jsonify(damageCases)

# Query damageCases med regNr
@app.route('/cases/<regnr>/query', methods=['GET'])
def query_by_regnr(regnr):
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

    # Ensure regNr is always set from URL
    data["regNr"] = regNr

    cursor = mycol.insert_one(data)

    return jsonify({
        "message": "Damagecase added",
        "regNr": regNr,
        "inserted_id": str(cursor.inserted_id)
    }), 201


#PUT damageCases med caseId 
@app.route('/cases/<caseId>', methods=['PUT'])
def update_case(caseId):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    
    cursor = mycol.update_one(
        {"_id": ObjectId(caseId)},
        {"$set": data}
    )

    if cursor.matched_count == 0:
        return jsonify({"error": "Case not found"}), 404

    return jsonify({"message": "Case updated"}), 200

# DELETE damageCase på caseId 
@app.route('/cases/<caseId>', methods=['DELETE'])
def delete_case(caseId):
    result = mycol.delete_one({"_id": ObjectId(caseId)})

    # Check if any document was actually deleted
    if result.deleted_count == 0:
        abort(404, description=f"Case with ID {caseId} not found.")

    return jsonify({"message": f"Case with ID {caseId} deleted"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)