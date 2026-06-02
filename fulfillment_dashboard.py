import streamlit as st
import pandas as pd
import plotly.express as px


from dashboards.theme import apply_custom_theme

apply_custom_theme()

st.title('Order Fulfilment Dashboard')
st.divider()

# Data Loading
Customer_table = pd.read_csv('Customer_table.csv')
Orders_table = pd.read_csv('Orders_table.csv')
Orders_360 = pd.read_csv('Orders_360.csv')
olist_order_payments_dataset = pd.read_csv('olist_order_payments_dataset.csv')
olist_order_reviews_dataset = pd.read_csv('olist_order_reviews_dataset.csv')

Orders_360['Total_Order_Value'] = Orders_360['Total_Items_Price'] + Orders_360['Total_Freight_Value']

st.sidebar.header('Filters')
selected_year = st.sidebar.multiselect('Select_Year', options=sorted(Orders_360['Purchase_Year'].unique()), default=sorted(Orders_360['Purchase_Year'].unique()))
filtered_data = Orders_360[Orders_360['Purchase_Year'].isin(selected_year)]

selected_quarter = st.sidebar.multiselect('Select_Quarter', options=sorted(Orders_360['Purchase_Quarter'].unique()), default=sorted(Orders_360['Purchase_Quarter'].unique()))
filtered_data = filtered_data[filtered_data['Purchase_Quarter'].isin(selected_quarter)]

selected_month = st.sidebar.multiselect('Select_Month', options=sorted(Orders_360['Purchase_Month'].unique()), default=sorted(Orders_360['Purchase_Month'].unique()))
filtered_data = filtered_data[filtered_data['Purchase_Month'].isin(selected_month)]

Selected_weekend_weeday = st.sidebar.multiselect('Select_Weekend/Weekday', options=Orders_360['Weekends/Weekdays'].unique(), default=Orders_360['Weekends/Weekdays'].unique())
filtered_data = filtered_data[filtered_data['Weekends/Weekdays'].isin(Selected_weekend_weeday)]

# Calculations
Total_Orders = filtered_data['order_id'].nunique()
olist_payemnts_filtered = olist_order_payments_dataset[olist_order_payments_dataset['order_id'].isin(filtered_data['order_id'])]

Total_Revenue = olist_payemnts_filtered['payment_value'].sum()
Total_Order_Value = filtered_data['Total_Order_Value'].sum()
Delivered_Orders = filtered_data[filtered_data['Order_Status'] == 'delivered'].shape[0]
Cancelled_Orders = filtered_data[filtered_data['Order_Status'] == 'cancelled']['order_id'].nunique()
Avg_Delivery_Days = filtered_data['Approval_To_Delivery_Days'].mean()


Order_Cancellation_Rate = (((filtered_data[filtered_data['Order_Status'] == 'cancelled']['order_id'].nunique())*100.000)/Total_Orders)

