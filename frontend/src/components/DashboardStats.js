import React from 'react';
import { Activity, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';

const DashboardStats = ({ stats }) => {
  return (
    <div 
      className="absolute top-4 left-4 w-96 bg-zinc-950/90 backdrop-blur-md border border-white/10 rounded-md shadow-2xl z-10"
      data-testid="dashboard-stats-panel"
    >
      <div className="p-4 border-b border-white/10">
        <h2 className="text-xl font-bold text-white" style={{ fontFamily: 'Chivo, sans-serif' }}>
          System Statistics
        </h2>
      </div>

      <div className="p-4 space-y-4">
        {/* Stat Grid */}
        <div className="grid grid-cols-2 gap-3">
          <StatCard
            label="Total Buildings"
            value={stats.total_buildings}
            icon={Activity}
            color="text-cyan-400"
          />
          <StatCard
            label="Total Detections"
            value={stats.total_detections}
            icon={TrendingUp}
            color="text-green-400"
          />
          <StatCard
            label="Pending Changes"
            value={stats.pending_changes}
            icon={AlertTriangle}
            color="text-yellow-400"
          />
          <StatCard
            label="Pending Reviews"
            value={stats.pending_reviews}
            icon={AlertTriangle}
            color="text-orange-400"
          />
        </div>

        {/* Accuracy */}
        <div className="p-3 bg-zinc-900/50 border border-white/10 rounded-md">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs uppercase tracking-wider text-zinc-400">Accuracy Rate</span>
            <CheckCircle className="w-4 h-4 text-green-400" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-white font-mono">
              {stats.accuracy_rate.toFixed(1)}%
            </span>
          </div>
          <div className="mt-2 h-2 bg-zinc-800 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-green-500 to-green-400 transition-all duration-500"
              style={{ width: `${stats.accuracy_rate}%` }}
            />
          </div>
        </div>

        {/* Recent Activity */}
        {stats.recent_activity && stats.recent_activity.length > 0 && (
          <div>
            <h3 className="text-xs uppercase tracking-wider text-zinc-400 mb-2">Recent Activity</h3>
            <div className="space-y-2">
              {stats.recent_activity.slice(0, 3).map((activity, idx) => (
                <div key={idx} className="p-2 bg-zinc-900/50 border border-white/10 rounded text-xs">
                  <div className="flex justify-between items-center">
                    <span className="text-zinc-300">{activity.type}</span>
                    <span className="font-mono text-primary">{(activity.confidence * 100).toFixed(0)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, color }) => {
  return (
    <div className="p-3 bg-zinc-900/50 border border-white/10 rounded-md" data-testid={`stat-${label.toLowerCase().replace(/\s+/g, '-')}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs uppercase tracking-wider text-zinc-400">{label}</span>
        <Icon className={`w-4 h-4 ${color}`} />
      </div>
      <div className="text-2xl font-black text-white font-mono">
        {value}
      </div>
    </div>
  );
};

export default DashboardStats;
