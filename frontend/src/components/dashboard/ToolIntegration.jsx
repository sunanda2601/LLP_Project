import React from 'react';
import { Brain, BookOpen, Languages, Volume2, SpellCheck } from 'lucide-react';

const ToolIntegration = ({ data }) => {
  if (!data) return null;

  const { vocabulary, translation, pronunciation, grammar } = data;

  // Requirement 10: Hide card if no tool data is available
  const hasData = vocabulary || translation || pronunciation || grammar;

  if (!hasData) return null;

  return (
    <div className="dashboard-card" style={{ gap: '1rem' }}>
      <div className="card-title" style={{ color: '#818cf8' }}>
        <Brain size={16} /> Tool Integration
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {vocabulary && (
          <div className="tool-box" style={{ background: 'rgba(168, 85, 247, 0.15)', border: '1px solid rgba(168, 85, 247, 0.3)', padding: '0.85rem', borderRadius: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
              <BookOpen size={14} color="#c084fc" />
              <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#c084fc', textTransform: 'uppercase' }}>Vocabulary</span>
            </div>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>{vocabulary.word}</div>
            <div style={{ fontSize: '0.78rem', color: '#cbd5e1', marginTop: '0.2rem' }}>{vocabulary.meaning}</div>
          </div>
        )}

        {translation && (
          <div className="tool-box" style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', padding: '0.85rem', borderRadius: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
              <Languages size={14} color="#34d399" />
              <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#34d399', textTransform: 'uppercase' }}>Translation</span>
            </div>
            <div style={{ fontSize: '0.78rem', color: '#cbd5e1' }}>English: {translation.english}</div>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff', marginTop: '0.2rem' }}>Telugu: {translation.telugu}</div>
          </div>
        )}

        {pronunciation && (
          <div className="tool-box" style={{ background: 'rgba(6, 182, 212, 0.15)', border: '1px solid rgba(6, 182, 212, 0.3)', padding: '0.85rem', borderRadius: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
              <Volume2 size={14} color="#22d3ee" />
              <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#22d3ee', textTransform: 'uppercase' }}>Pronunciation</span>
            </div>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>{pronunciation.word}</div>
            <div style={{ fontSize: '0.8rem', color: '#38bdf8', fontStyle: 'italic', marginTop: '0.2rem' }}>{pronunciation.phonetic}</div>
          </div>
        )}

        {grammar && (
          <div className="tool-box" style={{ background: 'rgba(245, 158, 11, 0.15)', border: '1px solid rgba(245, 158, 11, 0.3)', padding: '0.85rem', borderRadius: '14px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
              <SpellCheck size={14} color="#fbbf24" />
              <span style={{ fontSize: '0.7rem', fontWeight: 800, color: '#fbbf24', textTransform: 'uppercase' }}>Grammar Advisor</span>
            </div>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#ffffff' }}>{grammar.rule}</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ToolIntegration;
