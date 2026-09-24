import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
import joblib
import os
import json
from datetime import datetime
from feature_engineering import engineer_features

def mean_absolute_percentage_error(y_true, y_pred):
    """Calculates MAPE safely handling near-zero true values."""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    # Avoid division by zero by replacing zero with a small epsilon or ignoring
    mask = y_true > 0.1
    if not np.any(mask):
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def train_and_select():
    print("Loading raw data from database...")
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../stocksense.db'))
    import sqlite3
    conn = sqlite3.connect(db_path)
    sales = pd.read_sql_query("SELECT * FROM sales", conn)
    prods = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    
    print("Engineering features...")
    df = engineer_features(sales, prods)
    
    # Define features and target
    features = [
        'lag_1', 'lag_7', 'lag_14', 'lag_30',
        'rolling_7_mean', 'rolling_14_mean', 'rolling_30_mean', 'demand_std_30',
        'day_of_week', 'month', 'is_weekend'
    ]
    target = 'quantity_sold'
    
    # Drop rows with NaN features
    df = df.dropna(subset=features + [target])
    
    # Chronological Split
    # Since the database is dynamically growing, we will reserve the last 6 months for validation (3) and test (3).
    # All data before that will be used for training.
    df['date'] = pd.to_datetime(df['date'])
    max_date = df['date'].max()
    val_end = max_date - pd.DateOffset(months=3)
    train_end = val_end - pd.DateOffset(months=3)
    
    train_df = df[df['date'] < train_end]
    val_df = df[(df['date'] >= train_end) & (df['date'] < val_end)]
    test_df = df[df['date'] >= val_end]
    
    X_train, y_train = train_df[features], train_df[target]
    X_val, y_val = val_df[features], val_df[target]
    X_test, y_test = test_df[features], test_df[target]
    
    print(f"Train size: {len(X_train)}, Val size: {len(X_val)}, Test size: {len(X_test)}")
    
    # 1. Evaluate XGBoost
    print("Evaluating XGBoost Regressor...")
    model = xgb.XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror')
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    preds = np.maximum(0, preds)
    
    mae = mean_absolute_error(y_val, preds)
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    mape = mean_absolute_percentage_error(y_val, preds)
    
    results = {
        "XGBoost": {
            "MAE": float(mae),
            "RMSE": float(rmse),
            "MAPE": float(mape) if not np.isnan(mape) else None
        }
    }
    
    mape_str = f"{mape:.2f}%" if not np.isnan(mape) else "N/A"
    print("\n--- Model Evaluation Results (Validation Set) ---")
    print(f"XGBoost: MAE={mae:.3f}, RMSE={rmse:.3f}, MAPE={mape_str}")
    
    best_model_name = "XGBoost"
    best_val_rmse = rmse
    best_model = model
    
    # Re-train best model on train+val before final test evaluation
    print(f"\nRe-training {best_model_name} on Train+Val data...")
    X_train_val = pd.concat([X_train, X_val])
    y_train_val = pd.concat([y_train, y_val])
    best_model.fit(X_train_val, y_train_val)
    
    # Test Evaluation
    test_preds = np.maximum(0, best_model.predict(X_test))
    test_mae = mean_absolute_error(y_test, test_preds)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_preds))
    test_mape = mean_absolute_percentage_error(y_test, test_preds)
    
    results[best_model_name]["Test_MAE"] = float(test_mae)
    results[best_model_name]["Test_RMSE"] = float(test_rmse)
    results[best_model_name]["Test_MAPE"] = float(test_mape) if not np.isnan(test_mape) else None
    print(f"Test Set Performance -> MAE: {test_mae:.3f}, RMSE: {test_rmse:.3f}")
    
    # Persist model
    os.makedirs(os.path.join(os.path.dirname(__file__), '../models'), exist_ok=True)
    model_path = os.path.join(os.path.dirname(__file__), '../models/best_model.joblib')
    joblib.dump(best_model, model_path)
    print(f"Saved best model to {model_path}")
    
    # Save metadata
    metadata = {
        "selected_model": best_model_name,
        "training_date": datetime.now().isoformat(),
        "dataset_period": f"{df['date'].min().date()} to {df['date'].max().date()}",
        "num_samples": len(df),
        "features": features,
        "results": results
    }
    with open("models/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
if __name__ == "__main__":
    train_and_select()
