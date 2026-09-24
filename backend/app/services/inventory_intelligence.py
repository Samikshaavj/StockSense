from sqlalchemy.orm import Session
from backend.database.schema import Product, Inventory, Sale
from backend.app.schemas.schemas import *
from ml.predict import predict_demand
import pandas as pd
from datetime import datetime, timedelta

def get_current_stock(db: Session, product_id: str) -> int:
    # Get latest inventory record for this product
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).order_by(Inventory.date.desc()).first()
    return inv.closing_stock if inv else 0

def get_current_business_date(db: Session):
    return datetime.now().date()

def get_stock_status(current_stock: int, safety_stock: int) -> str:
    if current_stock <= 0:
        return "Out of Stock"
    if current_stock <= safety_stock:
        return "Critical"
    if current_stock <= safety_stock * 1.5:
        return "Low"
    if current_stock <= safety_stock * 2:
        return "Monitor"
    return "Healthy"

def calculate_stock_out_risk(db: Session, product_id: str) -> StockOutRisk:
    product = db.query(Product).filter(Product.product_id == product_id).first()
    current_stock = get_current_stock(db, product_id)
    
    forecast = predict_demand(product_id, horizon_days=7)
    predicted_daily = sum(forecast) / len(forecast) if forecast else 0
    
    if predicted_daily <= 0.05:
        days_remaining = 999.0 # Effectively infinite
        risk_level = "Low"
    else:
        days_remaining = current_stock / predicted_daily
        if days_remaining <= 3:
            risk_level = "Critical"
        elif days_remaining <= 7:
            risk_level = "High"
        elif days_remaining <= 14:
            risk_level = "Medium"
        else:
            risk_level = "Low"
            
    return StockOutRisk(
        product_id=product.product_id,
        product_name=product.product_name,
        current_stock=current_stock,
        predicted_daily_demand=predicted_daily,
        days_remaining=days_remaining,
        risk_level=risk_level
    )

def calculate_reorder_recommendation(db: Session, product_id: str) -> ReorderRecommendation:
    product = db.query(Product).filter(Product.product_id == product_id).first()
    current_stock = get_current_stock(db, product_id)
    
    planning_horizon = 14 # Plan for 2 weeks
    forecast = predict_demand(product_id, horizon_days=planning_horizon)
    expected_demand = sum(forecast)
    
    # Safety stock based on minimum level or a simple standard deviation of historical demand
    # For simplicity, we use the minimum_stock_level from the product table as the safety baseline
    safety_stock = product.minimum_stock_level or 5
    
    required_stock = expected_demand + safety_stock
    reorder_quantity = max(0, int(required_stock - current_stock))
    
    if reorder_quantity > 0 and current_stock <= safety_stock:
        status = "Reorder Now"
    elif reorder_quantity > 0:
        status = "Reorder Soon"
    elif current_stock < (safety_stock * 1.5):
        status = "Monitor"
    else:
        status = "No Action"
        
    return ReorderRecommendation(
        product_id=product.product_id,
        product_name=product.product_name,
        current_stock=current_stock,
        predicted_demand=expected_demand,
        safety_stock=safety_stock,
        required_stock=required_stock,
        recommended_reorder_quantity=reorder_quantity,
        status=status
    )

def classify_movement(db: Session, product_id: str) -> MovementClassification:
    product = db.query(Product).filter(Product.product_id == product_id).first()
    
    # Check last 30 days of sales based on current business date
    current_date = get_current_business_date(db)
    thirty_days_ago = current_date - timedelta(days=30)
    sales = db.query(Sale).filter(Sale.product_id == product_id, Sale.date >= thirty_days_ago).all()
    
    total_qty = sum(s.quantity_sold for s in sales)
    avg_daily = total_qty / 30.0
    
    if avg_daily >= 1.0:
        cls = "Fast Moving"
    elif avg_daily >= 0.2:
        cls = "Medium Moving"
    else:
        cls = "Slow Moving"
        
    return MovementClassification(
        product_id=product.product_id,
        product_name=product.product_name,
        classification=cls,
        average_daily_demand=avg_daily
    )

def identify_dead_stock(db: Session, product_id: str) -> DeadStockProduct:
    product = db.query(Product).filter(Product.product_id == product_id).first()
    current_stock = get_current_stock(db, product_id)
    
    last_sale = db.query(Sale).filter(Sale.product_id == product_id).order_by(Sale.date.desc()).first()
    
    if last_sale:
        current_date = get_current_business_date(db)
        days_since = (current_date - last_sale.date).days
    else:
        days_since = 999
        
    inv_value = current_stock * (product.purchase_price_inr or 0)
    
    # Check last 90 days demand
    current_date = get_current_business_date(db)
    ninety_days_ago = current_date - timedelta(days=90)
    
    if days_since > 90 and current_stock > 0:
        status = "Dead Stock"
    elif days_since > 60 and current_stock > 0:
        status = "At Risk"
    else:
        status = "Healthy"
        
    return DeadStockProduct(
        product_id=product.product_id,
        product_name=product.product_name,
        current_stock=current_stock,
        days_since_last_sale=days_since,
        historical_demand=0.0, # Placeholder
        inventory_value=inv_value,
        status=status
    )
