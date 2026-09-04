import React from 'react';
import { Compass, CheckCircle2, Circle, Target, ChevronRight, BarChart, Flag } from 'lucide-react';

const TodayPlan = ({ data, hasProfile, onToggleTask, onCompleteDay }) => {
  // Requirement 8: Empty State if no plan exists
  if (!hasProfile || !data) {
    return (
      <div className="dashboard-card" style={{ textAlign: 'center', padding: '2.5rem 1.5rem', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ background: 'rgba(99, 102, 241, 0.15)', width: '56px', height: '56px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.25rem' }}>
          <Compass size={28} color="#818cf8" />
        </div>
        <h4 style={{ fontSize: '1rem', color: '#ffffff', margin: '0 0 0.5rem', fontWeight: 700 }}>Curriculum Locked</h4>
        <p style={{ fontSize: '0.82rem', color: '#94a3b8', margin: 0, lineHeight: 1.4 }}>Initialize your learning profile in the chat to generate today's plan.</p>
      </div>
    );
  }

  const allCompleted = data.tasks && data.tasks.length > 0 && data.tasks.every(t => t.completed);

  return (
    <div className="dashboard-card" style={{ gap: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div className="card-title" style={{ color: '#818cf8' }}>
          <Compass size={16} /> TODAY'S PLAN
        </div>
        <div style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', color: '#ffffff', padding: '0.25rem 0.9rem', borderRadius: '20px', fontSize: '0.72rem', fontWeight: 800 }}>
          DAY {data.day}
        </div>
      </div>

      <div style={{ background: 'rgba(30, 41, 59, 0.6)', padding: '1.1rem', borderRadius: '14px', border: '1px solid rgba(255, 255, 255, 0.12)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
          <Target size={14} color="#38bdf8" />
          <span style={{ fontSize: '0.7rem', color: '#38bdf8', fontWeight: 700, letterSpacing: '0.05em' }}>OBJECTIVE</span>
        </div>
        <div style={{ fontSize: '1rem', fontWeight: 700, color: '#ffffff', lineHeight: 1.4 }}>
          {data.objective}
        </div>
      </div>

      <div className="tasks-list" style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
        <div style={{ fontSize: '0.7rem', color: '#94a3b8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>TASKS TO COMPLETE</div>
        {data.tasks.map((task, idx) => (
          <div
            key={idx}
            onClick={() => onToggleTask(idx)}
            className="task-item-premium"
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.8rem',
              padding: '0.85rem',
              borderRadius: '12px',
              background: task.completed ? 'rgba(16, 185, 129, 0.15)' : 'rgba(30, 41, 59, 0.5)',
              border: `1px solid ${task.completed ? 'rgba(16, 185, 129, 0.4)' : 'rgba(255, 255, 255, 0.12)'}`,
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            <div style={{ marginTop: '0.1rem' }}>
              {task.completed ? <CheckCircle2 size={18} color="#34d399" /> : <Circle size={18} color="#94a3b8" />}
            </div>
            <span style={{
              fontSize: '0.9rem',
              fontWeight: 600,
              textDecoration: task.completed ? 'line-through' : 'none',
              color: task.completed ? '#a7f3d0' : '#ffffff',
              lineHeight: 1.3
            }}>
              {task.name}
            </span>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '0.5rem' }}>
        <div style={{ background: 'rgba(30, 41, 59, 0.5)', padding: '0.85rem', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.25rem' }}>
            <BarChart size={13} color="#818cf8" />
            <span style={{ fontSize: '0.65rem', color: '#818cf8', fontWeight: 700, textTransform: 'uppercase' }}>ASSESSMENT</span>
          </div>
          <div style={{ fontSize: '0.82rem', color: '#ffffff', lineHeight: 1.35, fontWeight: 500 }}>{data.assessment}</div>
        </div>
        <div style={{ background: 'rgba(30, 41, 59, 0.5)', padding: '0.85rem', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.25rem' }}>
            <Flag size={13} color="#22d3ee" />
            <span style={{ fontSize: '0.65rem', color: '#22d3ee', fontWeight: 700, textTransform: 'uppercase' }}>OUTCOME</span>
          </div>
          <div style={{ fontSize: '0.82rem', color: '#ffffff', lineHeight: 1.35, fontWeight: 500 }}>{data.expected_outcome}</div>
        </div>
      </div>

      {allCompleted ? (
        <button
          onClick={onCompleteDay}
          style={{
            marginTop: '0.5rem',
            padding: '0.95rem',
            background: 'linear-gradient(135deg, #10b981, #059669)',
            color: '#ffffff',
            border: 'none',
            borderRadius: '14px',
            fontWeight: 800,
            fontSize: '0.95rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.6rem',
            boxShadow: '0 4px 20px rgba(16, 185, 129, 0.4)',
            transition: 'transform 0.2s'
          }}
          onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.02)'}
          onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
        >
          COMPLETE DAY & ADVANCE <ChevronRight size={18} />
        </button>
      ) : (
        <div style={{ textAlign: 'center', padding: '0.5rem', fontSize: '0.78rem', color: '#94a3b8', fontStyle: 'italic' }}>
          Complete all tasks to unlock next day
        </div>
      )}
    </div>
  );
};

export default TodayPlan;
