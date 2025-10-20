import streamlit as st



st.set_page_config("TeaTime", page_icon="☕", layout="wide")
st.title("☕ Welcome to CTD-TeaTime!")
st.header("Need Some Tea?")
if st.button("Start Ordering"):
        st.switch_page("pages/1_menu.py")

# st.markdown("""
# <style>
#     .main {
#         padding: 2rem;
#     }
#     .stButton>button {
#         width: 100%;
#         background-color: #FF6B6B;
#         color: white;
#         font-weight: bold;
#         padding: 0.75rem;
#         border-radius: 10px;
#         border: none;
#         font-size: 1.1rem;
#     }
#     .stButton>button:hover {
#         background-color: #FF5252;
#     }
#             </style>
# """, unsafe_allow_html=True)

