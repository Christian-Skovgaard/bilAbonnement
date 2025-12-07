import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

# Data
controller = CookieController()

tasks = []


# Logik
try:
    response = requests.get("http://localhost:5001/task-management-service/tasks", headers={"Authorization": controller.get("Authorization")})
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
        if st.button(label="Skader"):
            st.query_params = {}
            
    with tasksBtn:
        if st.button(label="Opgaver", type="primary"):
            st.switch_page("pages/tasks.py")
            st.rerun()

    with subscriptionsBtn:
        if st.button(label="Abonnementer"):
            st.switch_page("pages/subscriptions.py")

    with customerSuppBtn:
        if st.button(label="Kundeservice"):
            st.switch_page("pages/customersupport.py")

tasks = st.columns([6,4])
with tasks[0]:
    st.subheader("Oversigt over opgaver")
    with st.container(border=True):
        edited_df = st.data_editor(
            dataframe, 
            hide_index=True, 
            column_config={
                "_id": None,
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["pending", "in-progress", "completed"],
                    required=True
                )
            },
            disabled=["title", "description", "assignedTo"]
        )
        
        if st.button("Gem ændringer"):
            # Finder de steder hvor der har været ændringer i status
            for index, row in edited_df.iterrows():
                original_status = dataframe.loc[index, 'status']
                new_status = row['status']
                
                if original_status != new_status:
                    try:
                        response = requests.put(
                            f"http://localhost:5001/task-management-service/tasks/{row['_id']}/status",
                            headers={"Authorization": controller.get("Authorization"), "Content-Type": "application/json"},
                            json={"status": new_status}
                        )
                        if response.status_code == 200:
                            st.success(f"Status opdateret for: {row['title']}")
                        else:
                            st.error(f"Fejl ved opdatering af {row['title']}: {response.status_code}")
                    except Exception as e:
                        st.error(f"Fejl: {str(e)}")
            
            st.rerun()
    
