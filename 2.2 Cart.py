import streamlit as st
import ngrok as ng



col1, space_col, col2= st.columns([1,0.1,1])
with col1:
    st.image("C:/Users/rainy/Desktop/CTD Project/CTD-TeaTime/Images/Green.png", width=150)
with space_col:
    pass
with col2:
    st.image("C:/Users/rainy/Desktop/CTD Project/CTD-TeaTime/Images/Bubble.png", width=170)

col3, col4= st.columns(2)
with col3:
    if st.button("Make Payment"):
        st.switch_page("pages/2.3 Card payment.py")

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


