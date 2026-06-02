import streamlit as st
import pandas as pd
import plotly.io as pio
import plotly.express as px
import datetime as dt

# 1️⃣ DATA LOADING FUNCTION
@st.cache_data
def load_data():
    Customer_table = pd.read_csv('Customer_table.csv')
    Customer_360 = pd.read_csv('Customer_360.csv')
    Orders_table = pd.read_csv('Orders_table.csv')
    Orders_360 = pd.read_csv('Orders_360.csv')
    product_360 = pd.read_csv('product_360.csv')
    olist_product_new = pd.read_csv('olist_product_new.csv')
    olist_orders_new = pd.read_csv('olist_orders_new.csv')
    
    return Customer_table, Customer_360, Orders_table, Orders_360, product_360, olist_product_new, olist_orders_new

# Sahi tarike se 7 variables ko catch kar rahe hain
Customer_table, Customer_360, Orders_table, Orders_360, product_360, olist_product_new, olist_orders_new = load_data()

# Page Title
st.title('Customer Fulfillment Dashboard')

# Aapki global theme file jo pages folder mein hai
from dashboards.theme import apply_custom_theme
apply_custom_theme()

st.divider()

# Sidebar Filters Configuration
st.sidebar.header('Filters')

Customer_360['Order_Purchase_Year'] = pd.to_datetime(Customer_360['order_purchase_timestamp']).dt.year
Customer_360['Order_Purchase_Quarter'] = pd.to_datetime(Customer_360['order_purchase_timestamp']).dt.quarter
Customer_360['Order_Purchase_Month'] = pd.to_datetime(Customer_360['order_purchase_timestamp']).dt.month
Customer_360['Order_Purchase_Weekend/Weekday'] = pd.to_datetime(Customer_360['order_purchase_timestamp']).dt.day_name().apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')

selected_year = st.sidebar.multiselect('Select_Year', options=sorted(Customer_360['Order_Purchase_Year'].unique()), default=sorted(Customer_360['Order_Purchase_Year'].unique()))
filtered_data = Customer_360[Customer_360['Order_Purchase_Year'].isin(selected_year)]

selected_quarter = st.sidebar.multiselect('Select_Quarter', options=sorted(Customer_360['Order_Purchase_Quarter'].unique()), default=sorted(Customer_360['Order_Purchase_Quarter'].unique()))
filtered_data = filtered_data[filtered_data['Order_Purchase_Quarter'].isin(selected_quarter)]

selected_month = st.sidebar.multiselect('Select_Month', options=sorted(Customer_360['Order_Purchase_Month'].unique()), default=sorted(Customer_360['Order_Purchase_Month'].unique()))
filtered_data = filtered_data[filtered_data['Order_Purchase_Month'].isin(selected_month)]

Selected_weekend_weeday = st.sidebar.multiselect('Select_Weekend/Weekday', options=Customer_360['Order_Purchase_Weekend/Weekday'].unique(), default=Customer_360['Order_Purchase_Weekend/Weekday'].unique())
filtered_data = filtered_data[filtered_data['Order_Purchase_Weekend/Weekday'].isin(Selected_weekend_weeday)]

# Metrics Calculations
Total_Customers = filtered_data['customer_unique_id'].nunique()
Total_Repeat_Customers = filtered_data[filtered_data['Customer_Type'] == 'Repeat_Customer']['customer_unique_id'].nunique()
Total_Customer_Repeat_Rate = (Total_Repeat_Customers / Total_Customers * 100) if Total_Customers > 0 else 0
Avg_Customer_Lifetime_Value = filtered_data['Customer_Lifetime_Days'].mean()
Churn_Customer_Rate = (filtered_data[filtered_data['Recency_Segments'] == 'Dormant']['customer_unique_id'].nunique() / Total_Customers * 100) if Total_Customers > 0 else 0
Total_orders = filtered_data['Total_orders'].sum()
Cancelled_Orders_Rate = (filtered_data['canceled'].sum() / Total_orders * 100) if Total_orders > 0 else 0
Delivered_Orders_Rate = (filtered_data['delivered'].sum() / Total_orders * 100) if Total_orders > 0 else 0

