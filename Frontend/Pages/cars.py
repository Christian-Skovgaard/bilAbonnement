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
            if value not in (None, "", "null"):
                queryString += f"{key}={value}&"
        return queryString[:-1]  # remove last "&"
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




# Streamlit
st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

col1, col2 = st.columns([5,1], vertical_alignment="center")
with col1:
    st.header("Bilabonnement")

user = st.session_state.get("username", "Guest")
if user == "Guest":
    st.switch_page("login.py")


    # ✅ Load cars once when landing on /cars
if "cars_df" not in st.session_state:
    response = requests.get(
        "http://gateway:5001/car-catalog-service/cars",
        headers={"Authorization": controller.get("Authorization")}
    )
    if response.status_code == 200:
        st.session_state["cars_df"] = pd.DataFrame(response.json())
    else:
        st.session_state["cars_df"] = pd.DataFrame([])  # fallback empty


with col2:
    st.subheader(f"Hej {user}!")
    if st.button(label="Log ud"):
        if "Authorization" in controller.getAll():
            controller.remove("Authorization")
        if "JWT" in controller.getAll():
            controller.remove("JWT")
        st.switch_page("login.py")

with st.container(border=True):
    carsPageBtn, damageRegiBtn, tasksBtn, subscriptionsBtn, customerSuppBtn = st.columns(5)
    with carsPageBtn:
        if st.button(label="Biler", type="primary"):
            st.query_params = {}
            st.rerun()

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
        if st.button(label="Abonnementer"):
            st.switch_page("pages/subscriptions.py")

    with customerSuppBtn:
        if st.button(label="Kundeservice"):
            st.switch_page("pages/customersupport.py")

carLeft, carRight = st.columns([6,4])

with carLeft:
    st.subheader("Oversigt over biler")
    with st.container(border=True):
        if "cars_df" in st.session_state:
            st.dataframe(st.session_state["cars_df"], hide_index=True)    

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
                if st.button(label="Anvend", type="primary"):
                    # Build query parameters only when button is pressed
                    updateQueryParams(filterRegNr, "regNr")
                    updateQueryParams(filterBrand, "brand")
                    updateQueryParams(filterModel, "model")
                    updateQueryParams(filterModelYear, "modelYear")

                if filterPropellant == "Alle":
                    updateQueryParams("", "propellant")
                else:
                    updateQueryParams(filterPropellant, "propellant")

                # Kilometer range
                st.query_params["minKm"] = 0
                st.query_params["maxKm"] = filterMaxKmDriven

                # Price range
                st.query_params["minPrice"] = filterMonthlyPrice[0]
                st.query_params["maxPrice"] = filterMonthlyPrice[1]

                # Availability
                if filterAvailable:
                    st.query_params["available"] = "true"
                else:
                    st.query_params.pop("available", None)

                # Build query string
                query_string = queryParamsToString()

                # ✅ Call backend only once here
                if query_string:
                    response = requests.get(
                        f"http://gateway:5001/car-catalog-service/cars/query?{query_string}",
                        headers={"Authorization": controller.get("Authorization")}
                    )
                else:
                    response = requests.get(
                        "http://gateway:5001/car-catalog-service/cars",
                        headers={"Authorization": controller.get("Authorization")}
                    )

                cars = response.json()
                st.session_state["cars_df"] = pd.DataFrame(cars)



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
                    addResponse = requests.post("http://gateway:5001/car-catalog-service/cars", json={
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
                updateResponse = requests.put(f"http://gateway:5001/car-catalog-service/cars/{updateRegNr.replace(' ', '')}", json=removeEmptyFromDict({
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
                removalResponse = requests.delete(f"http://gateway:5001/car-catalog-service/cars/{removalRegNr.replace(' ', '')}", headers={"Authorization": controller.get("Authorization")})
                if removalResponse.status_code == 200:
                    st.write("Bilen er nu slettet.")
                    st.rerun()
                else:
                    st.write(f":red[Bilen kunne ikke findes.]")
