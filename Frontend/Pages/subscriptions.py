import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

controller = CookieController()

st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

# we defy session state!
def defSessionState(): # har lavet i funtion så jeg kan lukke den så den ikke fylder, har ikke noget praktisk formål
    if "filterActive" not in st.session_state:
        st.session_state.filterActive = ""
    if "filterName" not in st.session_state:
        st.session_state.filterName = ""
    if "filterBrand" not in st.session_state:
        st.session_state.filterBrand = ""
    if "filterModel" not in st.session_state:
        st.session_state.filterModel = ""
    if "filterLocation" not in st.session_state:
        st.session_state.filterLocation = ""
    

    #create
    if "createNewUser" not in st.session_state:
        st.session_state.createNewUser = "Opret ny bruger"
    if "createNewUserFName" not in st.session_state:
        st.session_state.createNewUserFName = ""
    if "createNewUserFName" not in st.session_state:
        st.session_state.createNewUserFName = ""
    if "createNewUserAge" not in st.session_state:
        st.session_state.createNewUserAge = ""
    if "createNewUserAge" not in st.session_state:
        st.session_state.createNewUserAge = ""
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

    if "createMsg" not in st.session_state:
        st.session_state.createMsg = ""
defSessionState()

def getAuthToken():
    return "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2NDg4OTE4MSwianRpIjoiNDE2MGQwODQtYzI4Yy00NmVlLWI0MmItMDlkYzQ3N2ZhZDNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkJvIiwibmJmIjoxNzY0ODg5MTgxLCJjc3JmIjoiODJiYzVkZDItZmVjOC00NGNiLWFkOTQtZDI3NThjZGE3ZmU1IiwiZXhwIjoxNzcwMDczMTgxLCJyb2xlIjoiYWRtaW4iLCJkZXBhcnRtZW50IjoiS29saW5nIn0.ervCIhnk4iyzZNB4DpuU4IvrtMttntWcdcrvytnUrfauFuGqvPm6_nqH0Ps45gCqhCIUI3YUQti7jk3JTiLsA4L8RFhYOdaFv6LrYjACHINtl6Q1XO5IJTlSAGsuWc3EiWrvpHRfUvDB5-8n6xRNa5qEdwEToZofjcvYrxCuWsZ067rNYVumWR6e9oAOc7IUFHcC_L1vYGwti2SbB8XJAxxkdJc3Zr8YTOD9EBscal1pOOdznRHR4pS3QUUDIpJJxBssINq1wClaS9_8zPYhTW4eMgeq3NDVoqtwaW7y7cwG5BXNIhyicRGD-WD33oAklHr2Ess8wfNrmSs-Ozp-WA"

def onCreateClick():
    displayObj = {}
    userId = None

    if st.session_state["createNewUser"] == "Opret ny bruger":
        customerResp = requests.request(
            method="POST",
            url="http://localhost:5001/customer-management-service/customers",
            headers={
                "Authorization": getAuthToken(),
                "Content-Type": "application/json"
            },
            json={
                
            }
        )
        customerJson = customerResp.json()
        userId = customerJson["_id"]
    else:
        userId = st.session_state["createExistingUserId"]

    

    resp = requests.request(
        method="POST",
        url="http://localhost:5001/subscription-management-service/subscriptions",
        headers={
            "Authorization": getAuthToken(),
            "Content-Type": "application/json"
            },
        json={
            "startDate":st.session_state.createDateStart,
            "endDate":st.session_state.createDateEnd,
            "pickupLocation":st.session_state.createLocation,
            "associatedCustommerId":userId,
            "associatedRegNr":st.session_state.createCarRegNr,
            "pricePrMonth":st.session_state.createPricePrMonth
        }
    )
    jsonResp = resp.json()
    st.session_state["createMsg"]["msg"] = jsonResp
    

