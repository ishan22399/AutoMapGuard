import React from 'react';
import { ConfidenceBadge, ChangeTypeBadge } from './Badges';
import { Button } from './ui/button';
import { ScrollArea } from './ui/scroll-area';
import { CheckCircle, XCircle, MapPin } from 'lucide-react';

const ChangeInspector = ({ changes, onSelectChange, selectedChange, onApprove, onReject }) => {
  return (
    <div 
      className="absolute top-4 right-4 w-96 max-h-[calc(100vh-2rem)] bg-zinc-950/90 backdrop-blur-md border border-white/10 rounded-md shadow-2xl z-10"
      data-testid="change-inspector-panel"
    >
      <div className="p-4 border-b border-white/10">
        <h2 className="text-xl font-bold text-white" style={{ fontFamily: 'Chivo, sans-serif' }}>
          Change Inspector
        </h2>
        <p className="text-sm text-zinc-400 mt-1">
          {changes.length} changes detected
        </p>
      </div>

      <ScrollArea className="h-[calc(100vh-12rem)]">
        <div className="p-4 space-y-3">
          {changes.length === 0 ? (
            <div className="text-center py-8 text-zinc-400">
              <MapPin className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p>No changes detected</p>
            </div>
          ) : (
            changes.map((change) => (
              <div
                key={change.id}
                onClick={() => onSelectChange && onSelectChange(change)}
                className={`p-3 bg-zinc-900/50 border rounded-md cursor-pointer transition-all duration-200 ${
                  selectedChange?.id === change.id
                    ? 'border-primary shadow-[0_0_10px_rgba(56,189,248,0.3)]'
                    : 'border-white/10 hover:border-white/20'
                }`}
                data-testid={`change-item-${change.id}`}
              >
                <div className="flex items-start justify-between mb-2">
                  <ChangeTypeBadge type={change.change_type} size="small" />
                  <ConfidenceBadge confidence={change.confidence} size="small" />
                </div>
                <div className="text-sm space-y-1">
                  <div className="flex justify-between text-zinc-400">
                    <span className="uppercase text-xs tracking-wider">Area:</span>
                    <span className="font-mono text-white">{change.area.toFixed(2)} m²</span>
                  </div>
                  <div className="flex justify-between text-zinc-400">
                    <span className="uppercase text-xs tracking-wider">Status:</span>
                    <span className="font-mono text-white">{change.status}</span>
                  </div>
                </div>
                {change.status === 'pending' && (
                  <div className="flex gap-2 mt-3">
                    <Button
                      size="sm"
                      variant="ghost"
                      className="flex-1 text-green-400 hover:bg-green-500/10 hover:text-green-300"
                      onClick={(e) => {
                        e.stopPropagation();
                        onApprove && onApprove(change);
                      }}
                      data-testid={`approve-change-${change.id}`}
                    >
                      <CheckCircle className="w-4 h-4 mr-1" />
                      Approve
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      className="flex-1 text-red-400 hover:bg-red-500/10 hover:text-red-300"
                      onClick={(e) => {
                        e.stopPropagation();
                        onReject && onReject(change);
                      }}
                      data-testid={`reject-change-${change.id}`}
                    >
                      <XCircle className="w-4 h-4 mr-1" />
                      Reject
                    </Button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </ScrollArea>
    </div>
  );
};

export default ChangeInspector;
