import streamlit as st

st.set_page_config(layout='centered')

st.subheader('Detail Page')
st.write(st.session_state['country_data'])