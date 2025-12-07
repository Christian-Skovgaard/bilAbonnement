import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

# Data
cases = []

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

user = st.session_state["username"] or "Guest"

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