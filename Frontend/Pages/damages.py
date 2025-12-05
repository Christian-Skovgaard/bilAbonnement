import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

# Data
controller = CookieController()

damageCases = []

# Logik
try:
    response = requests.get("http://localhost:5001/damage-registration-service/cases", headers={"Authorization": controller.get("Authorization")})
    damageCases = response.json()
    dataframe = pd.DataFrame(damageCases)
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
        if "Authorization" in controller.getAll(): # KUN RELEVANT FOR TESTING OG BUG FIXING
            controller.remove("Authorization")
        if "JWT" in controller.getAll(): # KUN RELEVANT FOR TESTING OG BUG FIXING
            controller.remove("JWT")
        st.switch_page("login.py")

with st.container(border=True):
    carsPageBtn, damageRegiBtn, tasksBtn, subscriptionsBtn, customerSuppBtn = st.columns(5)
    with carsPageBtn:
        if st.button(label="Biler"):
            st.query_params = {}
            st.switch_page("pages/cars.py")

    with damageRegiBtn:
        if st.button(label="Skader", type="primary"):
            st.query_params = {}
            st.rerun()

    with tasksBtn:
        if st.button(label="Opgaver"):
            st.switch_page("pages/tasks.py")

    with subscriptionsBtn:
        if st.button(label="Abonnementer"):
            st.switch_page("pages/subscriptions.py")

    with customerSuppBtn:
        if st.button(label="Kundeservice"):
            st.switch_page("pages/customersupport.py")

damagesLeft, damagesRight = st.columns([6,4])
with damagesLeft:
    if "damageRegNr" in st.session_state:
        test1, test2 = st.columns([1,8])
        with test1:
            if st.button("<-"):
                del st.session_state["damageRegNr"]
                if "damageDetails" in st.session_state:
                    del st.session_state["damageDetails"]
                st.rerun()
        with test2:
            st.subheader(f"Skadesrapporter for {st.session_state["damageRegNr"]}")
    else:
        st.subheader("Oversigt over skadesrapporter")
    with st.container(border=True):
        if "damageRegNr" in st.session_state:
            if "damageDetails" in st.session_state: # Nulstil, hvis en skadesrapport allerede er valgt
                del st.session_state["damageDetails"]
            event = st.dataframe(
                dataframe,
                on_select='rerun',
                selection_mode='single-row'
            )
            if len(event.selection['rows']):
                selected_row = event.selection['rows'][0]
                caseData = dataframe.iloc[selected_row]
                tempDamageDetails = {}
                for column_name, value in caseData.items():
                    tempDamageDetails[column_name] = value
                st.session_state['damageDetails'] = tempDamageDetails
        else:
            st.write("Indtast registreringsnummer for at se tilhørende skadesrapporter.")

with damagesRight:
    if "damageDetails" in st.session_state:
        st.subheader(f"ID: {st.session_state.damageDetails["_id"]}")
    else:
        st.subheader("Kontrolpanel")
    with st.container(border=True):
        if "damageRegNr" in st.session_state:
            if "damageDetails" in st.session_state:
                detailsCount = 0 # Bruges til næste for-loop for columns.
                for damageKey, damageValue in st.session_state.damageDetails.items():
                    if damageKey != "_id":
                        st.text_input(label=damageKey, placeholder=f"Indtast {damageKey}", value=damageValue)
            else:
                st.write("Vælg en skadesrapport for at se mere.")
        else:
            damageRegNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer")
            if st.button("Find skadesrapporter"):
                st.session_state["damageRegNr"] = damageRegNr
                st.rerun()
        if 'key' not in st.session_state:
            st.session_state['key'] = 'value'