import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests
# import subscriptionDataUtil as dataUtil

controller = CookieController()

st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

# we defy session state!
def defSessionState(): # har lavet i funtion så jeg kan lukke den så den ikke fylder, har ikke noget praktisk formål
    if "filteractive" not in st.session_state:
        st.session_state.filteractive = True
    if "filterfirstName" not in st.session_state:
        st.session_state.filterfirstName = ""
    if "filterlastName" not in st.session_state:
        st.session_state.filterlastName = ""
    if "filterBrand" not in st.session_state:
        st.session_state.filterBrand = ""
    if "filterModel" not in st.session_state:
        st.session_state.filterModel = ""
    if "filterregNr" not in st.session_state:
        st.session_state.filterregNr = ""
    if "filterpickupLocation" not in st.session_state:
        st.session_state.filterpickupLocation = ""
    if "filtersubscriptionId" not in st.session_state:
        st.session_state.filtersubscriptionId = ""
    

    #create
    if "createNewUser" not in st.session_state:
        st.session_state.createNewUser = "Opret ny bruger"
    
    if "createNewUserFName" not in st.session_state:
        st.session_state.createNewUserFName = ""
    if "createNewUserLName" not in st.session_state:
        st.session_state.createNewUserLName = ""
    if "createNewUserAge" not in st.session_state:
        st.session_state.createNewUserAge = ""
    if "createNewUserDriversLicense" not in st.session_state:
        st.session_state.createNewUserDriversLicense = ""
    
    if "createExistingUserId" not in st.session_state:
        st.session_state.createExistingUserId = ""
    
    if "createDateStart" not in st.session_state:
        st.session_state.createDateStart = ""
    if "createDateEnd" not in st.session_state:
        st.session_state.createDateEnd = ""
    if "createCarRegNr" not in st.session_state:
        st.session_state.createCarRegNr = ""
    if "createPricePrMonth" not in st.session_state:
        st.session_state.createPricePrMonth = ""
    if "createLocation" not in st.session_state:
        st.session_state.createLocation = ""

    if "statusMsg" not in st.session_state:
        st.session_state.statusMsg = ""

    # update
    if "updateId" not in st.session_state:
        st.session_state.updateId = ""
    if "updateActive" not in st.session_state:
        st.session_state.updateActive = ""
    if "updateCustommerId" not in st.session_state:
        st.session_state.updateCustommerId = ""
    if "updateRegNr" not in st.session_state:
        st.session_state.updateRegNr = ""
    if "updatePricePrMonth" not in st.session_state:
        st.session_state.updatePricePrMonth = ""
    if "updatePickupLocation" not in st.session_state:
        st.session_state.updatePickupLocation = ""
    if "updateStartDate" not in st.session_state:
        st.session_state.updateStartDate = ""
    if "updateEndDate" not in st.session_state:
        st.session_state.updateEndDate = ""

defSessionState()

def onCreateClick():
    displayObj = {}
    userId = None

    if st.session_state["createNewUser"] == "Opret ny bruger":
        customerResp = requests.request(
            method="POST",
            url="http://gateway:5001/customer-management-service/customers",
            headers={
                "Authorization": controller.get("Authorization"),
                "Content-Type": "application/json"
            },
            json={
                "age": st.session_state["createNewUserAge"],
	            "driversLicense": st.session_state["createNewUserDriversLicense"],
                "firstName": st.session_state["createNewUserFName"],
                "lastName": st.session_state["createNewUserLName"]
            }
        )
        customerJson = customerResp.json()
        userId = customerJson["_id"]
    else:
        userId = st.session_state["createExistingUserId"]

    resp = requests.request(
        method="POST",
        url="http://gateway:5001/subscription-management-service/subscriptions",
        headers={
            "Authorization": controller.get("Authorization"),
            "Content-Type": "application/json"
            },
        json={
            "startDate":st.session_state.createDateStart,
            "endDate":st.session_state.createDateEnd,
            "pickupLocation":st.session_state.createLocation,
            "associatedCustomerId":userId,
            "associatedRegNr":st.session_state.createCarRegNr,
            "pricePrMonth":int(st.session_state.createPricePrMonth)
        }
    )
    jsonResp = resp.json()
    print(jsonResp)
    if jsonResp.get("error"):
        st.session_state["statusMsg"] = jsonResp.get("error")
    else:
        st.session_state["statusMsg"] = jsonResp.get("msg")
    
