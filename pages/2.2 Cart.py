import streamlit as st



st.set_page_config(page_title="Shopping Cart", page_icon="🛒", layout="wide")

if 'cart' not in st.session_state: 
    st.session_state.cart = []

st.title("🛒 Your Shopping Cart")
st.markdown("---")

if not st.session_state.cart:
    st.warning("Your cart is empty!")
    st.info("Add some delicious drinks from our menu!")
    if st.button("🍹 Back to Menu"):
        st.switch_page("pages/1_menu.py")
else:
    # Back button
    if st.button("⬅️ Back to Menu"):
        st.switch_page("pages/1_menu.py")
    
    # Display cart items
    total_before_discount = 0
    
    for idx, item in enumerate(st.session_state.cart, 1):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"### {idx}. {item['drink']}")
            st.write(f"**Size:** {item['size']}")
            if item['toppings']:
                st.write(f"**Toppings:** {', '.join(item['toppings'])}")
            else:
                st.write("**Toppings:** None")
            st.write(f"**Ice:** {item['ice']} | **Sugar:** {item['sugar']} | **Milk:** {item['milk']}")
        
        with col2:
            st.markdown(f"### ${item['price']:.2f}")
        
        with col3:
            if st.button(f"🗑️ Remove", key=f"remove_{idx}"):
                st.session_state.cart.pop(idx-1)
                st.rerun()
        
        total_before_discount += item['price']
        st.markdown("---")
    
    # Calculate item quantities for bulk discount
    item_groups = {}
    for item in st.session_state.cart:
        # we need to choose the drinks with exactly the same adds
        item_key = (
            item['drink'],
            item['size'],
            tuple(sorted(item['toppings'])),  # sort the topings, so the order is the same for all the sets
            item['ice'],
            item['sugar'],
            item['milk'],
            item['price']
        )
        
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
    
    # Calculate potential bulk discounts 
    bulk_discount_amount = 0
    bulk_discount_details = []
    best_discount_group = None
    
    # all the groups with the number >= 3
    eligible_groups = []
    for item_key, group_data in item_groups.items():
        if group_data['count'] >= 3:
            eligible_groups.append({
                'group_data': group_data,
                'discount_value': group_data['price'],  # цена одного товара (все одинаковые)
            })
    
    # we're looking for the most expensive group
    if eligible_groups:
        # sort
        eligible_groups.sort(key=lambda x: x['discount_value'], reverse=True)
        best_group = eligible_groups[0]
        best_discount_group = best_group['group_data']
        
        bulk_discount_amount = best_group['discount_value']
    
    has_bulk_eligible = bulk_discount_amount > 0
    
    # Discount section
    st.markdown("## 🎁 Select Your Discount")
    st.info("💡 **You can choose only ONE discount**")
    
    # Discount options
    discount_options = ["No discount"]
    
    # Добавляем студенческую скидку
    discount_options.append("🎓 Student Discount - 15% off entire order")
    
    # Добавляем промокод
    discount_options.append("🔑 Promo Code 20SALE - 20% off entire order")
    
    # Добавляем bulk discount если доступен
    if has_bulk_eligible:
        discount_options.append(f"📦 Bulk Discount (3 for 2) - Save ${bulk_discount_amount:.2f}")
    else:
        discount_options.append("📦 Bulk Discount - Not available")
    
    selected_discount = st.radio(
        "Choose your discount:",
        discount_options,
        index=0
    )
    
    # Promo code input (only if selected)
    promo_code = ""
    if "Promo Code" in selected_discount:
        promo_code = st.text_input("🔑 Enter promo code '20SALE':")
        if promo_code and promo_code.upper() != "20SALE":
            st.error("❌ Invalid promo code. Please enter '20SALE'")
            selected_discount = "No discount"
    
    # Calculate final discount
    discount_amount = 0
    discount_details = []
    
    if "Student Discount" in selected_discount:
        discount_amount = total_before_discount * 0.15
        discount_details.append(f"Student discount (15%): -${discount_amount:.2f}")
    
    elif "Promo Code" in selected_discount and promo_code.upper() == "20SALE":
        discount_amount = total_before_discount * 0.20
        discount_details.append(f"Promo code 20SALE (20%): -${discount_amount:.2f}")
    
    elif "Bulk Discount" in selected_discount and has_bulk_eligible:
        discount_amount = bulk_discount_amount
        discount_details.extend(bulk_discount_details)
    
    final_total = total_before_discount - discount_amount
    
    # Order summary
    st.markdown("## 💰 Order Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price Details")
        st.write(f"**Subtotal:** ${total_before_discount:.2f}")
        
        if discount_details:
            st.write("**Applied Discount:**")
            for detail in discount_details:
                st.write(f"• {detail}")
        else:
            st.write("**Discount:** None")
        
        st.write("---")
        st.success(f"### **Total: ${final_total:.2f}**")
    
    with col2:
        st.subheader("Discount Information")
        st.info("""
        **Available Discounts (choose one):**
        
        🎓 **Student Discount** - 15% off entire order
        
        🔑 **Promo Code** - Use "20SALE" for 20% off entire order
        
        📦 **Bulk Discount** - Buy 3 identical drinks, pay for 2
          • Drinks must be COMPLETELY identical (same drink, size, 
            toppings, ice, sugar, milk)
          • Applied only ONCE to the most expensive eligible group
          • Example: If you have multiple groups with 3+ identical drinks,
            discount applies to group with highest individual price
        """)
        
        # Show eligible groups for bulk discount
        if eligible_groups:
            st.subheader("Eligible Groups for Bulk Discount:")
            for i, group_info in enumerate(eligible_groups):
                group_data = group_info['group_data']
                group_desc = f"{group_data['drink_name']} ({group_data['size']})"
                if group_data['toppings']:
                    group_desc += f" with {', '.join(group_data['toppings'])}"
                group_desc += f" | {group_data['ice']}, {group_data['sugar']}, {group_data['milk']}"
                
                if group_info == eligible_groups[0]:
                    st.write(f"{i+1}. **{group_desc}** - ${group_data['price']:.2f} each (BEST - selected)")
                else:
                    st.write(f"{i+1}. {group_desc} - ${group_data['price']:.2f} each")
    
    st.markdown("---")
    
    # Payment methods
    st.markdown("## 💳 Payment Method")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📱 Pay with QR Code", type="primary", use_container_width=True):
            # Save order details to session state for receipt
            st.session_state.final_order = {
                "items": st.session_state.cart.copy(),
                "subtotal": total_before_discount,
                "discount_amount": discount_amount,
                "discount_details": discount_details,
                "final_total": final_total,
                "selected_discount": selected_discount
            }
            st.switch_page("pages/2.3.1 QR code.py")
    
    with col2:
        if st.button("💳 Pay with Card", type="secondary", use_container_width=True):
            # Save order details to session state for receipt
            st.session_state.final_order = {
                "items": st.session_state.cart.copy(),
                "subtotal": total_before_discount,
                "discount_amount": discount_amount,
                "discount_details": discount_details,
                "final_total": final_total,
                "selected_discount": selected_discount
            }
            st.switch_page("pages/2.3 Card payment.py")
    
    # Clear cart button
    st.markdown("---")
    if st.button("🗑️ Clear Entire Cart", type="secondary"):
        st.session_state.cart = []
        st.rerun()

# Display cart count in sidebar
if st.session_state.cart:
    st.sidebar.success(f"🛒 Cart: {len(st.session_state.cart)} item(s)")
    st.sidebar.markdown("### Your Cart Preview:")
    for idx, item in enumerate(st.session_state.cart[:3], 1):  # Show first 3 items
        st.sidebar.markdown(f"**{idx}. {item['drink']}** - ${item['price']:.2f}")
    if len(st.session_state.cart) > 3:
        st.sidebar.info(f"... and {len(st.session_state.cart) - 3} more items")
else:
    st.sidebar.info("🛒 Cart is empty")