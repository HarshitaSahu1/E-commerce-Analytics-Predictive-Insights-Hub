import streamlit as st
import pandas as pd

from utils.data_loader import load_data

from theme import apply_custom_theme

apply_custom_theme()

Customer_table, Customer_360, Orders_table, Orders_360, product_360, olist_product_new, olist_order_items_new,olist_order_new,olist_order_items_360, olist_seller_new, sellers_360= load_data()

#st.set_page_config(page_title = 'Product Fulfillment Dashboard',layout = "wide", initial_sidebar_state = 'expanded')
st.title('Product Fulfillment Dashboard')
st.divider()


st.sidebar.header('Filters')

product_360['Total_order_value'] = product_360['Total_items_price'] + product_360['Total_freight_value']

product_360['Avg_items_price'] = product_360['Total_items_price']/product_360['Total_order_items']

data_dim = Orders_360[['Purchase_Year', 'Purchase_Quarter', 'Purchase_Month', 'Weekends/Weekdays']].drop_duplicates()

Selected_Year = st.sidebar.multiselect('Select Year',options = sorted(data_dim['Purchase_Year'].unique()), default = sorted(data_dim['Purchase_Year'].unique()))

Selected_Quarter = st.sidebar.multiselect('Select Quarter', options = sorted(data_dim['Purchase_Quarter'].unique()), default = sorted(data_dim['Purchase_Quarter'].unique()))

Selected_Month = st.sidebar.multiselect('Select Month',options = sorted(data_dim['Purchase_Month'].unique()), default = sorted(data_dim['Purchase_Month'].unique()))

Selected_Weekend_Weekday = st.sidebar.multiselect('Select Weekend/Weekday', options = data_dim['Weekends/Weekdays'].unique(), default = data_dim['Weekends/Weekdays'].unique())


unique_orders_filtered =Orders_360[(Orders_360['Purchase_Year'].isin(Selected_Year)) & (Orders_360['Purchase_Quarter'].isin(Selected_Quarter)) & (Orders_360['Purchase_Month'].isin(Selected_Month)) & (Orders_360['Weekends/Weekdays'].isin(Selected_Weekend_Weekday))]['order_id'].unique()

unique_products_filtered = olist_order_items_new[olist_order_items_new['order_id'].isin(unique_orders_filtered)]['product_id'].unique()

filtered_data = product_360[product_360['product_id'].isin(unique_products_filtered)]


Total_Products = filtered_data['product_id'].nunique()
Avg_Product_Price = filtered_data['Total_items_price'].mean()
Avg_Review_Score = filtered_data['Avg_Review_Score'].mean()
Top_Category_Bin = filtered_data.groupby('Category_Bin')['Total_orders'].sum().idxmax()
Top_Product = filtered_data.groupby('product_category')['Total_orders'].sum().idxmax()
Top_Expensive_Product = filtered_data.groupby('Product_Category_Basket')['Items_Price_Mean'].mean().idxmax()
Top_Reviewed_Product = filtered_data.groupby('product_category')['Avg_Review_Score'].mean().idxmax()

