import requests

def getAuthToken():
    return "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2NDg4OTE4MSwianRpIjoiNDE2MGQwODQtYzI4Yy00NmVlLWI0MmItMDlkYzQ3N2ZhZDNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkJvIiwibmJmIjoxNzY0ODg5MTgxLCJjc3JmIjoiODJiYzVkZDItZmVjOC00NGNiLWFkOTQtZDI3NThjZGE3ZmU1IiwiZXhwIjoxNzcwMDczMTgxLCJyb2xlIjoiYWRtaW4iLCJkZXBhcnRtZW50IjoiS29saW5nIn0.ervCIhnk4iyzZNB4DpuU4IvrtMttntWcdcrvytnUrfauFuGqvPm6_nqH0Ps45gCqhCIUI3YUQti7jk3JTiLsA4L8RFhYOdaFv6LrYjACHINtl6Q1XO5IJTlSAGsuWc3EiWrvpHRfUvDB5-8n6xRNa5qEdwEToZofjcvYrxCuWsZ067rNYVumWR6e9oAOc7IUFHcC_L1vYGwti2SbB8XJAxxkdJc3Zr8YTOD9EBscal1pOOdznRHR4pS3QUUDIpJJxBssINq1wClaS9_8zPYhTW4eMgeq3NDVoqtwaW7y7cwG5BXNIhyicRGD-WD33oAklHr2Ess8wfNrmSs-Ozp-WA"

def getData ():

    subResp = requests.request(
        method="GET",
        url="http://localhost:5001/subscription-management-service/subscriptions",
        headers={"Authorization": getAuthToken()},
    )
    subJson = subResp.json()

    customerResp = requests.request(
        method="GET",
        url="http://localhost:5001/customer-management-service/customers",
        headers={"Authorization": getAuthToken()},
    )
    customerJson = customerResp.json()
    
    carResp = requests.request(
        method="GET",
        url="http://localhost:5001/car-catalog-service/cars",
        headers={"Authorization": getAuthToken()},
    )
    carJson = carResp.json()

    return {
        "subList":subJson,
        "customerList":customerJson,
        "carList":carJson
    }

def joinLists(db1, db2, key1, key2):
    result = []
    for d1 in db1:
        matched = False

        for d2 in db2:
            if d1.get(key1) == d2.get(key2):
                combined = {**d1, **d2}
                combined.pop(key1, None)
                combined.pop(key2, None)
                result.append(combined)
                matched = True

        # If nothing matched in db2, still output d1
        if not matched:
            result.append(d1.copy())

    return result


def getFormattedData ():
    unformatedData = getData()
    subCar = joinLists(
        unformatedData["subList"],
        unformatedData["carList"],
        "associatedRegNr",
        "regNr"
        )
    return subCar


print(getData()["customerList"])

