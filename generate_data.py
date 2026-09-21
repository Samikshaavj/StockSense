import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import uuid
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# --- 1. VEHICLES ---
vehicles_data = [
    {"vehicle_id": "V01", "brand": "Honda", "model": "Activa", "vehicle_type": "scooter", "engine_cc": 110, "fuel_type": "Petrol"},
    {"vehicle_id": "V02", "brand": "Honda", "model": "Shine", "vehicle_type": "motorcycle", "engine_cc": 125, "fuel_type": "Petrol"},
    {"vehicle_id": "V03", "brand": "Honda", "model": "SP 125", "vehicle_type": "motorcycle", "engine_cc": 125, "fuel_type": "Petrol"},
    {"vehicle_id": "V04", "brand": "Honda", "model": "Unicorn", "vehicle_type": "motorcycle", "engine_cc": 160, "fuel_type": "Petrol"},
    {"vehicle_id": "V05", "brand": "Hero", "model": "Splendor", "vehicle_type": "motorcycle", "engine_cc": 100, "fuel_type": "Petrol"},
    {"vehicle_id": "V06", "brand": "Hero", "model": "HF Deluxe", "vehicle_type": "motorcycle", "engine_cc": 100, "fuel_type": "Petrol"},
    {"vehicle_id": "V07", "brand": "Hero", "model": "Passion", "vehicle_type": "motorcycle", "engine_cc": 110, "fuel_type": "Petrol"},
    {"vehicle_id": "V08", "brand": "Hero", "model": "Glamour", "vehicle_type": "motorcycle", "engine_cc": 125, "fuel_type": "Petrol"},
    {"vehicle_id": "V09", "brand": "TVS", "model": "Jupiter", "vehicle_type": "scooter", "engine_cc": 110, "fuel_type": "Petrol"},
    {"vehicle_id": "V10", "brand": "TVS", "model": "Apache", "vehicle_type": "motorcycle", "engine_cc": 160, "fuel_type": "Petrol"},
    {"vehicle_id": "V11", "brand": "TVS", "model": "Raider", "vehicle_type": "motorcycle", "engine_cc": 125, "fuel_type": "Petrol"},
    {"vehicle_id": "V12", "brand": "TVS", "model": "Sport", "vehicle_type": "motorcycle", "engine_cc": 100, "fuel_type": "Petrol"},
    {"vehicle_id": "V13", "brand": "Bajaj", "model": "Pulsar", "vehicle_type": "motorcycle", "engine_cc": 150, "fuel_type": "Petrol"},
    {"vehicle_id": "V14", "brand": "Bajaj", "model": "Platina", "vehicle_type": "motorcycle", "engine_cc": 100, "fuel_type": "Petrol"},
    {"vehicle_id": "V15", "brand": "Bajaj", "model": "CT", "vehicle_type": "motorcycle", "engine_cc": 100, "fuel_type": "Petrol"},
    {"vehicle_id": "V16", "brand": "Suzuki", "model": "Access", "vehicle_type": "scooter", "engine_cc": 125, "fuel_type": "Petrol"},
    {"vehicle_id": "V17", "brand": "Suzuki", "model": "Gixxer", "vehicle_type": "motorcycle", "engine_cc": 155, "fuel_type": "Petrol"},
    {"vehicle_id": "V18", "brand": "Yamaha", "model": "FZ", "vehicle_type": "motorcycle", "engine_cc": 150, "fuel_type": "Petrol"},
    {"vehicle_id": "V19", "brand": "Yamaha", "model": "Fascino", "vehicle_type": "scooter", "engine_cc": 125, "fuel_type": "Petrol"},
    {"vehicle_id": "V20", "brand": "Yamaha", "model": "Ray", "vehicle_type": "scooter", "engine_cc": 125, "fuel_type": "Petrol"},
]
vehicles_df = pd.DataFrame(vehicles_data)
vehicles_df.to_csv("vehicles.csv", index=False)

# --- 2. PRODUCTS ---
# Categories
categories = {
    "Engine parts": ["Piston", "Valve", "Timing Chain"],
    "Clutch components": ["Clutch Plate", "Clutch Cable"],
    "Transmission": ["Gear Pinion", "Sprocket"],
    "Braking system": ["Brake Pad", "Brake Shoe", "Brake Cable"],
    "Filters": ["Air Filter", "Oil Filter"],
    "Electrical": ["Spark Plug", "Battery", "Bulb", "Indicator", "CDI Unit"],
    "Chain and sprocket": ["Chain Sprocket Kit", "Drive Chain"],
    "Bearings": ["Wheel Bearing", "Engine Bearing"],
    "Cables": ["Accelerator Cable", "Speedometer Cable"],
    "Suspension": ["Fork Seal", "Shock Absorber"],
    "Tyres and tubes": ["Tyre", "Tube"],
    "Lighting": ["Headlight Bulb", "Tail Light Assembly"],
    "Body parts": ["Mirror", "Mudguard", "Side Panel"],
    "Gaskets and seals": ["Engine Gasket Kit", "O-Ring"],
    "Lubricants": ["Engine Oil", "Gear Oil", "Fork Oil", "Chain Lube", "Grease", "Brake Fluid"]
}

