from flask import Flask, jsonify, request
import pymongo
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://task-management-db:27017/")
db = client["task-management-db"]
tasks_collection = db["tasks"]

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor = tasks_collection.find({})  # Query
    tasks = []
    for task in cursor:
        task['_id'] = str(task['_id'])
        tasks.append(task)
    return jsonify(tasks)

#Get tasks by department
@app.route('/tasks/department/<department_name>', methods=['GET'])
def get_tasks_by_department(department_name):
    cursor = tasks_collection.find({"assignedTo": department_name})
    tasks = []
    for task in cursor:
        task['_id'] = str(task['_id'])
        tasks.append(task)
    return jsonify(tasks)

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    task_data = request.json
    tasks_collection.insert_one(task_data)
    return jsonify({"message": "Task created successfully"}), 201

# Change task status
@app.route('/tasks/<task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    new_status = request.json.get('status')
    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": new_status}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task status updated successfully"})

#Change task details by id
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task_details(task_id):
    task_data = request.json
    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task_data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    
    updated_task = tasks_collection.find_one({"_id": ObjectId(task_id)}, {"_id": 0})
    return jsonify(updated_task)

# Delete a task
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)

