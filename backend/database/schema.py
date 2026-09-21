from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(String, primary_key=True)
    product_name = Column(String, nullable=False)
    category = Column(String)
    subcategory = Column(String)
    brand = Column(String)
    part_number = Column(String)
    vehicle_category = Column(String)
    compatible_models = Column(String)
    product_type = Column(String)
    viscosity_grade = Column(String)
    pack_size = Column(Float)
    unit = Column(String)
    purchase_price_inr = Column(Float)
    selling_price_inr = Column(Float)
    minimum_stock_level = Column(Integer)
    maximum_stock_level = Column(Integer)
    initial_stock = Column(Integer)

class Vehicle(Base):
    __tablename__ = 'vehicles'
    
    vehicle_id = Column(String, primary_key=True)
    brand = Column(String)
    model = Column(String)
    vehicle_type = Column(String)
    engine_cc = Column(Integer)
    fuel_type = Column(String)

class Sale(Base):
    __tablename__ = 'sales'
    
    transaction_id = Column(String, primary_key=True)
    date = Column(Date, nullable=False)
    product_id = Column(String, ForeignKey('products.product_id'))
    vehicle_id = Column(String)
    quantity_sold = Column(Integer)
    unit_selling_price = Column(Float)
    total_amount = Column(Float)
    customer_type = Column(String)
    payment_method = Column(String)

class Purchase(Base):
    __tablename__ = 'purchases'
    
    purchase_id = Column(String, primary_key=True)
    purchase_date = Column(Date, nullable=False)
    product_id = Column(String, ForeignKey('products.product_id'))
    quantity_purchased = Column(Integer)
    purchase_price_inr = Column(Float)

class InventoryAdjustment(Base):
    __tablename__ = 'inventory_adjustments'
    
    adjustment_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    product_id = Column(String, ForeignKey('products.product_id'))
    previous_quantity = Column(Integer)
    new_quantity = Column(Integer)
    adjustment_amount = Column(Integer)
    reason = Column(String)

class Inventory(Base):
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    product_id = Column(String, ForeignKey('products.product_id'))
    opening_stock = Column(Integer)
    quantity_purchased = Column(Integer)
    quantity_sold = Column(Integer)
    adjustment_quantity = Column(Integer, default=0)
    closing_stock = Column(Integer)
    stockout_flag = Column(Integer)

# Database connection setup
DATABASE_URL = "sqlite:///stocksense.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
