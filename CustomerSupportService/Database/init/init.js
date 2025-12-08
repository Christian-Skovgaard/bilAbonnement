// Switch to your database
db = db.getSiblingDB("customer-service-db");

// Create a collection
db.createCollection("complaints");

// Insert sample documents
db.complaints.insertMany([
  { 
    regNr: "XD69420", 
    name: "magnus", 
    date: "2020-01-10",
    complaint: "help!!",
    completed: true
  },

{   
    regNr: "XD69420", 
    name: "victor", 
    date: "2020-01-10",
    complaint: "help!!",
    completed: false
}]);