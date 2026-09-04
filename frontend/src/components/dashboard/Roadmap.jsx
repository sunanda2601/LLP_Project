import React from 'react';
import { Layers, Check, Lock, Play } from 'lucide-react';

const Roadmap = ({ data, hasProfile }) => {
  if (!hasProfile || !data) {
    return (
      <div className="dashboard-card">
        <div className="card-title">
          <Layers size={16} /> 30-Day Roadmap
        </div>
        <div className="profile-empty" style={{ padding: '1rem', textAlign: 'center', color: '#86868b', fontSize: '0.8rem' }}>
          No roadmap generated yet
        </div>
      </div>
    );
  }

  // Render roadmap dynamically based on keys returned by backend
  // Backend returns: { "week1": { "name": "...", "status": "..." }, ... }
  const roadmapKeys = Object.keys(data).sort(); // Sort to ensure sequence

  return (
    <div className="dashboard-card">
      <div className="card-title" style={{ color: '#818cf8' }}>
        <Layers size={16} /> 30-Day Roadmap
      </div>

      <div className="roadmap-timeline" style={{ marginTop: '0.6rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {roadmapKeys.map((key, idx) => {
          const weekData = data[key];
          const isCompleted = weekData?.status === 'completed';
          const isActive = weekData?.status === 'in-progress';

          // Format key (e.g., "week1" -> "Week 1")
          const label = key.charAt(0).toUpperCase() + key.slice(1).replace(/(\d+)/, ' $1');

          return (
            <div key={idx} className={`roadmap-item ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`} style={{ display: 'flex', gap: '0.85rem', alignItems: 'center' }}>
              <div className="roadmap-icon" style={{ background: isCompleted ? '#10b981' : isActive ? '#6366f1' : 'rgba(255,255,255,0.06)', color: '#ffffff', borderColor: isCompleted ? '#10b981' : isActive ? '#6366f1' : 'rgba(255,255,255,0.15)' }}>
                {isCompleted ? <Check size={14} /> : isActive ? <Play size={12} fill="currentColor" /> : <Lock size={12} />}
              </div>
              <div className="roadmap-content">
                <div style={{ fontSize: '0.7rem', color: '#94a3b8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{label}</div>
                <div style={{ fontSize: '0.92rem', fontWeight: 700, color: isCompleted ? '#34d399' : isActive ? '#ffffff' : '#94a3b8' }}>
                  {weekData?.name || 'Locked'}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Roadmap;
