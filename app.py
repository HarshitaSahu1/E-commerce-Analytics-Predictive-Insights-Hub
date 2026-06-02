import streamlit as st
import os

st.write("Current Directory Files:", os.listdir('.'))

# 1. Page Config (Sabse upar)
st.set_page_config(page_title="E-Commerce Analytics Hub", layout="wide")

# 2. Login Logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- LOGIN SCREEN ---
    st.markdown("<h1 style='text-align: center;'>🔐 Secure Access</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            if password == "12345":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Password!")
else:
    # --- NAVIGATION (Updated paths with 'dashboards' folder) ---
    
    # Define Pages (Paths updated)
    main_dashboard = st.Page("dashboards/fulfillment_dashboard.py", title="🛒 Order Fulfillment", icon="📊", default=True)
    customer_dashboard = st.Page("dashboards/customer.py", title="👥 Customer Analytics", icon="👥")
    product_dashboard = st.Page("dashboards/Products.py", title="📦 Product Insights", icon="📦")
    seller_dashboard = st.Page("dashboards/seller.py", title="🏭 Seller Performance", icon="🏭")
    prediction_dashboard = st.Page("dashboards/ml_prediction/order_volume_dashboard.py", title="🔮 Predictions", icon="📈")

    # Navigation menu
    pg = st.navigation({
        "Main Dashboards": [main_dashboard, customer_dashboard, product_dashboard, seller_dashboard],
        "ML & Predictions": [prediction_dashboard]
    })
    
    # Logout Button (Sidebar mein)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Run navigation
    pg.run()