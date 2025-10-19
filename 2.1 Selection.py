import streamlit as st
import ngrok as ng

# Page configuration
st.set_page_config(page_title="Customize Your Drink", page_icon="☕", layout="wide")


col1, col2= st.columns(2)
with col1:
    if st.button("Back to Menu"):
        st.switch_page("pages/1_menu.py")
with col2:
    if st.button("Add to Cart"):
        st.switch_page("pages/2.2 Cart.py")

# Custom CSS for styling
#st.markdown(multiline string, unsafe_allow_html=True)
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
    .topping-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .price-tag {
        color: #28a745;
        font-weight: bold;
    }
    .order-summary {
        background-color: #011729;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_coffee' not in st.session_state:
    st.session_state.selected_coffee = "Tea"
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Header
st.title("☕ Customize Your Drink")
st.markdown(f"### Customizing: **{st.session_state.selected_coffee}**")
st.markdown("---")

# Toppings data
toppings = [
    {"name": "Pearl", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/feb1a05c-547e-42a8-b293-2cda95c33050/Topping_Pearls+%28Boba%29.png?format=1000w", "desc": ""},
    {"name": "Honey Jelly", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/1e91bb32-9e6d-4e00-a7cf-28eaae4bee93/Topping_HoneyJelly.png?format=1000w", "desc": ""},
    {"name": "Lychee Jelly", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/fc64125a-bc3e-476e-a0b6-4d48757b1d77/Topping_LycheeJelly+%281%29.png?format=1000w", "desc": ""},
    {"name": "Strawberry Boba", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/8d9305b6-65bb-4fcd-8ac3-0368c22cdaf7/Topping_StrawberryPoppingBoba.png?format=1000w", "desc": ""},
    {"name": "Mango Boba", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/8da7f0f0-1587-47f9-a573-46f997b2883f/Topping_MangoPoppingBoba.png?format=1000w", "desc": ""},
    {"name": "Cream", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/c9746d52-a8ab-4ecb-9c62-46c4e7d45b34/Topping_Creama.png?format=1000w", "desc": ""},
    {"name": "Ice Cream", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/ee270494-a5e6-4080-96ae-3e21cccfa0d6/Topping_IceCream.png?format=1000w", "desc": ""},
]

base_price = 5.00

# Toppings Section
st.markdown("## 🧋 Select Your Toppings")
st.markdown("Choose as many as you like!")

# Create columns for toppings grid
cols_per_row = 2
selected_toppings = []

for i in range(0, len(toppings), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, col in enumerate(cols):
        if i + j < len(toppings):
            topping = toppings[i + j]
            with col:
                with st.container():
                    st.image(topping['emoji'], width=198)  # Image about 3rem wide
                    st.markdown(f"**{topping['name']}**")
                    st.markdown(f"<div style='font-size: 0.85rem; color: #666;'>{topping['desc']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='price-tag' style='margin-top: 0.5rem;'>${topping['price']:.2f}</div>", unsafe_allow_html=True)

                if st.checkbox(f"Add {topping['name']}", key=f"topping_{i+j}"):
                    selected_toppings.append(topping)

st.markdown("---")

# Customization Options
st.markdown("## ⚙️ Customize Your Drink")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧊 Ice Level")
    ice_level = st.radio(
        "Choose ice amount:",
        ["Regular Ice", "Less Ice", "No Ice"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 🍬 Sugar Level")
    sugar_level = st.radio(
        "Choose sweetness:",
        ["Normal (100%)", "Less Sweet (80%)", "Half Sweet (50%)", "Light (30%)", "No Sugar (0%)"],
        label_visibility="collapsed"
    )

with col3:
    st.markdown("### 🥛 Milk Type")
    milk_type = st.selectbox(
        "Choose milk:",
        ["Regular Milk", "Almond Milk", "Coconut Milk", "Oat Milk", "Soy Milk"],
        label_visibility="collapsed"
    )

st.markdown("---")

# Order Summary
st.markdown("## 📋 Order Summary")

toppings_total = sum([t['price'] for t in selected_toppings])
total_price = base_price + toppings_total

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    <div class="order-summary">
        <h4>Your Order:</h4>
        <p><strong>Coffee:</strong> {st.session_state.selected_coffee} - ${base_price:.2f}</p>
    """, unsafe_allow_html=True)

    if selected_toppings:
        st.markdown("<p><strong>Toppings:</strong></p>", unsafe_allow_html=True)
        for topping in selected_toppings:
            st.markdown(f"<p style='margin-left: 1rem;'>• {topping['name']} - ${topping['price']:.2f}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p><strong>Toppings:</strong> None selected</p>", unsafe_allow_html=True)

    st.markdown(f"""
        <p><strong>Ice Level:</strong> {ice_level}</p>
        <p><strong>Sugar Level:</strong> {sugar_level}</p>
        <p><strong>Milk Type:</strong> {milk_type}</p>
        <hr>
        <h3 style="color: #2196F3;">Total: ${total_price:.2f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### ")
    if st.button("🛒 Add to Cart", type="primary"):
        order = {
            "coffee": st.session_state.selected_coffee,
            "toppings": [t['name'] for t in selected_toppings],
            "ice": ice_level,
            "sugar": sugar_level,
            "milk": milk_type,
            "price": total_price
        }
        st.session_state.cart.append(order)
        st.success("✅ Added to cart successfully!")
        st.balloons()

    st.markdown("### ")
    if st.button("⬅️ Back to Menu"):
        st.switch_page("pages/1_menu.py")
       

        # In a real app, this would navigate back
        st.markdown("*Navigation to main menu would happen here*")
# Display cart count in sidebar
if st.session_state.cart:
    st.sidebar.success(f"🛒 Cart: {len(st.session_state.cart)} item(s)")
    if st.sidebar.button("View Cart"):
         st.switch_page("pages/2.2 Cart.py")
         st.sidebar.markdown("### Your Cart:")
         for idx, item in enumerate(st.session_state.cart, 1):
            st.sidebar.markdown(f"**{idx}. {item['coffee']}** - ${item['price']:.2f}")
 



