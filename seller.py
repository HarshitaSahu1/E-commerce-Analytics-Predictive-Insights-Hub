import streamlit as st
import pandas as pd
import datetime as dt

from dashboards.theme import apply_custom_theme

apply_custom_theme()

from utils.data_loader import load_data
Customer_table, Customer_360, Orders_table, Orders_360, product_360, olist_product_new, olist_order_items_new,olist_order_new,olist_order_items_360, olist_seller_new, sellers_360= load_data()


#st.set_page_config(page_title = 'Seller Fulfillment Dashboard',layout = "wide", initial_sidebar_state = 'expanded')
st.title('Seller Fulfillment Dashboard')

st.divider()

st.sidebar.header('Filters')

sellers_360['Total_order_Value'] = sellers_360['Total_items_price'] + sellers_360['Total_freight_value']

sellers_360['Sellers_grp'] = ['High Value Seller' if i >= 400 else 'Medium Value Seller' if i >= 250 else 'Low Value Seller' for i in sellers_360['Total_order_Value']]

olist_order_items_360['shipping_limit_date'] = pd.to_datetime(olist_order_items_360['shipping_limit_date'])

shipping_year = st.sidebar.multiselect('Select Shipping Year', olist_order_items_360['shipping_limit_date'].dt.year.unique(),default = olist_order_items_360['shipping_limit_date'].dt.year.unique())
shipping_quarter = st.sidebar.multiselect('Select Shipping Quarter', olist_order_items_360['shipping_limit_date'].dt.quarter.unique(),default = olist_order_items_360['shipping_limit_date'].dt.quarter.unique())
shipping_month = st.sidebar.multiselect('Select Shipping Month', olist_order_items_360['shipping_limit_date'].dt.month.unique(),default = olist_order_items_360['shipping_limit_date'].dt.month.unique())
shipping_weekend_weekday = st.sidebar.multiselect('Select Shipping Weekend/Weekday', olist_order_items_360['shipping_limit_date'].dt.day_name().apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday').unique(),default = olist_order_items_360['shipping_limit_date'].dt.day_name().apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday').unique())


