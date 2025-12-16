# Subscription Management Service


## 📋 Description

This microservice is part of the [microsystem network](https://github.com/Christian-Skovgaard/bilAbonnement) developed by Team SAFers as part of the EK ITA 3rd semester autumn exam 2025. The system stands as an MVP for a potential internal system for Bilabonnement.dk in an effort to make them more data driven and effective.

The purpose of this service is to manage subscriptions for cars in Bilabonnement.dk's system. 
The service is equipped to handle event both at the beginning and end of a subscriptions lifecycle, but the functionality has not been implemented.
  

## ❓ How to Use

This service is expected to run as part of a bigger service. To learn more about how to get the service running, check out the README at the [Bilabonnement repository](https://github.com/Christian-Skovgaard/bilAbonnement).

  

### 💬 API Endpoints

The service exposes a RESTful API to manage subscriptions stored in the MongoDB database. All endpoints are prefixed with the base path (e.g., `http://car-catalog-service:5002`).

  

| HTTP Method | Endpoint | Description |

| :--- | :--- | :--- |

| **GET** | `/subscriptions` | Retrieves a list of **all** subscriptions currently in the database. |

| **GET** | `/subscriptions/query` | Retrieves **all** subscriptions associated with a specific set of query parameters. |

| **POST** | `/subscriptions` | Creates and inserts a **new** subscription into the database. Expects a JSON payload. |

| **PUT** | `/subscriptions/<regNr>` | **Updates** an existing subscription identified by registration number (`regNr`). Expects a JSON payload with the fields to be updated. |

| **DELETE** | `/subscriptions/<regNr>` | **Deletes** a specific subscription identified by its registration number (`regNr`). |

  

#### 🔍 Advanced Filtering (GET `/subscriptions/query`)

  

The query endpoint allows for flexible filtering of subscriptions for a given vehicle registration number. You can pass additional search criteria as **query parameters** in the URL.


* **Behavior:** The search uses a **case-insensitive** regular expression (`$regex` with `$options: "i"`) to find matches in the specified fields.

* **Example:** To find subscriptions that belong to people named Liam, you would include firstName=Liam


    `/subscriptions/query?firstName=Liam`


## 🪳 Known Issues

* Timebased events har not implemented
