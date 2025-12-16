# Customer Support Service

## 📋 Description

This microservice is part of the [microsystem network](https://github.com/Christian-Skovgaard/bilAbonnement) developed by Team SAFers as part of the EK ITA 3rd semester autumn exam 2025. The system stands as an MVP for a potential internal system for Bilabonnement.dk in an effort to make them more data driven and effective.

This is a simple RESTful API for managing customer complaints. The API is built with **Flask** and uses **MongoDB** to store complaint data. It allows for creating, reading, updating, and deleting complaints (CRUD operations).

## ❓ How to Use

This service is expected to run as part of a bigger service. To learn more about how to get the service running, check out the README at the [Bilabonnement repository](https://github.com/Christian-Skovgaard/bilAbonnement).

### 💬 API Endpoints

The service exposes a RESTful API to manage damage cases stored in the MongoDB database. All endpoints are prefixed with the base path (e.g., `http://customer-support-service:5003`).

## API Endpoints

| HTTP Method | Endpoint                     | Description                                                                                                                               |
| :---------- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **GET**     | `/complaints`                | Retrieves a list of **all** complaints currently in the database.                                                                         |
| **GET**     | `/complaints/query`          | Retrieves complaints based on optional **query parameters** for advanced filtering. Supports strings, numbers, and boolean values.        |
| **POST**    | `/complaints`                | Creates and inserts a **new** complaint into the database. Expects a JSON payload.                                                        |
| **PUT**     | `/complaints/<complaint_id>` | **Updates** an existing complaint identified by its MongoDB `_id` (`complaint_id`). Expects a JSON payload with the fields to be updated. |
| **DELETE**  | `/complaints/<complaint_id>` | **Deletes** a specific complaint identified by its MongoDB `_id` (`complaint_id`).                                                        |

## 🔐 Access Control

Currently, access control is managed on the frontend. The following is a list of actions only allowed by a specific role:
| Role | HTTP Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| admin | **DELETE** | `/cases/<complaint_id>` | Only admins are allowed to delete complaints.

## 🪳 Known Issues

- Access control shouldn't happen on frontend.
- Sensitive information is sent in clear text.
