import React from 'react';
import { History, Clock } from 'lucide-react';

const AgentActivityFeed = ({ dashboardData }) => {
  if (!dashboardData?.has_profile) return null;

  // Simulate activities based on data changes
  const activities = [
    { time: 'Just now', desc: 'Curriculum Synchronization' },
    { time: '1 min ago', desc: `Progress sync: ${dashboardData.learning_analytics?.progress}%` },
    { time: '5 mins ago', desc: 'Long-term memory retrieval' },
    { time: '10 mins ago', desc: 'Agent session initialized' }
  ];

  return (
    <div className="dashboard-card">
      <div className="card-title" style={{ color: '#818cf8' }}>
        <History size={16} /> Activity Feed
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        {activities.map((act, i) => (
          <div key={i} style={{ display: 'flex', gap: '0.75rem', borderLeft: '2px solid rgba(255, 255, 255, 0.12)', paddingLeft: '0.85rem', position: 'relative' }}>
            <div style={{ position: 'absolute', left: '-5px', top: '2px', width: '8px', height: '8px', borderRadius: '50%', background: i === 0 ? '#38bdf8' : '#94a3b8', boxShadow: i === 0 ? '0 0 8px #38bdf8' : 'none' }} />
            <div>
              <div style={{ fontSize: '0.85rem', fontWeight: 700, color: '#ffffff' }}>{act.desc}</div>
              <div style={{ fontSize: '0.7rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '0.25rem', marginTop: '0.15rem' }}>
                <Clock size={12} color="#818cf8" /> {act.time}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgentActivityFeed;
