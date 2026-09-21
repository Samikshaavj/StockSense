import { useState, useEffect } from 'react';
import { recordSale, getSalesHistory, getProducts } from '../services/api';
import type { Product } from '../services/api';
import { PlusCircle, Search } from 'lucide-react';

export default function Sales() {
  const [products, setProducts] = useState<Product[]>([]);
  const [sales, setSales] = useState<any[]>([]);
  
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [customerType, setCustomerType] = useState('Retail');
  const [paymentMethod, setPaymentMethod] = useState('Cash');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [prodsRes, salesRes] = await Promise.all([
        getProducts(),
        getSalesHistory()
      ]);
      setProducts(prodsRes.data);
      setSales(salesRes.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch data');
    }
  };

  const handleSale = async (e: React.FormEvent) => {
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
      await fetchData();
      setQuantity(1);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to record sale');
    } finally {
      setLoading(false);
    }
  };

  const filteredSales = sales.filter(s => 
    s.product_id.toLowerCase().includes(searchTerm.toLowerCase()) || 
    s.transaction_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Sales Operations</h1>
      
      {error && (
        <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

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
              onChange={e => setProductId(e.target.value)}
              required
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
            >
              <option value="">Select a product...</option>
              {products.map(p => (
                <option key={p.product_id} value={p.product_id}>
                  {p.product_name} (Stock: {p.current_stock})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Quantity</label>
            <input 
              type="number" 
              min="1"
              value={quantity}
              onChange={e => setQuantity(Number(e.target.value))}
              required
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Customer Type</label>
            <select 
              value={customerType} 
              onChange={e => setCustomerType(e.target.value)}
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
            >
              <option value="Retail">Retail</option>
              <option value="Wholesale">Wholesale</option>
              <option value="Mechanic">Mechanic</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Payment Method</label>
            <select 
              value={paymentMethod} 
              onChange={e => setPaymentMethod(e.target.value)}
              className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
            >
              <option value="Cash">Cash</option>
              <option value="Card">Card</option>
              <option value="UPI">UPI</option>
            </select>
          </div>
          <div>
            <button 
              type="submit" 
              disabled={loading || !productId}
              className="w-full bg-primary text-black font-semibold py-2 px-4 rounded-lg hover:bg-primary/90 transition disabled:opacity-50"
            >
              {loading ? 'Recording...' : 'Record Sale'}
            </button>
          </div>
        </form>
      </div>

      {/* Sales History */}
      <div className="bg-surface rounded-xl border border-gray-800 flex flex-col">
        <div className="p-6 border-b border-gray-800 flex justify-between items-center">
          <h2 className="text-xl font-semibold">Sales History</h2>
          <div className="relative">
            <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              type="text" 
              placeholder="Search ID or Product..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 bg-background border border-gray-700 rounded-lg text-white focus:outline-none focus:border-primary"
            />
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-gray-800/50 text-gray-400 text-sm">
              <tr>
                <th className="px-6 py-3 font-medium">Transaction ID</th>
                <th className="px-6 py-3 font-medium">Date</th>
                <th className="px-6 py-3 font-medium">Product ID</th>
                <th className="px-6 py-3 font-medium">Quantity</th>
                <th className="px-6 py-3 font-medium">Total Amount</th>
                <th className="px-6 py-3 font-medium">Customer</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {filteredSales.slice(0, 50).map((sale) => (
                <tr key={sale.transaction_id} className="hover:bg-gray-800/30">
                  <td className="px-6 py-4 text-sm font-mono text-gray-400">{sale.transaction_id.slice(0, 8)}...</td>
                  <td className="px-6 py-4">{sale.date}</td>
                  <td className="px-6 py-4 font-mono text-primary">{sale.product_id}</td>
                  <td className="px-6 py-4">{sale.quantity_sold}</td>
                  <td className="px-6 py-4">₹{sale.total_amount?.toLocaleString()}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 rounded-full text-xs bg-gray-800 text-gray-300">
                      {sale.customer_type}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
