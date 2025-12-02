import streamlit as st

st.set_page_config(page_title="Log ind | Bilabonnement", page_icon="⏱️", layout="centered")

with st.container(border=True):
    st.header("Bilabonnement")

    st.subheader("Log ind")

    st.text_input(label="Brugernavn")
    st.text_input(label="Password")

    st.button(label="Log ind")