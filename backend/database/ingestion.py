import pandas as pd
import sqlite3
import os
import sys

# Add the root directory to path to import schema
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.database.schema import init_db, engine

def ingest_data():
    print("Initializing database...")
    init_db()
    
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
    
    # Load CSVs
    print("Loading CSV files...")
    try:
        products_df = pd.read_csv(os.path.join(data_dir, 'products.csv'))
        vehicles_df = pd.read_csv(os.path.join(data_dir, 'vehicles.csv'))
        sales_df = pd.read_csv(os.path.join(data_dir, 'sales_transactions.csv'))
        purchases_df = pd.read_csv(os.path.join(data_dir, 'purchases.csv'))
        inventory_df = pd.read_csv(os.path.join(data_dir, 'inventory_history.csv'))
    except FileNotFoundError as e:
        print(f"Error loading CSVs: {e}")
        return

    # Basic validations
    print("Validating inventory relationships before insertion...")
    inconsistent = inventory_df[
        inventory_df['closing_stock'] != (inventory_df['opening_stock'] + inventory_df['quantity_purchased'] - inventory_df['quantity_sold'])
    ]
    if len(inconsistent) > 0:
        raise ValueError(f"Found {len(inconsistent)} inconsistent inventory records! Integration aborted.")

    print("Data validated successfully. Inserting into SQLite...")
    
    # Dates formatting for SQLite (YYYY-MM-DD)
    sales_df['date'] = pd.to_datetime(sales_df['date']).dt.date
    purchases_df['purchase_date'] = pd.to_datetime(purchases_df['purchase_date']).dt.date
    inventory_df['date'] = pd.to_datetime(inventory_df['date']).dt.date
    inventory_df['adjustment_quantity'] = 0

    with engine.begin() as conn:
        products_df.to_sql('products', conn, if_exists='append', index=False)
        vehicles_df.to_sql('vehicles', conn, if_exists='append', index=False)
        sales_df.to_sql('sales', conn, if_exists='append', index=False)
        purchases_df.to_sql('purchases', conn, if_exists='append', index=False)
        inventory_df.to_sql('inventory', conn, if_exists='append', index=False)
        
    print("Database ingestion completed successfully.")

if __name__ == "__main__":
    ingest_data()
