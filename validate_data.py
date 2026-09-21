import pandas as pd
import numpy as np
import json

def validate_and_report():
    print("Loading data...")
    products = pd.read_csv("products.csv")
    vehicles = pd.read_csv("vehicles.csv")
    sales = pd.read_csv("sales_transactions.csv")
    purchases = pd.read_csv("purchases.csv")
    inventory = pd.read_csv("inventory_history.csv")

    print("Validating...")
    report = []
    
    # 1. Dataset stats
    report.append("# Validation Report\n")
    report.append("## Dataset Statistics")
    report.append(f"- **Number of products**: {len(products)}")
    report.append(f"- **Number of vehicles**: {len(vehicles)}")
    report.append(f"- **Number of sales transactions**: {len(sales)}")
    report.append(f"- **Number of purchase records**: {len(purchases)}")
    
    date_min = sales['date'].min()
    date_max = sales['date'].max()
    report.append(f"- **Date range**: {date_min} to {date_max}")
    
    total_units_sold = sales['quantity_sold'].sum()
    report.append(f"- **Total units sold**: {total_units_sold}")
    
    num_months = (pd.to_datetime(date_max).year - pd.to_datetime(date_min).year) * 12 + (pd.to_datetime(date_max).month - pd.to_datetime(date_min).month) + 1
    report.append(f"- **Average monthly sales (units)**: {total_units_sold / num_months:.2f}")

    # Determine product speeds based on sales volume
    sales_by_product = sales.groupby('product_id')['quantity_sold'].sum()
    percentiles = sales_by_product.quantile([0.3, 0.7, 0.9])
    
    fast_moving = (sales_by_product > percentiles[0.9]).sum()
    medium_moving = ((sales_by_product <= percentiles[0.9]) & (sales_by_product > percentiles[0.7])).sum()
    slow_moving = ((sales_by_product <= percentiles[0.7]) & (sales_by_product > 0)).sum()
    dead_stock = len(products) - len(sales_by_product)

    report.append(f"- **Fast-moving product count**: {fast_moving}")
    report.append(f"- **Medium-moving product count**: {medium_moving}")
    report.append(f"- **Slow-moving product count**: {slow_moving}")
    report.append(f"- **Dead-stock count**: {dead_stock}")
    
    stock_outs = inventory['stockout_flag'].sum()
    report.append(f"- **Stock-out count**: {stock_outs}")
    
    # Missing values
    missing = (products.isna().sum().sum() + vehicles.isna().sum().sum() + 
              sales.isna().sum().sum() + purchases.isna().sum().sum() + 
              inventory.isna().sum().sum())
    total_cells = (products.size + vehicles.size + sales.size + purchases.size + inventory.size)
    report.append(f"- **Missing-value percentage**: {(missing/total_cells)*100:.4f}%")
    
    # Duplicates
    duplicates = (products.duplicated().sum() + vehicles.duplicated().sum() + 
                 sales.duplicated().sum() + purchases.duplicated().sum() + 
                 inventory.duplicated().sum())
    report.append(f"- **Duplicate count**: {duplicates}")
    
    # Inventory consistency check
    # closing_stock = opening_stock + quantity_purchased - quantity_sold
    inconsistent_inventory = inventory[
        inventory['closing_stock'] != (inventory['opening_stock'] + inventory['quantity_purchased'] - inventory['quantity_sold'])
    ]
    report.append(f"- **Inventory consistency result**: {'Pass' if len(inconsistent_inventory) == 0 else f'Fail ({len(inconsistent_inventory)} inconsistent records)'}")
    
    with open('validation_report.md', 'w') as f:
        f.write('\n'.join(report))
    
    print("Validation report generated.")
    
    # Generate data dictionary
    dd = """# Data Dictionary

## 1. products.csv
| Column | Description | Data Type |
|--------|-------------|-----------|
| product_id | Unique identifier for each product | String |
| product_name | Name of the product | String |
| category | Main category of the product (e.g., Engine parts, Lubricants) | String |
| subcategory | Sub-category of the product | String |
| brand | Brand or manufacturer | String |
| part_number | Unique part number | String |
| vehicle_category | universal or specific | String |
| compatible_models | Vehicle ID or 'Universal' or 'Scooter specific' | String |
| product_type | Consumable or Spare Part | String |
| viscosity_grade | Grade for lubricants, empty otherwise | String |
| pack_size | Size of the pack | Float |
| unit | Unit of measurement (Litre, Piece) | String |
| purchase_price_inr | Purchase price in Indian Rupees | Float |
| selling_price_inr | Selling price in Indian Rupees | Float |
| minimum_stock_level | Reorder point | Integer |
| maximum_stock_level | Maximum stock capacity | Integer |
| initial_stock | Initial stock count at start of history | Integer |

## 2. vehicles.csv
| Column | Description | Data Type |
|--------|-------------|-----------|
| vehicle_id | Unique identifier for the vehicle | String |
| brand | Brand of the vehicle | String |
| model | Model name | String |
| vehicle_type | motorcycle or scooter | String |
| engine_cc | Engine displacement in CC | Integer |
| fuel_type | Fuel type | String |

## 3. sales_transactions.csv
| Column | Description | Data Type |
|--------|-------------|-----------|
| transaction_id | Unique identifier for the sale | String |
| date | Date of the transaction | Date |
| product_id | Identifier of the sold product | String |
| vehicle_id | Vehicle ID for which part was bought, or Universal | String |
| quantity_sold | Number of units sold | Integer |
| unit_selling_price | Selling price per unit at time of sale | Float |
| total_amount | Total amount for this transaction line | Float |
| customer_type | Retail or Workshop | String |
| payment_method | Cash, UPI, or Card | String |

## 4. purchases.csv
| Column | Description | Data Type |
|--------|-------------|-----------|
| purchase_id | Unique identifier for the purchase | String |
| purchase_date | Date of the purchase | Date |
| product_id | Identifier of the purchased product | String |
| quantity_purchased | Number of units purchased | Integer |
| purchase_price_inr | Purchase price per unit at time of purchase | Float |

## 5. inventory_history.csv
| Column | Description | Data Type |
|--------|-------------|-----------|
| date | Date of the inventory record | Date |
| product_id | Identifier of the product | String |
| opening_stock | Stock quantity at the beginning of the day | Integer |
| quantity_purchased | Quantity received/purchased on this day | Integer |
| quantity_sold | Quantity sold on this day | Integer |
| closing_stock | Stock quantity at the end of the day | Integer |
| stockout_flag | Binary flag indicating if a stockout occurred (1) or not (0) | Integer |
"""
    with open('data_dictionary.md', 'w') as f:
        f.write(dd)
        
    print("Data dictionary generated.")

if __name__ == '__main__':
    validate_and_report()
