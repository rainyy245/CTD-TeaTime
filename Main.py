import streamlit as st
import time


# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = " QR Code Page"

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Time logic
elapsed_time = time.time() - st.session_state.start_time

# Automatically switch after 10 seconds
if st.session_state.page == "" and elapsed_time >= 10:
    st.session_state.page = "Process Page"
    st.experimental_rerun()

# Display current page
if st.session_state.page == "QR Code Page":
    st.title("🍽️ QR Code Page")
    st.write("You will be redirected to the Process Page in 10 seconds...")
    st.write(f"Time left: {int(10 - elapsed_time)} seconds")

elif st.session_state.page == "Process Page":
    st.title("⚙️ Process Page")
    st.success("You have been redirected here after 10 seconds!")
    