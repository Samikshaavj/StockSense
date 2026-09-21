import pandas as pd
import numpy as np

def engineer_features(sales_df: pd.DataFrame, products_df: pd.DataFrame):
    """
    Creates point-in-time features for machine learning.
    Target: quantity_sold for product P on day T.
    Features must only use data available *strictly before* day T.
    """
    # 1. Aggregate sales to daily level per product
    daily_sales = sales_df.groupby(['date', 'product_id'])['quantity_sold'].sum().reset_index()
    daily_sales['date'] = pd.to_datetime(daily_sales['date'])
    
    # Generate full date range to capture 0-demand days properly
    min_date = daily_sales['date'].min()
    max_date = daily_sales['date'].max()
    date_range = pd.date_range(min_date, max_date)
    
    # Cartesian product of dates and product_ids
    product_ids = products_df['product_id'].unique()
    all_dates = pd.MultiIndex.from_product([date_range, product_ids], names=['date', 'product_id']).to_frame(index=False)
    
    # Merge and fill zero
    df = pd.merge(all_dates, daily_sales, on=['date', 'product_id'], how='left')
    df['quantity_sold'] = df['quantity_sold'].fillna(0)
    
    df = df.sort_values(by=['product_id', 'date'])
    
    # 2. Lag Features (1, 7, 14, 30 days)
    # Using shift(1) means the feature is the sales from the previous day.
    df['lag_1'] = df.groupby('product_id')['quantity_sold'].shift(1)
    df['lag_7'] = df.groupby('product_id')['quantity_sold'].shift(7)
    df['lag_14'] = df.groupby('product_id')['quantity_sold'].shift(14)
    df['lag_30'] = df.groupby('product_id')['quantity_sold'].shift(30)
    
    # 3. Rolling Features (Strictly shifted to avoid leakage)
    # rolling_7 is the average of the 7 days *before* day T
    df['rolling_7_mean'] = df.groupby('product_id')['lag_1'].transform(lambda x: x.rolling(7).mean())
    df['rolling_14_mean'] = df.groupby('product_id')['lag_1'].transform(lambda x: x.rolling(14).mean())
    df['rolling_30_mean'] = df.groupby('product_id')['lag_1'].transform(lambda x: x.rolling(30).mean())
    
    # Demand standard deviation over 30 days
    df['demand_std_30'] = df.groupby('product_id')['lag_1'].transform(lambda x: x.rolling(30).std())
    
    # 4. Calendar Features
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # 5. Drop NA rows created by shifting
    df = df.dropna().reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    sales = pd.read_csv('data/sales_transactions.csv')
    prods = pd.read_csv('data/products.csv')
    feat_df = engineer_features(sales, prods)
    print(f"Generated {len(feat_df)} feature rows. Max date: {feat_df['date'].max()}, Min date: {feat_df['date'].min()}")
