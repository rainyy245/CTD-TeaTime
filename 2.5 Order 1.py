import streamlit as st
import ngrok as ng

st.badge(" Completed")
st.title(" Time for a tea !")

col3, col4= st.columns(2)
with col3:
    if st.button("continue ordering"):
        st.switch_page("pages/1_menu.py")
with col4:
    if st.button("Finish"):
        st.switch_page("C:/Users/rainy/Desktop/CTD Project/CTD-TeaTime\home.py")
