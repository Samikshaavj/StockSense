import os
import sys
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up paths to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.main import app
from backend.database.schema import Base, Product, Inventory
from backend.app.api.endpoints import get_db

# Use a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_stocksense.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

class TestTransactions(unittest.TestCase):
    def setUp(self):
        # Reset DB
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        # Add a dummy product
        db = TestingSessionLocal()
        test_product = Product(
            product_id="P_TEST_001",
            product_name="Test Product",
            category="Test",
            purchase_price_inr=100.0,
            selling_price_inr=150.0,
            minimum_stock_level=10,
            maximum_stock_level=100,
            initial_stock=50
        )
        db.add(test_product)
        
        # Add initial inventory
        from backend.app.services.inventory_intelligence import get_current_business_date
        today = get_current_business_date(db)
        inv = Inventory(
            date=today,
            product_id="P_TEST_001",
            opening_stock=50,
            quantity_purchased=0,
            quantity_sold=0,
            adjustment_quantity=0,
            closing_stock=50,
            stockout_flag=0
        )
        db.add(inv)
        db.commit()
        db.close()

    def test_insufficient_stock_fails_gracefully(self):
        response = client.post(
            "/api/sales",
            json={
                "product_id": "P_TEST_001",
                "quantity": 100, # More than initial stock of 50
                "customer_type": "Retail",
                "payment_method": "Cash"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Insufficient stock", response.json()["detail"])

    def test_inventory_invariant(self):
        # 1. Sale of 10
        client.post("/api/sales", json={
            "product_id": "P_TEST_001", "quantity": 10, "customer_type": "Retail", "payment_method": "Cash"
        })
        
        # 2. Purchase of 20
        client.post("/api/purchases", json={
            "product_id": "P_TEST_001", "quantity": 20, "purchase_price_inr": 100.0
        })
        
        # 3. Adjustment of -5
        client.post("/api/inventory/adjustments", json={
            "product_id": "P_TEST_001", "adjustment_amount": -5, "reason": "Damage"
        })
        
        # Verify invariant in DB
        db = TestingSessionLocal()
        inv = db.query(Inventory).filter(Inventory.product_id == "P_TEST_001").order_by(Inventory.date.desc()).first()
        
        expected_closing = inv.opening_stock + inv.quantity_purchased - inv.quantity_sold + inv.adjustment_quantity
        self.assertEqual(inv.closing_stock, expected_closing)
        
        # Initial 50 - 10 (sale) + 20 (purchase) - 5 (adj) = 55
        self.assertEqual(inv.closing_stock, 55)
        db.close()

if __name__ == "__main__":
    unittest.main()
