import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Inventory from './pages/Inventory';
import DemandForecast from './pages/DemandForecast';
import ReorderRecommendations from './pages/ReorderRecommendations';
import SalesAnalytics from './pages/SalesAnalytics';
import ProductIntelligence from './pages/ProductIntelligence';
import MLPerformance from './pages/MLPerformance';
import Sales from './pages/Sales';
import Purchases from './pages/Purchases';
import { Package, TrendingUp, Box, Activity, PackagePlus, DollarSign, Brain, Target, ShoppingCart, ShoppingBag } from 'lucide-react';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-background text-gray-100 font-sans">
        {/* Sidebar */}
        <div className="w-64 bg-surface border-r border-gray-800 flex flex-col">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-primary flex items-center gap-2">
              <Box className="w-8 h-8" /> Ranu Autoparts
            </h1>
          </div>
          <nav className="mt-6 flex-1 overflow-y-auto">
            <div className="px-6 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">Operations</div>
            <Link to="/" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <Activity className="w-5 h-5" /> Dashboard
            </Link>
            <Link to="/sales-ops" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <ShoppingCart className="w-5 h-5" /> Sales
            </Link>
            <Link to="/purchases" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <ShoppingBag className="w-5 h-5" /> Purchases
            </Link>
            <Link to="/inventory" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <Package className="w-5 h-5" /> Inventory Master
            </Link>

            <div className="px-6 py-2 mt-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Analytics & Intelligence</div>
            <Link to="/sales-analytics" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <DollarSign className="w-5 h-5" /> Sales Analytics
            </Link>
            <Link to="/product-intelligence" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <Brain className="w-5 h-5" /> Product Intelligence
            </Link>
            <Link to="/demand-forecast" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <TrendingUp className="w-5 h-5" /> Demand Forecast
            </Link>
            <Link to="/reorder-recs" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <PackagePlus className="w-5 h-5" /> Reorder Recs
            </Link>
            
            <div className="px-6 py-2 mt-4 text-xs font-semibold text-gray-500 uppercase tracking-wider">Machine Learning</div>
            <Link to="/ml-performance" className="flex items-center gap-3 px-6 py-3 hover:bg-gray-800 text-gray-300 hover:text-white transition">
              <Target className="w-5 h-5" /> ML Performance
            </Link>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 overflow-auto bg-background">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/sales-ops" element={<Sales />} />
            <Route path="/purchases" element={<Purchases />} />
            <Route path="/sales-analytics" element={<SalesAnalytics />} />
            <Route path="/inventory" element={<Inventory />} />
            <Route path="/product-intelligence" element={<ProductIntelligence />} />
            <Route path="/demand-forecast" element={<DemandForecast />} />
            <Route path="/reorder-recs" element={<ReorderRecommendations />} />
            <Route path="/ml-performance" element={<MLPerformance />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
