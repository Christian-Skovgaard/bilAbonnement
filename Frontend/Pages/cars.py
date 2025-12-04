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

def hasEmpty(list):
    for value in list:
        if value == "" or value == None:
            return True
    return False

try:
    if len(st.query_params.items()) != 0: # Hvis der er query parameters
        response = requests.get(f"http://localhost:5001/car-catalog-service/cars/query?{queryParamsToString()}", headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"})
    else: # Hvis der ikke er query parameters
        response = requests.get("http://localhost:5001/car-catalog-service/cars", headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"})
    cars = response.json()
    dataframe = pd.DataFrame(cars)
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
    with st.container(border=True):
        if not canConnect:
            st.dataframe(dataframe, hide_index=True)
            st.write("Can't connect :(")
        else:
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

            anvendBtn, nulstilBtn = st.columns(2)
            with anvendBtn:
                if st.button(label="Anvend"):
                    st.query_params["regNr"] = filterRegNr
                    st.query_params["brand"] = filterBrand
                    st.query_params["model"] = filterModel
                    if filterModelYear == None:
                        st.query_params["modelYear"] = "" # Hvis "None" sæt til tom string.
                    else:
                        st.query_params["modelYear"] = filterModelYear
                    if filterPropellant == "Alle":
                        st.query_params["propellant"] = "" # "Alle" skal ikke sendes med som en query parameter - det skal bare være tomt.
                    else:
                        st.query_params["propellant"] = filterPropellant
                    #st.query_params["maxKmDriven"] = filterMaxKmDriven
                    #st.query_params["monthlyMin"] = monthlyPrice[0] # min
                    #st.query_params["monthlyMax"] = monthlyPrice[1] # max
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
            
            if st.button(label="Tilføj"):
                if hasEmpty([addRegNr, addBrand, addModel, addModelYear, addPropellant, addKmDriven, addPrice]): # Hvis et af felterne ikke er udfyldt.
                    st.write(f":red[Alle felter skal udfyldes]")
                else:
                    st.write("Send request :3") # POST request goes here
                #    response = requests.post("http://localhost:5001/car-catalog-service/addCar", json={
                #        "regNr": addRegNr,
                #        "brand": addBrand,
                #        "model": addModel,
                #        "modelYear": addModelYear,
                #        "propellant": addPropellant,
                #       "price": addPrice
                #    })
                #   st.write("Bil oprettet")
                #   st.rerun()

    with tab3:
        with st.container(border=True):
            updateRegNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer", key="updateRegNr")

            if st.button(label="Find bil", key="updateFindCar"):
                if updateRegNr == "":
                    st.write(f":red[Indtast registreringsnummer]")
                else:
                    try:
                        updateResponse = requests.get(f"http://localhost:5001/car-catalog-service/cars/query?regNr={updateRegNr}", headers={"Authorization": controller.get("Authorization")})
                    except:
                        if "Authorization" in controller.getAll():
                            controller.remove("Authorization")
                        if "JWT" in controller.getAll():
                            controller.remove("JWT")
                        st.switch_page("login.py")

                    if len(updateResponse.json()) == 0:
                        st.write(f":red[Bil ikke fundet]")
                    elif len(updateResponse.json()) > 1:
                        st.write(f":red[Flere biler fundet - specificer registreringsnummer]")
                    else:
                        updateBrand = st.text_input(label="Mærke", placeholder="Indtast mærke", value=updateResponse.json()[0]["brand"])
                        updateModel = st.text_input(label="Model", placeholder="Indtast model", value=updateResponse.json()[0]["model"])
                        updateCol1, updateCol2 = st.columns(2)
                        with updateCol1:
                            updateModelYear = st.text_input(label="Årstal", placeholder="Indtast årstal", value=updateResponse.json()[0]["modelYear"])
                        with updateCol2:
                            updatePropellant = st.text_input(label="Drivmiddel", placeholder="Indtast drivmiddel", value=updateResponse.json()[0]["propellant"])
                        updateCol3, updateCol4 = st.columns(2)
                        with updateCol3:
                            updateKmDriven = st.text_input(label="Km kørt", placeholder="Indtast km kørt", value=updateResponse.json()[0]["kmDriven"])
                        with updateCol4:
                            updatePrice = st.text_input(label="Månedlig pris", placeholder="Indtast pris", value=updateResponse.json()[0]["monthlyPrice"])
                        if st.button(label="Opdater bil", type="primary"):
                            st.write("Ok :3") # PUT request goes here.

    with tab4: # Mangler access control via. roles
        with st.container(border=True):
            removeRegNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer", key="removeRegNr")

            if st.button(label="Find bil"):
                if removeRegNr == "":
                    st.write(f":red[Indtast registreringsnummer]")
                else:
                    try:
                        removalResponse = requests.get(f"http://localhost:5001/cars/query?regNr={removeRegNr}", headers={"Authorization": controller.get("Authorization")})
                    except:
                        if "Authorization" in controller.getAll():
                            controller.remove("Authorization")
                        if "JWT" in controller.getAll():
                            controller.remove("JWT")
                        st.switch_page("login.py")

                    if len(removalResponse.json()) == 0:
                        st.write(f":red[Bil ikke fundet]")
                    elif len(removalResponse.json()) > 1:
                        st.write(f":red[Flere biler fundet - specificer registreringsnummer]")
                    else:
                        removalBrand = st.text_input(label="Mærke", placeholder="Indtast mærke", value=removalResponse.json()[0]["brand"], disabled=True, key="removalBrand")
                        removalModel = st.text_input(label="Model", placeholder="Indtast model", value=removalResponse.json()[0]["model"], disabled=True, key="removalModel")
                        removalCol1, removalCol2 = st.columns(2)
                        with removalCol1:
                            removalModelYear = st.text_input(label="Årstal", placeholder="Indtast årstal", value=removalResponse.json()[0]["modelYear"], disabled=True, key="removalmodelYear")
                        with removalCol2:
                            removalPropellant = st.text_input(label="Drivmiddel", placeholder="Indtast drivmiddel", value=removalResponse.json()[0]["propellant"], disabled=True, key="removalPropellant")
                        removalCol3, removalCol4 = st.columns(2)
                        with removalCol3:
                            removalKmDriven = st.text_input(label="Km kørt", placeholder="Indtast km kørt", value=removalResponse.json()[0]["kmDriven"], disabled=True, key="removalKmDriven")
                        with removalCol4:
                            removalPrice = st.text_input(label="Månedlig pris", placeholder="Indtast pris", value=removalResponse.json()[0]["monthlyPrice"], disabled=True, key="removalPrice")
                        st.write(f":red[Er du sikker på, at du vil slette denne bil?]")
                        if st.button(label="Slet bil", type="primary"):
                            st.write("Ok :3") # DELETE request goes here.