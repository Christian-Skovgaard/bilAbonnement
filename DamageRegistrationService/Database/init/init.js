// Switch to your database
db = db.getSiblingDB("damage-registrations-db");

// Create a collection
db.createCollection("registrations");

// Insert sample documents
db.registrations.insertMany([
  {
    caseId: 1,
    regNr: "XD 69 420",
    car: "Toyota",
    model: "GT86"
  },
  {
    caseId: 2,
    regNr: "XD 69 420",
    car: "audi",
    model: "rs6"
  }
]);