st.markdown("""
<style>
    [data-testid="stMetricLabel"] p { font-size: 13px !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] div { font-size: 22px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


col1, col2, col3, col4,col5, col6, col7 = st.columns(7)

with col1: st.metric('Total Customers', f"{Total_Customers:,}")
with col2: st.metric('Repeat Customers', f"{Total_Repeat_Customers:,}")
with col3: st.metric('Repeat Rate', f'{Total_Customer_Repeat_Rate:.2f}%')
with col4: st.metric('Avg Lifetime', f'{Avg_Customer_Lifetime_Value:.2f} Days')

 #= st.columns(3)

with col5: st.metric('Churn Rate', f'{Churn_Customer_Rate:.2f}%')
with col6: st.metric('Cancelled Rate', f'{Cancelled_Orders_Rate:.2f}%')
with col7: st.metric('Delivered Rate', f'{Delivered_Orders_Rate:.2f}%')



st.divider()

# ==================== CHARTS SECTION ====================

cust_year_trends = olist_orders_new[olist_orders_new['customer_id'].isin(filtered_data['customer_id'])]

olist_orders_new['order_purchase_timestamp'] = pd.to_datetime(olist_orders_new['order_purchase_timestamp'])
cust_year_trends['orders_year'] = olist_orders_new['order_purchase_timestamp'].dt.year
cust_year_trends['orders_year'] = cust_year_trends['orders_year'].astype(str)

col1,col2 = st.columns(2)

with col1:
    st.subheader('Customer Trend')
    purchase_year_customer_trend = cust_year_trends.groupby('orders_year')['customer_id'].nunique().reset_index(name='Customer_Count')
    fig1 = px.line(purchase_year_customer_trend, x='orders_year', y='Customer_Count', markers=True)
    fig1.update_xaxes(dtick=1)
    st.plotly_chart(fig1, use_container_width=True) 
    with st.expander("📈 Click here to view Customer Acquisition & Forecast Analysis"):
        st.markdown("""
        * **Strong Upward Trend:** **Customer Acquisition** is showing a highly positive trend, consistently increasing year-over-year. This indicates that our brand reach and market penetration are expanding successfully.
        * **Future Prediction:** This continuous growth serves as a strong indicator that our business will sustain a **positive trajectory** in acquiring new customers moving forward.
        * **Strategic Move:** To capitalize on this momentum, the business should focus on optimizing onboarding funnels and scaling high-performing acquisition channels to handle the projected influx of new users efficiently.
        """)


with col2:
    st.subheader('Customer Distribution Based On State')
    customer_distribution_by_state = filtered_data.groupby('customer_state')['customer_unique_id'].nunique().reset_index(name='Customer_Count')
    fig2 = px.bar(customer_distribution_by_state, x='customer_state', y='Customer_Count', title='Customer Distribution Based On State', color='customer_state', text='Customer_Count')
    fig2.update_traces(textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)
    with st.expander("🗺️ Click here to view Geographic Dominance Analysis"):
        st.markdown("""
        * **Regional Concentration:** Our customer base is heavily concentrated in specific regions, with the **highest number of customers originating from state SP**, followed closely by **RJ**. 
        * **Market Dominance:** This clearly indicates a strong geographic dominance, where a few key states act as the primary drivers for customer acquisition and order volumes.
        * **Business Recommendation:** Operations should focus on optimizing supply chain routes and establishing closer fulfillment centers near these high-density hubs to enable faster deliveries. Simultaneously, targeted marketing campaigns can be launched in low-performing states to diversify our geographical reach.
        """)

col3,col4 = st.columns(2)

with col3:
    st.subheader('Customer Distribution Based on Customer Type')
    customer_type_distribution = filtered_data.groupby('Customer_Type')['customer_unique_id'].nunique().reset_index(name='Customer_Count')
    fig3 = px.pie(customer_type_distribution, names='Customer_Type', values='Customer_Count', title='Customer Type Distribution')
    st.plotly_chart(fig3, use_container_width=True) 
    with st.expander("🍕 Click here to view Customer Retention & Product Nature Analysis"):
        st.markdown("""
        * **One-Time Dominance:** A massive **96.9% of our customer base consists of one-time buyers**, indicating that the business revenue is currently heavily dependent on continuous new customer acquisition.
        * **Product Behavior & Lifecycle:** This high percentage is driven by our **product category behavior**. Since most products fall into the high-ticket, expensive, and long-lasting category, customers naturally do not require frequent repeat purchases.
        * **Strategic Insight:** While a low repeat-customer rate is normal for durable goods, the business should focus heavily on high-impact referral marketing and explore cross-selling complementary accessories or service plans to extract more lifetime value (LTV) from this massive one-time buyer pool.
        """)

with col4:
    st.subheader('Customer Distribution Based On RFM Segments')
    customer_distribution_based_on_rfm = filtered_data.groupby('RFM_Customer_Segment')['customer_unique_id'].nunique().reset_index(name='Customer_Count')
    fig4 = px.bar(customer_distribution_based_on_rfm, x='RFM_Customer_Segment', y='Customer_Count', title='Customer Distribution Based On RFM Segments', color='RFM_Customer_Segment', text='Customer_Count')
    st.plotly_chart(fig4, use_container_width=True) 
    with st.expander("💎 Click here to view RFM Behavioral Insights"):
        st.markdown("""
        * **Standard Base Dominance:** The majority of our user base falls under the **'Other Customer'** category. These are standard, baseline customers who do not exhibit high frequency or extreme recency but form the volume foundation of our transactions.
        * **Retention Alert:** The second most dominant segment is **'Churn Risk'** customers. This high volume of inactive users is a critical warning sign, indicating that a large portion of our acquired base is fading away and needs immediate re-engagement campaigns.
        * **The Elite Few:** On the upper end, **VIP Customers are the least represented, with only 6 customers** making the cut. While small in number, this elite group contributes disproportionately high revenue and requires exclusive premium loyalty perks or personalized retention strategies.
        """)

col5,col6 = st.columns(2)

with col5:
    st.subheader('Customer Distribution Based On Recency Segments')
    customer_distribution_based_on_recency = filtered_data.groupby('Recency_Segments')['customer_unique_id'].nunique().reset_index(name='Customer_Count')
    fig5 = px.bar(customer_distribution_based_on_recency, x='Recency_Segments', y='Customer_Count', title='Customer Distribution Based On Recency Segments', color='Recency_Segments', text='Customer_Count')
    st.plotly_chart(fig5, use_container_width=True) 
    with st.expander("⏳ Click here to view Customer Recency Analysis"):
        st.markdown("""
        * **Balanced Distribution:** Interestingly, our customer base is **almost equally split** across all three recency segments. Dormant (**32,120**), Occasional (**32,085**), and Recent (**31,884**) customers hold an identical share of the pie.
        * **Healthy Inflow vs Inactivity:** Having nearly **32k Recent customers** shows a strong and continuous incoming pipeline of new or active users. However, having an equally large pool of **Dormant customers** means customer retention needs immediate attention.
        * **Actionable Strategy:** This perfect 1/3rd split means the marketing team should divide their budget equally into three specialized funnels: **Welcome & Onboarding** for recent users, **Nurturing/Offers** for occasional users, and **Win-back/Re-engagement campaigns** to wake up the massive dormant base.
        """)

with col6:
    st.subheader('Customer Distribution Based On EMI Segments')
    customer_distribution_based_on_emi = filtered_data.groupby('Total_Segments')['customer_unique_id'].nunique().reset_index(name='Customer_Count')
    fig6 = px.bar(customer_distribution_based_on_emi, y='Customer_Count', x='Total_Segments', title='Customer Distribution Based On EMI Segments', color='Total_Segments', text='Customer_Count')
    st.plotly_chart(fig6, use_container_width=True) 
    with st.expander("💳 Click here to view EMI & Purchase Behavior Insights"):
        st.markdown("""
        * **Upfront Dominance:** The chart shows a **large dominance of Upfront Payers**. The majority of our customers prefer to clear their payments in a single transaction, ensuring immediate and healthy cash flow for the business.
        * **Polarized Financing:** Interestingly, **Heavy EMI Users** outnumber moderate users. This indicates that when customers do choose financing, they heavily lean towards long-term or high-installment options, likely to distribute the cost of our premium, high-ticket products.
        * **Strategic Opportunity:** Since **Moderate EMI Users** represent the smallest share, the business could collaborate with banking partners to introduce attractive, low-cost short-term EMI plans (e.g., 3 or 6 months no-cost EMI) to capture more budget-conscious shoppers.
        """)