import streamlit as st



st.set_page_config(page_title="Customize Your Drink", page_icon="☕", layout="wide")

if 'cart' not in st.session_state: 
        st.session_state.cart = []

# Checking wether the user has chosen the drink
selected_drink = st.session_state.get("selected_drink")
    
if not selected_drink:
    st.title("☕ Customize Your Drink")
    st.error("❌ You didn't choose the drink")
    st.info("Please, choose the drink on the Menu page")
    if st.button("⬅️ Back to Menu"):
        st.switch_page("pages/1_menu.py")

else:
    # Button on the top
    if st.button("⬅️ Back to Menu"):
        st.switch_page("pages/1_menu.py")

    # Header
    st.title("☕ Customize Your Drink")
    st.markdown(f"### Customizing: **{selected_drink}**")
    st.markdown("---")

    # Toppings data
    toppings = [
        {"name": "Pearl", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/feb1a05c-547e-42a8-b293-2cda95c33050/Topping_Pearls+%28Boba%29.png?format=1000w", "desc": "Standard boba"},
        {"name": "Honey Jelly", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/1e91bb32-9e6d-4e00-a7cf-28eaae4bee93/Topping_HoneyJelly.png?format=1000w", "desc": "Sweet boba with a taste of honey"},
        {"name": "Lychee Jelly", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/fc64125a-bc3e-476e-a0b6-4d48757b1d77/Topping_LycheeJelly+%281%29.png?format=1000w", "desc": "Tropical taste"},
        {"name": "Strawberry Boba", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/8d9305b6-65bb-4fcd-8ac3-0368c22cdaf7/Topping_StrawberryPoppingBoba.png?format=1000w", "desc": "Sour and sweet pink boba"},
        {"name": "Mango Boba", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/8da7f0f0-1587-47f9-a573-46f997b2883f/Topping_MangoPoppingBoba.png?format=1000w", "desc": "Seasonal boba"},
        {"name": "Cream", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/c9746d52-a8ab-4ecb-9c62-46c4e7d45b34/Topping_Creama.png?format=1000w", "desc": "Cheesy salt and sweet cream"},
        {"name": "Ice Cream", "price": 0.75, "emoji": "https://images.squarespace-cdn.com/content/v1/61e8bb2a2cf8670534839093/ee270494-a5e6-4080-96ae-3e21cccfa0d6/Topping_IceCream.png?format=1000w", "desc": "Fresh vanilla"},
    ]

    # base price for each drink of medium size
    base_price = 5.00

    # Size Selection
    st.markdown("## 📏 Select Size")
    st.markdown("### $1.00 for large!")
    size_option = st.radio(
        "Choose your drink size:",
        ["Medium", "Large"],
        horizontal=True
    )
    
    # Calculate size price
    size_price = 0.0
    if size_option == "Large":
        size_price = 1.00
    
    st.markdown("---")

    # Quantity Selection
    st.markdown("## 🔢 Select Quantity")
    quantity = st.number_input(
        "How many drinks would you like?",
        min_value=1,
        max_value=10,
        value=1,
        step=1,
        key="customize_quantity"  # Key for the widget
    )
    
    st.markdown("---")

    # Toppings Section
    st.markdown("## 🧋 Select Your Toppings")
    st.markdown("Choose as many as you like!")

    # Create columns for toppings grid
    cols_per_row = 2
    selected_toppings = []

    # Placing the toppings elements on the screen (one column)
    for topping in toppings:
        st.image(topping['emoji'], width=198)
        st.write(f"**{topping['name']}**")
        st.write(topping['desc'])
        st.write(f"Price: ${topping['price']:.2f}")
        
        if st.checkbox(f"Add {topping['name']}", key=topping['name']):
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
            ["No Milk", "Regular Milk", "Almond Milk", "Coconut Milk", "Oat Milk", "Soy Milk"],
            label_visibility="collapsed"
        )

    st.markdown("---")

    # Order Summary
    st.markdown("## 📋 Order Summary")

    toppings_total = sum([t['price'] for t in selected_toppings])
    total_price_per_item = base_price + toppings_total + size_price
    total_price = total_price_per_item * quantity

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Your Order:")
        st.write(f"**Drink:** {selected_drink} - ${base_price:.2f}")
        st.write(f"**Size:** {size_option} - ${size_price:.2f}")
        st.write(f"**Quantity:** {quantity}")
        
        st.write("**Toppings:**")
        if selected_toppings:
            for topping in selected_toppings:
                st.write(f"• {topping['name']} - ${topping['price']:.2f}")
        else:
            st.write("None selected")
        
        st.write("---")
        st.write(f"**Ice Level:** {ice_level}")
        st.write(f"**Sugar Level:** {sugar_level}")
        st.write(f"**Milk Type:** {milk_type}")
        st.write("---")
        st.write(f"**Price per item: ${total_price_per_item:.2f}**")
        st.success(f"**Total: ${total_price:.2f}**")

    with col2:
        if st.button("🛒 Add to Cart", type="primary"):
            # Add multiple items to cart based on quantity
            for i in range(quantity):
                order = {
                    "drink": selected_drink,
                    "size": size_option,
                    "toppings": [t['name'] for t in selected_toppings],
                    "ice": ice_level,
                    "sugar": sugar_level,
                    "milk": milk_type,
                    "price": total_price_per_item
                }
                st.session_state.cart.append(order)
            
            st.success(f"✅ Added {quantity} item(s) to cart successfully!")
            st.balloons()
        
    # Display cart count in sidebar
    if st.session_state.cart:
        st.sidebar.success(f"🛒 Cart: {len(st.session_state.cart)} item(s)")
        if st.sidebar.button("View Cart"):
            st.switch_page("pages/2.2 Cart.py")
            st.sidebar.markdown("### Your Cart:")
            for idx, item in enumerate(st.session_state.cart, 1):
                st.sidebar.markdown(f"**{idx}. {item['drink']}** - ${item['price']:.2f}")