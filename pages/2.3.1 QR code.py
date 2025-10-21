import streamlit as st
import time

st.set_page_config(page_title="QR Code Payment", page_icon="💳", layout="centered")

st.title("💳 QR Code Payment")

if 'final_order' not in st.session_state:
    st.error("No order found. Please go back to cart.")
    if st.button("⬅️ Back to Cart"):
        st.switch_page("pages/2.2 Cart.py")
else:
    order = st.session_state.final_order
    
    # Display order summary
    st.subheader("Order Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Number of items:** {len(order['items'])}")
        st.write(f"**Subtotal:** ${order['subtotal']:.2f}")
        
        if order['discount_details']:
            st.write("**Applied Discount:**")
            for detail in order['discount_details']:
                st.write(f"• {detail}")
        else:
            st.write("**Discount:** None")
    
    with col2:
        st.success(f"**Final Total: ${order['final_total']:.2f}**")
    
    st.markdown("---")
    
    # Payment processing section
    st.subheader("Payment Processing")
    
    if st.button("💳 Scan QR Code", type="primary"):
        # Create a placeholder for the processing message
        processing_placeholder = st.empty()
        
        # Show processing message for 10 seconds
        with processing_placeholder.container():
            st.image("Image/QR.png", width=170)
            st.info("💳 **Processing payment...**")
            progress_bar = st.progress(0)
            
            time.sleep(5)
        
        # Clear the processing message
        processing_placeholder.empty()
        
        # Show success message
        st.balloons()
        st.success("🎉 Payment Successful! Thank you for your order!")
        
        st.session_state.cart = []
    
    if st.button("⬅️ Back to Home"):
        st.switch_page("home.py")