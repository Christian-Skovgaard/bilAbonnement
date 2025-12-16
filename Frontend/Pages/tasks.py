import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

# Data
controller = CookieController()

tasks = []


# Logik
try:
    response = requests.get("http://gateway:5001/task-management-service/tasks", headers={"Authorization": controller.get("Authorization")})
    tasks = response.json()
    dataframe = pd.DataFrame(tasks)
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

user = st.session_state.get("username", "Guest")
if user == "Guest":
    st.switch_page("login.py")

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
            st.query_params = {}
            st.switch_page("pages/cars.py")

    with damageRegiBtn:
        if st.button(label="Skader"):
            if "damageRegNr" in st.session_state:
                del st.session_state["damageRegNr"]
            if "damageDetails" in st.session_state:
                del st.session_state["damageDetails"] # Slet session state fra damage-registration hvis de findes.
            st.query_params = {}
            st.switch_page("pages/damages.py")
            
    with tasksBtn:
        if st.button(label="Opgaver", type="primary"):
            st.switch_page("pages/tasks.py")
            st.rerun()

    with subscriptionsBtn:
        if st.button(label="Abonnementer"):
            st.switch_page("pages/subscriptions.py")

    with customerSuppBtn:
        if st.button(label="Kundeservice"):
            st.query_params = {}
            st.switch_page("pages/customersupport.py")

#Add tasks panel
with st.container(border=True):
    st.subheader("Tilføj ny opgave")
    addTitle = st.text_input(label="Titel", placeholder="Titel på opgave")
    addDescription = st.text_area(label="Beskrivelse", placeholder="Beskrivelse af opgave")
    addStatus = st.selectbox(label="Status", options=["pending", "in-progress", "completed"], index=0)
    addAssignedTo = st.selectbox(label="Tildelt til", options=["Reception", "Inspection", "Salesmen"], index=0)

    if st.button("Tilføj opgave"):
        try:
            response = requests.post(
                "http://localhost:5001/task-management-service/tasks",
                headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"},
                json={
                    "title": addTitle,
                    "description": addDescription,
                    "status": addStatus,
                    "assignedTo": addAssignedTo
                }
            )
            if response.status_code == 201:
                st.toast("Opgave tilføjet!", icon="✅")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Fejl: {response.status_code}")
        except Exception as e:
            st.error(f"Fejl: {str(e)}")


#Tasks management panel
st.subheader("Oversigt over opgaver")

if len(dataframe) > 0:
    for index, row in dataframe.iterrows():
        with st.container(border=True):
            col1, col2, col3 = st.columns([4, 2, 1])
            
            with col1:
                st.markdown(f"**{row['title']}**")
                st.write(row['description'])
            
            with col2:
                st.write(f"**Tildelt til:** {row['assignedTo']}")
                new_status = st.selectbox(
                    "Status",
                    ["pending", "in-progress", "completed"],
                    index=["pending", "in-progress", "completed"].index(row['status']),
                    key=f"status_{row['_id']}"
                )
            
            with col3:
                st.write("")  # Spacing
                if st.button("Gem", key=f"save_{row['_id']}"):
                    try:
                        response = requests.put(
                            f"http://gateway:5001/task-management-service/tasks/{row['_id']}/status",
                            headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"},
                            json={"status": new_status}
                        )
                        if response.status_code == 200:
                            st.success("Gemt!")
                            st.rerun()
                        else:
                            st.error(f"Fejl: {response.status_code}")
                    except Exception as e:
                        st.error(f"Fejl: {str(e)}")
else:
    st.info("Ingen opgaver tilgængelige")
    