# get data
resp = requests.request(
    method="GET",
    url="http://localhost:5001/subscription-management-service/subscriptions/query",
    headers={"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2NDg4OTE4MSwianRpIjoiNDE2MGQwODQtYzI4Yy00NmVlLWI0MmItMDlkYzQ3N2ZhZDNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkJvIiwibmJmIjoxNzY0ODg5MTgxLCJjc3JmIjoiODJiYzVkZDItZmVjOC00NGNiLWFkOTQtZDI3NThjZGE3ZmU1IiwiZXhwIjoxNzcwMDczMTgxLCJyb2xlIjoiYWRtaW4iLCJkZXBhcnRtZW50IjoiS29saW5nIn0.ervCIhnk4iyzZNB4DpuU4IvrtMttntWcdcrvytnUrfauFuGqvPm6_nqH0Ps45gCqhCIUI3YUQti7jk3JTiLsA4L8RFhYOdaFv6LrYjACHINtl6Q1XO5IJTlSAGsuWc3EiWrvpHRfUvDB5-8n6xRNa5qEdwEToZofjcvYrxCuWsZ067rNYVumWR6e9oAOc7IUFHcC_L1vYGwti2SbB8XJAxxkdJc3Zr8YTOD9EBscal1pOOdznRHR4pS3QUUDIpJJxBssINq1wClaS9_8zPYhTW4eMgeq3NDVoqtwaW7y7cwG5BXNIhyicRGD-WD33oAklHr2Ess8wfNrmSs-Ozp-WA"},
    params={
        "associatedCustommerId":st.session_state["filterName"],
        "associatedRegNr":st.session_state["filterBrand"],
        "pickupLocation":st.session_state["filterLocation"]
        }
)
json = resp.json()
df = pd.DataFrame(json)

def joinLists(db1, db2, key1, key2):
    result = []
    for d1 in db1:
        for d2 in db2:
            if d1[key1] == d2[key2]:
                # Combine dictionaries, excluding the matching keys
                combined = {**d1, **d2}
                combined.pop(key1, None)
                combined.pop(key2, None)
                result.append(combined)
    return result




col1, col2 = st.columns([5,1], vertical_alignment="center")
with col1:
    st.header("Bilabonnement")

with col2:
    st.subheader("Hej Victor!")
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
            st.switch_page("pages/customersupport.py")


subLeft, subRight = st.columns([6,4])
with subLeft:
    st.subheader("Oversigt over Abonnetmenter")
    with st.container(border=True): # Dataframe opdateres ved hver ændring i text_input eller button presses.
        st.dataframe(df, hide_index=True)

with subRight:
    carRightTitle = st.subheader("Kontrolpanel")
    tab1, tab2, tab3 = st.tabs(["Søg og filtrér", "Opret abonnetment", "Opdater"])

    with tab1:
        with st.container(border=True): # filterer
            filterActive = st.checkbox(label="Kun aktive", key="filterAktive", value=True)

            filterName = st.text_input(label="Navn", placeholder="id", key="filterName")
            
            brand, model = st.columns(2)
            with brand:
                filterBrand = st.text_input(label="Bilmærke", placeholder="temp reg nr", key="filterBrand")
            with model:
                filterModel = st.text_input(label="Model", key="filterPropellant")

            filterLocation = st.text_input(label="lokation", key="filterLocation")

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
                createStartDate = st.text_input(label="start dato", placeholder="yyyy-mm-dd", key="createStartDate")
                createCarRegNr = st.text_input(label="registreringsnummer",key="createCarRegNr")
            with createLeft:
                createEndDate = st.text_input(label="start dato", placeholder="yyyy-mm-dd", key="createEndDate")
                createPricePrMonth = st.text_input(label="aftalt pris pr måned",key="createPricePrMonth")

            createLocation = st.selectbox(label="Afhentnings sted", options=("","Aarhus", "Kolding", "København"), key="createLocation")
            
            

            st.button(label="opret!",on_click=onCreateClick)

    if st.session_state["createMsg"] != "":
        st.write(st.session_state["createMsg"])
