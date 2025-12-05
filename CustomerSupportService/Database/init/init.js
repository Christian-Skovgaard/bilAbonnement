// Switch to your database
db = db.getSiblingDB("customer-service-db");

// Create a collection
db.createCollection("complaints");

// Insert sample documents
db.complaints.insertMany([
  { complaintId: 1, 
    name: "magnus", 
    date: "2020-01-10",
    complaint: "help!!"
  },

{ complaintId: 2, 
    name: "victor", 
    date: "2020-01-10",
    complaint: "help!!"
}]);