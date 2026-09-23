import { useEffect, useState } from 'react';
import { getReorderRecs } from '../services/api';

import { PackagePlus } from 'lucide-react';

const ReorderRecommendations = () => {
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    getReorderRecs().then((res) => setRecs(res.data));
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'Reorder Now':return 'bg-red-500/20 text-red-400 border-red-500/50';
      case 'Reorder Soon':return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50';
      case 'Monitor':return 'bg-blue-500/20 text-blue-400 border-blue-500/50';
      default:return 'bg-gray-500/20 text-gray-400 border-gray-500/50';
    }
  };

  return (
    <div className="p-8">
      <div className="flex items-center gap-3 mb-8">
        <PackagePlus className="text-primary w-8 h-8" />
        <h1 className="text-3xl font-bold text-white">Reorder Recommendations</h1>
      </div>

      <div className="bg-surface rounded-xl border border-gray-800 shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-[#1e293b]">
              <tr className="text-gray-300">
                <th className="px-6 py-4 font-medium">Product Name</th>
                <th className="px-6 py-4 font-medium">Current Stock</th>
                <th className="px-6 py-4 font-medium">Safety Stock</th>
                <th className="px-6 py-4 font-medium">Predicted Demand (14 Days)</th>
                <th className="px-6 py-4 font-medium">Required Stock</th>
                <th className="px-6 py-4 font-medium">Reorder Qty</th>
                <th className="px-6 py-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {recs.map((rec) =>
              <tr key={rec.product_id} className="hover:bg-gray-800/50 transition">
                  <td className="px-6 py-4 text-white font-medium">{rec.product_name}</td>
                  <td className="px-6 py-4 text-gray-300">{rec.current_stock}</td>
                  <td className="px-6 py-4 text-gray-400">{rec.safety_stock}</td>
                  <td className="px-6 py-4 text-gray-400">{rec.predicted_demand.toFixed(1)}</td>
                  <td className="px-6 py-4 text-gray-300">{rec.required_stock.toFixed(1)}</td>
                  <td className="px-6 py-4">
                    <span className="font-bold text-primary">+{rec.recommended_reorder_quantity}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getStatusColor(rec.status)}`}>
                      {rec.status}
                    </span>
                  </td>
                </tr>
              )}
              {recs.length === 0 &&
              <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-gray-500">
                    No reorder recommendations at this time. Inventory levels are optimal.
                  </td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      </div>
    </div>);

};

export default ReorderRecommendations;