import { useState, useEffect } from 'react';
import { receiveStock, getPurchaseHistory, getProducts } from '../services/api';

import { ShoppingBag, Search } from 'lucide-react';

export default function Purchases() {
  const [products, setProducts] = useState(() => JSON.parse(localStorage.getItem('inventoryProducts')) || []);

  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState(10);
  const [purchasePrice, setPurchasePrice] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const [isProductsLoading, setIsProductsLoading] = useState(true);

  const fetchData = async () => {
    setIsProductsLoading(true);
    try {
      const prodsRes = await getProducts();
      setProducts(prodsRes.data);
      localStorage.setItem('inventoryProducts', JSON.stringify(prodsRes.data));
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch data');
    } finally {
      setIsProductsLoading(false);
    }
  };

  const handleProductChange = (id) => {
    setProductId(id);
    const prod = products.find((p) => p.product_id === id);
    if (prod) {
      // Assuming you might want to pre-fill standard purchase price if it existed in Product
      // But we just leave it 0 for user to input actual cost
      setPurchasePrice(prod.selling_price_inr * 0.7); // Mock estimated cost
    }
  };

  const handlePurchase = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await receiveStock({
        product_id: productId,
        quantity,
        purchase_price_inr: purchasePrice
      });
      await fetchData();
      setQuantity(10);
      setPurchasePrice(0);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to record purchase');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Purchase Operations</h1>
      
      {error &&
      <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded mb-6">
          {error}
        </div>
      }

      {/* Receive Stock Form */}
      <div className="bg-surface p-6 rounded-xl border border-gray-800 mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <ShoppingBag className="w-5 h-5 text-primary" /> Receive Stock
        </h2>
        <form onSubmit={handlePurchase} className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Product</label>
            <select
              value={productId}
              onChange={(e) => handleProductChange(e.target.value)}
              required
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary">
              
              <option value="">{isProductsLoading ? 'Loading products...' : 'Select a product...'}</option>
              {products.map((p) =>
              <option key={p.product_id} value={p.product_id}>
                  {p.product_name}
                </option>
              )}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Quantity Received</label>
            <input
              type="number"
              min="1"
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
              required
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary" />
            
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Unit Cost (₹)</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={purchasePrice}
              onChange={(e) => setPurchasePrice(Number(e.target.value))}
              required
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary" />
            
          </div>
          <div>
            <button
              type="submit"
              disabled={loading || !productId}
              className="w-full bg-primary text-black font-semibold py-2 px-4 rounded-lg hover:bg-primary/90 transition disabled:opacity-50">
              
              {loading ? 'Processing...' : 'Record Purchase'}
            </button>
          </div>
        </form>
      </div>
    </div>);

}