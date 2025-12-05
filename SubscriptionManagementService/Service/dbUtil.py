import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
import datetime
import os

load_dotenv()

myclient = pymongo.MongoClient("mongodb://subscription-management-db:27017") # "mongodb://subscription-management-db:27017"
mydb = myclient["subscriptionDB"] # Choose database "car-catalog-db"
mycol = mydb["subscriptions"] # Choose collection

def insertSubscription (subObj): #works
    try:
        result = mycol.insert_one(subObj)
        print(f"Subscription inserted with _id: {result.inserted_id}")
        return {
            "success": True,
            "id": str(result.inserted_id)
            }
    except:
        print("failed to put stuff in the box")
        return {"success": False}
   

def updateSubscriptionOnId(sub_id, update_fields):
    
    try:
        if isinstance(sub_id, str): # sikre os at id er et ObjectId, ellers brokker den sig meget
            sub_id = ObjectId(sub_id)

        result = mycol.update_one(
            {"_id": sub_id},
            {"$set": update_fields}
        )

        if result.matched_count == 0:
            return {
                "success": False,
                "message": "No document found with that ID"
            }

        return {
            "success": True,
            "modified_count": result.modified_count
        }

    except Exception as e:
        print("Error updating subscription:", e)
        return {
            "success": False,
            "message": str(e)
        }
    
