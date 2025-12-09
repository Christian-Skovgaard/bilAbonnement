# Car Catalog Service

## 📋 Description
This microservice is part of the [microsystem network](https://github.com/Christian-Skovgaard/bilAbonnement) developed by Team SAFers as part of the EK ITA 3rd semester autumn exam 2025. The system stands as an MVP for a potential internal system for Bilabonnement.dk in an effort to make them more data driven and effective.

The purpose of this service is to view, create, edit, and delete cars of a given registration number in the Bilabonnement.dk system.

## ❓ How to Use
This service is expected to run as part of a bigger service. To learn more about how to get the service running, check out the README at the [Bilabonnement repository](https://github.com/Christian-Skovgaard/bilAbonnement).

### 💬 API Endpoints
The service exposes a RESTful API to manage cars stored in the MongoDB database. All endpoints are prefixed with the base path (e.g., `http://car-catalog-service:5002`).

| HTTP Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/cars` | Retrieves a list of **all** cars currently in the database. |
| **GET** | `/cars/query` | Retrieves **all** cars associated with a specific set of query parameters. |
| **POST** | `/cars` | Creates and inserts a **new** car into the database. Expects a JSON payload. |
| **PUT** | `/cars/<regNr>` | **Updates** an existing car identified by registration number (`regNr`). Expects a JSON payload with the fields to be updated. |
| **DELETE** | `/cars/<regNr>` | **Deletes** a specific car identified by its registration number (`regNr`). |

#### 🔍 Advanced Filtering (GET `/cases/query`)

The query endpoint allows for flexible filtering of cars for a given vehicle registration number. You can pass additional search criteria as **query parameters** in the URL.

* **Behavior:** The search uses a **case-insensitive** regular expression (`$regex` with `$options: "i"`) to find matches in the specified fields.
* **Example:** To find cars for `regnr=AB12345` where the cars kilometercounter is between 25.000km and 50.000km and car model contains the word "accord" (case-insensitive):

    ```
    /cars/query?regNr=AB12345&minKm=25000maxKm=50000&model=accord
    ```

## 🔐 Access Control
Currently, access control is managed on the frontend. The following is a list of actions only allowed by a specific role:
| Role | HTTP Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| admin | **DELETE** | `/car/<regNr>` | Only admins are allowed to delete cars.

## 🪳 Known Issues
* Access control shouldn't happen on frontend.
* Sensitive information is sent in clear text.