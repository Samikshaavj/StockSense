import { useEffect, useState } from 'react';
import { getSalesAnalytics } from '../services/api';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, DollarSign, ShoppingCart } from 'lucide-react';

const SalesAnalytics = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    getSalesAnalytics().then((res) => setData(res.data));
  }, []);

  if (!data) return <div className="p-8 text-white">Loading...</div>;

  return (
    <div className="p-8 h-full flex flex-col gap-6">
      <div className="flex items-center gap-3 mb-4">
        <TrendingUp className="text-primary w-8 h-8" />
        <h1 className="text-3xl font-bold text-white">Sales Analytics (Last 30 Days)</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-surface border border-gray-800 p-6 rounded-xl shadow-lg flex items-center gap-6">
          <div className="p-4 bg-primary/20 rounded-full">
            <DollarSign className="w-8 h-8 text-primary" />
          </div>
          <div>
            <h3 className="text-gray-400 font-medium">Total Revenue (30d)</h3>
            <p className="text-3xl font-bold text-white">₹{data.total_revenue_30d.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
          </div>
        </div>

        <div className="bg-surface border border-gray-800 p-6 rounded-xl shadow-lg flex items-center gap-6">
          <div className="p-4 bg-secondary/20 rounded-full">
            <ShoppingCart className="w-8 h-8 text-secondary" />
          </div>
          <div>
            <h3 className="text-gray-400 font-medium">Total Units Sold (30d)</h3>
            <p className="text-3xl font-bold text-white">{data.total_units_30d.toLocaleString()} units</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 flex-1">
        <div className="xl:col-span-2 bg-surface border border-gray-800 p-6 rounded-xl shadow-lg flex flex-col">
          <h2 className="text-xl font-bold text-white mb-6">Daily Revenue Trend</h2>
          <div className="flex-1 min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.daily_sales} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9ca3af" tick={{ fontSize: 12 }} />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #374151', color: '#fff' }} />
                <Legend />
                <Bar dataKey="total_revenue" name="Revenue (INR)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-surface border border-gray-800 p-6 rounded-xl shadow-lg flex flex-col overflow-hidden">
          <h2 className="text-xl font-bold text-white mb-6">Top 5 Products</h2>
          <div className="flex-1 overflow-auto">
            <div className="space-y-4">
              {data.top_products.map((product, idx) =>
              <div key={product.product_id} className="bg-gray-800/50 p-4 rounded-lg flex justify-between items-center border border-gray-700/50">
                  <div>
                    <p className="text-gray-400 text-xs font-semibold mb-1">#{idx + 1} | {product.product_id}</p>
                    <p className="text-white font-medium line-clamp-1">{product.product_name}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-primary font-bold">₹{product.revenue.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}</p>
                    <p className="text-gray-400 text-sm">{product.units_sold} sold</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>);

};

export default SalesAnalytics;