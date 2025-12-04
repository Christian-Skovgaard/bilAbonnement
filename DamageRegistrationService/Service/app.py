from flask import Flask, jsonify, request
import pymongo

myclient = pymongo.MongoClient("mongodb://damage-registrations-db:27017")
mydb = myclient["damage-registrations-db"] # Choose database "car-catalog-db"
mycol = mydb["registrations"] # Choose collection

app = Flask(__name__)

# Get all registrations
@app.route('/registrations', methods=['GET'])
def get_registrations():
    cursor = mycol.find({}, {"_id": 0}) # Query and remove MongoDB _id (surpress_id)
    registrations = list(cursor)
    return jsonify(registrations)

# Get queried registrations
@app.route('/registrations/<regnr>/query', methods=['GET'])
def search_registrations_by_regnr(regnr):
    queryParams = request.args
    query = [{"regNr": regnr}]  # Start med regnr som filter

    # Tilføj yderligere query-parametre, hvis de ikke er tomme
    for key, value in queryParams.items():
        if value != "":
            query.append({key: value})

    if query:
        mongo_filter = {"$and": query}
    else:
        mongo_filter = {}

    cursor = mycol.find(mongo_filter, {"_id": 0})
    registrations = list(cursor)
    return jsonify(registrations)

#POST complaints
@app.route('/registrations', methods=['POST']) 
def add_registrations():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    cursor = mycol.insert_one(data)
    return jsonify({
        "message": "Complaint added",
        "inserted_id": str(cursor.inserted_id)
    }), 201

#PUT registrations med caseId 
@app.route('/registrations/<int:caseId>', methods=['PUT'])
def update_registrations(caseId):
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


