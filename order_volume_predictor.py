import pandas as pd
import numpy as np

from data_loader_ml import load_raw_data
from preprocessing import run_preprocessing



def get_data(mode, olist_orders, olist_order_items, uploaded_df, manual_df):

    if mode == 'default':
        oo = olist_orders.merge(olist_order_items, on='order_id', how='left')

    elif mode == 'file':
        oo = uploaded_df.copy()

    elif mode == 'manual':
        oo = manual_df.copy()

    return oo


def create_features(oo):

    if 'order_purchase_timestamp' in oo.columns:

        oo['order_purchase_timestamp'] = pd.to_datetime(oo['order_purchase_timestamp'])

        summary = oo.groupby(
            pd.Grouper(key='order_purchase_timestamp', freq='ME')
        )['order_id'].nunique().reset_index(name='Orders_Count')

        summary = summary[summary['Orders_Count'] > 100]

    else:
        summary = oo[oo['Orders_Count'] > 100]

    # LAG FEATURES
    summary['previous_1_month_orders'] = summary['Orders_Count'].shift(1).bfill().ffill()
    summary['previous_2_month_orders'] = summary['Orders_Count'].shift(2).bfill().ffill()
    summary['rolling_mean_3'] = summary['Orders_Count'].rolling(3).mean().bfill().ffill()

    summary.dropna(inplace=True)

    X = summary.drop(['Orders_Count'], axis=1)

    if 'order_purchase_timestamp' in oo.columns:
        X['order_purchase_year'] = X['order_purchase_timestamp'].dt.year
        X['order_purchase_month'] = X['order_purchase_timestamp'].dt.month
        X.drop(columns='order_purchase_timestamp', inplace=True)

    Y = summary['Orders_Count']

    return X, Y


def train_model(X, Y, i):

    X_train = X.iloc[:-i]
    X_test = X.iloc[-i:]

    Y_train = Y.iloc[:-i]
    Y_test = Y.iloc[-i:]

    from sklearn.ensemble import RandomForestRegressor
    reg = RandomForestRegressor(n_estimators=200, random_state=101, max_depth=10)
    reg.fit(X_train, Y_train)

    reg_predict = reg.predict(X_test)

    from sklearn.metrics import mean_absolute_error
    mae = mean_absolute_error(Y_test, reg_predict)

    from sklearn.metrics import mean_absolute_percentage_error
    mape = mean_absolute_percentage_error(Y_test, reg_predict)

    next_month_predicted_orders_volume = pd.DataFrame({
        "Predicted_Months": X_test['order_purchase_month'].values,
        "Actual_Order_Volume": Y_test.values,
        "Predicted_Order_Volume": reg_predict
    })

    if mape * 100 <= 10:
        k = 'Model Performing is Excellent'
    elif mape * 100 <= 20:
        k = 'Model Performing is Good'
    elif mape * 100 <= 30:
        k = 'Model Performing Okay'
    else:
        k = 'Weak Model Prediction'

    return mape, mae, next_month_predicted_orders_volume, k, reg


def forecast_next_month(reg, X, Y):

    last_row = X.iloc[-1:].copy()
    next_row = last_row.copy()

    prev_1 = Y.iloc[-1]
    prev_2 = Y.iloc[-2]
    prev_3 = Y.iloc[-3:].mean()

    month = next_row['order_purchase_month'].iloc[0] + 1
    year = next_row['order_purchase_year'].iloc[0]

    if month > 12:
        month = 1
        year += 1

    next_row['order_purchase_month'] = month
    next_row['order_purchase_year'] = year

    next_row['previous_1_month_orders'] = prev_1
    next_row['previous_2_month_orders'] = prev_2
    next_row['rolling_mean_3'] = prev_3

    next_pred = reg.predict(next_row)[0]

    return {
        "month": month,
        "year": year,
        "predicted_orders": next_pred
    }


def order_volume_monthly_predictions(
    mode="default",
    olist_orders=None,
    olist_order_items=None,
    uploaded_df=None,
    manual_df=None,
    i=3
):

    if uploaded_df is not None:
        uploaded_df = pd.read_csv(uploaded_df)
        mode = 'file'
    elif manual_df is not None:
        mode = 'manual'
    else:
        mode = 'default'

    oo = get_data(mode, olist_orders, olist_order_items, uploaded_df, manual_df)

    X, Y = create_features(oo)

    mape, mae, backtest_df, k, reg = train_model(X, Y, i)

    # ⭐ ADD THIS (IMPORTANT FIX)
    future_prediction = forecast_next_month(reg, X, Y)

    return mape, mae, backtest_df, k, future_prediction


if __name__ == "__main__":

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

    print("Data Loaded Successfully")

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

    print("Preprocessing Completed Successfully")