shipping_filter_ids = olist_order_items_360[(olist_order_items_360['shipping_limit_date'].dt.year.isin(shipping_year))
                                            & (olist_order_items_360['shipping_limit_date'].dt.quarter.isin(shipping_quarter))
                                            & (olist_order_items_360['shipping_limit_date'].dt.month.isin(shipping_month))
                                            & (olist_order_items_360['shipping_limit_date'].dt.day_name().apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday').isin(shipping_weekend_weekday))
                                            ]['seller_id'].unique()

filtered_data = sellers_360[sellers_360['seller_id'].isin(shipping_filter_ids)]

seller_state = st.sidebar.multiselect('Select Seller State', filtered_data['seller_state'].unique(), default=filtered_data['seller_state'].unique()[0])

Total_Sellers = filtered_data['seller_id'].nunique()

Avg_Order_Value = filtered_data['Total_order_Value'].mean()

#Avg_Delivery_Days = filtered_data['Approval_To_Delivery_Days'].mean()

Avg_Order_Items = filtered_data['Total_order_items'].mean()

Cancellation_Rate = filtered_data['cancelled_orders'].sum()/filtered_data['Total_orders'].sum()*100

Avg_Review_Score = filtered_data['Avg_review_score'].mean()

Total_Seller_State = filtered_data['seller_state'].nunique()

st.markdown("""
<style>
    [data-testid="stMetricLabel"] p { font-size: 13px !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] div { font-size: 22px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

col1, col2 ,col3 = st.columns(3)

with col1:
    st.metric('Total_Sellers', Total_Sellers)

with col2:
    st.metric('Avg_Order_Value', f'${Avg_Order_Value:.2f}')

#with col3:
#    st.metric('Avg_Delivery_Days', f'{Avg_Delivery_Days:.2f} Days')

with col3:
    st.metric('Avg_Order_Items', f'{Avg_Order_Items:.2f}')





col4,col5,col6 = st.columns(3)

with col4:
    st.metric('Cancellation_Rate', f'{Cancellation_Rate:.2f}%')

with col5:
    st.metric('Avg_Review_Score', f'{Avg_Review_Score:.2f}')

with col6:
    st.metric('Total_Seller_State', Total_Seller_State)


st.divider()

import plotly.express as px

col1, col2 = st.columns(2)

with col1:
    st.subheader('Distribution Of Sellers By State')

    seller_state_counts = filtered_data.groupby('seller_state')['seller_id'].nunique().reset_index(name='Seller_Counts')

    fig = px.bar(seller_state_counts, y='seller_state', x='Seller_Counts')
    #fig.update_traces(textposition='outside') 
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("🗺️ Click here to view Seller-Customer Regional Analysis"):
        st.markdown("""
        * **Positive Market Correlation:** There is a strong **positive relationship** between seller counts and customer counts per state. The states with the highest customer density naturally attract and host the largest number of sellers.
        * **Hub Dominance:** **State SP** emerges as the absolute epicenter for both supply and demand, dominating the charts in both seller presence and customer acquisition.
        * **Business Value:** This synergy reduces cross-state logistics overhead for SP. However, it also flags a strategic need to recruit more regional sellers in other high-customer states to balance the fulfillment network.
        """)


with col2:
    st.subheader('Distribution Of Seller Groups')

    orders_dist_grps = filtered_data.groupby('Sellers_grp')['seller_id'].nunique().reset_index(name='Seller_Counts')

    fig = px.bar(orders_dist_grps, x='Sellers_grp', y='Seller_Counts',text = orders_dist_grps['Seller_Counts'] )
    fig.update_traces(textposition='outside') 
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("💰 Click here to view Seller Valuation Distribution"):
        st.markdown("""
        * **High-Value Dominance:** The business possesses a remarkably healthy structure, where **High-Value Sellers (Total Order Value $\ge$ 400)** form the largest group.
        * **The Mid-Tier Gap:** Interestingly, **Medium-Value Sellers (Order Value < 250)** constitute the smallest segment. This indicates a highly polarized merchant marketplace where sellers either scale rapidly into the top-tier or remain micro-sellers, leaving the middle tier underrepresented.
        """)

col3, col4 = st.columns(2)

with col3:
    st.subheader('Delivery Performance')

    orders_items_filtering = olist_order_items_360[olist_order_items_360['seller_id'].isin(filtered_data['seller_id'])]

    seller_based_delivery_performance = orders_items_filtering.groupby('Delivery_Performance')['order_id'].count().reset_index(name='Orders_Counts')

    fig = px.funnel(seller_based_delivery_performance, x='Orders_Counts', y='Delivery_Performance')
    fig.update_layout(
        margin=dict(l=160, r=20, t=20, b=20), 
        yaxis_title=None,                    
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("🚚 Click here to view Fulfillment & Delay Analysis"):
        st.markdown("""
        * **Core Operational Strength:** A massive volume of **~93.6K orders enjoy Smooth Delivery**, proving that the primary logistical pipeline functions reliably.
        * **Supply Chain Bottlenecks:** On the risk side, **6,240 orders faced Shipment Delays**, marking courier/transit performance as our largest single operational concern.
        * **Compound Friction:** Additionally, **2,471 orders suffered Overall Delay** (delays caused by *both* the seller handling time and the shipment transit). This compound delay severely threatens customer satisfaction and requires strict SLA enforcement for both merchants and logistics partners.
        """)


with col4:
    st.subheader('Seller Portfolio Breadth Analysis')

    sellers_category_range = filtered_data.groupby('Total_Unique_Category_Sold')['seller_id'].nunique().reset_index(name='Seller_Counts')

    fig = px.pie(sellers_category_range, names='Total_Unique_Category_Sold', values='Seller_Counts' )
    st.plotly_chart(fig, use_container_width=True)
  

    with st.expander("📦 Click here to view Seller Category Diversity Insights"):
        st.markdown("""
        * **Niche Specialization:** The data reveals that the **vast majority of sellers deal strictly in only 1 unique product category**, with a small subset expanding to 2.
        * **Operational Simplicity:** This high concentration shows that our merchants prefer operating as niche specialists rather than multi-category department stores. This keeps their inventory management clean but limits cross-selling opportunities within the same storefront.
        """)

st.subheader('Seller Group Performance')

seller_summary = filtered_data.groupby('Sellers_grp')[[
    'No_Repeat_Customers','Total_orders','Avg_review_score'
]].agg(
    Total_repeat_customer=('No_Repeat_Customers','sum'),
    Total_orders=('Total_orders','sum'),
    Avg_Review_Score=('Avg_review_score','mean')
).reset_index()

import plotly.graph_objects as go

fig = go.Figure()

fig.add_bar(x=seller_summary['Sellers_grp'], y=seller_summary['Total_orders'], name='Total Orders',text=seller_summary['Total_orders'] )
fig.add_bar(x=seller_summary['Sellers_grp'], y=seller_summary['Total_repeat_customer'], name='Repeat Customers',text=seller_summary['Total_repeat_customer'])

fig.add_trace(go.Scatter(
    x=seller_summary['Sellers_grp'],
    y=seller_summary['Avg_Review_Score'],
    mode='lines+markers',
    name='Avg Review Score',
    yaxis='y2'
))

fig.update_layout(
    barmode='group',
    yaxis2=dict(overlaying='y', side='right')
)

st.plotly_chart(fig, use_container_width=True)
with st.expander("🏆 Click here to view Multi-Dimensional Performance Insights"):
    st.markdown("""
    * **Revenue & Retention Drivers:** **High-Value Sellers** heavily dominate overall business volume, and notably, the rate of **Repeat Customers** is also exceptionally high within this elite tier.
    * **The Quality Paradox:** Conversely, while **Medium-Value Sellers** have the lowest order volumes, they boast the **highest average customer review scores**. 
    * **Strategic Takeaway:** This indicates that mid-tier sellers offer superior customer service or product quality, but lack the scale or marketing push that high-value sellers possess. The business should help these high-rating medium sellers scale up their volume.
    """)
