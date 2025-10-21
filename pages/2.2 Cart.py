import streamlit as st

# Configure the page settings
st.set_page_config(page_title="Shopping Cart", page_icon="🛒", layout="wide")

# Initialize cart in session state if it doesn't exist
if 'cart' not in st.session_state: 
    st.session_state.cart = []

# Page title and separator
st.title("🛒 Your Shopping Cart")
st.markdown("---")

# Check if cart is empty
if not st.session_state.cart:
    # Display empty cart message and back to menu button
    st.warning("Your cart is empty!")
    st.info("Add some delicious drinks from our menu!")
    if st.button("🍹 Back to Menu"):
        st.switch_page("pages/1_menu.py")
else:
    # Back button to return to menu
    if st.button("⬅️ Back to Menu"):
        st.switch_page("pages/1_menu.py")

    st.markdown("---")
    
    # Display cart items and calculate total before discount
    total_before_discount = 0
    
    # Loop through each item in the cart with index
    for idx, item in enumerate(st.session_state.cart, 1):
        # Create columns for item display, price, and remove button
        col1, col2, col3 = st.columns([3, 1, 1])
        
        # Column 1: Item details
        with col1:
            st.markdown(f"### {idx}. {item['drink']}")
            st.write(f"**Size:** {item['size']}")
            # Display toppings if any, otherwise show "None"
            if item['toppings']:
                st.write(f"**Toppings:** {', '.join(item['toppings'])}")
            else:
                st.write("**Toppings:** None")
            st.write(f"**Ice:** {item['ice']} | **Sugar:** {item['sugar']} | **Milk:** {item['milk']}")
        
        # Column 2: Item price
        with col2:
            st.markdown(f"### ${item['price']:.2f}")
        
        # Column 3: Remove button
        with col3:
            if st.button(f"🗑️ Remove", key=f"remove_{idx}"):
                # Remove item from cart and refresh page
                st.session_state.cart.pop(idx-1)
                st.rerun()
        
        # Add item price to total and display separator
        total_before_discount += item['price']
        st.markdown("---")
    
    # Group identical items for bulk discount calculation
    item_groups = {}
    for item in st.session_state.cart:
        # Create a unique key for each item configuration
        item_key = (
            item['drink'],
            item['size'],
            tuple(sorted(item['toppings'])),  # Sort toppings for consistent grouping
            item['ice'],
            item['sugar'],
            item['milk'],
            item['price']
        )
        
        # Add to existing group or create new one
        if item_key in item_groups:
            item_groups[item_key]['count'] += 1
            item_groups[item_key]['items'].append(item)
        else:
            item_groups[item_key] = {
                'count': 1,
                'items': [item],
                'drink_name': item['drink'],
                'size': item['size'],
                'toppings': item['toppings'],
                'ice': item['ice'],
                'sugar': item['sugar'],
                'milk': item['milk'],
                'price': item['price']
            }
    
    # Calculate potential bulk discounts (buy 3 for 2)
    bulk_discount_amount = 0
    bulk_discount_details = []
    best_discount_group = None
    
    # Find groups eligible for bulk discount (3 or more identical items)
    eligible_groups = []
    for item_key, group_data in item_groups.items():
        if group_data['count'] >= 3:
            eligible_groups.append({
                'group_data': group_data,
                'discount_value': group_data['price'],  # Price of one item (all are identical)
            })
    
    # Select the most expensive eligible group for discount
    if eligible_groups:
        # Sort groups by discount value (price) in descending order
        # Lambda in a sort function showes the key we use to sort. In our case, 
        # we sort by the price from the most expensive one to the least expensive one
        eligible_groups.sort(key=lambda x: x['discount_value'], reverse=True)
        best_group = eligible_groups[0]
        best_discount_group = best_group['group_data']
        
        # Set discount amount to the price of one item (buy 3, pay for 2)
        bulk_discount_amount = best_group['discount_value']
    
    # Check if bulk discount is available
    has_bulk_eligible = bulk_discount_amount > 0
    
    # Discount selection section
    st.markdown("## 🎁 Select Your Discount")
    st.info("💡 **You can choose only ONE discount**")
    
    # Available discount options
    discount_options = ["No discount"]
    
    # Add student discount option
    discount_options.append("🎓 Student Discount - 15% off entire order")
    
    # Add promo code option
    discount_options.append("🔑 Promo Code - 20% off entire order")
    
    # Add bulk discount option if available
    if has_bulk_eligible:
        discount_options.append(f"📦 Bulk Discount (3 for 2) - Save ${bulk_discount_amount:.2f}")
    else:
        discount_options.append("📦 Bulk Discount - Not available")
    
    # Discount selection radio buttons
    selected_discount = st.radio(
        "Choose your discount:",
        discount_options,
        index=0
    )
    
    # Promo code input field (only shown when promo code option is selected)
    promo_code = ""
    if "Promo Code" in selected_discount:
        promo_code = st.text_input("🔑 Enter promo code:")
        # Validate promo code
        if promo_code and promo_code.upper() != "20SALE":
            st.error("❌ Invalid promo code. Please enter correct discount")
            selected_discount = "No discount"
    
    # Calculate final discount amount based on selected discount
    discount_amount = 0
    discount_details = []
    
    # Student discount calculation (15% off)
    if "Student Discount" in selected_discount:
        discount_amount = total_before_discount * 0.15
        discount_details.append(f"Student discount (15%): -${discount_amount:.2f}")
    
    # Promo code discount calculation (20% off)
    elif "Promo Code" in selected_discount and promo_code.upper() == "20SALE":
        discount_amount = total_before_discount * 0.20
        discount_details.append(f"Promo code 20SALE (20%): -${discount_amount:.2f}")
    
    # Bulk discount calculation (buy 3, pay for 2)
    elif "Bulk Discount" in selected_discount and has_bulk_eligible:
        discount_amount = bulk_discount_amount
        discount_details.extend(bulk_discount_details)
    
    # Calculate final total after discount
    final_total = total_before_discount - discount_amount
    
    # Order summary section
    st.markdown("## 💰 Order Summary")
    
    # Create two columns for order details and discount info
    col1, col2 = st.columns(2)
    
    # Column 1: Price breakdown
    with col1:
        st.subheader("Price Details")
        st.write(f"**Subtotal:** ${total_before_discount:.2f}")
        
        # Display applied discounts if any
        if discount_details:
            st.write("**Applied Discount:**")
            for detail in discount_details:
                st.write(f"• {detail}")
        else:
            st.write("**Discount:** None")
        
        st.write("---")
        st.success(f"### **Total: ${final_total:.2f}**")
    
    # Column 2: Discount information and eligible groups
    with col2:
        st.subheader("Discount Information")
        st.info("""
        **Available Discounts (choose one):**
        
        🎓 **Student Discount** - 15% off entire order
        
        🔑 **Promo Code** - Use promo codefor 20% off entire order
        
        📦 **Bulk Discount** - Buy 3 identical drinks, pay for 2
          • Drinks must be COMPLETELY identical (same drink, size, 
            toppings, ice, sugar, milk)
          • Applied only ONCE to the most expensive eligible group
          • Example: If you have multiple groups with 3+ identical drinks,
            discount applies to group with highest individual price
        """)
        
        # Display eligible groups for bulk discount
        if eligible_groups:
            st.subheader("Eligible Groups for Bulk Discount:")
            for i, group_info in enumerate(eligible_groups):
                group_data = group_info['group_data']
                # Create description for the group
                group_desc = f"{group_data['drink_name']} ({group_data['size']})"
                if group_data['toppings']:
                    group_desc += f" with {', '.join(group_data['toppings'])}"
                group_desc += f" | {group_data['ice']}, {group_data['sugar']}, {group_data['milk']}"
                
                # Highlight the best (selected) group
                if group_info == eligible_groups[0]:
                    st.write(f"{i+1}. **{group_desc}** - ${group_data['price']:.2f} each (BEST - selected)")
                else:
                    st.write(f"{i+1}. {group_desc} - ${group_data['price']:.2f} each")
    
    st.markdown("---")
    
    # Payment methods section
    st.markdown("## 💳 Payment Method")
    
    # Create two columns for payment options
    col1, col2 = st.columns(2)
    
    # QR code payment button
    with col1:
        if st.button("📱 Pay with QR Code", type="primary", use_container_width=True):
            # Save order details to session state for receipt page
            st.session_state.final_order = {
                "items": st.session_state.cart.copy(),
                "subtotal": total_before_discount,
                "discount_amount": discount_amount,
                "discount_details": discount_details,
                "final_total": final_total,
                "selected_discount": selected_discount
            }
            # Navigate to QR code payment page
            st.switch_page("pages/2.3.1 QR code.py")
    
    # Card payment button
    with col2:
        if st.button("💳 Pay with Card", type="secondary", use_container_width=True):
            # Save order details to session state for receipt page
            st.session_state.final_order = {
                "items": st.session_state.cart.copy(),
                "subtotal": total_before_discount,
                "discount_amount": discount_amount,
                "discount_details": discount_details,
                "final_total": final_total,
                "selected_discount": selected_discount
            }
            # Navigate to card payment page
            st.switch_page("pages/2.3 Card payment.py")
    
    # Clear cart button
    st.markdown("---")
    if st.button("🗑️ Clear Entire Cart", type="secondary"):
        st.session_state.cart = []
        st.rerun()

# Sidebar cart preview
if st.session_state.cart:
    # Display cart item count and preview
    st.sidebar.success(f"🛒 Cart: {len(st.session_state.cart)} item(s)")
    st.sidebar.markdown("### Your Cart Preview:")
    # Show first 3 items in cart preview
    for idx, item in enumerate(st.session_state.cart[:3], 1):
        st.sidebar.markdown(f"**{idx}. {item['drink']}** - ${item['price']:.2f}")
    # Show count of additional items if more than 3
    if len(st.session_state.cart) > 3:
        st.sidebar.info(f"... and {len(st.session_state.cart) - 3} more items")
else:
    # Display empty cart message in sidebar
    st.sidebar.info("🛒 Cart is empty")