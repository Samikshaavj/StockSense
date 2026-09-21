from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.schema import SessionLocal, Product
from backend.app.schemas.schemas import *
from backend.app.services.inventory_intelligence import (
    calculate_stock_out_risk,
    calculate_reorder_recommendation,
    classify_movement,
    identify_dead_stock
)
from ml.predict import predict_demand
import json
import os

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products", response_model=List[ProductBase])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    # Adding current stock manually for simplicity in this endpoint
    from backend.app.services.inventory_intelligence import get_current_stock
    result = []
    for p in products:
        result.append(ProductBase(
            product_id=p.product_id,
            product_name=p.product_name,
            category=p.category,
            brand=p.brand,
            selling_price_inr=p.selling_price_inr,
            current_stock=get_current_stock(db, p.product_id)
        ))
    return result

@router.get("/forecast/{product_id}", response_model=ForecastResponse)
def get_forecast(product_id: str, horizon: int = 7, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    forecast = predict_demand(product_id, horizon)
    avg_demand = sum(forecast) / len(forecast) if forecast else 0
    
    return ForecastResponse(
        product_id=product_id,
        horizon=horizon,
        forecast=forecast,
        average_daily_demand=avg_demand,
        total_predicted_demand=sum(forecast)
    )

@router.get("/stock-risk", response_model=List[StockOutRisk])
def get_all_stock_risk(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    risks = []
    for p in products:
        # Note: In production this would be batched/vectorized for performance
        risks.append(calculate_stock_out_risk(db, p.product_id))
    # Return sorted by highest risk
    return sorted(risks, key=lambda x: (x.risk_level != "Critical", x.risk_level != "High", x.days_remaining))

@router.get("/reorder-recommendations", response_model=List[ReorderRecommendation])
def get_all_reorder_recs(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    recs = []
    for p in products:
        rec = calculate_reorder_recommendation(db, p.product_id)
        if rec.status in ["Reorder Now", "Reorder Soon"]:
            recs.append(rec)
    return sorted(recs, key=lambda x: x.status != "Reorder Now")

@router.get("/dead-stock", response_model=List[DeadStockProduct])
def get_dead_stock(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    ds_list = []
    for p in products:
        ds = identify_dead_stock(db, p.product_id)
        if ds.status in ["Dead Stock", "At Risk"]:
            ds_list.append(ds)
    return sorted(ds_list, key=lambda x: x.days_since_last_sale, reverse=True)

@router.get("/sales/analytics", response_model=SalesAnalyticsResponse)
def get_sales_analytics(db: Session = Depends(get_db)):
    from sqlalchemy import func
    from datetime import date, timedelta
    from backend.database.schema import Sale
    
    # In a real app we'd use current date, but for synthetic data we'll use max date
    max_date = db.query(func.max(Sale.date)).scalar()
    if not max_date:
        return SalesAnalyticsResponse(daily_sales=[], top_products=[], total_revenue_30d=0, total_units_30d=0, data_available_through="")
        
    start_date = max_date - timedelta(days=30)
    
    # 30-day totals
    totals = db.query(
        func.sum(Sale.total_amount).label('rev'),
        func.sum(Sale.quantity_sold).label('units')
    ).filter(Sale.date >= start_date).first()
    
    total_rev = totals.rev or 0
    total_units = totals.units or 0
    
    # Daily sales
    daily = db.query(
        Sale.date,
        func.sum(Sale.total_amount).label('rev'),
        func.sum(Sale.quantity_sold).label('units')
    ).filter(Sale.date >= start_date).group_by(Sale.date).order_by(Sale.date).all()
    
    daily_sales = [DailySalesData(date=str(d.date), total_revenue=d.rev, total_units_sold=d.units) for d in daily]
    
    # Top products
    top = db.query(
        Product.product_id,
        Product.product_name,
        func.sum(Sale.quantity_sold).label('units'),
        func.sum(Sale.total_amount).label('rev')
    ).join(Sale, Product.product_id == Sale.product_id)\
     .filter(Sale.date >= start_date)\
     .group_by(Product.product_id, Product.product_name)\
     .order_by(func.sum(Sale.total_amount).desc())\
     .limit(5).all()
     
    top_products = [TopProduct(product_id=t.product_id, product_name=t.product_name, units_sold=t.units, revenue=t.rev) for t in top]
    
    return SalesAnalyticsResponse(
        daily_sales=daily_sales,
        top_products=top_products,
        total_revenue_30d=total_rev,
        total_units_30d=total_units,
        data_available_through=str(max_date)
    )

@router.get("/product-intelligence/{product_id}", response_model=ProductIntelligenceResponse)
def get_product_intelligence(product_id: str, db: Session = Depends(get_db)):
    from sqlalchemy import func
    from datetime import timedelta
    from backend.database.schema import Sale
    from backend.app.services.inventory_intelligence import get_current_stock
    
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    p_base = ProductBase(
        product_id=product.product_id,
        product_name=product.product_name,
        category=product.category,
        brand=product.brand,
        selling_price_inr=product.selling_price_inr,
        current_stock=get_current_stock(db, product_id)
    )
    
    risk = calculate_stock_out_risk(db, product_id)
    reorder = calculate_reorder_recommendation(db, product_id)
    
    # Forecast
    forecast_vals = predict_demand(product_id, 14)
    avg_demand = sum(forecast_vals) / len(forecast_vals) if forecast_vals else 0
    forecast_res = ForecastResponse(
        product_id=product_id,
        horizon=14,
        forecast=forecast_vals,
        average_daily_demand=avg_demand,
        total_predicted_demand=sum(forecast_vals)
    )
    
    movement = classify_movement(db, product_id)
    
    # Historical
    max_date = db.query(func.max(Sale.date)).scalar()
    hist_sales = 0
    hist_rev = 0
    if max_date:
        start_date = max_date - timedelta(days=30)
        totals = db.query(
            func.sum(Sale.quantity_sold).label('units'),
            func.sum(Sale.total_amount).label('rev')
        ).filter(Sale.product_id == product_id, Sale.date >= start_date).first()
        hist_sales = totals.units or 0
        hist_rev = totals.rev or 0
        
    return ProductIntelligenceResponse(
        product=p_base,
        stock_risk=risk,
        reorder_recommendation=reorder,
        forecast=forecast_res,
        movement_classification=movement,
        historical_sales_30d=hist_sales,
        historical_revenue_30d=hist_rev
    )

@router.get("/model-performance")
def get_model_performance():
    metadata_path = os.path.join(os.path.dirname(__file__), '../../../models/metadata.json')
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            return json.load(f)
    return {"message": "No model metadata found"}

import uuid
from backend.database.schema import Sale, Purchase, InventoryAdjustment, Inventory
from backend.app.services.inventory_intelligence import get_current_business_date, get_current_stock
from datetime import date as date_obj
import subprocess

def _update_inventory_for_today(db: Session, product_id: str, quantity_change_sold: int = 0, quantity_change_purchased: int = 0, quantity_change_adjustment: int = 0):
    today = get_current_business_date(db)
    
    # Check if there is an inventory record for today
    inv = db.query(Inventory).filter(Inventory.product_id == product_id, Inventory.date == today).first()
    
    if inv:
        inv.quantity_sold += quantity_change_sold
        inv.quantity_purchased += quantity_change_purchased
        inv.adjustment_quantity += quantity_change_adjustment
        inv.closing_stock = inv.opening_stock + inv.quantity_purchased - inv.quantity_sold + inv.adjustment_quantity
    else:
        # Create a new record for today
        # Find latest record
        latest_inv = db.query(Inventory).filter(Inventory.product_id == product_id).order_by(Inventory.date.desc()).first()
        opening = latest_inv.closing_stock if latest_inv else 0
        new_inv = Inventory(
            date=today,
            product_id=product_id,
            opening_stock=opening,
            quantity_purchased=quantity_change_purchased,
            quantity_sold=quantity_change_sold,
            adjustment_quantity=quantity_change_adjustment,
            closing_stock=opening + quantity_change_purchased - quantity_change_sold + quantity_change_adjustment,
            stockout_flag=0
        )
        db.add(new_inv)
        
    db.commit()

@router.post("/sales")
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    current_stock = get_current_stock(db, sale.product_id)
    if current_stock < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
        
    today = get_current_business_date(db)
    new_sale = Sale(
        transaction_id=str(uuid.uuid4()),
        date=today,
        product_id=sale.product_id,
        quantity_sold=sale.quantity,
        unit_selling_price=product.selling_price_inr,
        total_amount=product.selling_price_inr * sale.quantity,
        customer_type=sale.customer_type,
        payment_method=sale.payment_method
    )
    db.add(new_sale)
    _update_inventory_for_today(db, sale.product_id, quantity_change_sold=sale.quantity)
    return {"message": "Sale recorded successfully"}

@router.get("/sales")
def get_sales(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    sales = db.query(Sale).order_by(Sale.date.desc()).offset(skip).limit(limit).all()
    return sales

@router.post("/purchases")
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == purchase.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    today = get_current_business_date(db)
    new_purchase = Purchase(
        purchase_id=str(uuid.uuid4()),
        purchase_date=today,
        product_id=purchase.product_id,
        quantity_purchased=purchase.quantity,
        purchase_price_inr=purchase.purchase_price_inr
    )
    db.add(new_purchase)
    _update_inventory_for_today(db, purchase.product_id, quantity_change_purchased=purchase.quantity)
    return {"message": "Purchase recorded successfully"}

@router.get("/purchases")
def get_purchases(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    purchases = db.query(Purchase).order_by(Purchase.purchase_date.desc()).offset(skip).limit(limit).all()
    return purchases

@router.post("/inventory/adjustments")
def create_adjustment(adj: AdjustmentCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == adj.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    today = get_current_business_date(db)
    current_stock = get_current_stock(db, adj.product_id)
    
    new_adj = InventoryAdjustment(
        date=today,
        product_id=adj.product_id,
        previous_quantity=current_stock,
        new_quantity=current_stock + adj.adjustment_amount,
        adjustment_amount=adj.adjustment_amount,
        reason=adj.reason
    )
    db.add(new_adj)
    _update_inventory_for_today(db, adj.product_id, quantity_change_adjustment=adj.adjustment_amount)
    return {"message": "Adjustment recorded successfully"}

@router.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Generate ID based on total products to keep it simple, e.g., P015
    count = db.query(Product).count()
    new_id = f"P{count + 1:03d}"
    
    new_product = Product(
        product_id=new_id,
        product_name=product.product_name,
        category=product.category,
        brand=product.brand,
        part_number=product.part_number,
        vehicle_category=product.vehicle_category,
        compatible_models=product.compatible_models,
        product_type=product.product_type,
        viscosity_grade=product.viscosity_grade,
        pack_size=product.pack_size,
        unit=product.unit,
        purchase_price_inr=product.purchase_price_inr,
        selling_price_inr=product.selling_price_inr,
        minimum_stock_level=product.minimum_stock_level,
        maximum_stock_level=product.maximum_stock_level,
        initial_stock=product.initial_stock
    )
    db.add(new_product)
    
    # Initialize inventory for today
    today = get_current_business_date(db)
    new_inv = Inventory(
        date=today,
        product_id=new_id,
        opening_stock=product.initial_stock,
        quantity_purchased=0,
        quantity_sold=0,
        adjustment_quantity=0,
        closing_stock=product.initial_stock,
        stockout_flag=0
    )
    db.add(new_inv)
    db.commit()
    return {"message": "Product added successfully", "product_id": new_id}

@router.post("/model/train")
def train_model():
    script_path = os.path.join(os.path.dirname(__file__), '../../../ml/train_models.py')
    script_path = os.path.abspath(script_path)
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Model training failed: {result.stderr}")
    return {"message": "Model retrained successfully", "output": result.stdout}
