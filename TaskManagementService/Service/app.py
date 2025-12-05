from flask import Flask, jsonify, request
import pymongo

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://task-management-db:27017/")
db = client["task-management-db"]
tasks_collection = db["tasks"]


# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor = tasks_collection.find({}, {"_id": 0})  # Query and remove MongoDB _id (suppress_id)
    tasks = list(cursor)
    return jsonify(tasks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)