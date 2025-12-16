// Switch to your database
db = db.getSiblingDB("task-management-db");


db.createCollection("tasks", {
  validator: {
    $jsonSchema: {
        bsonType: "object",
        required: ["title", "description", "status", "assignedTo"],
        additionalProperties: false,
        properties: {
            _id: {
                bsonType: "objectId"
            },
            title: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            description: {
                bsonType: "string",
                description: "must be a string and is required"
            },
            status: {
                bsonType: "string",
                enum: ["pending", "in-progress", "completed"],
                description: "must be one of the allowed status values"
            },
            assignedTo: {
                bsonType: "string",
                enum: ["Reception", "Inspection", "Salesmen"],
                description: "must be a string representing the user assigned to the task"
            }
        }
    }
  },
  validationAction: "error" // reject invalid inserts/updates
});

// Insert sample documents
db.tasks.insertMany([
  {
    title: "Bekræft afhentningsaftale",
    description: "Bekræft afhentningsaftale med kunden.",
    status: "in-progress",
    assignedTo: "Reception"
    },
    {
    title: "Inspicer bil AB 123 456",
    description: "Kunden ønsker at få bilen inspiceret grundigt for eventuelle skader.",
    status: "pending",
    assignedTo: "Inspection"
    },
    {
    title: "Gennemgå aftale med kunde",
    description: "Gennemgå aftale med kunde for at sikre forståelse og accept af vilkår.",
    status: "completed",
    assignedTo: "Salesmen"
    },
    {
    title: "Opdater status for lejeaftale",
    description: "Opdater status for lejeaftale.",
    status: "pending",
    assignedTo: "Salesmen"
    }
]);
