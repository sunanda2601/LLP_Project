import { useState, useRef, useEffect } from "react";
import { 
  Sparkles, 
  MessageSquare, 
  BarChart3, 
  Calendar, 
  Wrench, 
  Compass, 
  LogOut
} from "lucide-react";
import { sendMessage, fetchDashboardData } from "../services/api";
import Hero from "../components/Hero";
import ProjectDescription from "../components/ProjectDescription";
import FeaturesGrid from "../components/FeaturesGrid";
import ChatDemo from "../components/ChatDemo";
import Footer from "../components/Footer";
import "./ChatPage.css";

export default function ChatPage({ user, onSignOut }) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);
  const [agentStatus, setAgentStatus] = useState("Idle");
  const [statusMessage, setStatusMessage] = useState("Idle - Ready to assist");
  const [activeTab, setActiveTab] = useState("chat");

  const chatSectionRef = useRef(null);
  const featuresSectionRef = useRef(null);

  const loadDashboard = async () => {
    try {
      const res = await fetchDashboardData();
      if (res && res.success) {
        setDashboardData(res);
      }
    } catch (err) {
      console.error("Failed to load dashboard data:", err);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const scrollToChat = () => {
    setActiveTab("chat");
  };

  const scrollToFeatures = () => {
    setActiveTab("features");
  };

  const handleTabChange = (tabId) => {
    setActiveTab(tabId);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleSend = async (text = message) => {
    const trimmed = text.trim();
    if (!trimmed) return;

    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: trimmed,
        time: timestamp,
      },
    ]);

    setMessage("");
    setLoading(true);
    if (activeTab !== "chat") {
      setActiveTab("chat");
    }

    // 1. Analyzing Intent
    setAgentStatus("Analyzing Intent");
    setStatusMessage("Classifying user request and identifying goals...");

    const memoryTimeout = setTimeout(() => {
      // 2. Retrieving Memory
      setAgentStatus("Retrieving Memory");
      setStatusMessage("Fetching learner profile and past performance...");
    }, 600);

    const planTimeout = setTimeout(() => {
      // 3. Generating Plan
      setAgentStatus("Generating Plan");
      setStatusMessage("Constructing reasoning path for optimal response...");
    }, 1200);

    const toolsTimeout = setTimeout(() => {
      // 4. Executing Tools
      setAgentStatus("Executing Tools");
      setStatusMessage("Running internal linguistic engines and cross-referencing...");
    }, 1800);

    const responseTimeout = setTimeout(() => {
      // 5. Generating Response
      setAgentStatus("Generating Response");
      setStatusMessage("Finalizing personalized AI response...");
    }, 2400);

    try {
      const data = await sendMessage(trimmed);

      clearTimeout(memoryTimeout);
      clearTimeout(planTimeout);
      clearTimeout(toolsTimeout);
      clearTimeout(responseTimeout);

      // 6. Completed
      setAgentStatus("Completed");
      setStatusMessage("Response generation successful!");

      const responseTimestamp = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.success ? data.response : (data.error || "An error occurred on the server."),
          intent: data.success ? data.intent : null,
          time: responseTimestamp,
        },
      ]);

      // Reload dashboard memory/progress values - SYNC AFTER CHAT
      await loadDashboard();

    } catch (error) {
      clearTimeout(memoryTimeout);
      clearTimeout(planTimeout);
      clearTimeout(toolsTimeout);
      clearTimeout(responseTimeout);

      setAgentStatus("Idle");
      setStatusMessage("Unable to connect to the Language Learning Pal backend service.");

      const responseTimestamp = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Unable to connect to the Language Learning Pal backend service. Please check your internet connection.",
          intent: null,
          time: responseTimestamp,
        },
      ]);
    }

    setLoading(false);

    // Revert status to Idle after 2.5 seconds
    setTimeout(() => {
      setAgentStatus("Idle");
      setStatusMessage("Idle - Ready to assist");
    }, 2500);
  };

  const handleFeatureClick = (prompt) => {
    setActiveTab("chat");
    handleSend(prompt);
  };

  const handlePromptClick = (prompt) => {
    setActiveTab("chat");
    handleSend(prompt);
  };

  const userInitial = (user?.name || user?.email || "U").charAt(0).toUpperCase();

  const featureTabs = [
    { id: "chat", label: "AI Coach Chat", icon: MessageSquare, badge: "Live" },
    { id: "analytics", label: "Profile & Stats", icon: BarChart3 },
    { id: "roadmap", label: "30-Day Plan", icon: Calendar },
    { id: "tools", label: "AI Tools & Practice", icon: Wrench },
    { id: "features", label: "Capabilities", icon: Sparkles },
    { id: "overview", label: "Getting Started", icon: Compass },
  ];

  return (
    <div className="apple-page-wrapper">
      {/* Top Header */}
      <header className="profile-header">
        <div className="profile-info">
          <div className="profile-avatar">{userInitial}</div>
          <div>
            <div className="profile-name">{user?.name || user?.email || "Guest User"}</div>
            <div className="profile-email">{user?.email || "Signed in"}</div>
          </div>
        </div>
        <button className="profile-signout" onClick={onSignOut}>
          <LogOut size={14} style={{ marginRight: "0.4rem", verticalAlign: "middle" }} />
          Sign out
        </button>
      </header>

      {/* W3-Inspired Sticky Navigation Toggles Bar */}
      <nav className="feature-toggles-bar">
        <div className="toggles-nav-container">
          <span className="toggles-brand">Language Learning Pal:</span>
          {featureTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                className={`feature-toggle-btn ${isActive ? "active" : ""}`}
                onClick={() => handleTabChange(tab.id)}
              >
                <Icon size={16} />
                <span>{tab.label}</span>
                {tab.badge ? <span className="feature-badge">{tab.badge}</span> : null}
              </button>
            );
          })}
        </div>
      </nav>

      <div className="content-wrapper">
        {/* Render Overview/Getting Started if active */}
        {activeTab === "overview" && (
          <>
            <Hero
              onStartLearning={scrollToChat}
              onExploreFeatures={scrollToFeatures}
            />
            <ProjectDescription />
          </>
        )}

        {/* Render Features Grid directly if active */}
        {activeTab === "features" && (
          <FeaturesGrid
            sectionRef={featuresSectionRef}
            onFeatureClick={handleFeatureClick}
          />
        )}
      </div>

      {/* Render Main Workspace Component based on active tab */}
      {activeTab !== "overview" && activeTab !== "features" && (
        <ChatDemo
          sectionRef={chatSectionRef}
          messages={messages}
          inputMessage={message}
          setInputMessage={setMessage}
          onSendMessage={() => handleSend()}
          onPromptClick={handlePromptClick}
          isLoading={loading}
          dashboardData={dashboardData}
          agentStatus={agentStatus}
          statusMessage={statusMessage}
          onRefreshDashboard={loadDashboard}
          activeTab={activeTab}
        />
      )}

      <Footer />
    </div>
  );
}
