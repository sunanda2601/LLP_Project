import React from 'react';
import { Brain, Database, Wrench, Zap, MessageSquare } from 'lucide-react';

const AgentReasoning = ({ dashboardData, lastIntent, agentStatus }) => {
  if (!dashboardData?.has_profile && agentStatus === "Idle") return null;

  const reasoning = {
    intent: lastIntent || "ANALYZING_INTENT",
    memory: {
      goal: dashboardData?.learner_profile?.goal || "None",
      level: dashboardData?.learner_profile?.level || "None",
      weak_areas: dashboardData?.learner_profile?.weak_areas?.join(', ') || "None"
    },
    tool: dashboardData?.tool_usage ? Object.keys(dashboardData.tool_usage).filter(k => dashboardData.tool_usage[k]).pop() : "None",
    action: dashboardData?.today_plan ? `Optimizing Day ${dashboardData.today_plan.day} Curriculum` : "Retrieving Memory"
  };

  return (
    <div className="dashboard-card" style={{ background: 'rgba(17, 24, 39, 0.85)', backdropFilter: 'blur(16px)', border: '1px solid rgba(255, 255, 255, 0.12)' }}>
      <div className="card-title" style={{ color: '#818cf8' }}>
        <Brain size={16} /> Agent Reasoning
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
          <Zap size={16} color="#fbbf24" style={{ marginTop: '0.2rem', flexShrink: 0 }} />
          <div>
            <div style={{ fontSize: '0.68rem', fontWeight: 700, color: '#fbbf24', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Intent Detected</div>
            <div style={{ fontSize: '0.92rem', fontWeight: 700, color: '#ffffff' }}>{reasoning.intent}</div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
          <Database size={16} color="#818cf8" style={{ marginTop: '0.2rem', flexShrink: 0 }} />
          <div>
            <div style={{ fontSize: '0.68rem', fontWeight: 700, color: '#818cf8', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Memory Context</div>
            <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.4 }}>
               Goal: <strong style={{ color: '#ffffff' }}>{reasoning.memory.goal}</strong><br/>
               Level: <span style={{ color: '#ffffff' }}>{reasoning.memory.level}</span>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
          <Wrench size={16} color="#34d399" style={{ marginTop: '0.2rem', flexShrink: 0 }} />
          <div>
            <div style={{ fontSize: '0.68rem', fontWeight: 700, color: '#34d399', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Tool Execution</div>
            <div style={{ fontSize: '0.88rem', color: '#ffffff', fontWeight: 700 }}>{reasoning.tool?.toUpperCase() || "NONE"}</div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
          <MessageSquare size={16} color="#38bdf8" style={{ marginTop: '0.2rem', flexShrink: 0 }} />
          <div>
            <div style={{ fontSize: '0.68rem', fontWeight: 700, color: '#38bdf8', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Current Action</div>
            <div style={{ fontSize: '0.88rem', color: '#ffffff', fontWeight: 700 }}>{reasoning.action}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentReasoning;
