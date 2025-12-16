// Switch to your database
db = db.getSiblingDB("subscriptionDB");

// Create a collection
db.createCollection("subscriptions");

// Insert sample documents
db.subscriptions.insertMany([
  {
    "_id": ObjectId("674d0001a1b2c3d4e5f60001"),
    "orderDate": "2025-12-01",
    "startDate": "2025-12-02",
    "endDate": "2026-02-22",
    "active": true,
    "pickupLocation": "Aarhus",
    "associatedCustomerId": "6936e20cd28bec25e19dc29d",
    "associatedRegNr": "XD69420",
    "pricePrMonth": 3600,
    "insuranceDealNr": 2
  },
  {
    "_id": ObjectId("674d0001a1b2c3d4e5f60002"),
    "orderDate": "2025-11-20",
    "startDate": "2025-11-22",
    "endDate": "2026-01-15",
    "active": true,
    "pickupLocation": "Copenhagen",
    "associatedCustomerId": "6936e20cd28bec25e19dc29f",
    "associatedRegNr": "JD97731",
    "pricePrMonth": 4100,
    "insuranceDealNr": 1
  },
  {
    "_id": ObjectId("674d0001a1b2c3d4e5f60003"),
    "orderDate": "2025-10-05",
    "startDate": "2025-10-06",
    "endDate": "2025-11-30",
    "active": false,
    "pickupLocation": "Aalborg",
    "associatedCustomerId": "6936e20cd28bec25e19dc29e",
    "associatedRegNr": "BQ38126",
    "pricePrMonth": 3300,
    "insuranceDealNr": 3
  },
  {
    "_id": ObjectId("674d0001a1b2c3d4e5f60004"),
    "orderDate": "2025-12-10",
    "startDate": "2025-12-12",
    "endDate": "2026-03-10",
    "active": true,
    "pickupLocation": "Aarhus",
    "associatedCustomerId": "6936e20cd28bec25e19dc2a0",
    "associatedRegNr": "DO17851",
    "pricePrMonth": 3900,
    "insuranceDealNr": 2
  },
  {
    "_id": ObjectId("674d0001a1b2c3d4e5f60005"),
    "orderDate": "2025-09-18",
    "startDate": "2025-09-19",
    "endDate": "2025-11-28",
    "active": false,
    "pickupLocation": "Kolding",
    "associatedCustomerId": "6936e20cd28bec25e19dc2a1",
    "associatedRegNr": "AD46784",
    "pricePrMonth": 3000,
    "insuranceDealNr": 4
  },
  {
    "_id": ObjectId("674d0001a1b2c3d4e5f60006"),
    "orderDate": "2025-12-03",
    "startDate": "2025-12-04",
    "endDate": "2026-02-18",
    "active": true,
    "pickupLocation": "Aarhus",
    "associatedCustomerId": "6936e20cd28bec25e19dc2a0",
    "associatedRegNr": "UG23317",
    "pricePrMonth": 3700,
    "insuranceDealNr": 1
  }
]);