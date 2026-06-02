import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

import streamlit as st
import pandas as pd
import numpy as np

from data_loader_ml import load_raw_data
from preprocessing import run_preprocessing
from order_volume_predictor import order_volume_monthly_predictions

from theme import apply_custom_theme

apply_custom_theme()

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Order Volume Predictor", layout="wide")

st.title("📊 Order Volume Prediction Dashboard")


# ---------------------------
# SIDEBAR MODE SELECTION
# ---------------------------
mode = st.sidebar.selectbox(
    "Select Mode",
    ["Default Prediction", "Manual Input Prediction"]
)


# =========================================================
# 1️⃣ DEFAULT MODE
# =========================================================
if mode == "Default Prediction":

    st.subheader("📌 Running Default ML Pipeline")

    if st.button("🚀 Run Default Prediction"):

        with st.spinner("Loading data and running model..."):

            # Load data
            (
                olist_orders,
                olist_order_items,
                olist_customers,
                olist_payments,
                olist_reviews,
                olist_products,
                olist_sellers,
                product_category_name_translations
            ) = load_raw_data()

            # Preprocessing
            (
                olist_orders,
                olist_customers,
                olist_order_items,
                product_chn
            ) = run_preprocessing(
                olist_orders,
                olist_payments,
                olist_customers,
                olist_order_items,
                olist_products,
                product_category_name_translations
            )

            # Prediction
            result = order_volume_monthly_predictions(
                mode="default",
                olist_orders=olist_orders,
                olist_order_items=olist_order_items,
                i=3
            )

        st.success("Done ✅")

        # =========================
        # UNPACK RESULT PROPERLY
        # =========================
        mape, mae, backtest_df, status, next_pred = result

        # =========================
        # METRICS
        # =========================
        st.subheader("📊 Model Performance")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("MAPE", f"{mape*100:.2f}%")

        with col2:
            st.metric("MAE", f"{mae:.2f}")

        # =========================
        # BACKTEST
        # =========================
        st.subheader("📉 Backtest Results")
        st.dataframe(backtest_df)

        st.success(f"📌 Model Status: {status}")

        # =========================
        # NEXT MONTH PREDICTION
        # =========================
        st.subheader("🚀 Next Month Forecast")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Month", next_pred['month'])

        with col2:
            st.metric("Year", next_pred['year'])

        with col3:
            st.metric(
                "Predicted Orders",
                f"{next_pred['predicted_orders']:.0f}"
            )


# =========================================================
# 2️⃣ MANUAL MODE
# =========================================================
else:

    st.subheader("✍ Manual Data Input")

    months_input = st.text_input("Enter Months (comma separated)", "6,7,8,9,10")
    year_input = st.text_input("Enter Year", "2014")
    orders_input = st.text_input("Enter Orders (comma separated)", "20000,30000,40000,60000,80000")

    if st.button("🚀 Predict with Manual Data"):

        try:
            months = [int(i.strip()) for i in months_input.split(",")]
            orders = [int(i.strip()) for i in orders_input.split(",")]
            year = int(year_input)

            # Validation
            if len(months) < 5:
                st.error("❌ Enter at least 5 months")
                st.stop()

            if len(months) != len(orders):
                st.error("❌ Months and Orders must match")
                st.stop()

            if not np.all(np.diff(months) == 1):
                st.error("❌ Months must be continuous (e.g. 6,7,8,9,10)")
                st.stop()

            # Create dataframe
            manual_df = pd.DataFrame({
                "order_purchase_month": months,
                "order_purchase_year": [year] * len(months),
                "Orders_Count": orders
            })

            st.subheader("📌 Input Data")
            st.dataframe(manual_df)

            # Prediction
            result = order_volume_monthly_predictions(
                mode="manual",
                manual_df=manual_df
            )

            st.success("Prediction Completed ✅")

            # =========================
            # UNPACK RESULT
            # =========================
            mape, mae, backtest_df, status, next_pred = result

            # =========================
            # METRICS
            # =========================
            st.subheader("📊 Model Performance")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("MAPE", f"{mape*100:.2f}%")

            with col2:
                st.metric("MAE", f"{mae:.2f}")

            # =========================
            # BACKTEST
            # =========================
            st.subheader("📉 Backtest Results")
            st.dataframe(backtest_df)

            st.success(f"📌 Model Status: {status}")

            # =========================
            # NEXT MONTH
            # =========================
            st.subheader("🚀 Next Month Forecast")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Month", next_pred['month'])

            with col2:
                st.metric("Year", next_pred['year'])

            with col3:
                st.metric(
                    "Predicted Orders",
                    f"{next_pred['predicted_orders']:.0f}"
                )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")