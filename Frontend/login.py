import streamlit as st
from streamlit_cookies_controller import CookieController
import requests

controller = CookieController()

st.set_page_config(page_title="Log ind | Bilabonnement", page_icon="⏱️", layout="centered")

with st.container(border=True):
    st.header("Bilabonnement")

    st.subheader("Log ind")

    username = st.text_input(label="Brugernavn")
    password = st.text_input(label="Password", type="password")
    
    if st.button(label="Log ind"):
        response = requests.post("http://localhost:5001/getAuthToken", json={"username": username, "password": password})
        
        if "access_token" in response.json():
            controller.set("Authorization", f"Bearer {response.json()["access_token"]}")
            st.switch_page("pages/cars.py")
        else:
            st.write(f":red[{response.json()["error"]}]")