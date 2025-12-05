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
    title: "Design Database Schema",
    description: "Create the initial database schema for the project.",
    status: "in-progress",
    assignedTo: "Reception"
    },
    {
    title: "Implement Authentication",
    description: "Set up user authentication and authorization.",
    status: "pending",
    assignedTo: "Inspection"
    },
    {
    title: "Set Up CI/CD Pipeline",
    description: "Configure continuous integration and deployment pipeline.",
    status: "completed",
    assignedTo: "Salesmen"
    }
]);
