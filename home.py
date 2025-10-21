import streamlit as st



st.set_page_config("TeaTime", page_icon="☕", layout="wide")
st.title("☕ Welcome to CTD-TeaTime!")
st.header("Need Some Tea?")
if st.button("Start Ordering"):
        st.switch_page("pages/1_menu.py")