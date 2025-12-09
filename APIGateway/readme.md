# API gateway

  

## 📋 Description

This microservice is part of the [microsystem network](https://github.com/Christian-Skovgaard/bilAbonnement) developed by Team SAFers as part of the EK ITA 3rd semester autumn exam 2025. The system stands as an MVP for a potential internal system for Bilabonnement.dk in an effort to make them more data driven and effective.

The purpose of this service is to act as a gateway for all traffic to, from and within the network. 
It works as a directory by keeping track of service locations and names, it also validates all traffic coming through using  their JWT authorization.

## ❓ How to Use

The gateway can be acces from everywhere and will route you to the desired service by providing the name of the service as the first path in the url. After providing the service name you can use the endpoints exposed by the service as usual. (see relevant documentation on each service)
example: `http://localhost:5001/customer-management-service/cars`

All traffic through the gateway requires a valid JWT with one exeption.
The gateway allows for the users to directly query the authorization-service on the endpoint "getAuthToken" without requiring a JWT. (see documentation on the authorization-service for details)
use: `http://localhost:5001/getAuthToken`

## ☎️ Available services

| Service | Path |
|---------|----------|----------|
| Car catalog service | car-catalog-service |
| Customer support service | customer-support-service |
| Authorization service | authorization-service |
| Damage registration service | damage-registration-service |
| Subscription management service | subscription-management-service |
| Customer management service | customer-management-service |
| Task management service | task-management-service |


This service is expected to run as part of a bigger service. To learn more about how to get the service running, check out the README at the [Bilabonnement repository](https://github.com/Christian-Skovgaard/bilAbonnement).

