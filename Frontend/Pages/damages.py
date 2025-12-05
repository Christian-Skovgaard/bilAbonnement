import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

# Data
controller = CookieController()

damageCases = []

# Logik
try:
    if "damageRegNr" in st.session_state:
        response = requests.get(f"http://localhost:5001/damage-registration-service/cases/{st.session_state["damageRegNr"]}", headers={"Authorization": controller.get("Authorization")})
    else:
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
        test1, test2 = st.columns([1,15], vertical_alignment="center")
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
        idHeaderCol, deleteCol = st.columns([8, 1], vertical_alignment="center")
        with idHeaderCol:
            st.subheader(f"ID: {st.session_state.damageDetails["_id"]}")
        with deleteCol:
            if st.button("Slet", type="primary"):
                removalResponse = requests.delete(f"http://localhost:5001/damage-registration-service/cases/{st.session_state["damageDetails"]["_id"]}", headers={"Authorization": controller.get("Authorization")})
                if removalResponse.status_code == 200:
                    st.rerun()
                else:
                    st.write("Fejl!") # Dette burde ikke blive set på grund af Streamlits skærm refresh.
    elif "damageRegNr" in st.session_state:
        st.subheader("Tilføj skadesrapport")
    else:
        st.subheader("Kontrolpanel")
    with st.container(border=True):
        if "damageRegNr" in st.session_state:
            if "damageDetails" in st.session_state: # Reg. nr. og specifik skadesrapport valgt.
                detailsCount = 0 # Bruges til næste for-loop for columns.
                for damageKey, damageValue in st.session_state.damageDetails.items():
                    if damageKey != "_id":
                        st.text_input(label=damageKey.title(), placeholder=f"Indtast {damageKey}", value=damageValue, key=f"update{damageKey}")
                if st.button("Gem ændringer"): # PUT funktionalitet. Knap kan evt. dukke op, når et text_input er blevet ændret.
                    updateBody = {}
                    updateDamageBody = {}
                    st.write(st.session_state.damageDetails.items())
                    for something in st.session_state.damageDetails.items():
                        if something[0] != "_id":
                            updateDamageBody[str(something[0])] = st.session_state[f"update{something[0]}"]
                    updateResponse = requests.put(f"http://localhost:5001/damage-registration-service/cases/{st.session_state["damageDetails"]["_id"]}", json=updateDamageBody, headers={"Authorization": controller.get("Authorization")})
                    if updateResponse.status_code == 200:
                        st.rerun()
                    else:
                        st.write(f"Case kunne ikke blive opdateret. Statuskode: {updateResponse.status_code}")
            else: # Reg. nr. valgt, men ikke specifik skadesrapport.
                if len(dataframe) == 0: # Ingen skadesrapporter på reg. nr.
                    st.write("Ingen skadesrapporter på reg. nr.")
                else:
                    for something in dataframe.items():
                        if something[0] != "_id":
                            st.text_input(label=something[0].title(), placeholder=f"Indtast {something[0]}", key=f"input{something[0]}")
                    if st.button("Tilføj"):
                        addDamageBody = {}
                        for something in dataframe.items():
                            if something[0] != "_id":
                                addDamageBody[str(something[0])] = st.session_state[f"input{something[0]}"]
                        addResponse = requests.post(f"http://localhost:5001/damage-registration-service/cases/{addDamageBody["regNr"]}", json=addDamageBody, headers={"Authorization": controller.get("Authorization")})
                        if addResponse.status_code == 200:
                            st.rerun()
                        else:
                            st.write("Kunne ikke tilføje bil.")
        else: # Reg. nr. ikke valgt.
            damageRegNr = st.text_input(label="Reg. nr.", placeholder="Indtast registreringsnummer")
            if st.button("Find skadesrapporter"):
                findCarResponse = requests.get(f"http://localhost:5001/car-catalog-service/cars/query?regNr={damageRegNr.replace(" ", "")}", headers={"Authorization": controller.get("Authorization")})
                if len(findCarResponse.json()) == 1: # Hvis præcis 1 resultat findes, vis skadesrapporter for gældende reg. nr.
                    st.session_state["damageRegNr"] = findCarResponse.json()[0]["regNr"]
                    st.rerun()
                elif len(findCarResponse.json()) > 1:
                    st.write(f":red[Flere resultater fundet - præcisér reg. nr.]")
                else:
                    st.write(f":red[Ingen bil fundet.]")