products_data = []
product_idx = 1

def add_product(name, cat, subcat, brand, p_type, vis, pack, unit, p_price, s_price, speed, comp_models):
    global product_idx
    min_stock = random.randint(2, 10) if speed == 'slow' else (random.randint(10, 20) if speed == 'medium' else random.randint(30, 50))
    max_stock = min_stock * random.randint(3, 5)
    init_stock = random.randint(min_stock, max_stock)
    
    products_data.append({
        "product_id": f"P{product_idx:03d}",
        "product_name": name,
        "category": cat,
        "subcategory": subcat,
        "brand": brand,
        "part_number": f"{brand[:3].upper()}-{random.randint(1000, 9999)}",
        "vehicle_category": "universal" if comp_models == "Universal" else "specific",
        "compatible_models": comp_models,
        "product_type": p_type,
        "viscosity_grade": vis,
        "pack_size": pack,
        "unit": unit,
        "purchase_price_inr": p_price,
        "selling_price_inr": s_price,
        "minimum_stock_level": min_stock,
        "maximum_stock_level": max_stock,
        "initial_stock": init_stock,
        "speed": speed # Will drop this later, used for sales generation
    })
    product_idx += 1

# Generate Lubricants (Fast moving, universal mostly)
add_product("Castrol Activ 4T", "Lubricants", "Engine Oil", "Castrol", "Consumable", "20W-40", 1, "Litre", 300, 380, "fast", "Universal")
add_product("Motul 3000 4T Plus", "Lubricants", "Engine Oil", "Motul", "Consumable", "20W-40", 1, "Litre", 320, 400, "fast", "Universal")
add_product("Motul 7100 4T", "Lubricants", "Engine Oil", "Motul", "Consumable", "10W-50", 1, "Litre", 750, 900, "medium", "Universal")
add_product("Mak 4T Plus", "Lubricants", "Engine Oil", "Mak", "Consumable", "20W-40", 1, "Litre", 280, 350, "fast", "Universal")
add_product("Castrol Scooter Oil", "Lubricants", "Engine Oil", "Castrol", "Consumable", "10W-30", 0.8, "Litre", 250, 320, "fast", "Scooter specific")
add_product("Motul Scooter LE", "Lubricants", "Engine Oil", "Motul", "Consumable", "10W-30", 0.8, "Litre", 280, 350, "fast", "Scooter specific")
add_product("Castrol Chain Lube", "Lubricants", "Chain Lube", "Castrol", "Consumable", "N/A", 0.5, "Litre", 150, 200, "fast", "Motorcycle specific")
add_product("Motul Chain Lube", "Lubricants", "Chain Lube", "Motul", "Consumable", "N/A", 0.4, "Litre", 180, 250, "fast", "Motorcycle specific")
add_product("Bosch Dot 3 Brake Fluid", "Lubricants", "Brake Fluid", "Bosch", "Consumable", "Dot 3", 0.25, "Litre", 80, 120, "medium", "Universal")
add_product("Endurance Fork Oil", "Lubricants", "Fork Oil", "Endurance", "Consumable", "20W", 0.35, "Litre", 120, 160, "medium", "Universal")

# Generate Spare Parts
brands = ["OEM", "Bosch", "Endurance", "Minda", "Gabriel", "NGK", "Rolon", "CEAT", "MRF", "Exide", "Amaron"]
speeds = ["fast", "medium", "slow", "dead"]

for _ in range(190): # Generate 120 parts
    cat = random.choice(list(categories.keys()))
    if cat == "Lubricants": continue
    subcat = random.choice(categories[cat])
    brand = random.choice(brands)
    
    speed_prob = random.random()
    if speed_prob < 0.2: speed = "fast"
    elif speed_prob < 0.6: speed = "medium"
    elif speed_prob < 0.9: speed = "slow"
    else: speed = "dead"
    
    # Prices
    p_price = random.randint(50, 2500)
    s_price = int(p_price * random.uniform(1.15, 1.5))
    
    # Compatibility
    if random.random() < 0.2 or cat in ["Electrical", "Bearings", "Tyres and tubes"]:
        comp = "Universal"
    else:
        v = random.choice(vehicles_data)
        comp = v["vehicle_id"]
        
    add_product(f"{brand} {subcat}", cat, subcat, brand, "Spare Part", "N/A", 1, "Piece", p_price, s_price, speed, comp)

products_df = pd.DataFrame(products_data)
product_speeds = dict(zip(products_df['product_id'], products_df['speed']))
products_df_out = products_df.drop(columns=['speed'])
products_df_out.to_csv("products.csv", index=False)

