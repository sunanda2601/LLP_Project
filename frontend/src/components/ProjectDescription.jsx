import React from "react";
import { motion } from "framer-motion";
import { 
  Brain, 
  Layers, 
  Cpu, 
  Activity, 
  ArrowRight
} from "lucide-react";
import "./ProjectDescription.css";

export default function ProjectDescription() {
  const capabilities = [
    {
      title: "Memory System",
      description: "Maintains persistent knowledge of user profiles, learning level, active goals, specific weak areas, and day-wise progress logs.",
      icon: Brain,
      color: "icon-blue"
    },
    {
      title: "Automated Planner",
      description: "Generates tailored 30-day curriculum roadmaps, calibrates week-wise focus areas, and structures daily exercises and outcomes.",
      icon: Layers,
      color: "icon-purple"
    },
    {
      title: "Tool Router",
      description: "Integrates external APIs including dictionaries, translation hubs, thesaurus helpers, and phonetic breakdown coaching modules.",
      icon: Cpu,
      color: "icon-green"
    },
    {
      title: "Progress Tracker",
      description: "Monitors daily streaks, completed curriculum tasks, vocabulary counts, grammar stats, and performance metrics dynamically.",
      icon: Activity,
      color: "icon-orange"
    }
  ];

  const workflowSteps = [
    { name: "User Query", desc: "Learner inputs request" },
    { name: "Intent Analysis", desc: "Parses query type" },
    { name: "Memory & Profile", desc: "Retrieves goals & level" },
    { name: "Plan Calibration", desc: "Checks active day plan" },
    { name: "Tool Routing", desc: "Executes APIs (Dict/Translate)" },
    { name: "Response & Update", desc: "Saves progress & responds" }
  ];

  const comparisonRows = [
    { feature: "Maintains User Memory", chatbot: false, agent: true },
    { feature: "Creates Personalized 30-Day plans", chatbot: false, agent: true },
    { feature: "Tracks Long-term Progress & Stats", chatbot: false, agent: true },
    { feature: "Runs External Tools & API Routers", chatbot: false, agent: true },
    { feature: "Generates Day-wise Curriculum", chatbot: false, agent: true },
    { feature: "Adapts Advice Based on Weak Areas", chatbot: false, agent: true }
  ];

  return (
    <motion.section 
      className="description-section"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* 1. Core Summary Card */}
      <div className="description-card">
        <h2>What is Language Learning Pal?</h2>
        <p className="description-text">
          Language Learning Pal is an <strong>intelligent, autonomous language-learning partner</strong> built to provide a structured, personalized English training experience. Unlike generic chatbots, it functions as a true AI agent by reasoning, utilizing tools, managing memory, and tracking progress.
        </p>
      </div>

      {/* 2. Core Agent Capabilities Grid */}
      <div className="capabilities-wrapper">
        <h3 className="section-subtitle">Core Agent Capabilities</h3>
        <div className="capabilities-grid">
          {capabilities.map((cap, idx) => (
            <div key={idx} className="capability-card">
              <div className="capability-icon-circle">
                <cap.icon size={20} className={`cap-icon ${cap.color}`} />
              </div>
              <h4>{cap.title}</h4>
              <p>{cap.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* 3. AI Agent Workflow Chart */}
      <div className="workflow-wrapper">
        <h3 className="section-subtitle">AI Agent Workflow Loop</h3>
        <div className="workflow-timeline">
          {workflowSteps.map((step, idx) => (
            <div key={idx} className="workflow-node-container">
              <div className="workflow-node">
                <span className="step-num">{idx + 1}</span>
                <span className="step-name">{step.name}</span>
                <span className="step-desc">{step.desc}</span>
              </div>
              {idx < workflowSteps.length - 1 && (
                <div className="workflow-arrow">
                  <ArrowRight size={16} />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 4. Comparison Table */}
      <div className="comparison-wrapper">
        <h3 className="section-subtitle">What Makes It an AI Agent?</h3>
        <div className="comparison-card">
          <div className="comparison-table-container">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Feature Capability</th>
                  <th className="align-center">Traditional Chatbot</th>
                  <th className="align-center highlight-header">Language Learning Pal Agent</th>
                </tr>
              </thead>
              <tbody>
                {comparisonRows.map((row, idx) => (
                  <tr key={idx}>
                    <td>{row.feature}</td>
                    <td className="align-center red-text">❌ No</td>
                    <td className="align-center green-text font-bold">✅ Yes</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </motion.section>
  );
}
