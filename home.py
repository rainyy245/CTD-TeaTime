import streamlit as st
import ngrok as ng

st.title("Welcome to CTD-TeaTime!")
x = st.text_input("Favourite Tea?")
st.write (f"Your favourite tea is :{x}") 
is_cliceked = st.button("Click Me") 
