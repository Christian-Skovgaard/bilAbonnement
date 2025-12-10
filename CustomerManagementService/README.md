# Customer Management Service

## 📋 Description

This microservice is part of the [microsystem network](https://github.com/Christian-Skovgaard/bilAbonnement) developed by Team SAFers as part of the EK ITA 3rd semester autumn exam 2025. The system stands as an MVP for a potential internal system for Bilabonnement.dk in an effort to make them more data driven and effective.

This service exposes a simple RESTful API for managing customer data. The API is built with Flask and uses MongoDB to store customer records. It supports creating, reading, querying, updating, and deleting customers (CRUD operations) and is used across the microsystem to fetch and maintain customer information.

## ❓ How to Use

This service is expected to run as part of a bigger service. To learn more about how to get the service running, check out the README at the [Bilabonnement repository](https://github.com/Christian-Skovgaard/bilAbonnement).

### 💬 API Endpoints

The service exposes a RESTful API to manage damage cases stored in the MongoDB database. All endpoints are prefixed with the base path (e.g., `http://customer-management-service:5009`).

## API Endpoints

| HTTP Method | Endpoint                   | Description                                                                                                                             |
| :---------- | :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| **GET**     | `/customers`               | Retrieves a list of **all** customers currently in the database.                                                                        |
| **GET**     | `/customers/query`         | Retrieves customers based on optional **query parameters** using case-insensitive regex matching for flexible searching and filtering.  |
| **POST**    | `/customers`               | Creates and inserts a **new** customer into the database. Expects a JSON payload.                                                       |
| **PUT**     | `/customers/<customer_id>` | **Updates** an existing customer identified by its MongoDB `_id` (`customer_id`). Expects a JSON payload with the fields to be updated. |
| **DELETE**  | `/customers/<customer_id>` | **Deletes** a specific customer identified by its MongoDB `_id` (`customer_id`).                                                        |
| **GET**     | `/test`                    | Simple health-check endpoint used to verify that the service is running.                                                                |
