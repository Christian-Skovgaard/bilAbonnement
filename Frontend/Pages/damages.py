import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

controller = CookieController()

st.set_page_config(page_title="Oversigt | Bilabonnement", page_icon="⏱️", layout="wide")

st.write(controller.getAll())

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
    carsPageBtn, damageRegiBtn, dealershipBtn, subscriptionsBtn, customerSuppBtn = st.columns(5)
    with carsPageBtn:
        if st.button(label="Biler"):
            st.switch_page("pages/cars.py")

    with damageRegiBtn:
        if st.button(label="Skader", type="primary"):
            st.query_params = {}
            st.rerun()

    with dealershipBtn:
        if st.button(label="Forhandler"):
            st.switch_page("pages/dealership.py")

    with subscriptionsBtn:
        if st.button(label="Abonnementer"):
            st.switch_page("pages/subscriptions.py")

    with customerSuppBtn:
        if st.button(label="Kundeservice"):
            st.switch_page("pages/customersupport.py")