def onUpdateClick():
    #make req body
    body = {
        "active": st.session_state["updateActive"],
        "associatedCustomerId": st.session_state["updateCustommerId"],
        "associatedRegNr": st.session_state["updateRegNr"],
        "pricePrMonth": st.session_state["updatePricePrMonth"],
        "pickupLocation": st.session_state["updatePickupLocation"],
        "startDate": st.session_state["updateStartDate"],
        "endDate": st.session_state["updateEndDate"],
    }

    url = f"http://localhost:5001/subscription-management-service/subscriptions/{st.session_state['updateId']}"

    resp = requests.request(
        method="PUT",
        url=url,
        json=body,
        headers={"Authorization": controller.get("Authorization")}
    )
    jsonResp = resp.json()

    if jsonResp.get("error"):
        st.session_state["statusMsg"] = jsonResp.get("error")
    else:
        st.session_state["statusMsg"] = jsonResp.get("message")

def onUpdateIdChange():
    subId = st.session_state.updateId

    resp = requests.request(
        method="GET",
        url=f"http://gateway:5001/subscription-management-service/subscriptions/{subId}",
        headers={"Authorization": controller.get("Authorization")}
    )
    json = resp.json()

    if json.get("error"):
        st.session_state["statusMsg"] = json["error"]
    else:
        st.session_state["updateActive"] = json["active"]
        st.session_state["updateCustommerId"] = json["associatedCustomerId"]
        st.session_state["updateRegNr"] = json["associatedRegNr"]
        st.session_state["updatePricePrMonth"] = str(json["pricePrMonth"]) # det er et tal, 
        st.session_state["updatePickupLocation"] = json["pickupLocation"]
        st.session_state["updateStartDate"] = json["startDate"]
        st.session_state["updateEndDate"] = json["endDate"]            

# kæmpe rod af funktioner, brude ryde op hvis jeg for tid, men har prøvet at give dem gode navne
# det her sker: 
#   Vi henter alt data fra 3 kilder: subsciptions, cars og customers
#   Vi "joiner" alt sammen på subscription-listen så vi for alle relevate info ved at matche "keys" med deres referance i subscription (ligesom joins i sql)
#   Vi lægge den "master-liste" i et panda dataframe
#   Nu laver vi et filterDict baseret på brugerInput og defaults (vi tager bare værdierne af inputfelterne hvis der er skrevet noget)
#   Nu filtere vi dataframet baseret på vores filterDict, det gør vi ved at gå igennem og matche values, og hvis match er mask=True (mask er en value for en row i et df som virker lidt ligesom "display", og det hele er formateret i et "pdSeries" som er sådan lidt ligesom en liste som har værdierne "index" og "mask")
#   Det filtrerede df bliver nu vist:D

