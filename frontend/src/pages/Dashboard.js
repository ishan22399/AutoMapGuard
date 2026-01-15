import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { apiService, setAuthToken } from '../utils/api';
import { toast } from 'sonner';
import { Button } from '../components/ui/button';
import MapView from '../components/MapView';
import ChangeInspector from '../components/ChangeInspector';
import DashboardStats from '../components/DashboardStats';
import { Layers, LogOut, Activity, RefreshCw } from 'lucide-react';

const Dashboard = () => {
  const { user, logout, token } = useAuth();
  const [changes, setChanges] = useState([]);
  const [selectedChange, setSelectedChange] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showStats, setShowStats] = useState(true);

  useEffect(() => {
    if (token) {
      setAuthToken(token);
      fetchChanges();
      fetchStats();
    }
  }, [token]);

  const fetchChanges = async () => {
    try {
      const response = await apiService.listChanges();
      setChanges(response.data);
    } catch (error) {
      console.error('Failed to fetch changes:', error);
      toast.error('Failed to load changes');
    }
  };

  const fetchStats = async () => {
    try {
      const response = await apiService.getDashboardStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handleDetectChanges = async () => {
    setLoading(true);
    try {
      const response = await apiService.detectChanges(true);
      toast.success(`Detected ${response.data.length} changes`);
      await fetchChanges();
      await fetchStats();
    } catch (error) {
      console.error('Failed to detect changes:', error);
      toast.error('Failed to detect changes');
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (change) => {
    try {
      // Find review item for this change
      const reviewResponse = await apiService.getReviewQueue();
      const reviewItem = reviewResponse.data.find(r => r.change_id === change.id);
      
      if (reviewItem) {
        await apiService.submitReview(reviewItem.id, 'approve');
        toast.success('Change approved');
        await fetchChanges();
        await fetchStats();
      }
    } catch (error) {
      console.error('Failed to approve change:', error);
      toast.error('Failed to approve change');
    }
  };

  const handleReject = async (change) => {
    try {
      const reviewResponse = await apiService.getReviewQueue();
      const reviewItem = reviewResponse.data.find(r => r.change_id === change.id);
      
      if (reviewItem) {
        await apiService.submitReview(reviewItem.id, 'reject');
        toast.success('Change rejected');
        await fetchChanges();
        await fetchStats();
      }
    } catch (error) {
      console.error('Failed to reject change:', error);
      toast.error('Failed to reject change');
    }
  };

  return (
    <div className="h-screen flex flex-col bg-zinc-950" data-testid="dashboard-page">
      {/* Header */}
      <header className="h-16 bg-zinc-900/50 backdrop-blur-md border-b border-white/10 flex items-center justify-between px-6 z-20">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-sm bg-primary/10 border border-primary/20 flex items-center justify-center">
            <Layers className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h1 className="text-xl font-black text-white" style={{ fontFamily: 'Chivo, sans-serif' }}>
              AutoMapGuard
            </h1>
            <p className="text-xs text-zinc-400">Urban Change Detection System</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowStats(!showStats)}
            className="text-zinc-300 hover:text-white"
            data-testid="toggle-stats-button"
          >
            <Activity className="w-4 h-4 mr-2" />
            {showStats ? 'Hide' : 'Show'} Stats
          </Button>
          <Button
            onClick={handleDetectChanges}
            disabled={loading}
            className="shadow-[0_0_10px_rgba(56,189,248,0.3)]"
            data-testid="detect-changes-button"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            {loading ? 'Detecting...' : 'Detect Changes'}
          </Button>
          <div className="flex items-center gap-3 pl-4 border-l border-white/10">
            <div className="text-right">
              <p className="text-sm font-medium text-white">{user?.full_name || user?.email}</p>
              <p className="text-xs text-zinc-400">GIS Analyst</p>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={logout}
              className="text-zinc-400 hover:text-white"
              data-testid="logout-button"
            >
              <LogOut className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 relative">
        {/* Map */}
        <div className="absolute inset-0">
          <MapView 
            changes={changes}
            onFeatureClick={(properties) => {
              const change = changes.find(c => c.id === properties.id);
              setSelectedChange(change);
            }}
          />
        </div>

        {/* Floating Panels */}
        {showStats && stats && (
          <DashboardStats stats={stats} />
        )}
        
        <ChangeInspector
          changes={changes}
          selectedChange={selectedChange}
          onSelectChange={setSelectedChange}
          onApprove={handleApprove}
          onReject={handleReject}
        />
      </div>
    </div>
  );
};

export default Dashboard;