# --- 3. SALES & INVENTORY ---
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
num_days = (end_date - start_date).days + 1
date_list = [start_date + timedelta(days=x) for x in range(num_days)]

inventory = {p["product_id"]: p["initial_stock"] for p in products_data}
inventory_history = []
sales_transactions = []
purchases = []

transaction_id_counter = 1
purchase_id_counter = 1

# Define probabilities for speed
daily_prob = {"fast": 0.5, "medium": 0.25, "slow": 0.08, "dead": 0.005}

for current_date in date_list:
    daily_sales = {}
    
    # Generate sales for the day
    for p in products_data:
        pid = p["product_id"]
        speed = p["speed"]
        
        # Seasonality factor (e.g. higher sales in summer/festivals)
        month = current_date.month
        seasonality = 1.0
        if month in [10, 11]: seasonality = 1.3 # Diwali/festival season
        if month in [7, 8]: seasonality = 0.8 # Monsoon
        
        prob = daily_prob[speed] * seasonality
        
        if random.random() < prob:
            # Sale happens
            qty = random.randint(1, 3) if speed == 'fast' else 1
            if inventory[pid] >= qty:
                # Can fulfill
                daily_sales[pid] = daily_sales.get(pid, 0) + qty
                
                # Create transaction records
                comp = p["compatible_models"]
                vid = "Universal" if comp == "Universal" else (comp if comp.startswith("V") else random.choice(vehicles_data)["vehicle_id"])
                
                sales_transactions.append({
                    "transaction_id": f"T{transaction_id_counter:07d}",
                    "date": current_date.strftime("%Y-%m-%d"),
                    "product_id": pid,
                    "vehicle_id": vid,
                    "quantity_sold": qty,
                    "unit_selling_price": p["selling_price_inr"],
                    "total_amount": qty * p["selling_price_inr"],
                    "customer_type": random.choices(["Retail", "Workshop"], weights=[0.8, 0.2])[0],
                    "payment_method": random.choices(["Cash", "UPI", "Card"], weights=[0.4, 0.5, 0.1])[0]
                })
                transaction_id_counter += 1
            else:
                # Stockout, can partially fulfill or not at all. We just record 0 sales and stockout flag later
                qty_sold = inventory[pid]
                if qty_sold > 0:
                    daily_sales[pid] = daily_sales.get(pid, 0) + qty_sold
                    comp = p["compatible_models"]
                    vid = "Universal" if comp == "Universal" else (comp if comp.startswith("V") else random.choice(vehicles_data)["vehicle_id"])
                    sales_transactions.append({
                        "transaction_id": f"T{transaction_id_counter:07d}",
                        "date": current_date.strftime("%Y-%m-%d"),
                        "product_id": pid,
                        "vehicle_id": vid,
                        "quantity_sold": qty_sold,
                        "unit_selling_price": p["selling_price_inr"],
                        "total_amount": qty_sold * p["selling_price_inr"],
                        "customer_type": random.choices(["Retail", "Workshop"], weights=[0.8, 0.2])[0],
                        "payment_method": random.choices(["Cash", "UPI", "Card"], weights=[0.4, 0.5, 0.1])[0]
                    })
                    transaction_id_counter += 1

    # End of day inventory update and ordering
    for p in products_data:
        pid = p["product_id"]
        opening = inventory[pid]
        sold = daily_sales.get(pid, 0)
        inventory[pid] -= sold
        
        # Check if we need to purchase
        purchased = 0
        if inventory[pid] <= p["minimum_stock_level"]:
            # Reorder up to max
            reorder_qty = p["maximum_stock_level"] - inventory[pid]
            # Delay in purchase (assuming arrived today)
            purchased = reorder_qty
            inventory[pid] += purchased
            
            purchases.append({
                "purchase_id": f"PR{purchase_id_counter:05d}",
                "purchase_date": current_date.strftime("%Y-%m-%d"),
                "product_id": pid,
                "quantity_purchased": purchased,
                "purchase_price_inr": p["purchase_price_inr"]
            })
            purchase_id_counter += 1
            
        closing = inventory[pid]
        stockout = 1 if closing == 0 and sold < (daily_sales.get(pid, 0) if pid in daily_sales else 0) else (1 if opening - sold == 0 else 0)
        
        inventory_history.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "product_id": pid,
            "opening_stock": opening,
            "quantity_purchased": purchased,
            "quantity_sold": sold,
            "closing_stock": closing,
            "stockout_flag": stockout
        })

pd.DataFrame(sales_transactions).to_csv("sales_transactions.csv", index=False)
pd.DataFrame(purchases).to_csv("purchases.csv", index=False)
pd.DataFrame(inventory_history).to_csv("inventory_history.csv", index=False)

print("Data generation complete.")

