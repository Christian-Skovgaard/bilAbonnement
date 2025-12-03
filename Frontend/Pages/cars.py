import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

# Data
cars = []

controller = CookieController()

# Logik
def queryParamsToString():
    if len(st.query_params.items()) != 0:
        queryString = ""
        for key, value in st.query_params.items():
            queryString += f"{key}={value}&"
        return queryString[0:len(queryString)-1] # Return query string and remove the last "&".
    else:
        return ""

try:
    if len(st.query_params.items()) != 0: # Hvis der er query parameters
        response = requests.get(f"http://localhost:5001/cars/query?{queryParamsToString()}", headers={"Authorization": controller.get("Authorization")})
    else: # Hvis der ikke er query parameters
        response = requests.get("http://localhost:5001/cars", headers={"Authorization": controller.get("Authorization")})
    cars = response.json()
    dataframe = pd.DataFrame(cars)
    canConnect = True
except:
        st.switch_page("login.py")
        canConnect = False # Eksisterer kun, hvis der findes en bedre løsning til at håndtere, at car-catalog-service er nede (AuthToken er stadig valid).
        dataframe = [] # Brugeren skal ikke smides ud, bare fordi car-catalog-service ikke kører.

# Streamlit

st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

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
    carsPageBtn, damageRegiBtn, dealershipBtn, subscriptionsBtn, customerSuppBtn = st.columns(5)
    with carsPageBtn:
        if st.button(label="Biler", type="primary"):
            st.query_params = {}
            st.rerun()

    with damageRegiBtn:
        if st.button(label="Skader"):
            st.switch_page("pages/damages.py")

    with dealershipBtn:
        if st.button(label="Forhandler"):
            st.switch_page("pages/dealership.py")

    with subscriptionsBtn:
        if st.button(label="Abonnementer"):
            st.switch_page("pages/subscriptions.py")

    with customerSuppBtn:
        if st.button(label="Kundeservice"):
            st.switch_page("pages/customersupport.py")

carLeft, carRight = st.columns([6,4])
with carLeft:
    st.subheader("Oversigt over biler")
    with st.container(border=True):
        if not canConnect:
            st.dataframe(dataframe, hide_index=True)
            st.write("Can't connect :(")
        else:
            st.dataframe(dataframe, hide_index=True)
        

with carRight:
    st.subheader("Filtrér og søg")
    with st.container(border=True):
        regNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer")
        brand = st.text_input(label="Mærke", placeholder="Indtast mærke")
        model = st.text_input(label="Model", placeholder="Indtast model")

        yearCol, propellantCol = st.columns(2)
        with yearCol:
            modelYear = st.number_input(label="Årstal", step=1, placeholder="Indtast årstal", value=None)
        with propellantCol:
            propellant = st.selectbox(label="Drivmiddel", options=("Alle", "Benzin", "El", "Hybrid"))

        maxKm = 500000 # Kan finde max km. kørt fra database
        kmDriven = st.slider(label="Max km. kørt", min_value=0, max_value=maxKm, value=maxKm, step=10000)

        minPrice = 2000 # Kan finde min og max månedlig pris fra database
        maxPrice = 12000
        monthlyPrice = st.slider(label="Månedlig pris", min_value=minPrice, max_value=maxPrice, value=(minPrice, maxPrice), step=500)

        anvendBtn, nulstilBtn = st.columns(2)
        with anvendBtn:
            if st.button(label="Anvend"):
                st.query_params["regNr"] = regNr
                st.query_params["brand"] = brand
                st.query_params["model"] = model
                if modelYear == None:
                    st.query_params["modelYear"] = "" # Hvis "None" sæt til tom string.
                else:
                    st.query_params["modelYear"] = modelYear
                if propellant == "Alle":
                    st.query_params["propellant"] = "" # "Alle" skal ikke sendes med som en query parameter - det skal bare være tomt.
                else:
                    st.query_params["propellant"] = propellant
                #st.query_params["kmDriven"] = kmDriven
                #st.query_params["monthlyMin"] = monthlyPrice[0] # min
                #st.query_params["monthlyMax"] = monthlyPrice[1] # max
                st.rerun()
        with nulstilBtn:
            if st.button(label="Nulstil"):
                st.query_params = {}
                st.rerun()