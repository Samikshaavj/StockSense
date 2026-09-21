import { useEffect, useState } from 'react';
import { getProducts, createProduct, adjustStock } from '../services/api';
import type { Product, ProductCreate } from '../services/api';
import { Search, Plus, Edit3 } from 'lucide-react';

const Inventory = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState('');
  
  const [isProdModalOpen, setProdModalOpen] = useState(false);
  const [isAdjModalOpen, setAdjModalOpen] = useState(false);
  const [selectedProductId, setSelectedProductId] = useState('');
  
  // Product Form State
  const [prodForm, setProdForm] = useState<ProductCreate>({
    product_name: '', category: 'Oil', brand: '', purchase_price_inr: 0, selling_price_inr: 0,
    minimum_stock_level: 10, maximum_stock_level: 100, initial_stock: 0
  });

  // Adj Form State
  const [adjAmount, setAdjAmount] = useState(0);
  const [adjReason, setAdjReason] = useState('Physical count reconciliation');

  const fetchInventory = () => {
    getProducts().then(res => setProducts(res.data));
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createProduct(prodForm);
      setProdModalOpen(false);
      fetchInventory();
    } catch (err) {
      console.error(err);
      alert('Failed to create product');
    }
  };

  const handleAdjustStock = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await adjustStock({
        product_id: selectedProductId,
        adjustment_amount: adjAmount,
        reason: adjReason
      });
      setAdjModalOpen(false);
      fetchInventory();
    } catch (err) {
      console.error(err);
      alert('Failed to adjust stock');
    }
  };

  const filteredProducts = products.filter(p => 
    p.product_name.toLowerCase().includes(search.toLowerCase()) ||
    p.product_id.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-white">Inventory Master</h1>
        <div className="flex items-center gap-4">
          <div className="relative w-72">
            <input
              type="text"
              placeholder="Search products..."
              className="w-full bg-surface border border-gray-700 rounded-lg pl-10 pr-4 py-2 text-white focus:outline-none focus:border-primary"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <Search className="absolute left-3 top-2.5 text-gray-400 w-5 h-5" />
          </div>
          <button 
            onClick={() => setProdModalOpen(true)}
            className="flex items-center gap-2 bg-primary text-black font-semibold px-4 py-2 rounded-lg hover:bg-primary/90 transition"
          >
            <Plus className="w-5 h-5" /> New Product
          </button>
        </div>
      </div>

      <div className="bg-surface rounded-xl border border-gray-800 shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-[#1e293b]">
              <tr className="text-gray-300">
                <th className="px-6 py-4 font-medium">Product ID</th>
                <th className="px-6 py-4 font-medium">Name</th>
                <th className="px-6 py-4 font-medium">Category</th>
                <th className="px-6 py-4 font-medium">Current Stock</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {filteredProducts.map((p) => {
                // Mock simple status logic based on stock (since the backend now provides this in Intelligence API, but we just want quick badge here)
                let badgeClass = 'bg-green-500/20 text-green-400';
                let statusText = 'Healthy';
                if (p.current_stock === 0) { badgeClass = 'bg-red-500/20 text-red-400'; statusText = 'Out of Stock'; }
                else if (p.current_stock < 15) { badgeClass = 'bg-orange-500/20 text-orange-400'; statusText = 'Low'; }

                return (
                <tr key={p.product_id} className="hover:bg-gray-800/50 transition">
                  <td className="px-6 py-4 text-gray-400 text-sm font-mono">{p.product_id}</td>
                  <td className="px-6 py-4 text-white font-medium">{p.product_name}</td>
                  <td className="px-6 py-4 text-gray-300">{p.category}</td>
                  <td className="px-6 py-4 text-gray-100 font-bold">{p.current_stock}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-md text-xs font-semibold ${badgeClass}`}>
                      {statusText}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-300">
                    <button 
                      onClick={() => { setSelectedProductId(p.product_id); setAdjAmount(0); setAdjModalOpen(true); }}
                      className="text-primary hover:text-primary/70 transition flex items-center gap-1 text-sm"
                    >
                      <Edit3 className="w-4 h-4" /> Adjust
                    </button>
                  </td>
                </tr>
              )})}
            </tbody>
          </table>
        </div>
      </div>

      {/* Adjust Modal */}
      {isAdjModalOpen && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
          <div className="bg-surface p-6 rounded-xl border border-gray-700 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Adjust Stock ({selectedProductId})</h2>
            <form onSubmit={handleAdjustStock} className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Adjustment Amount (+/-)</label>
                <input 
                  type="number" 
                  value={adjAmount} 
                  onChange={e => setAdjAmount(Number(e.target.value))}
                  className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white"
                  required 
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Reason</label>
                <input 
                  type="text" 
                  value={adjReason} 
                  onChange={e => setAdjReason(e.target.value)}
                  className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white"
                  required 
                />
              </div>
              <div className="flex justify-end gap-3 mt-6">
                <button type="button" onClick={() => setAdjModalOpen(false)} className="px-4 py-2 text-gray-400 hover:text-white">Cancel</button>
                <button type="submit" className="bg-primary text-black font-semibold px-4 py-2 rounded-lg">Apply Adjustment</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* New Product Modal */}
      {isProdModalOpen && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
          <div className="bg-surface p-6 rounded-xl border border-gray-700 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">Add New Product</h2>
            <form onSubmit={handleCreateProduct} className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <label className="block text-sm text-gray-400 mb-1">Product Name</label>
                <input type="text" value={prodForm.product_name} onChange={e => setProdForm({...prodForm, product_name: e.target.value})} className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white" required />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Category</label>
                <input type="text" value={prodForm.category} onChange={e => setProdForm({...prodForm, category: e.target.value})} className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Brand</label>
                <input type="text" value={prodForm.brand} onChange={e => setProdForm({...prodForm, brand: e.target.value})} className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Purchase Price (₹)</label>
                <input type="number" step="0.01" value={prodForm.purchase_price_inr} onChange={e => setProdForm({...prodForm, purchase_price_inr: Number(e.target.value)})} className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white" required />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Selling Price (₹)</label>
                <input type="number" step="0.01" value={prodForm.selling_price_inr} onChange={e => setProdForm({...prodForm, selling_price_inr: Number(e.target.value)})} className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white" required />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Min Stock Level (Safety)</label>
                <input type="number" value={prodForm.minimum_stock_level} onChange={e => setProdForm({...prodForm, minimum_stock_level: Number(e.target.value)})} className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white" required />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Max Stock Level</label>
                <input type="number" value={prodForm.maximum_stock_level} onChange={e => setProdForm({...prodForm, maximum_stock_level: Number(e.target.value)})} className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white" required />
              </div>
              <div className="col-span-2">
                <label className="block text-sm text-gray-400 mb-1">Initial Stock</label>
                <input type="number" value={prodForm.initial_stock} onChange={e => setProdForm({...prodForm, initial_stock: Number(e.target.value)})} className="w-full bg-background border border-gray-700 rounded-lg px-4 py-2 text-white" required />
              </div>
              
              <div className="col-span-2 flex justify-end gap-3 mt-4">
                <button type="button" onClick={() => setProdModalOpen(false)} className="px-4 py-2 text-gray-400 hover:text-white">Cancel</button>
                <button type="submit" className="bg-primary text-black font-semibold px-4 py-2 rounded-lg">Create Product</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default Inventory;
