import axios from 'axios';

const API_URL = '/api';

export const api = axios.create({
  baseURL: API_URL
});





















































































export const getProducts = () => api.get('/products');
export const getStockRisk = () => api.get('/stock-risk');
export const getReorderRecs = () => api.get('/reorder-recommendations');
export const getDeadStock = () => api.get('/dead-stock');
export const getForecast = (productId, horizon = 7) =>
api.get(`/forecast/${productId}?horizon=${horizon}`);
export const getSalesAnalytics = (month = null) => api.get('/sales/analytics' + (month ? `?month=${month}` : ''));
export const getProductIntelligence = (productId) => api.get(`/product-intelligence/${productId}`);
export const getModelPerformance = () => api.get('/model-performance');






































export const recordSale = (sale) => api.post('/sales', sale);
export const getSalesHistory = (month = null) => api.get('/sales' + (month ? `?month=${month}` : ''));
export const getSalesMonths = () => api.get('/sales/months');
export const receiveStock = (purchase) => api.post('/purchases', purchase);
export const getPurchaseHistory = () => api.get('/purchases');
export const adjustStock = (adj) => api.post('/inventory/adjustments', adj);
export const createProduct = (prod) => api.post('/products', prod);
export const retrainModels = () => api.post('/model/train');