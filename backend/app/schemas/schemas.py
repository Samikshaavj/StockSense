from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProductBase(BaseModel):
    product_id: str
    product_name: str
    category: str
    brand: str
    selling_price_inr: float
    current_stock: Optional[int] = None

class ForecastResponse(BaseModel):
    product_id: str
    horizon: int
    forecast: List[float]
    average_daily_demand: float
    total_predicted_demand: float

class ReorderRecommendation(BaseModel):
    product_id: str
    product_name: str
    current_stock: int
    predicted_demand: float
    safety_stock: float
    required_stock: float
    recommended_reorder_quantity: int
    status: str

class StockOutRisk(BaseModel):
    product_id: str
    product_name: str
    current_stock: int
    predicted_daily_demand: float
    days_remaining: float
    risk_level: str

class DeadStockProduct(BaseModel):
    product_id: str
    product_name: str
    current_stock: int
    days_since_last_sale: int
    historical_demand: float
    inventory_value: float
    status: str

class MovementClassification(BaseModel):
    product_id: str
    product_name: str
    classification: str # Fast Moving, Medium Moving, Slow Moving
    average_daily_demand: float

class DailySalesData(BaseModel):
    date: str
    total_revenue: float
    total_units_sold: int

class TopProduct(BaseModel):
    product_id: str
    product_name: str
    units_sold: int
    revenue: float

class SalesAnalyticsResponse(BaseModel):
    daily_sales: List[DailySalesData]
    top_products: List[TopProduct]
    total_revenue_30d: float
    total_units_30d: int
    data_available_through: str

class SaleCreate(BaseModel):
    product_id: str
    quantity: int
    customer_type: str
    payment_method: str

class PurchaseCreate(BaseModel):
    product_id: str
    quantity: int
    purchase_price_inr: float

class AdjustmentCreate(BaseModel):
    product_id: str
    adjustment_amount: int
    reason: str

class ProductCreate(BaseModel):
    product_name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    part_number: Optional[str] = None
    vehicle_category: Optional[str] = None
    compatible_models: Optional[str] = None
    product_type: Optional[str] = None
    viscosity_grade: Optional[str] = None
    pack_size: Optional[float] = None
    unit: Optional[str] = None
    purchase_price_inr: float
    selling_price_inr: float
    minimum_stock_level: int
    maximum_stock_level: int
    initial_stock: int

class ProductIntelligenceResponse(BaseModel):
    product: ProductBase
    stock_risk: StockOutRisk
    reorder_recommendation: ReorderRecommendation
    forecast: ForecastResponse
    movement_classification: MovementClassification
    historical_sales_30d: int
    historical_revenue_30d: float
