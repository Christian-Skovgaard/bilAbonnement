// Switch to your database
db = db.getSiblingDB("task-management-db");


db.createCollection("tasks", {
  validator: {
    $jsonSchema: {
        bsonType: "object",
        required: ["title", "description", "status", "assignedTo", "dueDate"],
        properties: {
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
            },
            dueDate: {
                bsonType: "date",
                description: "must be a date and is required"
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
    assignedTo: "Reception",
    dueDate: new Date("2025-05-12")
    },
    {
    title: "Implement Authentication",
    description: "Set up user authentication and authorization.",
    status: "pending",
    assignedTo: "Inspection",
    dueDate: new Date("2025-05-20")
    },
    {
    title: "Set Up CI/CD Pipeline",
    description: "Configure continuous integration and deployment pipeline.",
    status: "completed",
    assignedTo: "Salesmen",
    dueDate: new Date("2025-04-30")
    }
]);
