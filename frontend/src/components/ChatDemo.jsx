import React, { useRef, useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowUp,
  Languages,
  SpellCheck,
  BookOpen,
  Volume2,
  Shuffle,
  Calendar,
  MessageSquare,
  ArrowRight,
  Compass,
  MessageCircle,
  Lightbulb,
  Sparkles,
} from "lucide-react";
import { updateCompletedTasks, completeDay } from "../services/api";
import LearnerProfile from "./dashboard/LearnerProfile";
import LearningAnalytics from "./dashboard/LearningAnalytics";
import AgentStatus from "./dashboard/AgentStatus";
import Roadmap from "./dashboard/Roadmap";
import TodayPlan from "./dashboard/TodayPlan";
import ToolIntegration from "./dashboard/ToolIntegration";
import AgentReasoning from "./dashboard/AgentReasoning";
import AgentActivityFeed from "./dashboard/AgentActivityFeed";
import JourneyTimeline from "./dashboard/JourneyTimeline";
import "../styles/dashboard.css";
import "./ChatDemo.css";

const EXAMPLE_QUESTIONS = [
  { text: "I want to improve English", icon: Sparkles },
  { text: "Create a 30-Day Placement English Plan", icon: Calendar },
  { text: "What should I study today?", icon: Compass },
  { text: "Translate \"How are you?\" to Telugu", icon: Languages },
  { text: "Meaning of perseverance", icon: BookOpen },
];

