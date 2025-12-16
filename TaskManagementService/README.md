## 📋 Description

This microservice is part of the [microsystem network](https://github.com/Christian-Skovgaard/bilAbonnement) developed by Team SAFers as part of the EK ITA 3rd semester autumn exam 2025. The system stands as an MVP for a potential internal system for Bilabonnement.dk in an effort to make them more data driven and effective.

This is a simple RESTful API for managing tasks. The API is built with **Flask** and uses **MongoDB** to store task data. It allows for creating, reading, updating, and deleting tasks (CRUD operations).

## ❓ How to Use

This service is expected to run as part of a bigger service. To learn more about how to get the service running, check out the README at the [Bilabonnement repository](https://github.com/Christian-Skovgaard/bilAbonnement).

### 💬 API Endpoints

The service exposes a RESTful API to manage tasks stored in the MongoDB database. All endpoints are prefixed with the base path (e.g., `http://task-management-service:5010`).

## API Endpoints

| HTTP Method | Endpoint                         | Description                                                                                                                     |
| :---------- | :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| **GET**     | `/tasks`                         | Retrieves a list of **all** tasks currently in the database.                                                                    |
| **GET**     | `/tasks/department/<department>` | Retrieves tasks assigned to a specific **department** (e.g., Reception, Inspection, Salesmen).                                  |
| **POST**    | `/tasks`                         | Creates and inserts a **new** task into the database. Expects a JSON payload.                                                   |
| **PUT**     | `/tasks/<task_id>/status`        | **Updates** the status of an existing task identified by its MongoDB `_id` (`task_id`). Expects a JSON payload with `status`.   |
| **PUT**     | `/tasks/<task_id>`               | **Updates** an existing task identified by its MongoDB `_id` (`task_id`). Expects a JSON payload with the fields to be updated. |
| **DELETE**  | `/tasks/<task_id>`               | **Deletes** a specific task identified by its MongoDB `_id` (`task_id`).                                                        |

## 🔐 Access Control

Currently, access control is managed on the frontend. The following is a list of actions only allowed by a specific role:
| Role | HTTP Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| admin | **DELETE** | `/tasks/<task_id>` | Only admins are allowed to delete tasks.

## 🪳 Known Issues

- Access control shouldn't happen on frontend.
- Sensitive information is sent in clear text.
