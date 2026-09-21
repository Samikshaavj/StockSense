import axios from 'axios';

const API_URL = '/api';

export const api = axios.create({
  baseURL: API_URL,
});

export interface Product {
  product_id: string;
  product_name: string;
  category: string;
  brand: string;
  selling_price_inr: number;
  current_stock: number;
}

export interface StockRisk {
  product_id: string;
  product_name: string;
  current_stock: number;
  predicted_daily_demand: number;
  days_remaining: number;
  risk_level: string;
}

export interface ReorderRec {
  product_id: string;
  product_name: string;
  current_stock: number;
  predicted_demand: number;
  safety_stock: number;
  required_stock: number;
  recommended_reorder_quantity: number;
  status: string;
}

export interface DeadStock {
  product_id: string;
  product_name: string;
  current_stock: number;
  days_since_last_sale: number;
  inventory_value: number;
  status: string;
}

export interface Forecast {
  product_id: string;
  horizon: number;
  forecast: number[];
  total_predicted_demand: number;
  average_daily_demand: number;
}

export interface MovementClassification {
  product_id: string;
  product_name: string;
  classification: string;
  average_daily_demand: number;
}

export interface DailySalesData {
  date: string;
  total_revenue: number;
  total_units_sold: number;
}

export interface TopProduct {
  product_id: string;
  product_name: string;
  units_sold: number;
  revenue: number;
}

export interface SalesAnalyticsResponse {
  daily_sales: DailySalesData[];
  top_products: TopProduct[];
  total_revenue_30d: number;
  total_units_30d: number;
  data_available_through: string;
}

export interface ProductIntelligenceResponse {
  product: Product;
  stock_risk: StockRisk;
  reorder_recommendation: ReorderRec;
  forecast: Forecast;
  movement_classification: MovementClassification;
  historical_sales_30d: number;
  historical_revenue_30d: number;
}

export const getProducts = () => api.get<Product[]>('/products');
export const getStockRisk = () => api.get<StockRisk[]>('/stock-risk');
export const getReorderRecs = () => api.get<ReorderRec[]>('/reorder-recommendations');
export const getDeadStock = () => api.get<DeadStock[]>('/dead-stock');
export const getForecast = (productId: string, horizon: number = 7) => 
  api.get<Forecast>(`/forecast/${productId}?horizon=${horizon}`);
export const getSalesAnalytics = () => api.get<SalesAnalyticsResponse>('/sales/analytics');
export const getProductIntelligence = (productId: string) => api.get<ProductIntelligenceResponse>(`/product-intelligence/${productId}`);
export const getModelPerformance = () => api.get('/model-performance');

export interface SaleCreate {
  product_id: string;
  quantity: number;
  customer_type: string;
  payment_method: string;
}

export interface PurchaseCreate {
  product_id: string;
  quantity: number;
  purchase_price_inr: number;
}

export interface AdjustmentCreate {
  product_id: string;
  adjustment_amount: number;
  reason: string;
}

export interface ProductCreate {
  product_name: string;
  category?: string;
  brand?: string;
  part_number?: string;
  vehicle_category?: string;
  compatible_models?: string;
  product_type?: string;
  viscosity_grade?: string;
  pack_size?: number;
  unit?: string;
  purchase_price_inr: number;
  selling_price_inr: number;
  minimum_stock_level: number;
  maximum_stock_level: number;
  initial_stock: number;
}

export const recordSale = (sale: SaleCreate) => api.post('/sales', sale);
export const getSalesHistory = () => api.get('/sales');
export const receiveStock = (purchase: PurchaseCreate) => api.post('/purchases', purchase);
export const getPurchaseHistory = () => api.get('/purchases');
export const adjustStock = (adj: AdjustmentCreate) => api.post('/inventory/adjustments', adj);
export const createProduct = (prod: ProductCreate) => api.post('/products', prod);
export const retrainModels = () => api.post('/model/train');