export default function ChatDemo({
  messages,
  inputMessage,
  setInputMessage,
  onSendMessage,
  onPromptClick,
  isLoading,
  sectionRef,
  dashboardData,
  agentStatus,
  statusMessage,
  onRefreshDashboard,
  activeTab = "all"
}) {
  const chatBottomRef = useRef(null);
  const [updatingTask, setUpdatingTask] = useState(false);
  const [advancingDay, setAdvancingDay] = useState(false);

  // Extract last intent from messages
  const lastIntent = messages.filter(m => m.role === 'assistant' && m.intent).pop()?.intent;

  useEffect(() => {
    if (chatBottomRef.current) {
      chatBottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isLoading]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSendMessage();
    }
  };

  const handleToggleTask = async (idx) => {
    if (updatingTask || !dashboardData?.today_plan?.tasks) return;
    
    const tasks = dashboardData.today_plan.tasks;
    const updated = tasks.map((t, i) => i === idx ? { ...t, completed: !t.completed } : t);
    
    try {
      setUpdatingTask(true);
      const completedNames = updated.filter(t => t.completed).map(t => t.name);
      await updateCompletedTasks(completedNames);
      if (onRefreshDashboard) {
        await onRefreshDashboard();
      }
    } catch (err) {
      console.error("Failed to update tasks:", err);
    } finally {
      setUpdatingTask(false);
    }
  };

  const handleCompleteDay = async () => {
    if (advancingDay) return;
    try {
      setAdvancingDay(true);
      const res = await completeDay();
      if (res && res.success) {
        if (onRefreshDashboard) {
          await onRefreshDashboard();
        }
      }
    } catch (err) {
      console.error("Failed to advance day:", err);
    } finally {
      setAdvancingDay(false);
    }
  };

  const parseStructuredResponse = (text, headers) => {
    const sections = {};
    let currentHeader = null;
    const lines = text.split("\n");

    for (let line of lines) {
      const cleanLine = line.trim();
      if (cleanLine === "") continue;

      const normalizedLine = cleanLine
        .replace(/^\*+\s*/, "")
        .replace(/\*+$/, "")
        .replace(/:+$/, "")
        .trim()
        .toLowerCase();

      let matchedHeader = null;
      for (let header of headers) {
        const lowerHeader = header.toLowerCase();
        if (
          normalizedLine === lowerHeader ||
          normalizedLine.startsWith(lowerHeader + ":") ||
          normalizedLine.startsWith(lowerHeader)
        ) {
          matchedHeader = header;
          break;
        }
      }

      if (matchedHeader) {
        currentHeader = matchedHeader;
        sections[currentHeader] = [];
      } else if (currentHeader) {
        sections[currentHeader].push(line);
      }
    }

    for (let key in sections) {
      sections[key] = sections[key].join("\n").trim();
    }

    return sections;
  };

  const renderBotText = (text) => {
    if (!text) return null;
    const lines = text.split("\n");

    return lines.map((line, index) => {
      const isBullet = line.startsWith("- ") || line.startsWith("* ") || line.startsWith("• ");
      const isNumber = /^\d+\.\s/.test(line);

      let cleanLine = line;
      if (isBullet) cleanLine = line.substring(2);
      else if (isNumber) cleanLine = line.replace(/^\d+\.\s/, "");

      const parts = cleanLine.split(/\*\*(.*?)\*\*/g);
      const elements = parts.map((part, i) => {
        if (i % 2 === 1) return <strong key={i} style={{ color: "var(--accent-blue)", fontWeight: "600" }}>{part}</strong>;
        return part;
      });

      if (isBullet) return <li key={index} className="bot-bullet">{elements}</li>;
      if (isNumber) return <li key={index} className="bot-number">{elements}</li>;
      if (line.trim() === "") return <div key={index} className="bot-gap" />;
      return <p key={index} className="bot-para">{elements}</p>;
    });
  };

  const getFeatureIcon = (feature) => {
    switch (feature) {
      case "GRAMMAR": return SpellCheck;
      case "TRANSLATION": return Languages;
      case "VOCABULARY": return BookOpen;
      case "PRONUNCIATION": return Volume2;
      case "SYNONYMS":
      case "ANTONYMS": return Shuffle;
      case "WORD_OF_DAY": return Calendar;
      case "DAILY_PHRASES": return Compass;
      case "CONVERSATION": return MessageCircle;
      default: return Sparkles;
    }
  };

  const getFeatureTitle = (feature) => {
    switch (feature) {
      case "GRAMMAR": return "Grammar Advisor";
      case "TRANSLATION": return "Translation Hub";
      case "VOCABULARY": return "Vocabulary Insights";
      case "PRONUNCIATION": return "Pronunciation Guide";
      case "SYNONYMS": return "Synonym Finder";
      case "ANTONYMS": return "Antonym Companion";
      case "WORD_OF_DAY": return "Word of the Day";
      case "DAILY_PHRASES": return "Daily Phrase List";
      case "CONVERSATION": return "Conversation Coach";
      default: return "Language Learning Pal Assistant";
    }
  };

  const renderResponseCard = (feature, text) => {
    if (!text) return null;
    const FeatureIcon = getFeatureIcon(feature);
    const title = getFeatureTitle(feature);
    const allHeaders = ["Word", "Pronunciation", "Meaning", "Usage Tip", "Memory Trick", "Original", "Corrected", "Explanation", "Translation"];
    const parsed = parseStructuredResponse(text, allHeaders);
    const headerTitle = parsed.Word || parsed.Phrase || title;
    
    return (
      <div className="response-card premium-response-card" style={{ background: 'rgba(15, 23, 42, 0.95)', border: '1px solid rgba(255, 255, 255, 0.15)', borderRadius: '16px', padding: '1.1rem', color: '#ffffff' }}>
        <div className="card-header" style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', paddingBottom: '0.6rem', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <FeatureIcon size={18} style={{ color: '#38bdf8' }} />
          <span style={{ fontWeight: 700, fontSize: '0.95rem', color: '#ffffff' }}>{headerTitle}</span>
        </div>
        <div className="card-body" style={{ padding: 0 }}>
          <div className="card-content-wrapper">
            {parsed.Original && (
              <div className="card-row error-row" style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '10px', padding: '0.6rem', marginBottom: '0.6rem' }}>
                <span className="row-title" style={{ fontSize: '0.72rem', color: '#f87171', fontWeight: 700, textTransform: 'uppercase' }}>Original</span>
                <p className="row-text" style={{ margin: '0.2rem 0 0', color: '#f8fafc', fontWeight: 500 }}>{parsed.Original.replace(/^["']|["']$/g, "")}</p>
              </div>
            )}
            {parsed.Corrected && (
              <div className="card-row success-row" style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '10px', padding: '0.6rem', marginBottom: '0.6rem' }}>
                <span className="row-title" style={{ fontSize: '0.72rem', color: '#34d399', fontWeight: 700, textTransform: 'uppercase' }}>Corrected</span>
                <p className="row-text" style={{ margin: '0.2rem 0 0', color: '#ffffff', fontWeight: 600 }}>{parsed.Corrected.replace(/^["']|["']$/g, "")}</p>
              </div>
            )}
            {parsed.Translation && (
              <div className="card-row success-row" style={{ background: 'rgba(99, 102, 241, 0.15)', border: '1px solid rgba(99, 102, 241, 0.3)', borderRadius: '10px', padding: '0.6rem', marginBottom: '0.6rem' }}>
                <span className="row-title" style={{ fontSize: '0.72rem', color: '#818cf8', fontWeight: 700, textTransform: 'uppercase' }}>Translation</span>
                <p className="row-text" style={{ margin: '0.2rem 0 0', color: '#ffffff', fontWeight: 600 }}>{parsed.Translation}</p>
              </div>
            )}
            {parsed.Meaning && (
              <div className="card-row primary-meaning-row" style={{ marginBottom: '0.6rem' }}>
                <span className="row-title" style={{ fontSize: '0.72rem', color: '#94a3b8', fontWeight: 700, textTransform: 'uppercase' }}>Meaning</span>
                <p className="row-text" style={{ margin: '0.2rem 0 0', color: '#ffffff', fontWeight: 600 }}>{parsed.Meaning}</p>
              </div>
            )}
            {parsed.Explanation && <div className="info-row" style={{ fontSize: '0.92rem', color: '#cbd5e1' }}>{renderBotText(parsed.Explanation)}</div>}
          </div>
          {!Object.keys(parsed).length && <div className="formatted-bot-text" style={{ color: '#ffffff' }}>{renderBotText(text)}</div>}

          {(parsed["Usage Tip"] || parsed["Memory Trick"]) && (
            <div className="card-tips-area" style={{ marginTop: '0.85rem', borderTop: '1px solid rgba(255, 255, 255, 0.1)', paddingTop: '0.85rem' }}>
              {parsed["Usage Tip"] && (
                <div className="tip-box" style={{ background: 'rgba(6, 182, 212, 0.15)', border: '1px solid rgba(6, 182, 212, 0.3)', borderRadius: '10px', padding: '0.6rem', display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
                  <Lightbulb size={16} style={{ color: '#22d3ee', flexShrink: 0, marginTop: '2px' }} />
                  <div style={{ fontSize: '0.88rem', color: '#ffffff' }}><strong style={{ color: '#38bdf8' }}>Usage Tip:</strong> {parsed["Usage Tip"]}</div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
  };

  const getCleanBadgeLabel = (feature) => feature?.replace("_", " ").toUpperCase() || "";
  const hasProfile = dashboardData?.has_profile === true;

  return (
    <section className="chat-section" ref={sectionRef} style={{ width: '100%', padding: '2rem 0 4rem' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 1.5rem' }}>

        {/* TAB VIEW 1: CHAT COACH (also shown on 'all') */}
        {(activeTab === 'chat' || activeTab === 'all' || !activeTab) && (
          <div style={{ display: 'grid', gridTemplateColumns: activeTab === 'all' ? '1fr 1.3fr' : '1.2fr 0.8fr', gap: '2rem', alignItems: 'start' }}>
            {/* Left Chat Panel */}
            <div className="chat-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              <div className="agent-status-bar" style={{ background: 'rgba(17, 24, 39, 0.85)', backdropFilter: 'blur(16px)', borderColor: 'rgba(255, 255, 255, 0.12)', color: '#ffffff', borderRadius: '16px', padding: '0.9rem 1.4rem', boxShadow: '0 4px 20px rgba(0,0,0,0.3)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div className="status-indicator" style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                  <span className="status-dot-pulse" style={{ backgroundColor: agentStatus === 'Planning' ? '#f59e0b' : agentStatus === 'Executing' ? '#6366f1' : '#10b981' }} />
                  <span style={{ fontWeight: 700, color: '#ffffff', fontSize: '0.95rem' }}>{agentStatus}</span>
                </div>
                <span style={{ fontSize: '0.85rem', color: '#94a3b8', fontStyle: 'italic' }}>{statusMessage}</span>
              </div>

              <div className="example-queries-box" style={{ background: 'rgba(17, 24, 39, 0.75)', backdropFilter: 'blur(16px)', borderColor: 'rgba(255, 255, 255, 0.12)', borderRadius: '18px', padding: '1.2rem' }}>
                <p style={{ fontSize: '0.8rem', fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.8rem' }}>Practice Prompts</p>
                <div className="queries-chips-grid" style={{ display: 'flex', flexWrap: 'wrap', gap: '0.55rem' }}>
                  {EXAMPLE_QUESTIONS.map((q, i) => (
                    <button key={i} className="query-chip-btn" onClick={() => onPromptClick(q.text)} style={{ background: 'rgba(30, 41, 59, 0.6)', borderColor: 'rgba(255, 255, 255, 0.12)', color: '#ffffff', borderRadius: '20px', padding: '0.55rem 0.95rem', display: 'flex', alignItems: 'center', gap: '0.45rem', cursor: 'pointer', transition: 'all 0.2s ease' }}>
                      <q.icon size={14} style={{ color: '#818cf8' }} />
                      <span style={{ fontWeight: 600, fontSize: '0.85rem', color: '#ffffff' }}>{q.text}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="chat-console-dashboard" style={{ background: 'rgba(15, 23, 42, 0.92)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255, 255, 255, 0.12)', height: '600px', borderRadius: '24px', boxShadow: '0 10px 40px rgba(0,0,0,0.5)', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
                <div className="chat-messages-container" style={{ flex: 1, overflowY: 'auto', padding: '1.2rem' }}>
                  {messages.length === 0 ? (
                    <div className="chat-empty-state" style={{ textAlign: 'center', padding: '3rem 1rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                      <div className="empty-icon-circle" style={{ background: 'rgba(99, 102, 241, 0.15)', width: '60px', height: '60px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><MessageSquare size={30} color="#818cf8" /></div>
                      <h3 style={{ fontSize: '1.4rem', fontWeight: 800, marginTop: '1.2rem', color: '#ffffff' }}>Language Learning Pal AI Agent</h3>
                      <p style={{ color: '#94a3b8', maxWidth: '340px', margin: '0.5rem auto', textAlign: 'center', fontSize: '0.92rem' }}>
                        {hasProfile ? `Ready to continue your ${dashboardData.learner_profile.goal} roadmap?` : 'Your personal AI conversation coach is ready. Select a prompt or ask a question!'}
                      </p>
                    </div>
                  ) : (
                    <div className="messages-flow" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      {messages.map((msg, i) => (
                        <motion.div key={i} className={`message-row ${msg.role === 'user' ? 'user-row' : 'bot-row'}`} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                          <div className="bubble-wrapper">
                            {msg.role === 'assistant' && msg.intent && (
                              <div className="feature-badge" style={{ background: '#6366f1', color: '#ffffff', borderRadius: '12px', padding: '2px 8px', fontSize: '0.68rem', fontWeight: 700, display: 'inline-block', marginBottom: '0.3rem' }}>
                                <span>{getCleanBadgeLabel(msg.intent)}</span>
                              </div>
                            )}
                            <div className={`bubble ${msg.role === 'user' ? 'user-bubble' : 'bot-bubble'}`} style={msg.role === 'user' ? { background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)', color: '#ffffff', borderRadius: '18px 18px 4px 18px', padding: '0.85rem 1.1rem', fontWeight: 500 } : { background: 'rgba(30, 41, 59, 0.85)', color: '#ffffff', border: '1px solid rgba(255, 255, 255, 0.12)', borderRadius: '18px 18px 18px 4px' }}>
                              {msg.role === 'user' ? <p style={{ margin: 0, fontSize: '0.95rem', color: '#ffffff' }}>{msg.text}</p> : renderResponseCard(msg.intent, msg.text)}
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  )}
                  <div ref={chatBottomRef} />
                </div>
                <div className="chat-input-area" style={{ background: 'rgba(15, 23, 42, 0.95)', borderTop: '1px solid rgba(255, 255, 255, 0.1)', padding: '1rem 1.2rem' }}>
                  <div className="input-pill" style={{ background: 'rgba(30, 41, 59, 0.8)', border: '1px solid rgba(255, 255, 255, 0.15)', borderRadius: '24px', padding: '0.4rem 0.5rem 0.4rem 1.2rem', display: 'flex', alignItems: 'center' }}>
                    <input type="text" placeholder="Ask your AI tutor anything..." value={inputMessage} onChange={(e) => setInputMessage(e.target.value)} onKeyDown={handleKeyDown} style={{ color: '#ffffff', background: 'transparent', border: 0, outline: 0, width: '100%', fontSize: '0.95rem' }} />
                    <button className="send-button" onClick={() => onSendMessage()} style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', borderRadius: '50%', width: '38px', height: '38px', display: 'flex', alignItems: 'center', justifyContent: 'center', border: 0, cursor: 'pointer', color: '#ffffff', flexShrink: 0 }}><ArrowUp size={18} /></button>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Live Reasoning & Status for Chat tab */}
            {activeTab === 'chat' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                <AgentReasoning dashboardData={dashboardData} lastIntent={lastIntent} agentStatus={agentStatus} />
                <LearnerProfile data={dashboardData?.learner_profile} hasProfile={hasProfile} />
              </div>
            )}

            {/* Full Dashboard Widgets for 'all' tab */}
            {activeTab === 'all' && (
              <div className="dashboard-panel" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                  <AgentReasoning dashboardData={dashboardData} lastIntent={lastIntent} agentStatus={agentStatus} />
                  <LearnerProfile data={dashboardData?.learner_profile} hasProfile={hasProfile} />
                </div>
                <JourneyTimeline dashboardData={dashboardData} />
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                  <TodayPlan data={dashboardData?.today_plan} hasProfile={hasProfile} onToggleTask={handleToggleTask} onCompleteDay={handleCompleteDay} />
                  <LearningAnalytics data={dashboardData?.learning_analytics} hasProfile={hasProfile} />
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                  <Roadmap data={dashboardData?.roadmap} hasProfile={hasProfile} />
                  <ToolIntegration data={dashboardData?.tool_usage} />
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB VIEW 2: LEARNER PROFILE & ANALYTICS */}
        {activeTab === 'analytics' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
              <LearnerProfile data={dashboardData?.learner_profile} hasProfile={hasProfile} />
              <LearningAnalytics data={dashboardData?.learning_analytics} hasProfile={hasProfile} />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
              <AgentStatus status={agentStatus} message={statusMessage} />
              <AgentActivityFeed dashboardData={dashboardData} />
            </div>
          </div>
        )}

        {/* TAB VIEW 3: 30-DAY PLAN & ROADMAP */}
        {activeTab === 'roadmap' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.5rem', alignItems: 'start' }}>
              <TodayPlan
                data={dashboardData?.today_plan}
                hasProfile={hasProfile}
                onToggleTask={handleToggleTask}
                onCompleteDay={handleCompleteDay}
              />
              <Roadmap data={dashboardData?.roadmap} hasProfile={hasProfile} />
            </div>
            <JourneyTimeline dashboardData={dashboardData} />
          </div>
        )}

        {/* TAB VIEW 4: AI TOOLS & PRACTICE */}
        {activeTab === 'tools' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <ToolIntegration data={dashboardData?.tool_usage} />
            <div className="example-queries-box" style={{ background: 'rgba(17, 24, 39, 0.85)', backdropFilter: 'blur(16px)', borderColor: 'rgba(255, 255, 255, 0.12)', borderRadius: '20px', padding: '1.5rem' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#ffffff', marginBottom: '1rem' }}>Interactive Quick Prompts</h3>
              <div className="queries-chips-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '0.75rem' }}>
                {EXAMPLE_QUESTIONS.map((q, i) => (
                  <button key={i} className="query-chip-btn" onClick={() => onPromptClick(q.text)} style={{ background: 'rgba(30, 41, 59, 0.6)', borderColor: 'rgba(255, 255, 255, 0.12)', color: '#ffffff', borderRadius: '14px', padding: '0.85rem 1.1rem', display: 'flex', alignItems: 'center', gap: '0.6rem', cursor: 'pointer', transition: 'all 0.2s ease', textAlign: 'left' }}>
                    <q.icon size={18} style={{ color: '#818cf8', flexShrink: 0 }} />
                    <span style={{ fontWeight: 600, fontSize: '0.92rem', color: '#ffffff' }}>{q.text}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

      </div>
    </section>
  );
}
