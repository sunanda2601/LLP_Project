import React from 'react';
import { User, Target, Brain, Award } from 'lucide-react';

const LearnerProfile = ({ data, hasProfile }) => {
  if (!hasProfile) {
    return (
      <div className="dashboard-card">
        <div className="card-title" style={{ color: '#818cf8' }}>
          <User size={16} /> Learner Profile
        </div>
        <div style={{ textAlign: 'center', padding: '1.2rem', border: '1px dashed rgba(255, 255, 255, 0.15)', borderRadius: '14px', background: 'rgba(30, 41, 59, 0.4)' }}>
          <h4 style={{ fontSize: '0.95rem', color: '#ffffff', margin: '0 0 0.3rem', fontWeight: 700 }}>No Profile Available</h4>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: 0 }}>Start a conversation to create your learning identity.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-card">
      <div className="card-title" style={{ color: '#818cf8' }}>
        <User size={16} /> Learner Profile
      </div>

      <div className="profile-content" style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        <div className="info-row">
          <span className="info-label" style={{ fontSize: '0.68rem', textTransform: 'uppercase', fontWeight: 700, color: '#94a3b8', letterSpacing: '0.05em' }}>Current Level</span>
          <div className="badge-pill" style={{ background: 'rgba(99, 102, 241, 0.2)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.4)', fontWeight: 800, padding: '0.35rem 0.8rem', borderRadius: '20px', fontSize: '0.82rem', width: 'fit-content', marginTop: '0.2rem' }}>
            {data.level}
          </div>
        </div>

        <div className="info-row">
          <span className="info-label" style={{ fontSize: '0.68rem', textTransform: 'uppercase', fontWeight: 700, color: '#94a3b8', letterSpacing: '0.05em' }}>Primary Goal</span>
          <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#ffffff', marginTop: '0.1rem' }}>{data.goal}</div>
        </div>

        <div className="info-row">
          <span className="info-label" style={{ fontSize: '0.68rem', textTransform: 'uppercase', fontWeight: 700, color: '#94a3b8', letterSpacing: '0.05em' }}>Focus Areas</span>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.45rem', marginTop: '0.3rem' }}>
            {data.weak_areas && data.weak_areas.length > 0 ? (
              data.weak_areas.map((area, idx) => (
                <span key={idx} className="badge-pill" style={{ fontSize: '0.72rem', background: 'rgba(168, 85, 247, 0.2)', color: '#e9d5ff', border: '1px solid rgba(168, 85, 247, 0.4)', fontWeight: 700, padding: '0.2rem 0.65rem', borderRadius: '12px' }}>
                  {area}
                </span>
              ))
            ) : (
              <span style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>General Mastery</span>
            )}
          </div>
        </div>

        <div className="progress-container" style={{ marginTop: '0.6rem' }}>
          <div className="progress-header" style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', fontWeight: 800, marginBottom: '0.45rem' }}>
            <span style={{ color: '#94a3b8', letterSpacing: '0.05em' }}>COURSE PROGRESS</span>
            <span style={{ color: '#38bdf8' }}>{data.progress}%</span>
          </div>
          <div className="progress-track" style={{ height: '8px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '4px', overflow: 'hidden' }}>
            <div
              className="progress-fill"
              style={{ width: `${data.progress}%`, background: 'linear-gradient(90deg, #6366f1, #38bdf8)', height: '100%', borderRadius: '4px' }}
            />
          </div>
          <div style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: '0.45rem', textAlign: 'right', fontWeight: 700 }}>
            Day {data.current_day} / 30
          </div>
        </div>
      </div>
    </div>
  );
};

export default LearnerProfile;
