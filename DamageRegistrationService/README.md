# Damage Registration Service

## 📋 Description
This microservice is part of the [microsystem network](https://github.com/Christian-Skovgaard/bilAbonnement) developed by Team SAFers as part of the EK ITA 3rd semester autumn exam 2025. The system stands as an MVP for a potential internal system for Bilabonnement.dk in an effort to make them more data driven and effective.

The purpose of this service is to view, create, edit, and delete damage reports of a given registration number of an arbitrary car in the Bilabonnement.dk system.

## ❓ How to Use
This service is expected to run as part of a bigger service. To learn more about how to get the service running, check out the README at the [Bilabonnement repository](https://github.com/Christian-Skovgaard/bilAbonnement).

### 💬 API Endpoints
The service exposes a RESTful API to manage damage cases stored in the MongoDB database. All endpoints are prefixed with the base path (e.g., `http://damage-registration-service:5005`).

| HTTP Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/cases` | Retrieves a list of **all** damage cases currently in the database. |
| **GET** | `/cases/<regnr>` | Retrieves **all** damage cases associated with a specific vehicle registration number (`regnr`). |
| **GET** | `/cases/<regnr>/query` | Retrieves damage cases for a specific vehicle registration number (`regnr`), supporting optional **query parameters** for advanced filtering. |
| **POST** | `/cases/<regNr>` | Creates and inserts a **new** damage case into the database. The vehicle's registration number is taken from the URL path. Expects a JSON payload. |
| **PUT** | `/cases/<caseId>` | **Updates** an existing damage case identified by its MongoDB `_id` (`caseId`). Expects a JSON payload with the fields to be updated. |
| **DELETE** | `/cases/<caseId>` | **Deletes** a specific damage case identified by its MongoDB `_id` (`caseId`). |

#### 🔍 Advanced Filtering (GET `/cases/<regnr>/query`)

The query endpoint allows for flexible filtering of damage cases for a given vehicle registration number. You can pass additional search criteria as **query parameters** in the URL.

* **Behavior:** The search uses a **case-insensitive** regular expression (`$regex` with `$options: "i"`) to find matches in the specified fields.
* **Example:** To find cases for `regnr=AB12345` where the damage description contains the word "scratch" (case-insensitive):

    ```
    /cases/AB12345/query?description=scratch
    ```

## 🔐 Access Control
Currently, access control is managed on the frontend. The following is a list of actions only allowed by a specific role:
| Role | HTTP Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| admin | **DELETE** | `/cases/<caseId>` | Only admins are allowed to delete damage reports.

## 🪳 Known Issues
* Access control shouldn't happen on frontend.
* Sensitive information is sent in clear text.
