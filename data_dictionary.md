# Data Dictionary

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
