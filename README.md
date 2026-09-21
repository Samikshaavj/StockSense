# StockSense - AI Inventory Intelligence & Demand Forecasting System

## Overview
StockSense is a comprehensive full-stack machine learning application built for an Indian two-wheeler spare-parts retail shop. It processes historical sales, purchases, and inventory data to forecast future demand, identify critical stock-out risks, recommend reorders, and highlight dead stock.

## Technology Stack
- **Database**: SQLite (Ingested from CSVs)
- **Machine Learning**: Scikit-learn, XGBoost, Pandas (Time-Series Forecasting, feature engineering)
- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript + Vite + Tailwind CSS

## Setup and Running

### 1. Backend & ML
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt

# Ingest data into SQLite
python backend/database/ingestion.py

# Train models
python ml/train_models.py

# Start Backend Server
python -m uvicorn backend.app.main:app --reload --port 8000
```

### 2. Frontend
Ensure you have Node.js 18+ installed.
```bash
cd frontend
npm install
npm run dev
```

## Features
- **Dashboard**: Real-time KPI summaries for critical stock risks, actionable reorders, and dead stock.
- **Inventory Management**: Searchable and filterable master list of all products.
- **Demand Forecasting**: Gradient Boosting Regressor model selecting optimal lag and rolling features chronologically without data leakage.
- **Stock-Out Risk Prediction**: Advanced logic combining predictive ML with current stock levels.

## Usage Guide
Once the application is running, open your browser and navigate to `http://localhost:5173`. You can explore the application using the left sidebar:

1. **Dashboard**: Start here to get a high-level overview of your shop's health. You'll see immediate alerts for critical stock-out risks, items that need to be reordered immediately, and your total dead stock value.
2. **Sales Analytics**: Use this page to review your past 30 days of performance. It displays your total revenue, daily revenue trends via a bar chart, and a leaderboard of your top 5 best-selling products.
3. **Inventory Master**: View your entire catalog here. You can quickly see the current stock levels, unit prices, and categories for all your products.
4. **Product Intelligence**: This is a deep-dive page for individual items. Select a specific product from the dropdown to see its stock-out risk, historical 30-day revenue, movement classification (e.g., Fast Moving), and a 14-day AI demand forecast graph. It also tells you exactly how many units to reorder.
5. **Demand Forecast**: A dedicated view for the machine learning predictions. It shows the projected daily demand for items over the next week or two, helping you plan purchases in advance.
6. **Reorder Recs**: A consolidated list of all products that require your attention for reordering. It calculates the recommended reorder quantity based on predicted demand and safety stock requirements.
7. **ML Performance**: If you're curious about how accurate the AI is, check this page. It transparently displays the model's error metrics (like RMSE and MAE) so you can trust the forecasts it provides.
