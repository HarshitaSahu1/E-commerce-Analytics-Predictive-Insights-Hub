
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from pages.ml_prediction.data_loader_ml import load_raw_data
from pages.ml_prediction.preprocessing import run_preprocessing
from pages.ml_prediction.order_volume_predictor import order_volume_monthly_predictions


# 1. Load data
(
    olist_orders,
    olist_order_items,
    olist_customers,
    olist_payments,
    olist_reviews,
    olist_products,
    olist_sellers,
    olist_geolocations,
    product_category_name_translations
) = load_raw_data()


# 2. Preprocessing
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


# 3. Prediction
result = order_volume_monthly_predictions(
    mode="default",
    olist_orders=olist_orders,
    olist_order_items=olist_order_items,
    i=3
)

print(result)