st.markdown("""
<style>
    [data-testid="stMetricLabel"] p { font-size: 13px !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] div { font-size: 22px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

col1, col2 ,col3,col4 = st.columns(4)

with col1:
    st.metric('Total Products', Total_Products)

with col2:
    st.metric('Avg Product Price', f'R$ {Avg_Product_Price:,.2f}')

with col3:
    st.metric('Avg Review Score', f'{Avg_Review_Score:.2f}')

with col4:
    st.metric('Top Category Bin', Top_Category_Bin)

col5,col6,col7 = st.columns(3)

with col5:
    st.metric('Top Product', Top_Product)

with col6:
    st.metric('Top Expensive Product', Top_Expensive_Product)

with col7:
    st.metric('Top Reviewed Product', Top_Reviewed_Product)

import plotly.express as px

col1,col2 = st.columns(2)

with col1:
    st.subheader('Products Trend')
    Category_bin_orders_dist = filtered_data.groupby('Category_Bin')['Total_order_items'].sum().reset_index().sort_values(by = 'Total_order_items', ascending = False)
    fig = px.bar(Category_bin_orders_dist, x = 'Category_Bin', y = 'Total_order_items', title = 'Total Order Items by Category Bin', labels = {'Total_order_items': 'Total Order Items', 'Category_Bin': 'Category Bin'},text = 'Total_order_items' )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📈 Click here to view Product Category Tier Analysis"):
        st.markdown("""
        * **Premium Market Drive:** The trend shows that **expensive category products heavily dominate** our catalog and transaction volume, followed by medium-tier products.
        * **High Purchasing Power:** This clear preference for higher-priced items suggests that our user base consists of high-intent buyers who value premium/durable products and have a strong purchasing capacity.
        """)



product_category_based_total_orders_value_avg_items = filtered_data.groupby('product_category')[['Total_order_value','Avg_items_price']].agg({'Total_order_value': 'sum', 'Avg_items_price': 'mean'}).reset_index().sort_values(by = 'Total_order_value', ascending = False).head(5)

import plotly.graph_objects as go

with col2:
    st.subheader('Top5 Product_Categories Order Value & Avg_item_price')
    fig = go.Figure()

    # Bar
    fig.add_trace(
        go.Bar(
            x=product_category_based_total_orders_value_avg_items['product_category'],
            y=product_category_based_total_orders_value_avg_items['Total_order_value'],
            name='Total Order Value'
        )
    )

    # Line
    fig.add_trace(
        go.Scatter(
            x=product_category_based_total_orders_value_avg_items['product_category'],
            y=product_category_based_total_orders_value_avg_items['Avg_items_price'],
            mode='lines+markers',
            name='Avg Item Price',
            yaxis='y2'
        )
    )

    fig.update_layout(
        #title='Top 5 Product Categories',
        xaxis_title='Product Category',
        yaxis_title='Total Order Value',
        yaxis2=dict(
            title='Avg Item Price',
            overlaying='y',
            side='right'
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📊 Click here to view Category Revenue vs Quality Insights"):
        st.markdown("""
        * **The Revenue Leader's Risk:** **Health and Beauty** emerges as the highest contributor to overall order value. However, it suffers from a **low average review score**, which is highly concerning. This gap signals potential underlying issues in product authenticity, high customer expectations, or delivery condition.
        * **Premium Performers:** On the other hand, categories like **Watches and Gifts** command both high order values and high average item prices, proving to be extremely lucrative and highly valued segments for the business.
        """)




top_10_product_based_on_freight_value = filtered_data.groupby('Product_Category_Basket')[['Total_freight_value']].sum().reset_index().sort_values(by = 'Total_freight_value', ascending = False).head(10)


st.subheader('Top 10 Products Based Freight Value')
fig = px.scatter(top_10_product_based_on_freight_value, x = 'Product_Category_Basket', y = 'Total_freight_value', title = 'Top 10 Product Based On Total Freight Value', labels = {'Total_freight_value': 'Total Freight Value', 'Product_Category_Basket': 'Product Category Basket'},size = 'Total_freight_value', color = 'Product_Category_Basket')
fig.update_xaxes(
    tickangle=45,       # Labels ko 45-degree par ghuma diya taaki overlap na ho
    #title=dict(standoff=25)  # Main x-axis title ko labels se niche push kiya
)

# 🛠️ FIXED 3: Bottom margin badhaya taaki rotated text screen se bahar na jaye
fig.update_layout(
    margin=dict(b=120),  # Bottom padding di rotated labels ke liye
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)
with st.expander("📦 Click here to view Shipping Cost & Logistics Burden Analysis"):
    st.markdown("""
    * **Logistics Heavyweights:** This analysis clearly isolates our most expensive products to ship. **Home Furniture** leads the freight cost burden, closely followed by **Electronics**. This is highly logical due to their volumetric weight, bulkiness, and specialized handling requirements.
    * **Lightweight Efficiency:** Conversely, **Office Business** items incur the least freight cost among the top tier, representing a highly margin-friendly logistics profile.
    * **Action Item:** The business must explore regional fulfillment centers specifically for furniture and electronics to cut down these massive cross-regional freight costs.
    """)


#filtered_products_id = olist_order_items_360['product_id'].isin(filtered_data['product_id'].unique())

filters_order_items = olist_order_items_360.merge(filtered_data,on = 'product_id',how = 'right')



filtersss = filters_order_items.groupby(['review_status','Product_Category_Basket'])['order_id'].count().reset_index(name = 'Orders_Counts').sort_values(by = 'Orders_Counts', ascending = False)
st.subheader('Product Category Basket Based On Total orders & Review Status')
fig = px.bar(filtersss, x = 'Product_Category_Basket', y = 'Orders_Counts', color = 'review_status',  labels = {'Product_Category_Basket': 'Product Category Basket', 'Orders_Counts': 'Order Counts', 'review_status': 'Review Status'})
st.plotly_chart(fig, use_container_width=True)
with st.expander("🛒 Click here to view Basket Sentiment Analysis"):
    st.markdown("""
    * **Overwhelmingly Positive Sentiment:** Across all product category baskets, **Positive Reviews consistently contribute the highest share** to total orders. 
    * **Healthy Core Operations:** This uniform dominance of positive sentiment is an excellent health indicator for the business, showing that regardless of the category, the majority of customers walk away satisfied with their purchases.
    """)




