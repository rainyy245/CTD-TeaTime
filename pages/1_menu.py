import streamlit as st



st.set_page_config("Tea Selection Menu", page_icon="☕", layout="wide")
st.title("Tea Selection Menu")
st.header("What's the TEA")
st.markdown(f"## Cost for each drink: 5.00")
st.markdown("---")

# no need to write buttons in one column sertting and pictures in another
# we don't need ngrok cuz we never use it
# we dont need that path library rainee used, she just imports it and doesn't use it
# PEP8 -- done
# paths in rainee's code -- changed
# specific drink in paree's code -- done
# all the css -- delete it (it is prohibited to use it)

col1, space_col, col2= st.columns([1,0.1,1])

with col1:
    st.image("Image/Green Tea.png", width=200)
    if st.button("Green tea"):
        st.session_state.selected_drink = "Green Tea" #first we save the drink, next we change the page
        st.switch_page("pages/2.1 Selection.py")

with space_col:
    pass

with col2:
    st.image("Image/Bubble Tea.png", width=200)
    if st.button("Bubble tea"):
        st.session_state.selected_drink = "Bubble Tea" #first we save the drink, next we change the page
        st.switch_page("pages/2.1 Selection.py")
