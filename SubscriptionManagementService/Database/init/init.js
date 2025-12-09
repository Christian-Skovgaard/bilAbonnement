// Switch to your database
db = db.getSiblingDB("subscriptionDB");

// Create a collection
db.createCollection("subscriptions");

// Insert sample documents
db.subscriptions.insertMany([
  {
    "orderDate": "2025-12-01",
    "startDate": "2025-12-02",
    "endDate": "2026-02-22",
    "active": true,
    "pickupLocation": "Aarhus",
    "associatedCustomerId": "1",
    "associatedRegNr": "XD69420",
    "pricePrMonth": 3600,
    "insuranceDealNr": 2
  },
  {
    "orderDate": "2025-11-20",
    "startDate": "2025-11-22",
    "endDate": "2026-01-15",
    "active": true,
    "pickupLocation": "Copenhagen",
    "associatedCustomerId": "3",
    "associatedRegNr": "ab 2039",
    "pricePrMonth": 4100,
    "insuranceDealNr": 1
  },
  {
    "orderDate": "2025-10-05",
    "startDate": "2025-10-06",
    "endDate": "2025-11-30",
    "active": false,
    "pickupLocation": "Aalborg",
    "associatedCustomerId": "2",
    "associatedRegNr": "JD97731",
    "pricePrMonth": 3300,
    "insuranceDealNr": 3
  },
  {
    "orderDate": "2025-12-10",
    "startDate": "2025-12-12",
    "endDate": "2026-03-10",
    "active": true,
    "pickupLocation": "Aarhus",
    "associatedCustomerId": "4",
    "associatedRegNr": "kd 4401",
    "pricePrMonth": 3900,
    "insuranceDealNr": 2
  },
  {
    "orderDate": "2025-09-18",
    "startDate": "2025-09-19",
    "endDate": "2025-11-28",
    "active": false,
    "pickupLocation": "Kolding",
    "associatedCustomerId": "5",
    "associatedRegNr": "fy 5592",
    "pricePrMonth": 3000,
    "insuranceDealNr": 4
  },
  {
    "orderDate": "2025-12-03",
    "startDate": "2025-12-04",
    "endDate": "2026-02-18",
    "active": true,
    "pickupLocation": "Aarhus",
    "associatedCustomerId": "7",
    "associatedRegNr": "jh 2209",
    "pricePrMonth": 3700,
    "insuranceDealNr": 1
  }
]);