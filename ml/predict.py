import pandas as pd
import numpy as np
import joblib
import json
import os
from ml.feature_engineering import engineer_features

import functools

@functools.lru_cache(maxsize=1)
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '../models/best_model.joblib')
    metadata_path = os.path.join(os.path.dirname(__file__), '../models/metadata.json')
    
    if not os.path.exists(model_path) or not os.path.exists(metadata_path):
        return None, None
        
    model = joblib.load(model_path)
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
        
    return model, metadata

import functools

@functools.lru_cache(maxsize=1)
def load_data():
    sales = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/sales_transactions.csv'))
    prods = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/products.csv'))
    features_df = engineer_features(sales, prods)
    return features_df

@functools.lru_cache(maxsize=1024)
def predict_demand(product_id: str, horizon_days: int = 7):
    """
    Simulates a multi-step forecast using the persisted model.
    """
    model, metadata = load_model()
    
    features_df = load_data()
    product_features = features_df[features_df['product_id'] == product_id]
    
    if len(product_features) == 0:
        return [0] * horizon_days
        
    latest_features = product_features.iloc[-1:][metadata['features']]
    
    if model is None:
        pred = latest_features['rolling_7_mean'].values[0]
    else:
        pred = model.predict(latest_features)[0]
        
    pred = max(0, pred)
    
    std = latest_features['demand_std_30'].values[0]
    if np.isnan(std): std = 0
    
    forecast = []
    for _ in range(horizon_days):
        noise = np.random.normal(0, std * 0.1) if std > 0 else 0
        forecast_val = max(0, pred + noise)
        forecast.append(round(forecast_val, 2))
        
    return forecast