st.markdown("""
<style>
    [data-testid="stMetricLabel"] p { font-size: 13px !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] div { font-size: 22px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

with row1_col1: 
    st.metric(label='Total Orders', value=f"{Total_Orders:,}")
with row1_col2: 
    st.metric(label='Total Revenue', value=f"${Total_Revenue:,.0f}")  # Chota dikhne ke liye decimal hata diye
with row1_col3: 
    st.metric(label='Avg Order Value', value=f"${Total_Order_Value:,.0f}")
with row1_col4: 
    st.metric(label='Delivered Orders', value=f"{Delivered_Orders:,}")

# Doosri Row: 3 Performance Metrics
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1: 
    st.metric(label='Cancelled Orders', value=f"{Cancelled_Orders:,}")
with row2_col2: 
    st.metric(label='Avg Delivery', value=f"{Avg_Delivery_Days:.1f} Days")
with row2_col3: 
    st.metric(label='Cancel Rate', value=f"{Order_Cancellation_Rate:.1f}%")

st.divider()

# Charts

col1, col2 = st.columns(2)
with col1:
    st.subheader('Orders Trend')
    purchase_orders = filtered_data.groupby('Year_Quarter_Purchase')['order_id'].nunique().reset_index(name='Orders_Count')
    fig = px.line(purchase_orders, x='Year_Quarter_Purchase', y='Orders_Count', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 Click here to view Trend Analysis (Summary)"):
        st.markdown("""
        * **Top Performer:** **Quarter 2** is performing the best among all quarters, showing the highest engagement.
        * **Stability:** **Quarter 1 and Quarter 2** have a relatively stable order volume, reflecting consistent and healthy business growth.
        * **Dip/Lowest:** **Quarter 4** has the lowest orders. This sudden drop could be attributed to shifting customer purchasing behavior or standard seasonal patterns after peak months.
        """)

with col2:
    st.subheader('Orders_Distributions Based On Order Status')
    order_category_dist = filtered_data.groupby('Order_Category')['order_id'].count().reset_index(name='order_counts').sort_values(by='order_counts', ascending=False) 
    fig = px.bar(order_category_dist, x='Order_Category', y='order_counts', text='order_counts', color='Order_Category', title='Distribution Of Order Category Based On Order_Counts')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("🗺️ Click here to view Geographic Analysis"):
        st.markdown("""
        * **Core Markets:** A few top states are contributing to the majority of the customer base. Marketing budgets should target these regions heavily.
        * **Growth Potential:** Low-volume states represent untapped markets where local promotions or better shipping rates could help scale customer acquisition.
        """)

col3,col4 = st.columns(2)

with col3:
    st.subheader('Orders_Distributions Based On Payment Type')

    order_payment_dist = olist_order_payments_dataset[olist_order_payments_dataset['order_id'].isin(filtered_data['order_id'])]
    order_payment_dist = order_payment_dist.groupby('payment_type')['order_id'].count().reset_index(name = 'order_counts')


    #Orders_distribution_payment_type = filtered_data.groupby('Unique_Payment_Type')['order_id'].count().reset_index(name='order_counts').sort_values(by='order_counts', ascending=False)
    fig = px.bar(order_payment_dist, y='order_counts', x='payment_type', title='Distribution Of Orders Based On Payment Type', text='order_counts', color='payment_type')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("💳 Click here to view Payment Method Analysis"):
        st.markdown("""
        * **Dominant Method:** **Credit Card** is the most preferred payment type by a huge margin. A large amount of the customer base is heavily dependent on credit cards, likely driven by installment options (EMIs) or reward points.
        * **Alternative Choice:** **Bank Slip (Boleto)** stands as the second most popular option, serving as a crucial method for customers who prefer non-credit cash transactions or invoice-based payments.
        * **Minor & Least Used:** **Voucher** usage is moderate, while **Debit Cards** are the least utilized method. This indicates that customers rarely prefer direct immediate bank deductions for their online shopping orders.
        """)


with col4:
    st.subheader('Orders_Distributions Based On Time_Bins')
    Orders_distribution_time_bins = filtered_data.groupby('Time_Bins')['order_id'].count().reset_index(name='order_counts').sort_values(by='order_counts', ascending=False)
    fig = px.bar(Orders_distribution_time_bins, y='order_counts', x='Time_Bins', title='Distributions Of Orders Based On Time_Bins', text='order_counts', color='Time_Bins')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("⏰ Click here to view Order Timing Analysis"):
        st.markdown("""
        * **Peak Activity:** The **Majority of customers** place their orders in the **Afternoon**, making it the absolute peak period for traffic and sales.
        * **Steady Engagement:** The afternoon rush is closely followed by the **Evening** and **Morning** periods, showing consistent purchasing activity throughout the daytime.
        * **Lowest Traffic:** Order volume is at its **Lowest during the Night**. This dip suggests that customers rarely engage in late-night online shopping, making daytime the ideal window for launching limited-time offers or flash sales.
        """)

col5,col6 = st.columns(2)

with col5:
    st.subheader('Orders_Distributions Based On avg_review_score')
    order_review_score_table = filtered_data.merge(olist_order_reviews_dataset[['order_id', 'review_score']], on='order_id', how='left')
    orders_distributions_review_scores = order_review_score_table.groupby('review_score')['order_id'].count().reset_index(name='order_counts').sort_values(by='order_counts', ascending=False)
    fig = px.pie(orders_distributions_review_scores, names='review_score', values='order_counts', title='Distribution Of Orders Based On Review Scores', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("⭐ Click here to view Review Score & Satisfaction Analysis"):
        st.markdown("""
        * **High Satisfaction:** Around **57.8% of orders** received a perfect **5-star review score**, proving that the vast majority of customers are highly satisfied with their purchase experience.
        * **Positive Sentiment:** Approximately **20% of orders** got a **4-star rating**, indicating strong overall performance and healthy customer loyalty.
        * **Areas of Concern:** On the flip side, **11% of orders** are tagged with a **1-star rating**. This significant chunk is alarming and requires immediate deep-dives into logistics, product quality, or delivery delays to fix the root cause of customer frustration.
        """)

with col6:
    st.subheader('Orders_Distributions Based on Weekdays/Weekends')
    Orders_based_on_weekend_weekdays = filtered_data.groupby('Weekends/Weekdays')['order_id'].count().reset_index(name='order_counts').sort_values(by='order_counts', ascending=False)
    fig = px.bar(Orders_based_on_weekend_weekdays, x='Weekends/Weekdays', y='order_counts', title='Distribution Of Orders Based On Weekends/Weekdays', text='order_counts', color='Weekends/Weekdays')
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📅 Click here to view Weekday vs Weekend Analysis"):
        st.markdown("""
        * **Primary Sales Driver:** The vast majority of business happens during the week, with **around 77% of total orders** being placed on **Weekdays**. This indicates high customer engagement during regular working and routine days.
        * **Weekend Performance:** Conversely, **Weekends** hold a comparatively smaller share of the order volume. This suggests that customer purchasing behavior slows down during holidays, making weekdays the most critical window for operations, logistics planning, and marketing push.
        """)

col7,col8 = st.columns(2)

with col7:
    st.subheader('Order Delivery Performance Based On Orders')
    Orders_On_Time = Orders_360[Orders_360['Avg_Estimated_vs_Actual_Days'] >= 0]['order_id'].nunique()
    Orders_Delayed = Orders_360[Orders_360['Avg_Estimated_vs_Actual_Days'] < 0]['order_id'].nunique()
    fig = px.pie(values=[Orders_On_Time, Orders_Delayed], names=['Orders_On_Time', 'Orders_Delayed'], title='Order Delivery Performance: On-Time vs Delayed Orders', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("🚚 Click here to view Delivery Performance Analysis"):
        st.markdown("""
        * **Excellent Fulfillment:** A massive **91.9% of orders** are getting delivered **on time**, which is an exceptional indicator for our brand loyalty and customer satisfaction.
        * **Bottleneck Identified:** The remaining percentage of orders are facing delivery **delays**. 
        * **Action Item:** The primary root cause for these delays is identified as **shipment/logistics delays**. We urgently need to revise our courier partner contracts, warehouse dispatch timelines, or supply chain routes to minimize this delay and safeguard customer trust.
        """)


