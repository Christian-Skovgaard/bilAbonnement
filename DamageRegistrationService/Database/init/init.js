// Switch to your database
db = db.getSiblingDB("damage-registration-db");

// Create a collection
db.createCollection("cases", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["regNr", "brand", "model", "modelYear", "description", "date"],
      additionalProperties: false,
      properties: {
        _id: {
          bsonType: "objectId"
        },
        regNr: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        car: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        model: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        modelYear: {
          bsonType: "int",
          minimum: 1886, // first car invented
          maximum: 2100,
          description: "must be an integer year"
        },
        description: {
          bsonType: "string",
          description: "must be a string and is required"
        },
        date: {
          bsonType: "string",
          description: "must be a string and is required"
        }
      }
    }
  },
  validationAction: "error" // reject invalid inserts/updates
});

// Insert sample documents
db.cases.insertMany([
  {
    regNr: "XD69420",
    car: "Toyota",
    model: "GT86",
    modelYear: 2014,
    description: "crashed the car",
    date: "2025-01-12"
  },
  {
    regNr: "XD69420",
    car: "audi",
    model: "rs6",
    modelYear: 2016,
    description: "Hit a pole",
    date: "2022-02-10"
  }
]);