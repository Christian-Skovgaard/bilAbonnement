import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

controller = CookieController()

st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

# we defy session state!
def defSessionState(): # har lavet i funtion så jeg kan lukke den så den ikke fylder, har ikke noget praktisk formål
    if "filterActive" not in st.session_state:
        st.session_state.filterName = True
    if "filterName" not in st.session_state:
        st.session_state.filterName = ""
    if "filterBrand" not in st.session_state:
        st.session_state.filterBrand = ""
    if "filterModel" not in st.session_state:
        st.session_state.filterModel = ""
defSessionState()


# list at lægge vores data i som vi også opdatere
data = [
    {
        "name": "Darth Vader",
        "isHappy": False
    },
    {
        "name": "Benjamin",
        "isHappy": True
    }
] 


# get data
resp = requests.request(
    method="GET",
    url="http://localhost:5001/subscription-management-service/subscriptions/query",
    headers={"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2NDg4OTE4MSwianRpIjoiNDE2MGQwODQtYzI4Yy00NmVlLWI0MmItMDlkYzQ3N2ZhZDNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IkJvIiwibmJmIjoxNzY0ODg5MTgxLCJjc3JmIjoiODJiYzVkZDItZmVjOC00NGNiLWFkOTQtZDI3NThjZGE3ZmU1IiwiZXhwIjoxNzcwMDczMTgxLCJyb2xlIjoiYWRtaW4iLCJkZXBhcnRtZW50IjoiS29saW5nIn0.ervCIhnk4iyzZNB4DpuU4IvrtMttntWcdcrvytnUrfauFuGqvPm6_nqH0Ps45gCqhCIUI3YUQti7jk3JTiLsA4L8RFhYOdaFv6LrYjACHINtl6Q1XO5IJTlSAGsuWc3EiWrvpHRfUvDB5-8n6xRNa5qEdwEToZofjcvYrxCuWsZ067rNYVumWR6e9oAOc7IUFHcC_L1vYGwti2SbB8XJAxxkdJc3Zr8YTOD9EBscal1pOOdznRHR4pS3QUUDIpJJxBssINq1wClaS9_8zPYhTW4eMgeq3NDVoqtwaW7y7cwG5BXNIhyicRGD-WD33oAklHr2Ess8wfNrmSs-Ozp-WA"},
    params={"associatedCustommerId":"12"}
)
json = resp.json()
df = pd.DataFrame(json)

def updateQueryParams(input, parameter):    # TODO skal forstå
    if (input == "") or (input == None):
        if parameter in st.query_params:
            st.query_params.pop(parameter) # Fjern fra query parameters, hvis indholdet er opdateret til en tom værdi.
    else:
        st.query_params[parameter] = input


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
            st.switch_page("pages/cars.py")

    with damageRegiBtn:
        if st.button(label="Skader"):
            st.switch_page("pages/damages.py")

    with tasksBtn:
        if st.button(label="Opgaver"):
            st.switch_page("pages/tasks.py")

    with subscriptionsBtn:
        if st.button(label="Abonnementer", type="primary"):
            st.query_params = {}
            st.rerun()

    with customerSuppBtn:
        if st.button(label="Kundeservice"):
            st.switch_page("pages/customersupport.py")


subLeft, subRight = st.columns([6,4])
with subLeft:
    st.subheader("Oversigt over Abonnetmenter")
    with st.container(border=True): # Dataframe opdateres ved hver ændring i text_input eller button presses.
        st.dataframe(df, hide_index=True)

with subRight:
    carRightTitle = st.subheader("Kontrolpanel")
    tab1, tab2, tab3 = st.tabs(["Søg og filtrér", "Opret abonnetment", "Opdater bil"])

    with tab1:
        with st.container(border=True): # filterer
            filterAvailable = st.checkbox(label="Kun aktive", key="filterAktive", value=True)

            filterRegNr = st.text_input(label="Navn", placeholder="Indtast registreringsnummer", key="filterRegNr")
            
            yearCol, propellantCol = st.columns(2)
            with yearCol:
                filterModelYear = st.text_input(label="Bilmærke", placeholder="Indtast årstal", key="filterModelYear")
            with propellantCol:
                filterPropellant = st.text_input(label="Model", key="filterPropellant")

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