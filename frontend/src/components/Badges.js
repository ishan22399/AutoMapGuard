import React from 'react';
import { Activity, AlertTriangle, CheckCircle, XCircle, TrendingUp } from 'lucide-react';

export const ConfidenceBadge = ({ confidence, size = 'default' }) => {
  const getVariant = () => {
    if (confidence >= 0.8) return { color: 'bg-green-500/10 text-green-400 border-green-500/20', icon: CheckCircle };
    if (confidence >= 0.5) return { color: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20', icon: AlertTriangle };
    return { color: 'bg-red-500/10 text-red-400 border-red-500/20', icon: XCircle };
  };

  const variant = getVariant();
  const Icon = variant.icon;
  const sizeClasses = size === 'small' ? 'text-xs px-2 py-0.5' : 'text-xs px-2 py-1';

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full ${sizeClasses} font-medium font-mono uppercase tracking-wider border ${variant.color}`}
      data-testid="confidence-badge"
    >
      <Icon className="w-3 h-3" />
      {(confidence * 100).toFixed(0)}%
    </span>
  );
};

export const ChangeTypeBadge = ({ type, size = 'default' }) => {
  const getColor = () => {
    switch (type) {
      case 'new':
        return 'bg-green-500/10 text-green-400 border-green-500/20';
      case 'modified':
        return 'bg-orange-500/10 text-orange-400 border-orange-500/20';
      case 'removed':
        return 'bg-red-500/10 text-red-400 border-red-500/20';
      default:
        return 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20';
    }
  };

  const sizeClasses = size === 'small' ? 'text-xs px-2 py-0.5' : 'text-xs px-2 py-1';

  return (
    <span
      className={`inline-flex items-center rounded-full ${sizeClasses} font-medium font-mono uppercase tracking-wider border ${getColor()}`}
      data-testid="change-type-badge"
    >
      {type}
    </span>
  );
};

export const StatusBadge = ({ status, size = 'default' }) => {
  const getColor = () => {
    switch (status) {
      case 'approved':
      case 'auto_approved':
        return 'bg-green-500/10 text-green-400 border-green-500/20';
      case 'rejected':
        return 'bg-red-500/10 text-red-400 border-red-500/20';
      case 'pending':
        return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
      default:
        return 'bg-zinc-500/10 text-zinc-400 border-zinc-500/20';
    }
  };

  const sizeClasses = size === 'small' ? 'text-xs px-2 py-0.5' : 'text-xs px-2 py-1';

  return (
    <span
      className={`inline-flex items-center rounded-full ${sizeClasses} font-medium font-mono uppercase tracking-wider border ${getColor()}`}
      data-testid="status-badge"
    >
      {status}
    </span>
  );
};
