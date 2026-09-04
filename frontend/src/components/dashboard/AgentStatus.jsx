import React from 'react';
import { Activity } from 'lucide-react';

const AgentStatus = ({ status, message }) => {
  // Required execution timeline steps
  const steps = [
    { label: 'Analyzing Intent' },
    { label: 'Retrieving Memory' },
    { label: 'Generating Plan' },
    { label: 'Executing Tools' },
    { label: 'Generating Response' },
    { label: 'Progress Update' }
  ];

  const getStatusColor = () => {
    switch (status) {
      case 'Analyzing Intent': return '#ff9500'; // Amber
      case 'Retrieving Memory': return '#af52de'; // Purple
      case 'Generating Plan': return '#5856d6'; // Indigo
      case 'Executing Tools': return '#0071e3'; // Blue
      case 'Generating Response': return '#5ac8fa'; // Cyan
      case 'Completed': return '#34c759'; // Green
      default: return '#34c759'; // Idle (Ready)
    }
  };

  return (
    <div className="dashboard-card">
      <div className="card-title" style={{ color: '#818cf8' }}>
        <Activity size={16} /> Agent Intelligence Pipeline
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.35rem' }}>
        <div className="status-dot-pulse" style={{
          width: '10px',
          height: '10px',
          borderRadius: '50%',
          backgroundColor: getStatusColor(),
          boxShadow: `0 0 10px ${getStatusColor()}`
        }} />
        <span style={{ fontSize: '0.92rem', fontWeight: 800, color: '#ffffff' }}>{status}</span>
      </div>

      <div className="pipeline-container" style={{ display: 'flex', flexDirection: 'column', gap: '0.55rem', marginTop: '0.5rem' }}>
        {steps.map((step, idx) => {
          // Logic to show progression
          const stepOrder = steps.map(s => s.label);
          const currentIndex = stepOrder.indexOf(status);
          const isPast = currentIndex > idx || status === 'Completed';
          const isActive = status === step.label;

          return (
            <div key={idx} className={`pipeline-step ${isActive || isPast ? 'active' : ''}`} style={{ opacity: isActive || isPast ? 1 : 0.4 }}>
              <div className="step-dot" style={{ background: isPast ? '#34d399' : isActive ? getStatusColor() : 'rgba(255,255,255,0.2)' }} />
              <span className="step-name" style={{ fontWeight: isActive ? 800 : 500, color: isActive ? '#ffffff' : isPast ? '#34d399' : '#94a3b8', fontSize: '0.85rem' }}>
                {step.label} {isPast && '✓'}
              </span>
            </div>
          );
        })}
      </div>

      <p style={{ fontSize: '0.78rem', color: '#cbd5e1', marginTop: '0.75rem', fontStyle: 'italic', lineHeight: 1.35 }}>
        {message}
      </p>
    </div>
  );
};

export default AgentStatus;
