import { useEffect, useState } from 'react';
import { getProducts, getProductIntelligence } from '../services/api';
import type { Product, ProductIntelligenceResponse } from '../services/api';
import { Brain, Package, AlertTriangle, TrendingUp, DollarSign } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ProductIntelligence = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<string>('');
  const [intel, setIntel] = useState<ProductIntelligenceResponse | null>(null);

  useEffect(() => {
    getProducts().then(res => {
      setProducts(res.data);
      if (res.data.length > 0) {
        setSelectedProduct(res.data[0].product_id);
      }
    });
  }, []);

  useEffect(() => {
    if (selectedProduct) {
      getProductIntelligence(selectedProduct).then(res => setIntel(res.data));
    }
  }, [selectedProduct]);

  if (!intel) return <div className="p-8 text-white">Loading Intelligence...</div>;

  const chartData = intel.forecast.forecast.map((val, idx) => ({
    day: `Day ${idx + 1}`,
    PredictedDemand: val
  }));

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Critical': return 'text-red-500 bg-red-500/10 border-red-500/20';
      case 'High': return 'text-orange-500 bg-orange-500/10 border-orange-500/20';
      case 'Medium': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20';
      case 'Low': return 'text-green-500 bg-green-500/10 border-green-500/20';
      default: return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
    }
  };

  return (
    <div className="p-8 h-full flex flex-col gap-6 overflow-y-auto">
      <div className="flex justify-between items-center mb-2">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <Brain className="text-primary w-8 h-8" />
          Product Intelligence
        </h1>
        <div className="w-80">
          <select 
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
            className="w-full bg-surface border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary"
          >
            {products.map(p => (
              <option key={p.product_id} value={p.product_id}>
                {p.product_id} - {p.product_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-surface p-6 rounded-xl border border-gray-800 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <Package className="w-5 h-5 text-gray-400" />
            <h3 className="text-gray-400 font-medium">Inventory</h3>
          </div>
          <p className="text-3xl font-bold text-white">{intel.product.current_stock} <span className="text-lg font-normal text-gray-500">units</span></p>
        </div>

        <div className="bg-surface p-6 rounded-xl border border-gray-800 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <AlertTriangle className="w-5 h-5 text-gray-400" />
            <h3 className="text-gray-400 font-medium">Stock-Out Risk</h3>
          </div>
          <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${getRiskColor(intel.stock_risk.risk_level)}`}>
            {intel.stock_risk.risk_level}
          </span>
          <p className="text-gray-400 mt-3 text-sm">{intel.stock_risk.days_remaining.toFixed(1)} days remaining</p>
        </div>

        <div className="bg-surface p-6 rounded-xl border border-gray-800 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="w-5 h-5 text-gray-400" />
            <h3 className="text-gray-400 font-medium">Movement Class</h3>
          </div>
          <p className="text-xl font-bold text-white">{intel.movement_classification.classification}</p>
          <p className="text-gray-400 mt-2 text-sm">{intel.movement_classification.average_daily_demand.toFixed(2)} units/day avg</p>
        </div>

        <div className="bg-surface p-6 rounded-xl border border-gray-800 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <DollarSign className="w-5 h-5 text-gray-400" />
            <h3 className="text-gray-400 font-medium">30d Revenue</h3>
          </div>
          <p className="text-3xl font-bold text-white">₹{intel.historical_revenue_30d.toLocaleString()}</p>
          <p className="text-gray-400 mt-1 text-sm">{intel.historical_sales_30d} units sold</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        <div className="lg:col-span-2 bg-surface p-6 rounded-xl border border-gray-800 shadow-lg flex flex-col">
          <h2 className="text-xl font-bold text-white mb-6">14-Day Demand Forecast</h2>
          <div className="flex-1 min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="day" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #374151', color: '#fff' }} />
                <Legend />
                <Line type="monotone" dataKey="PredictedDemand" name="Predicted Demand" stroke="#10b981" strokeWidth={3} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-surface p-6 rounded-xl border border-gray-800 shadow-lg flex flex-col gap-6">
          <div>
             <h2 className="text-xl font-bold text-white mb-4">Reorder Action</h2>
             <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
               <p className="text-gray-400 mb-1 text-sm">Action Status</p>
               <p className="font-bold text-lg text-white mb-3">{intel.reorder_recommendation.status}</p>
               
               <p className="text-gray-400 mb-1 text-sm">Recommended Quantity</p>
               <p className="font-bold text-3xl text-primary">+{intel.reorder_recommendation.recommended_reorder_quantity}</p>
             </div>
          </div>
          
          <div>
            <h2 className="text-xl font-bold text-white mb-4">Product Specs</h2>
            <ul className="space-y-3">
              <li className="flex justify-between border-b border-gray-800 pb-2">
                <span className="text-gray-400">Category</span>
                <span className="text-white font-medium">{intel.product.category}</span>
              </li>
              <li className="flex justify-between border-b border-gray-800 pb-2">
                <span className="text-gray-400">Brand</span>
                <span className="text-white font-medium">{intel.product.brand}</span>
              </li>
              <li className="flex justify-between border-b border-gray-800 pb-2">
                <span className="text-gray-400">Unit Price</span>
                <span className="text-white font-medium">₹{intel.product.selling_price_inr}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductIntelligence;
