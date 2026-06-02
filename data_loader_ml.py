import pandas as pd
import os

def load_raw_data():
    # Base folder path: dashboards/ml_prediction/raw_data/
    base_path = "dashboards/ml_prediction/raw_data"
    
    olist_orders = pd.read_csv(os.path.join(base_path, "olist_orders_dataset.csv"))
    olist_order_items = pd.read_csv(os.path.join(base_path, "olist_order_items_dataset.csv"))
    olist_customers = pd.read_csv(os.path.join(base_path, "olist_customers_dataset.csv"))
    olist_payments = pd.read_csv(os.path.join(base_path, "olist_order_payments_dataset.csv"))
    olist_reviews = pd.read_csv(os.path.join(base_path, "olist_order_reviews_dataset.csv"))
    olist_products = pd.read_csv(os.path.join(base_path, "olist_products_dataset.csv"))
    olist_sellers = pd.read_csv(os.path.join(base_path, "olist_sellers_dataset.csv"))
    product_category_name_translations = pd.read_csv(os.path.join(base_path, "product_category_name_translation.csv"))

    return (
        olist_orders,
        olist_order_items,
        olist_customers,
        olist_payments,
        olist_reviews,
        olist_products,
        olist_sellers,
        product_category_name_translations
    )