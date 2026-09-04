import React from 'react';
import { TrendingUp, Book, CheckCircle, Zap, SpellCheck } from 'lucide-react';

const LearningAnalytics = ({ data, hasProfile }) => {
  // Requirement 7: Initialize with zero values if no profile exists
  // dashboardData.learning_analytics keys: overall_progress, vocabulary_learned, grammar_exercises, days_completed, current_streak
  const metrics = [
    {
      label: 'Progress',
      value: hasProfile ? `${data.progress}%` : '0%',
      icon: TrendingUp,
      color: '#38bdf8',
      bg: 'rgba(56, 189, 248, 0.15)'
    },
    {
      label: 'Vocabulary',
      value: hasProfile ? data.vocabulary_learned : '0',
      icon: Book,
      color: '#c084fc',
      bg: 'rgba(192, 132, 252, 0.15)'
    },
    {
      label: 'Grammar',
      value: hasProfile ? data.grammar_exercises : '0',
      icon: SpellCheck,
      color: '#f87171',
      bg: 'rgba(248, 113, 113, 0.15)'
    },
    {
      label: 'Completed',
      value: hasProfile ? data.days_completed : '0',
      icon: CheckCircle,
      color: '#34d399',
      bg: 'rgba(52, 211, 153, 0.15)'
    },
    {
      label: 'Streak',
      value: hasProfile ? data.current_streak : '0',
      icon: Zap,
      color: '#fbbf24',
      bg: 'rgba(251, 191, 36, 0.15)'
    },
  ];

  return (
    <div className="dashboard-card">
      <div className="card-title" style={{ color: '#818cf8' }}>
        <TrendingUp size={16} /> Learning Analytics
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(85px, 1fr))', gap: '0.75rem' }}>
        {metrics.map((metric, idx) => (
          <div key={idx} className="metric-card" style={{ padding: '0.85rem 0.6rem', display: 'flex', flexDirection: 'column', alignItems: 'center', background: 'rgba(30, 41, 59, 0.5)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '14px' }}>
            <div style={{ background: metric.bg, padding: '0.45rem', borderRadius: '50%', marginBottom: '0.5rem' }}>
              <metric.icon size={16} style={{ color: metric.color }} />
            </div>
            <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#ffffff' }}>{metric.value}</div>
            <div style={{ fontSize: '0.65rem', color: '#94a3b8', fontWeight: 700, textTransform: 'uppercase', marginTop: '0.15rem', letterSpacing: '0.04em' }}>{metric.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LearningAnalytics;
