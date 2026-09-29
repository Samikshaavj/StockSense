import { useEffect, useState } from 'react';
import { getStockRisk, getReorderRecs, getDeadStock } from '../services/api';

import { AlertTriangle, TrendingDown, Clock, Package, PlusCircle, ArrowDownCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [stockRisk, setStockRisk] = useState(() => JSON.parse(localStorage.getItem('stockRisk')) || []);
  const [reorderRecs, setReorderRecs] = useState(() => JSON.parse(localStorage.getItem('reorderRecs')) || []);
  const [deadStock, setDeadStock] = useState(() => JSON.parse(localStorage.getItem('deadStock')) || []);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getStockRisk().then((res) => {
        const data = res.data.filter((r) => r.risk_level === 'Critical' || r.risk_level === 'High');
        setStockRisk(data);
        localStorage.setItem('stockRisk', JSON.stringify(data));
      }),
      getReorderRecs().then((res) => {
        const data = res.data.filter((r) => r.status === 'Reorder Now');
        setReorderRecs(data);
        localStorage.setItem('reorderRecs', JSON.stringify(data));
      }),
      getDeadStock().then((res) => {
        const data = res.data.filter((d) => d.status === 'Dead Stock');
        setDeadStock(data);
        localStorage.setItem('deadStock', JSON.stringify(data));
      })
    ]).finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Inventory Intelligence Dashboard</h1>
        </div>
        <div className="flex gap-4 items-center">
          <Link to="/sales-ops" className="flex items-center gap-2 bg-primary text-black font-semibold px-4 py-2 rounded-lg hover:bg-primary/90 transition">
            <PlusCircle className="w-5 h-5" /> New Sale
          </Link>
          <Link to="/purchases" className="flex items-center gap-2 bg-surface border border-gray-700 text-white font-semibold px-4 py-2 rounded-lg hover:bg-gray-800 transition">
            <ArrowDownCircle className="w-5 h-5" /> Receive Stock
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-surface rounded-xl p-6 border border-gray-800 flex items-center shadow-lg">
          <div className="bg-red-500/10 p-4 rounded-lg mr-4">
            <AlertTriangle className="text-danger w-8 h-8" />
          </div>
          <div>
            <p className="text-gray-400 text-sm">Critical Stock-Out Risk</p>
            <p className="text-3xl font-bold text-white">{stockRisk.length}</p>
          </div>
        </div>

        <div className="bg-surface rounded-xl p-6 border border-gray-800 flex items-center shadow-lg">
          <div className="bg-yellow-500/10 p-4 rounded-lg mr-4">
            <TrendingDown className="text-warning w-8 h-8" />
          </div>
          <div>
            <p className="text-gray-400 text-sm">Actionable Reorders</p>
            <p className="text-3xl font-bold text-white">{reorderRecs.length}</p>
          </div>
        </div>

        <div className="bg-surface rounded-xl p-6 border border-gray-800 flex items-center shadow-lg">
          <div className="bg-gray-500/10 p-4 rounded-lg mr-4">
            <Clock className="text-gray-400 w-8 h-8" />
          </div>
          <div>
            <p className="text-gray-400 text-sm">Dead Stock Items</p>
            <p className="text-3xl font-bold text-white">{deadStock.length}</p>
          </div>
        </div>


      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Critical Risks */}
        <div className="bg-surface rounded-xl border border-gray-800 p-6 shadow-lg">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-danger">
            <AlertTriangle className="w-5 h-5" /> Urgent Attention
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="text-gray-400 border-b border-gray-800">
                  <th className="pb-3 font-medium">Product</th>
                  <th className="pb-3 font-medium">Current Stock</th>
                  <th className="pb-3 font-medium">Days Remaining</th>
                </tr>
              </thead>
              <tbody>
                {stockRisk.slice(0, 5).map((risk) =>
                <tr key={risk.product_id} className="border-b border-gray-800/50">
                    <td className="py-4 text-white truncate max-w-[200px]" title={risk.product_name}>
                      {risk.product_name}
                    </td>
                    <td className="py-4 text-white">
                      <span className="bg-red-500/20 text-red-400 px-2 py-1 rounded-md text-sm font-semibold">
                        {risk.current_stock}
                      </span>
                    </td>
                    <td className="py-4 text-danger font-medium">{risk.days_remaining.toFixed(1)} days</td>
                  </tr>
                )}
                {stockRisk.length === 0 && !isLoading &&
                <tr>
                    <td colSpan={3} className="py-4 text-gray-500 text-center">No critical risks currently.</td>
                  </tr>
                }
                {stockRisk.length === 0 && isLoading &&
                <tr>
                    <td colSpan={3} className="py-4 text-gray-500 text-center">Loading critical risks...</td>
                  </tr>
                }
              </tbody>
            </table>
          </div>
        </div>

        {/* Reorder Action */}
        <div className="bg-surface rounded-xl border border-gray-800 p-6 shadow-lg">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-warning">
            <Package className="w-5 h-5" /> Recommended Reorders
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="text-gray-400 border-b border-gray-800">
                  <th className="pb-3 font-medium">Product</th>
                  <th className="pb-3 font-medium">Current</th>
                  <th className="pb-3 font-medium">Reorder Qty</th>
                </tr>
              </thead>
              <tbody>
                {reorderRecs.slice(0, 5).map((rec) =>
                <tr key={rec.product_id} className="border-b border-gray-800/50">
                    <td className="py-4 text-white truncate max-w-[200px]" title={rec.product_name}>
                      {rec.product_name}
                    </td>
                    <td className="py-4 text-white">{rec.current_stock}</td>
                    <td className="py-4 text-warning font-medium">+{rec.recommended_reorder_quantity}</td>
                  </tr>
                )}
                {reorderRecs.length === 0 && !isLoading &&
                <tr>
                    <td colSpan={3} className="py-4 text-gray-500 text-center">No actionable reorders right now.</td>
                  </tr>
                }
                {reorderRecs.length === 0 && isLoading &&
                <tr>
                    <td colSpan={3} className="py-4 text-gray-500 text-center">Loading recommendations...</td>
                  </tr>
                }
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Dead Stock Items */}
      <div className="mt-8 bg-surface rounded-xl border border-gray-800 p-6 shadow-lg">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-gray-400">
          <Clock className="w-5 h-5" /> Dead Stock Items
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-gray-400 border-b border-gray-800">
                <th className="pb-3 font-medium">Product</th>
                <th className="pb-3 font-medium">Current Stock</th>
              </tr>
            </thead>
            <tbody>
              {deadStock.slice(0, 10).map((item) =>
              <tr key={item.product_id} className="border-b border-gray-800/50">
                  <td className="py-4 text-white truncate max-w-[200px]" title={item.product_name}>
                    {item.product_name}
                  </td>
                  <td className="py-4 text-white">{item.current_stock}</td>
                </tr>
              )}
              {deadStock.length === 0 && !isLoading &&
              <tr>
                  <td colSpan={2} className="py-4 text-gray-500 text-center">No dead stock found. Great!</td>
                </tr>
              }
              {deadStock.length === 0 && isLoading &&
              <tr>
                  <td colSpan={2} className="py-4 text-gray-500 text-center">Loading dead stock data...</td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      </div>
    </div>);

};

export default Dashboard;