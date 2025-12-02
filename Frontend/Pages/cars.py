import streamlit as st
import pandas as pd
import requests

# Data
cars = []

# Funktioner
try:
    response = requests.get('http://localhost:5001/cars')
    print(response.status_code)
    cars = response.json()
    dataframe = pd.DataFrame(cars)
    canConnect = True
except:
    canConnect = False
    dataframe = []


# Streamlit

st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

col1, col2 = st.columns([5,1], vertical_alignment="center")
with col1:
    st.header("Bilabonnement")

with col2:
    st.subheader("Hej Victor!")
    if st.button(label="Log ud"):
        st.switch_page("login.py") # Manglende funktionalitet (Fjern JWT i cookies)

carLeft, carRight = st.columns([6,4])
with carLeft:
    st.subheader("Oversigt over biler")
    with st.container(border=True):
        if not canConnect:
            st.dataframe(dataframe, hide_index=True)
            st.write("Can't connect :(")
        else:
            st.dataframe(dataframe, hide_index=True)

        # Boilerplate / easter egg
        if "regNr" in st.query_params:
            if(st.query_params["regNr"] == "XD"):
                st.write("You're so fcking funny bro XD")
        

with carRight:
    st.subheader("Filtrér og søg")
    with st.container(border=True):
        regNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer")
        brand = st.text_input(label="Mærke", placeholder="Indtast mærke")
        model = st.text_input(label="Model", placeholder="Indtast model")

        yearCol, propellantCol = st.columns(2)
        with yearCol:
            modelYear = st.number_input(label="Årstal", step=1, placeholder="Indtast årstal")
        with propellantCol:
            propellant = st.selectbox(label="Drivmiddel", options=("Benzin", "El", "Hybrid"))

        maxKm = 500000 # Kan finde max km. kørt fra database
        kmDriven = st.slider(label="Max km. kørt", min_value=0, max_value=maxKm, value=maxKm, step=10000)

        minPrice = 2000 # Kan finde min og max månedlig pris fra database
        maxPrice = 12000
        monthlyPrice = st.slider(label="Månedlig pris", min_value=minPrice, max_value=maxPrice, value=(minPrice, maxPrice), step=500)

        if st.button(label="Anvend"):
            st.query_params["regNr"] = regNr
            st.query_params["brand"] = brand
            st.query_params["model"] = model
            st.query_params["modelYear"] = modelYear
            st.query_params["propellant"] = propellant
            st.query_params["kmDriven"] = kmDriven
            st.query_params["monthlyMin"] = monthlyPrice[0] # min
            st.query_params["monthlyMax"] = monthlyPrice[1] # max
            st.rerun()