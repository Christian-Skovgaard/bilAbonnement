import streamlit as st
import pandas as pd

# Data
cars = [
    {
        "regnr": "XD 69 420",
        "brand": "Toyota",
        "model": "GT86",
        "year": "2012",
        "available": True
    },
    {
        "regnr": "AB 13 043",
        "brand": "Audi",
        "model": "A6",
        "year": "2021",
        "available": True
    },
    {
        "regnr": "KG 73 492",
        "brand": "Chevrolet",
        "model": "Suburban",
        "year": "2006",
        "available": False
    },
    {
        "regnr": "YC 21 344",
        "brand": "BMW",
        "model": "iX3",
        "year": "2025",
        "available": True
    },
    {
        "regnr": "QH 82 259",
        "brand": "Mercedez-Benz",
        "model": "CLA",
        "year": "2024",
        "available": True
    }
]

# Funktioner



# Streamlit

st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")


col1, col2 = st.columns([5,1], vertical_alignment="center")
with col1:
    st.header("Bilabonnement")

with col2:
    st.subheader("Hej Victor!")
    if st.button(label="Log ud"):
        st.switch_page("login.py") # Manglende funktionalitet (Fjern JWT i cookies)

carCatalogService, damageRegistrationService, dealershipManagementService, subscriptionManagementService, customerSupportService = st.tabs(["Biler", "Skader", "Forhandler", "Abonnementer", "Kundeservice"])

with carCatalogService:
    carLeft, carRight = st.columns([6,4])

    with carLeft:
        st.subheader("Oversigt over biler")
        with st.container(border=True):
            dataframe = st.dataframe(
                pd.DataFrame(cars),
                hide_index=True
                )

    with carRight:
        st.subheader("Filtrér og søg")
        with st.container(border=True):
            st.text_input(label="Søg", placeholder="Indtast registreringsnummer")
            st.number_input(label="Årstal", step=1, value=None, placeholder="Indtast årstal")
            st.html(f'''
            <form action="./cars?username=Victor&password=1234">
                <input type="hidden" name="username" value="test1"/>
                <input type="hidden" name="password" value="test2"/>
                <input type="submit" value="Anvend"/>
            </form>''')

with damageRegistrationService:
    st.write("Hi :3 - Damage registration service")

with dealershipManagementService:
    st.write("Hi :3 - dealership service")

with subscriptionManagementService:
    st.write("Hi :3 - Subscription service")

with customerSupportService:
    st.write("Hi :3 - Customer support service")