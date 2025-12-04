import time
import requests
from celery_app import celery

# Service URLs (internal Docker network)
services = {
    "car-catalog-service": "http://car-catalog-service:5002",
    "customer-support-service": "http://customer-support-service:5003/",
    "authorization-service": "http://authorization-service:5004",
    "customer-managment-service": "temp:5005",
    "subscription-managment-service": "temp:5006",
    "payment-service": "temp:5007",
    "subscription-management-service": "http://subscription-management-service:5008"
}


@celery.task(name="tasks.process_heavy_data")
def process_heavy_data(payload):
    """
    This runs inside the Worker Container.
    """
    print(f"WORKER: Received task")
    
    # Simulate heavy lifting (AI inference, video encoding, etc.)
    time.sleep(10)
    
    result = f"Processed items."
    print(f"WORKER: Finished. Result: {result}")
    return result

@celery.task(name="getCars")
def getCars(payload):
    time.sleep(10)
    response = requests.get("http://car-catalog-service:5002/cars")
    return response
