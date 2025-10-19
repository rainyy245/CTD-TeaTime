import streamlit as st
import ngrok as ng

st.title(" Payment Page")


col1, space_col, col2= st.columns([1,0.1,1])
with col1:
    st.image("C:/Users/rainy/Desktop/CTD Project/CTD-TeaTime/Images/Credit.png", width=150)
with space_col:
    pass
with col2:
    st.image("C:/Users/rainy/Desktop/CTD Project/CTD-TeaTime/Images/QR.png", width=170)

col3, col4= st.columns(2)
with col3:
    if st.button("Card payment"):
        st.switch_page("pages/2.4 Proccess.py")
with col4:
    if st.button("QR payment"):
        st.switch_page("pages/2.3.1 QR code.py")

st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #FF5252;
    }
            </style>
""", unsafe_allow_html=True)