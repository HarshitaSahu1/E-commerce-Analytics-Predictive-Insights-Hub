import pandas as pd

def load_raw_data():

    olist_orders = pd.read_csv(
        r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\olist_orders_dataset.csv"
    )

    olist_order_items = pd.read_csv(
        r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\olist_order_items_dataset.csv"
    )

    olist_customers = pd.read_csv(
        r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\olist_customers_dataset.csv"
    )

    olist_payments = pd.read_csv(
        r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\olist_order_payments_dataset.csv"
    )

    olist_reviews = pd.read_csv(
        r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\olist_order_reviews_dataset.csv"
    )

    olist_products = pd.read_csv(r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\olist_products_dataset.csv")

    olist_sellers = pd.read_csv(r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\olist_sellers_dataset.csv")

    #olist_geolocations = pd.read_csv(r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\olist_geolocation_dataset.csv") 

    product_category_name_translations = pd.read_csv(r"C:\Users\Harshita Sahu\Downloads\Harshita Sahu\olist_ecommerce\cleaned_datasets\pages\ml_prediction\raw_data\product_category_name_translation.csv")


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