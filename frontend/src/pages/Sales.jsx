import { useState, useEffect } from 'react';
import { recordSale, getSalesHistory, getProducts, getSalesMonths } from '../services/api';

import { PlusCircle, Search } from 'lucide-react';

export default function Sales() {
  const [products, setProducts] = useState(() => JSON.parse(localStorage.getItem('inventoryProducts')) || []);

  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [customerType, setCustomerType] = useState('Retail');
  const [paymentMethod, setPaymentMethod] = useState('Cash');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [isProductsLoading, setIsProductsLoading] = useState(true);

  useEffect(() => {
    getProducts().then((res) => {
      setProducts(res.data);
      localStorage.setItem('inventoryProducts', JSON.stringify(res.data));
    }).catch((err) => setError(err.response?.data?.detail || 'Failed to fetch products'))
    .finally(() => setIsProductsLoading(false));
  }, []);

  const handleSale = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await recordSale({
        product_id: productId,
        quantity,
        customer_type: customerType,
        payment_method: paymentMethod
      });
      setQuantity(1);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to record sale');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Sales Operations</h1>
      
      {error &&
      <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded mb-6">
          {error}
        </div>
      }

      {/* New Sale Form */}
      <div className="bg-surface p-6 rounded-xl border border-gray-800 mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <PlusCircle className="w-5 h-5 text-primary" /> New Sale
        </h2>
        <form onSubmit={handleSale} className="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
          <div className="md:col-span-2">
            <label className="block text-sm text-gray-400 mb-1">Product</label>
            <select
              value={productId}
              onChange={(e) => setProductId(e.target.value)}
              required
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary">
              
              <option value="">{isProductsLoading ? 'Loading products...' : 'Select a product...'}</option>
              {products.map((p) =>
              <option key={p.product_id} value={p.product_id}>
                  {p.product_name} (Stock: {p.current_stock})
                </option>
              )}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Quantity</label>
            <input
              type="number"
              min="1"
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
              required
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary" />
            
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Customer Type</label>
            <select
              value={customerType}
              onChange={(e) => setCustomerType(e.target.value)}
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary">
              
              <option value="Retail">Retail</option>
              <option value="Wholesale">Wholesale</option>
              <option value="Mechanic">Mechanic</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Payment Method</label>
            <select
              value={paymentMethod}
              onChange={(e) => setPaymentMethod(e.target.value)}
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary">
              
              <option value="Cash">Cash</option>
              <option value="Card">Card</option>
              <option value="UPI">UPI</option>
            </select>
          </div>
          <div>
            <button
              type="submit"
              disabled={loading || !productId}
              className="w-full bg-primary text-black font-semibold py-2 px-4 rounded-lg hover:bg-primary/90 transition disabled:opacity-50">
              
              {loading ? 'Recording...' : 'Record Sale'}
            </button>
          </div>
        </form>
      </div>
    </div>);

}