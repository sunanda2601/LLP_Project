import React from 'react';
import { Calendar } from 'lucide-react';

const JourneyTimeline = ({ dashboardData }) => {
  if (!dashboardData?.has_profile) return null;

  const currentDay = dashboardData.learner_profile?.current_day || 1;
  const days = Array.from({ length: 30 }, (_, i) => i + 1);

  return (
    <div className="dashboard-card">
      <div className="card-title" style={{ color: '#818cf8' }}>
        <Calendar size={16} /> 30-Day Learning Journey
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(15, 1fr)', gap: '0.45rem', marginTop: '0.6rem' }}>
        {days.map(day => {
          const isCompleted = day < currentDay;
          const isCurrent = day === currentDay;

          return (
            <div
              key={day}
              title={`Day ${day}`}
              style={{
                height: '28px',
                borderRadius: '6px',
                background: isCompleted ? '#10b981' : isCurrent ? 'linear-gradient(135deg, #6366f1, #8b5cf6)' : 'rgba(30, 41, 59, 0.5)',
                border: isCurrent ? '2px solid #818cf8' : '1px solid rgba(255, 255, 255, 0.1)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.7rem',
                fontWeight: 800,
                color: (isCompleted || isCurrent) ? '#ffffff' : '#94a3b8',
                boxShadow: isCurrent ? '0 0 12px rgba(99, 102, 241, 0.5)' : 'none'
              }}
            >
              {day}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default JourneyTimeline;
