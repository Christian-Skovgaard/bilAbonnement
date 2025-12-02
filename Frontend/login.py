import streamlit as st

st.set_page_config(page_title="Log ind | Bilabonnement", page_icon="⏱️", layout="centered")

with st.container(border=True):
    st.header("Bilabonnement")

    st.subheader("Log ind")

    username = st.text_input(label="Brugernavn")
    password = st.text_input(label="Password", type="password")

    st.write(str(username))

    st.html(f'''
            <form action="./cars">
                <input type="submit" value="Log ind"/>
            </form>''')