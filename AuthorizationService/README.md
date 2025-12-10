# Car Catalog Service

## 📋 Description
This microservice is part of the [microsystem network](https://github.com/Christian-Skovgaard/bilAbonnement) developed by Team SAFers as part of the EK ITA 3rd semester autumn exam 2025. The system stands as an MVP for a potential internal system for Bilabonnement.dk in an effort to make them more data driven and effective.

The purpose of this service is to authenticate users and issue JWT tokens that can be used query the gateway and gain acces to the rest of the system. It also exposes the public key used to verify these tokens by the gateway.

## ❓ How to Use
This service is expected to run as part of a bigger service. To learn more about how to get the service running, check out the README at the [Bilabonnement repository](https://github.com/Christian-Skovgaard/bilAbonnement).

### 💬 API Endpoints
The service exposes a RESTful API for authentication and key distribution. All endpoints are prefixed with the base path (e.g., 'http://auth-service:5004').

| HTTP Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/getAuthToken` | Authenticates a user with username and password (JSON payload). Returns a JWT access token with user role as claims. |
| **GET** | `/getPublicKey` | Returns the public key used to verify JWT tokens. |

## 🔐 JWT claims
JWT tokens issued contains:
* identity: the username of the user
* role: the user's role (e.g., "admin", "user")
* department: (e.g., "Aarhus","Copenhagen") this value can be NULL

## 🪳 Known Issues
* Passwords are currently stored in plain text.
* The service does not use any sort of rate limiting to protect against bruteforce attacks.