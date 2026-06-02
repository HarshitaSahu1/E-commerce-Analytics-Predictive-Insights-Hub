
import streamlit as st
import pandas as pd
@st.cache_data
def load_data():
    Customer_table = pd.read_csv('Customer_table.csv')
    Customer_360 = pd.read_csv('Customer_360.csv')
    Orders_table = pd.read_csv('Orders_table.csv')
    Orders_360 = pd.read_csv('Orders_360.csv')
    product_360 = pd.read_csv('product_360.csv')
    olist_product_new = pd.read_csv('olist_product_new.csv')
    olist_order_items_new = pd.read_csv('olist_order_items_new.csv')
    olist_order_new = pd.read_csv('olist_orders_new.csv')
    olist_order_items_360 = pd.read_csv('olist_order_items_360.csv')
    olist_seller_new = pd.read_csv('olist_seller_new.csv')
    sellers_360 = pd.read_csv('sellers_360.csv')
    
    return Customer_table, Customer_360, Orders_table, Orders_360, product_360, olist_product_new, olist_order_items_new,olist_order_new,olist_order_items_360, olist_seller_new, sellers_360