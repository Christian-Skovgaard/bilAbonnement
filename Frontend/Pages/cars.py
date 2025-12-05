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
            if value != None or value != "" or value != null:
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
    if (input == "") or (input == None):
        if parameter in st.query_params:
            st.query_params.pop(parameter) # Fjern fra query parameters, hvis indholdet er opdateret til en tom værdi.
    else:
        st.query_params[parameter] = input

def removeEmptyFromDict(dict):
    result = {}
    for key, value in dict.items():
        if (value != "") and (value != None):
            result[key] = value
    return result

try:
    if len(st.query_params.items()) != 0: # Hvis der er query parameters
        response = requests.get(f"http://localhost:5001/car-catalog-service/cars/query?{queryParamsToString()}", headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"})
    else: # Hvis der ikke er query parameters
        response = requests.get("http://localhost:5001/car-catalog-service/cars", headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"})
    cars = response.json()
    dataframe = pd.DataFrame(cars)
except:
    if "Authorization" in controller.getAll():
        controller.remove("Authorization")
    if "JWT" in controller.getAll():
        controller.remove("JWT")
    st.switch_page("login.py")


# Streamlit
st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

col1, col2 = st.columns([5,1], vertical_alignment="center")
with col1:
    st.header("Bilabonnement")

with col2:
    st.subheader("Hej Victor!")
    if st.button(label="Log ud"):
        if "Authorization" in controller.getAll():
            controller.remove("Authorization")
        if "JWT" in controller.getAll():
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
    with st.container(border=True): # Dataframe opdateres ved hver ændring i text_input eller button presses.
        st.dataframe(dataframe, hide_index=True)
        

with carRight:
    carRightTitle = st.subheader("Kontrolpanel")
    tab1, tab2, tab3, tab4 = st.tabs(["Søg og filtrér", "Tilføj ny bil", "Opdater bil", "Slet bil"])

    with tab1:
        with st.container(border=True):
            filterRegNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer", key="filterRegNr")
            filterBrand = st.text_input(label="Mærke", placeholder="Indtast mærke", key="filterBrand")
            filterModel = st.text_input(label="Model", placeholder="Indtast model", key="filterModel")

            yearCol, propellantCol = st.columns(2)
            with yearCol:
                filterModelYear = st.number_input(label="Årstal", step=1, placeholder="Indtast årstal", value=None, key="filterModelYear")
            with propellantCol:
                filterPropellant = st.selectbox(label="Drivmiddel", options=("Alle", "Benzin", "El", "Hybrid"), key="filterPropellant")

            maxKm = 500000 # Kan finde max km. kørt fra database
            filterMaxKmDriven = st.slider(label="Max km. kørt", min_value=0, max_value=maxKm, value=maxKm, step=10000, key="filterKmDriven")

            minPrice = 2000 # Kan finde min og max månedlig pris fra database
            maxPrice = 12000
            filterMonthlyPrice = st.slider(label="Månedlig pris", min_value=minPrice, max_value=maxPrice, value=(minPrice, maxPrice), step=500, key="filterMonthlyPrice")
            filterAvailable = st.checkbox(label="Tilgængelig", key="filterAvailable")

            anvendBtn, nulstilBtn = st.columns(2)
            with anvendBtn:
                if st.button(label="Anvend"):
                    updateQueryParams(filterRegNr, "regNr")
                    updateQueryParams(filterBrand, "brand")
                    updateQueryParams(filterModel, "model")
                    updateQueryParams(filterModelYear, "modelYear")
                    updateQueryParams(filterBrand, "brand")
                    updateQueryParams(filterBrand, "brand")
                    updateQueryParams(filterBrand, "brand")
                    if filterPropellant == "Alle":
                        updateQueryParams("", "propellant") # "Alle" skal ikke sendes med som en query parameter - det skal bare være tomt.
                    else:
                        updateQueryParams(filterPropellant, "propellant")
                    #st.query_params["maxKmDriven"] = filterMaxKmDriven
                    #st.query_params["monthlyMin"] = monthlyPrice[0] # min
                    #st.query_params["monthlyMax"] = monthlyPrice[1] # max
                    if filterAvailable == False:
                        updateQueryParams("", "available") # "False" skal ikke sendes med som en query parameter - det skal bare være tomt.
                    else:
                        updateQueryParams(filterPropellant, "available")
                        st.query_params["available"] = filterAvailable
                    st.rerun()
            with nulstilBtn:
                if st.button(label="Nulstil"):
                    st.query_params = {}
                    st.rerun()

    with tab2: # Mangler access control via. roles
        with st.container(border=True):
            addRegNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer")
            addBrand = st.text_input(label="Mærke", placeholder="Indtast mærke")
            addModel = st.text_input(label="Model", placeholder="Indtast model")

            yearCol, propellantCol = st.columns(2)
            with yearCol:
                addModelYear = st.number_input(label="Årstal", step=1, placeholder="Indtast årstal", value=None)
            with propellantCol:
                addPropellant = st.text_input(label="Drivmiddel", placeholder="Indtast drivmiddel")
            
            kmCol, priceCol = st.columns(2)
            with kmCol:
                addKmDriven = st.number_input(label="Km kørt", step=1, placeholder="Indtast km kørt", value=None)
            with priceCol:
                addPrice = st.number_input(label="Månedlig pris", step=1, placeholder="Indtast pris", value=None)
            
            addAvailable = st.checkbox(label="Tilgængelig", key="addAvailable", value=False)
            
            if st.button(label="Tilføj", type="primary"):
                if hasEmpty([addRegNr, addBrand, addModel, addModelYear, addPropellant, addKmDriven, addPrice]): # Hvis et af felterne ikke er udfyldt.
                    st.write(f":red[Alle felter skal udfyldes]")
                else:
                    addResponse = requests.post("http://localhost:5001/car-catalog-service/cars", json={
                            "regNr": addRegNr.replace(" ", ""),
                            "brand": addBrand,
                            "model": addModel,
                            "modelYear": addModelYear,
                            "propellant": addPropellant,
                            "kmDriven": addKmDriven,
                            "monthlyPrice": addPrice,
                            "available": addAvailable
                        }, headers={"Authorization": controller.get("Authorization")})
                    if addResponse.status_code != 201:
                        st.write(f":red[Kunne ikke tilføje bil]. Statuskode: {addResponse.status_code}")
                    else:
                        st.rerun()

    with tab3:
        with st.container(border=True): # Lorte streamlit. Løsningen virker, men kunne være meget federe.
            updateRegNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer", key="updateRegNr")

            updateBrand = st.text_input(label="Mærke", placeholder="Indtast mærke", key="updateBrand")
            updateModel = st.text_input(label="Model", placeholder="Indtast model", key="updateModel")
            updateCol1, updateCol2 = st.columns(2)
            with updateCol1:
                updateModelYear = st.number_input(label="Årstal", step=1,placeholder="Indtast årstal", key="updateModelYear", value=None)
            with updateCol2:
                updatePropellant = st.text_input(label="Drivmiddel", placeholder="Indtast drivmiddel", key="updatePropellant")
            updateCol3, updateCol4 = st.columns(2)
            with updateCol3:
                updateKmDriven = st.number_input(label="Km kørt", step=1, placeholder="Indtast km kørt", key="updateKmDriven", value=None)
            with updateCol4:
                updatePrice = st.number_input(label="Månedlig pris", step=1, placeholder="Indtast pris", key="updatePrice", value=None)
            updateAvailable = st.checkbox(label="Tilgængelig", key="updateAvailable")

            if st.button(label="Opdater bil", type="primary"):
                updateResponse = requests.put(f"http://localhost:5001/car-catalog-service/cars/{updateRegNr.replace(" ", "")}", json=removeEmptyFromDict({
                    "brand": updateBrand,
                    "model": updateModel,
                    "modelYear": updateModelYear,
                    "propellant": updatePropellant,
                    "kmDriven": updateKmDriven,
                    "monthlyPrice": updatePrice,
                    "available": updateAvailable}), 
                                              headers={"Authorization": controller.get("Authorization")})
                if updateResponse.status_code == 200:
                    st.rerun()
                else:
                    st.write(f":red[Kunne ikke opdatere bilen. Statuskode: {updateResponse.status_code}]")

    with tab4: # Mangler access control via. roles
        with st.container(border=True): # Lorte streamlit. Løsningen virker, men kunne være meget federe.
            removalRegNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer", key="removalRegNr")

            if st.button(label="Slet bil", type="primary"):
                removalResponse = requests.delete(f"http://localhost:5001/car-catalog-service/cars/{removalRegNr.replace(" ", "")}", headers={"Authorization": controller.get("Authorization")})
                if removalResponse.status_code == 200:
                    st.write("Bilen er nu slettet.")
                    st.rerun()
                else:
                    st.write(f":red[Bilen kunne ikke findes.]")