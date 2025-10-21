import streamlit as st



st.set_page_config("Tea Selection Menu", page_icon="☕", layout="wide")
st.title("Tea Selection Menu")
st.header("What's the TEA")
st.markdown(f"## Cost for each drink: 5.00")

st.markdown("---")

col1, space_col, col2= st.columns([1,0.1,1])

with col1:
    st.image("Image/Green Tea.png", width=200)
    if st.button("Green tea"):
        st.session_state.selected_drink = "Green Tea"
        st.switch_page("pages/2.1 Selection.py")

with space_col:
    pass

with col2:
    st.image("Image/Bubble Tea.png", width=200)
    if st.button("Bubble tea"):
        st.session_state.selected_drink = "Bubble Tea"
        st.switch_page("pages/2.1 Selection.py")