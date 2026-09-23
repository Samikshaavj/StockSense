import { useEffect, useState } from 'react';
import { getModelPerformance, retrainModels } from '../services/api';
import { Target, Activity, Settings, RefreshCw } from 'lucide-react';

const MLPerformance = () => {
  const [perf, setPerf] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchPerf = () => {
    getModelPerformance().then((res) => setPerf(res.data));
  };

  useEffect(() => {
    fetchPerf();
  }, []);

  const handleRetrain = async () => {
    setLoading(true);
    try {
      await retrainModels();
      await fetchPerf();
    } catch (err) {
      console.error(err);
      alert('Failed to retrain models.');
    } finally {
      setLoading(false);
    }
  };

  if (!perf) return <div className="p-8 text-white">Loading Performance Metrics...</div>;

  const bestModelData = perf.selected_model && perf.results ? perf.results[perf.selected_model] : null;

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-3">
          <Target className="text-primary w-8 h-8" />
          <h1 className="text-3xl font-bold text-white">Model Performance</h1>
        </div>
        <button
          onClick={handleRetrain}
          disabled={loading}
          className="flex items-center gap-2 bg-primary text-black font-semibold px-4 py-2 rounded-lg hover:bg-primary/90 transition disabled:opacity-50">
          
          <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
          {loading ? 'Training...' : 'Retrain Models'}
        </button>
      </div>

      <div className="max-w-4xl space-y-6">
        <div className="bg-surface border border-gray-800 p-8 rounded-xl shadow-lg">
          <div className="flex items-center gap-3 mb-6">
            <Activity className="text-secondary w-6 h-6" />
            <h2 className="text-xl font-bold text-white">Evaluation Metrics (Test Set)</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-gray-800/30 rounded-lg border border-gray-700/50">
              <h3 className="text-gray-400 font-medium mb-2">RMSE</h3>
              <p className="text-4xl font-bold text-white">{bestModelData?.Test_RMSE?.toFixed(4) || 'N/A'}</p>
            </div>
            <div className="p-6 bg-gray-800/30 rounded-lg border border-gray-700/50">
              <h3 className="text-gray-400 font-medium mb-2">MAE</h3>
              <p className="text-4xl font-bold text-white">{bestModelData?.Test_MAE?.toFixed(4) || 'N/A'}</p>
            </div>
            <div className="p-6 bg-gray-800/30 rounded-lg border border-gray-700/50">
              <h3 className="text-gray-400 font-medium mb-2">MAPE</h3>
              <p className="text-4xl font-bold text-primary">{bestModelData?.Test_MAPE ? `${bestModelData.Test_MAPE.toFixed(2)}%` : 'N/A'}</p>
            </div>
          </div>
        </div>

        <div className="bg-surface border border-gray-800 p-8 rounded-xl shadow-lg">
          <div className="flex items-center gap-3 mb-6">
            <Settings className="text-gray-400 w-6 h-6" />
            <h2 className="text-xl font-bold text-white">Model Configuration</h2>
          </div>
          <ul className="space-y-4 text-gray-300">
            <li className="flex items-center justify-between border-b border-gray-800 pb-3">
              <span className="font-medium text-gray-400">Selected Algorithm</span>
              <span className="font-mono bg-gray-800 px-3 py-1 rounded">{perf.selected_model || 'N/A'}</span>
            </li>
            <li className="flex items-center justify-between border-b border-gray-800 pb-3">
              <span className="font-medium text-gray-400">Last Trained</span>
              <span className="font-mono bg-gray-800 px-3 py-1 rounded">
                {perf.training_date ? new Date(perf.training_date).toLocaleString() : 'N/A'}
              </span>
            </li>
            <li className="flex items-center justify-between border-b border-gray-800 pb-3">
              <span className="font-medium text-gray-400">Dataset Period</span>
              <span className="font-mono bg-gray-800 px-3 py-1 rounded">{perf.dataset_period || 'N/A'}</span>
            </li>
            <li className="flex items-center justify-between border-b border-gray-800 pb-3">
              <span className="font-medium text-gray-400">Samples Used</span>
              <span className="font-mono bg-gray-800 px-3 py-1 rounded">{perf.num_samples || 'N/A'}</span>
            </li>
            <li className="flex items-center justify-between pb-3">
              <span className="font-medium text-gray-400">Features</span>
              <span className="font-mono bg-gray-800 px-3 py-1 rounded text-xs truncate max-w-xs">
                {perf.features ? perf.features.join(', ') : 'N/A'}
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>);

};

export default MLPerformance;