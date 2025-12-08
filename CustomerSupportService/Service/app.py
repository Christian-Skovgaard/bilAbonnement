from flask import Flask, jsonify, request
from mongoengine import connect, Document, StringField, IntField
from bson import Regex
from bson import ObjectId

import pymongo

myclient = pymongo.MongoClient("mongodb://customer-service-db:27017")
mydb = myclient["customer-service-db"] 
mycol = mydb["complaints"] # Choose collection

app = Flask(__name__)

# Get all complaints
@app.route('/complaints', methods=['GET'])
def get_complaints():
    cursor = mycol.find({})
    complaints = []
    
    for doc in cursor:
        # Konverter MongoDB ObjectId til string
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        complaints.append(doc)

    return jsonify(complaints)
# Get queried complaints
@app.route('/complaints/query', methods=['GET']) 
def search_complaints():
    queryParams = request.args # Dict of query parameters
    query = []

    for key, value in queryParams.items():      
        if value.lower() == ("true"): # Is boolean?
            query.append({key: True})
        elif value.lower() == ("false"):
            query.append({key: False})
        elif value.isdigit():
            query.append({key: int(value)})
        else: # Is string.
            if queryParams[key] != "": # Ignorerer parametre som "cars/query?regNr=&model="
                query.append({key: Regex(value, "i")})
        
    if query:
        mongo_filter = {"$and": query} # Request parameters given.
    else:
        mongo_filter = {}  # No request parameters given / empty request parameters like: ?brand=&model=

    cursor = mycol.find(mongo_filter, {"_id": 0}) # Query and remove MongoDB _id (surpress _id)
    complaints = list(cursor)
    return jsonify(complaints)

#POST complaints
@app.route('/complaints', methods=['POST']) 
def add_complaints():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    result = mycol.insert_one(data)
    return jsonify({
        "message": "Complaint added",
        "inserted_id": str(result.inserted_id)
    }), 201


#PUT Complaints med complaintId 
@app.route('/complaints/<string:complaint_id>', methods=['PUT'])
def update_complaint(complaint_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400

    # Fjern _id, hvis brugeren sender det i JSON body
    data.pop("_id", None)

    try:
        obj_id = ObjectId(complaint_id)
    except:
        return jsonify({"error": "Invalid MongoDB _id"}), 400

    result = mycol.update_one(
        {"_id": obj_id},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Complaint not found"}), 404

    return jsonify({"message": "Complaint updated"}), 200


#DELETE ud fra complaintsId
@app.route('/complaints/<string:complaint_id>', methods=['DELETE'])
def delete_complaint(complaint_id):
    try:
        obj_id = ObjectId(complaint_id)
    except:
        return jsonify({"error": "Invalid MongoDB _id"}), 400

    result = mycol.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Complaint not found"}), 404

    return jsonify({"message": "Complaint deleted"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)