def getData (): 
    # denne funktion bliver ikke brugt mere pga problemer med cookiecontroler og funktioner (kan slettes)
    subResp = requests.request(
        method="GET",
        url="http://gateway:5001/subscription-management-service/subscriptions",
        headers={"Authorization": controller.get("Authorization")},
    )
    subJson = subResp.json()

    customerResp = requests.request(
        method="GET",
        url="http://gateway:5001/customer-management-service/customers",
        headers={"Authorization": controller.get("Authorization")},
    )
    customerJson = customerResp.json()
    
    carResp = requests.request(
        method="GET",
        url="http://gateway:5001/car-catalog-service/cars",
        headers={"Authorization": controller.get("Authorization")},
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
                result.append(combined)
                matched = True

        if not matched:
            result.append(d1.copy())

    return result

def renameKey(list_of_dicts, old_key, new_key):
    new_list = []
    for d in list_of_dicts:
        if old_key in d:
            d[new_key] = d.pop(old_key)
        new_list.append(d)
    return new_list

def getFormattedData (unformatedData):    # kombinerer alle vores tre lists til en baseret på subscriptions
    #unformatedData = getData()
    subCar = joinLists(
        unformatedData["subList"],
        unformatedData["carList"],
        "associatedRegNr",
        "regNr"
        )
    formatedSubCar = renameKey(subCar,"_id","subscriptionId")
    subCarCustomer = joinLists(
        formatedSubCar,
        unformatedData["customerList"],
        "associatedCustomerId",
        "_id"
        )
    formatedSubCarCustomer = renameKey(subCarCustomer,"_id","customer Id")
    return formatedSubCarCustomer

def extract_filters(sessionStateDict): # her henter vi brugerfiltrene fra sessionstate
    result = {}
    for key, value in sessionStateDict.items():
        if key.startswith("filter") and value:  # de hedder alle sammen de rigtige keys, men skal have fjernet "filter"
            # Remove 'filter' prefix
            new_key = key[len("filter"):] if key != "filter" else ""
            if new_key:  # Only add if new_key is not empty
                result[new_key] = value
    return result

def filter_dataframe(df, filter_dict):
    mask = pd.Series(True, index=df.index)  # de to argumenter er de to "kulonner" i serien, en af dem er index og den anden er altid true (så der er to værdier, true og index i serien)
    for key, value in filter_dict.items():        
        mask &= (df[key] == value)  # &= betyder "and equal to", så den tjekker bare begge conditions, i det her tilfælde er mask enten true eller false
    return df[mask] #her aplyer vi bare maskSerisen til df, ligesom vi senere tilføjer column listen:D


subResp = requests.request(
        method="GET",
        url="http://gateway:5001/subscription-management-service/subscriptions",
        headers={"Authorization": controller.get("Authorization")},
    )
subJson = subResp.json()

customerResp = requests.request(
        method="GET",
        url="http://gateway:5001/customer-management-service/customers",
        headers={"Authorization": controller.get("Authorization")},
    )
customerJson = customerResp.json()
    
carResp = requests.request(
        method="GET",
        url="http://gateway:5001/car-catalog-service/cars",
        headers={"Authorization": controller.get("Authorization")},
    )
carJson = carResp.json()

rawData =  {
        "subList":subJson,
        "customerList":customerJson,
        "carList":carJson
    }


data = getFormattedData(rawData)

df = pd.DataFrame(data)

filter = extract_filters(st.session_state)

filterdDF = filter_dataframe(df,filter)

filterdDF = filterdDF[["active","startDate","endDate","firstName","lastName","brand","model","regNr","pricePrMonth","insuranceDealNr","pickupLocation","orderDate","customer Id","subscriptionId"]]


col1, col2 = st.columns([5,1], vertical_alignment="center")
with col1:
    st.header("Bilabonnement")

user = st.session_state.get("username", "Guest")
if user == "Guest":
    st.switch_page("login.py")

with col2:
    st.subheader(f"Hej {user}!")
    if st.button(label="Log ud"):
        if "Authorization" in controller.getAll(): # KUN RELEVANT FOR TESTING OG BUG FIXING
            controller.remove("Authorization")
        if "JWT" in controller.getAll(): # KUN RELEVANT FOR TESTING OG BUG FIXING
            controller.remove("JWT")
        st.switch_page("login.py")

with st.container(border=True):
    carsPageBtn, damageRegiBtn, tasksBtn, subscriptionsBtn, customerSuppBtn = st.columns(5)
    with carsPageBtn:
        if st.button(label="Biler"):
            st.switch_page("pages/cars.py")

    with damageRegiBtn:
        if st.button(label="Skader"):
            if "damageRegNr" in st.session_state:
                del st.session_state["damageRegNr"]
            if "damageDetails" in st.session_state:
                del st.session_state["damageDetails"] # Slet session state fra damage-registration hvis de findes.
            st.switch_page("pages/damages.py")

    with tasksBtn:
        if st.button(label="Opgaver"):
            st.switch_page("pages/tasks.py")

    with subscriptionsBtn:
        if st.button(label="Abonnementer", type="primary"):
            st.query_params = {}
            st.rerun()

    with customerSuppBtn:
        if st.button(label="Kundeservice"):
            st.query_params = {}
            st.switch_page("pages/customersupport.py")


subLeft, subRight = st.columns([6,4])
with subLeft:
    st.subheader("Oversigt over Abonnetmenter")
    with st.container(border=True): # Dataframe opdateres ved hver ændring i text_input eller button presses.
        st.dataframe(filterdDF, hide_index=True)

with subRight:
    carRightTitle = st.subheader("Kontrolpanel")
    tab1, tab2, tab3 = st.tabs(["Søg og filtrér", "Opret abonnetment", "Opdater"])

    with tab1:
        with st.container(border=True): # filterer
            filteractive = st.checkbox(label="Kun aktive", key="filteractive", value=st.session_state.filteractive)
            
            filterRight, filterLeft = st.columns(2)
            with filterRight:
                filterfirstName = st.text_input(label="Fornavn", key="filterfirstName")
                filterBrand = st.text_input(label="Bilmærke", key="filterBrand")
                filterregNr = st.text_input(label="Reg Nr", key="filterregNr")
            with filterLeft:
                filterlastName = st.text_input(label="Efternavn", key="filterlastName")
                filterModel = st.text_input(label="Model", key="filterPropellant")
                filterpickupLocation = st.selectbox(label="Afhentnings sted", options=("","Aarhus", "Kolding", "København"), key="filterpickupLocation")
            filtersubscriptionId = st.text_input(label="Subscription ID", key="filtersubscriptionId")

            

    with tab2:
        with st.container(border=True):
            createNewUser = st.selectbox(label="Ny bruger?", options=("Opret ny bruger", "Eksisterende bruger"), key="createNewUser")

            if st.session_state.createNewUser == "Opret ny bruger":
                fName, lName = st.columns(2)
                with fName:
                    createNewUserFName = st.text_input(label="fornavn",key="createNewUserFName")
                with lName: 
                    createNewUserLName = st.text_input(label="efternavn",key="createNewUserLName")
                createNewUserAge = st.text_input(label="age",key="createNewUserAge")
                createNewUserDriversLicense = st.text_input(label="kørekortsnummer",key="createNewUserDriversLicense")
            else:
                createExistingUserId = st.text_input(label="bruger Id", key="createExistingUserId")
            
            createRight, createLeft = st.columns(2)
            with createRight:
                createStartDate = st.text_input(label="start dato", placeholder="yyyy-mm-dd", key="createDateStart")
                createCarRegNr = st.text_input(label="registreringsnummer",key="createCarRegNr")
            with createLeft:
                createEndDate = st.text_input(label="start dato", placeholder="yyyy-mm-dd", key="createDateEnd")
                createPricePrMonth = st.text_input(label="aftalt pris pr måned",key="createPricePrMonth")

            createLocation = st.selectbox(label="Afhentnings sted", options=("","Aarhus", "Kolding", "København"), key="createLocation")
            
            

            st.button(label="opret!",on_click=onCreateClick)

    with tab3:
        updateId = st.text_input(label="Subscription Id", key="updateId", value=st.session_state.updateId, on_change=onUpdateIdChange)

        if st.session_state.updateId != "":

            updateActive = st.checkbox(label="aktiv", key="updateActive", value=st.session_state.updateActive)

            updateLeft, updateRight = st.columns(2)
            with updateLeft:
                updateCustommerId = st.text_input(label="Subscription Id", key="updateCustommerId", value=st.session_state.updateCustommerId)
                updatePricePrMonth = st.text_input(label="updatePricePrMonth", key="updatePricePrMonth", value=st.session_state.updatePricePrMonth)
                updateStartDate = st.text_input(label="updateStartDate", key="updateStartDate", value=st.session_state.updateStartDate)
            with updateRight:
                updateRegNr = st.text_input(label="updateRegNr", key="updateRegNr", value=st.session_state.updateRegNr)
                updatePickupLocation = st.text_input(label="updatePickupLocation", key="updatePickupLocation", value=st.session_state.updatePickupLocation)
                updateEndDate = st.text_input(label="updateEndDate", key="updateEndDate", value=st.session_state.updateEndDate)

        st.button(label="update!",on_click=onUpdateClick)


    if st.session_state["statusMsg"] != "":
        st.write(st.session_state["statusMsg"])
