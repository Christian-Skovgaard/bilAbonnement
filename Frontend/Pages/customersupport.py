import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests
import jwt

# Data
cases = []

controller = CookieController()

try:
    claims = jwt.decode(
        controller.get("Authorization")[7:], # Fjern "bearer" fra cookie.
        options={"verify_signature": False},
        algorithms=["HS256"]
    )
except jwt.ExpiredSignatureError:
    print("Token is expired (even without verification, PyJWT checks 'exp' claim)")
except Exception as e:
    print(f"An error occurred during decoding: {e}")


# Logik
def queryParamsToString():
    if len(st.query_params.items()) != 0:
        queryString = ""
        for key, value in st.query_params.items():
            queryString += f"{key}={value}&"
        return queryString[0:len(queryString)-1] # Return query string and remove the last "&".
    else:
        return ""

def hasEmpty(list):
    for value in list:
        if value == "" or value == None:
            return True
    return False

def updateQueryParams(input, parameter):
    params = dict(st.query_params)

    if input is not None and input != "":
        params[parameter] = input
    else:
        params.pop(parameter, None)

    st.query_params = params

def removeEmptyFromDict(dict):
    result = {}
    for key, value in dict.items():
        if (value != "") and (value != None):
            result[key] = value
    return result



try:
    if len(st.query_params.items()) != 0: # Hvis der er query parameters
        response = requests.get(f"http://localhost:5001/customer-support-service/complaints/query?{queryParamsToString()}", headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"})
    else: # Hvis der ikke er query parameters
        response = requests.get("http://localhost:5001/customer-support-service/complaints", headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"})
    cases = response.json()
    dataframe = pd.DataFrame(cases)
    canConnect = True
except:
    if "Authorization" in controller.getAll():
        controller.remove("Authorization")
    if "JWT" in controller.getAll():
        controller.remove("JWT")
    st.switch_page("login.py")
    canConnect = False # Eksisterer kun, hvis der findes en bedre løsning til at håndtere, at car-catalog-service er nede (AuthToken er stadig valid).
    dataframe = [] # Brugeren skal ikke smides ud, bare fordi car-catalog-service ikke kører.


# Streamlit
st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

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
            st.switch_page("pages/damages.py")

    with tasksBtn:
        if st.button(label="Opgaver"):
            st.switch_page("pages/tasks.py")

    with subscriptionsBtn:
        if st.button(label="Abonnementer"):
            st.switch_page("pages/subscriptions.py")

    with customerSuppBtn:
        if st.button(label="Kundeservice", type="primary"):
            st.query_params = {}
            st.rerun()


customerSuppLeft, customerSuppRight = st.columns([6,4])
with customerSuppLeft:
    st.subheader("Oversigt over kundeservice")
    with st.container(border=True): # Dataframe opdateres ved hver ændring i text_input eller button presses.
        st.dataframe(dataframe, hide_index=True)
        

with customerSuppRight:
    customerSuppRightTitle = st.subheader("Kontrolpanel")
    tab1, tab2, tab3, tab4 = st.tabs(["Søg og filtrér sag", "Tilføj ny sag", "Opdater sag", "Slet sag"])

    with tab1:
        with st.container(border=True):
            filterComplaint = st.text_input(label="Klage", placeholder="Indtast din klage", key="filterComplaint")
            filterRegNr = st.text_input(label="Reg Nr.", placeholder="Indtast Reg Nr.", key="filterRegNr")
            filterDate = st.text_input(label="Dato", placeholder="Indtast dato", key="filterDate")
            filterName = st.text_input(label="Navn", placeholder="Indtast navn", key="filterName")
            filterAfsluttet = st.checkbox(label="Afsluttet", key="filterAfsluttet")





            anvendBtn, nulstilBtn = st.columns(2)
            with anvendBtn:
                if st.button(label="Anvend"):
                    updateQueryParams(filterComplaint, "complaint")
                    updateQueryParams(filterRegNr, "regNr")
                    updateQueryParams(filterDate, "date")
                    updateQueryParams(filterName, "name")
                    if filterAfsluttet:
                        st.query_params["completed"] = "true"
                    else:
                        st.query_params["completed"] = "false"
    
                    st.rerun()
            with nulstilBtn:
                if st.button(label="Nulstil"):
                    st.query_params = {}
                    st.rerun()


    with tab2: # Mangler access control via. roles
        with st.container(border=True):
            addComplaint = st.text_input(label="Klage", placeholder="Indtast din klage")
            addRegNr = st.text_input(label="Reg Nr.", placeholder="Indtast Reg Nr.")
            addDate = st.text_input(label="Dato", placeholder="Indtast dato")
            addName = st.text_input(label="Navn", placeholder="Indtast navn")
            addAfsluttet = st.checkbox(label="Afsluttet", key="addAfsluttet")
        ##
            if st.button(label="Tilføj", type="primary"):
                if hasEmpty([addComplaint, addDate, addName]): # Hvis et af felterne ikke er udfyldt.
                    st.write(f":red[Alle felter skal udfyldes]")
                else:
                    addResponse = requests.post("http://localhost:5001/customer-support-service/complaints", json={
                            "complaint": addComplaint,
                            "regNr": addRegNr,
                            "date": addDate,
                            "name": addName,
                            "completed": addAfsluttet
                        }, headers={"Authorization": controller.get("Authorization")})
                    if addResponse.status_code != 201:
                        st.write(f":red[Kunne ikke tilføje sagen]. Statuskode: {addResponse.status_code}")
                    else:
                        st.rerun()

    with tab3:
        with st.container(border=True): # Lorte streamlit. Løsningen virker, men kunne være meget federe.
            updateMongoId = st.text_input(label="Id", placeholder="Indtast Id", key="updateMongoId")


            updateComplaint = st.text_input(label="Klage", placeholder="Indtast klage", key="updateComplaint")
            updateRegNr = st.text_input(label="Reg Nr.", placeholder="Indtast Reg Nr.", key="updateRegNr")
            updateDate = st.text_input(label="Dato", placeholder="Indtast dato", key="updateDate")
            updateName = st.text_input(label="Navn", placeholder="Indtast navn", key="updateName")
            updateCompleted = st.checkbox(label="Afsluttet", key="updateCompleted")



            if st.button(label="Opdater sag", type="primary"):
                updateResponse = requests.put(f"http://localhost:5001/customer-support-service/complaints/{updateMongoId}", json=removeEmptyFromDict({
                    "complaint": updateComplaint,
                    "regNr": updateRegNr,
                    "date": updateDate,
                    "name": updateName,
                    "completed": updateCompleted
                    
                    }), 
                                              headers={"Authorization": controller.get("Authorization")})
                if updateResponse.status_code == 200:
                    st.rerun()
                else:
                    st.write(f":red[Kunne ikke opdatere sagen. Statuskode: {updateResponse.status_code}]")

    with tab4:
        if claims.get("role") != "admin":
            st.warning("Du har ikke adgang til at slette sager.")
        else:
            with st.container(border=True): # Lorte streamlit. Løsningen virker, men kunne være meget federe.
                removalMongoId = st.text_input(label="ID", placeholder="Indtast Id", key="removalMongoId")

            if st.button(label="Slet Sag", type="primary"):
                removalResponse = requests.delete(f"http://localhost:5001/customer-support-service/complaints/{removalMongoId}", headers={"Authorization": controller.get("Authorization")})
                if removalResponse.status_code == 200:
                    st.write("Sagen er nu slettet.")
                    st.rerun()
                else:
                    st.write(f":red[Sagen kunne ikke findes.]")