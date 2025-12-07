from flask import Flask, jsonify, request
from mongoengine import connect, Document, StringField, IntField
from bson import Regex

import pymongo

myclient = pymongo.MongoClient("mongodb://customer-service-db:27017")
mydb = myclient["customer-service-db"] 
mycol = mydb["complaints"] # Choose collection

app = Flask(__name__)

# Get all complaints
@app.route('/complaints', methods=['GET'])
def get_complaints():
    cursor = mycol.find({}, {"_id": 0}) # Query and remove MongoDB _id (surpress_id)
    complaints = list(cursor)
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
@app.route('/complaints/<int:complaintId>', methods=['PUT'])
def update_complaint(complaintId):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    
    data.pop("_id", None)

    result = mycol.update_one(
        {"complaintId": complaintId},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Complaint not found"}), 404

    return jsonify({"message": "Complaint updated"}), 200

#DELETE ud fra complaintsId
@app.route('/complaints/<int:complaintId>', methods=['DELETE'])
def delete_complaint(complaintId):

    result = mycol.delete_one({"complaintId": complaintId})

    if result.deleted_count == 0:
        return jsonify({"error": "Complaint not found"}), 404

    return jsonify({"message": "Complaint deleted"}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)










"""
connect(db='customer-service-db', host='customer-service-db', port=27017)

app = Flask(__name__)

class Complaint(Document):
    complaintId = IntField(required=True)
    name = StringField(required=True)
    year = IntField()
    meta = {"collection": "complaints"}

def complaints_to_dict(complaint):
    d = complaint.to_mongo().to_dict()
    d['id'] = str(d.pop('_id'))
    return d

@app.route('/complaints', methods=['GET'])
def get_complaints():
    complaints = Complaint.objects()
    return jsonify([complaints_to_dict(c) for c in complaints])


@app.route('/complaints', methods=['POST'])
def add_complaints():
    data = request.get_json(force=True)
    complaintId = data.get('complaintId')
    name = data.get('name')
    year = data.get('year')
    complaints = Complaint(complaintId=complaintId, name=name, year=year)
    complaints.save()
    return jsonify(complaints_to_dict(complaints)), 201


#get complaints by query parameters
@app.route('/complaints/query', methods=['GET'])
def search_complaints():
    complaintId = request.args.get('complaintId')
    name = request.args.get('name')
    year = request.args.get('year')

    filters = {}
    
    if complaintId:
        filters['complaintId'] = int(complaintId)  
    
    if name:
        filters['name__icontains'] = name

    if year:
        filters['year'] = int(year)

    complaints = Complaint.objects(**filters)

    return jsonify([complaints_to_dict(c) for c in complaints])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

    """