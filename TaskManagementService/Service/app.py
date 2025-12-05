from flask import Flask, jsonify, request
import pymongo

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://task-management-db:27017/")
db = client["task-management-db"]
tasks_collection = db["tasks"]


# Get all tasks