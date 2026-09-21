import pandas as pd
import numpy as np
import joblib
import json
import os
from ml.feature_engineering import engineer_features

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '../models/best_model.joblib')
    metadata_path = os.path.join(os.path.dirname(__file__), '../models/metadata.json')
    
    if not os.path.exists(model_path) or not os.path.exists(metadata_path):
        return None, None
        
    model = joblib.load(model_path)
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
        
    return model, metadata

def predict_demand(product_id: str, horizon_days: int = 7):
    """
    Simulates a multi-step forecast using the persisted model.
    In a real scenario, this would autoregressively predict or use a direct multi-step strategy.
    For this prototype, we'll extract the latest known features for the product
    and generate a naive horizon projection based on the model's single-step output 
    combined with historical rolling stats.
    """
    model, metadata = load_model()
    
    # Load recent data to build features
    # (In a production system, this would hit the DB, but we use the CSVs for simplicity in the ML script context.
    # The actual FastAPI backend will pass DB records).
    sales = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/sales_transactions.csv'))
    prods = pd.read_csv(os.path.join(os.path.dirname(__file__), '../data/products.csv'))
    
    # We only need the product in question
    sales = sales[sales['product_id'] == product_id]
    prods = prods[prods['product_id'] == product_id]
    
    if len(sales) == 0:
        return [0] * horizon_days
        
    df = engineer_features(sales, prods)
    if len(df) == 0:
        return [0] * horizon_days
        
    # Get the latest day's features
    latest_features = df.iloc[-1:][metadata['features']]
    
    if model is None:
        # Fallback to Baseline (Moving Average)
        pred = latest_features['rolling_7_mean'].values[0]
    else:
        pred = model.predict(latest_features)[0]
        
    pred = max(0, pred)
    
    # For a horizon, we could just return the same daily average, or introduce slight variation
    # based on the standard deviation for realism.
    std = latest_features['demand_std_30'].values[0]
    if np.isnan(std): std = 0
    
    forecast = []
    for _ in range(horizon_days):
        # Add slight noise bounded by std, ensuring >= 0
        noise = np.random.normal(0, std * 0.1) if std > 0 else 0
        forecast_val = max(0, pred + noise)
        forecast.append(round(forecast_val, 2))
        
    return forecast
