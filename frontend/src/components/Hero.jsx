import React, { useState } from "react";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import "./Hero.css";

export default function Hero({ onStartLearning, onExploreFeatures }) {
  const [coords, setCoords] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setCoords({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  return (
    <section className="hero-section">
      <motion.div 
        className="hero-content"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      >
        <motion.h1 
          className="hero-logo"
          initial={{ backgroundPosition: "0% 50%" }}
          animate={{ backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        >
          Language Learning Pal
        </motion.h1>
        
        <motion.p 
          className="hero-tagline"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
        >
          AI-Powered Language Learning Partner
        </motion.p>
        
        <motion.p 
          className="hero-description"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
        >
          Learn vocabulary, improve grammar, translate text, and practice daily communication with an intelligent AI assistant.
        </motion.p>

        <motion.div
          className="hero-capabilities"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          <div className="capability-item">
            <span className="capability-check">✓</span>
            <span>Personalized Learning Plans</span>
          </div>
          <div className="capability-item">
            <span className="capability-check">✓</span>
            <span>Vocabulary Assistance</span>
          </div>
          <div className="capability-item">
            <span className="capability-check">✓</span>
            <span>Translation Support</span>
          </div>
          <div className="capability-item">
            <span className="capability-check">✓</span>
            <span>Progress Tracking</span>
          </div>
          <div className="capability-item">
            <span className="capability-check">✓</span>
            <span>Pronunciation Guidance</span>
          </div>
          <div className="capability-item">
            <span className="capability-check">✓</span>
            <span>Memory-Based Learning</span>
          </div>
        </motion.div>
        
        <div 
          className="hero-actions-container"
          onMouseMove={handleMouseMove}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
        >
          {/* Interactive cursor glow background */}
          {isHovered && (
            <div
              className="cursor-glow-backdrop"
              style={{
                left: `${coords.x}px`,
                top: `${coords.y}px`,
              }}
            />
          )}
          
          <div className="hero-actions">
            <motion.button 
              className="btn btn-primary" 
              onClick={onStartLearning}
              whileHover={{ y: -3, scale: 1.02 }}
              whileTap={{ y: 0, scale: 0.98 }}
              transition={{ type: "spring", stiffness: 400, damping: 15 }}
            >
              <span>Start Chat</span>
              <Sparkles size={14} className="btn-icon" />
            </motion.button>
            
            <motion.button 
              className="btn btn-secondary" 
              onClick={onExploreFeatures}
              whileHover={{ y: -3, scale: 1.02 }}
              whileTap={{ y: 0, scale: 0.98 }}
              transition={{ type: "spring", stiffness: 400, damping: 15 }}
            >
              <span>View Features</span>
              <ArrowRight size={14} className="btn-icon" />
            </motion.button>
          </div>
        </div>
      </motion.div>
    </section>
  );
}
