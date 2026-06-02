import streamlit as st

def apply_custom_theme():
    st.markdown("""
    <style>
    /* ===================================================
       1️⃣ MAIN BACKGROUND & CONTAINER
    =================================================== */
    /* Naye Streamlit versions ke liye background target */
    .stAppViewContainer, .stMainBlockContainer, .main {
        background-color: #F5F9FF !important;
    }
    
    .block-container {
        background-color: #F5F9FF !important;
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* ===================================================
       2️⃣ KPI CARDS (METRICS)
    =================================================== */
    [data-testid="stMetric"], [data-testid="metric-container"] {
        background-color: #E6F0FF !important;
        border: 2px solid #1E3A8A !important;
        border-radius: 14px !important;
        padding: 18px !important;
        box-shadow: 0px 4px 6px rgba(30, 58, 138, 0.1) !important;
    }
    
    /* KPI LABEL */
    [data-testid="stMetricLabel"] p {
        color: #1E3A8A !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    /* KPI VALUE */
    [data-testid="stMetricValue"] div {
        color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 32px !important;
    }
    
    /* ===================================================
       3️⃣ HEADINGS & TEXT
    =================================================== */
    h1, [data-testid="stHeader"] h1 {
        color: #0F172A !important;
        font-weight: 900 !important;
        font-size: 34px !important;
    }
    
    h2, [data-testid="stHeader"] h2 {
        color: #1E3A8A !important;
        font-weight: 800 !important;
    }
    
    h3, h4 {
        color: #1D4ED8 !important;
        font-weight: 700 !important;
    }
    
    /* ===================================================
       4️⃣ PLOTLY CHARTS WRAPPER
    =================================================== */
    .stPlotlyChart, .stPyplot {
        background-color: #FFFFFF !important;
        border-radius: 14px !important;
        padding: 12px !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* ===================================================
       5️⃣ SIDEBAR NAV & BACKGROUND
    =================================================== */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        background-color: #1E3A8A !important;
    }
    
    /* Sidebar ke andar ka saara text white karne ke liye */
    [data-testid="stSidebar"] *, [data-testid="stSidebarNavigation"] * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    /* Active/Selected page highlight color in sidebar navigation */
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* ===================================================
       6️⃣ INPUT FIELDS & SELECT BOX
    =================================================== */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #1E3A8A !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="select"] * {
        color: #0F172A !important; /* TAki dropdown text readable rahe */
    }
    
    /* ===================================================
       7️⃣ BUTTONS
    =================================================== */
    .stButton > button {
        background-color: #1E3A8A !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
    }
    
    .stButton > button:hover {
        background-color: #0F172A !important;
    }
    </style>
    """, unsafe_allow_html=True)