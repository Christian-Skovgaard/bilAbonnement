// Switch to your database
db = db.getSiblingDB("customer-service-db");

// Create a collection
db.createCollection("complaints");

// Insert sample documents
db.complaints.insertMany([
  { complaintId: 1, name: "magnus", year: 2020 },
  { complaintId: 2, name: "victor", year: 2021 }
]);