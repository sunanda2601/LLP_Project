import React from "react";
import { motion } from "framer-motion";
import {
  BookOpen,
  SpellCheck,
  Globe,
  Compass,
  MessageCircle,
  Volume2,
  Shuffle,
  Calendar,
} from "lucide-react";
import "./FeaturesGrid.css";

const LANGUAGE_LEARNING_PAL_FEATURES = [
  {
    id: "VOCABULARY",
    title: "Vocabulary Learning",
    description: "Learn word meanings, definitions, examples, and usage.",
    prompt: "Teach me 5 advanced English words",
    icon: BookOpen,
  },
  {
    id: "GRAMMAR",
    title: "Grammar Correction",
    description: "Correct grammatical mistakes and explain rules.",
    prompt: "Correct: I am go to college everyday",
    icon: SpellCheck,
  },
  {
    id: "TRANSLATION",
    title: "Translation",
    description: "Translate text between languages.",
    prompt: "Translate hello to Telugu",
    icon: Globe,
  },
  {
    id: "DAILY_PHRASES",
    title: "Daily Phrases",
    description: "Provide practical everyday expressions.",
    prompt: "Give common workplace phrases in English",
    icon: Compass,
  },
  {
    id: "CONVERSATION",
    title: "Conversation Practice",
    description: "Practice real-world communication.",
    prompt: "Practice English conversation with me",
    icon: MessageCircle,
  },
  {
    id: "PRONUNCIATION",
    title: "Pronunciation Guidance",
    description: "Help users pronounce difficult words.",
    prompt: "How to pronounce Environment",
    icon: Volume2,
  },
  {
    id: "SYNONYMS_ANTONYMS",
    title: "Synonyms & Antonyms",
    description: "Provide similar and opposite words.",
    prompt: "Give synonyms of Happy",
    icon: Shuffle,
  },
  {
    id: "WORD_OF_DAY",
    title: "Word of the Day",
    description: "Display a new vocabulary word daily.",
    prompt: "Give me today's word",
    icon: Calendar,
  },
];

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { 
    opacity: 1, 
    y: 0,
    transition: { type: "spring", stiffness: 100, damping: 15 }
  },
};

export default function FeaturesGrid({ onFeatureClick, sectionRef }) {
  return (
    <motion.section 
      className="features-section" 
      ref={sectionRef}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: "-100px" }}
    >
      <div className="features-header">
        <h2>Features</h2>
        <p>Explore language learning tools designed to build your skills step-by-step.</p>
      </div>

      <motion.div 
        className="features-grid"
        variants={containerVariants}
      >
        {LANGUAGE_LEARNING_PAL_FEATURES.map((feat) => {
          const Icon = feat.icon;
          return (
            <motion.div
              key={feat.id}
              className="feature-card"
              onClick={() => onFeatureClick(feat.prompt)}
              variants={cardVariants}
              whileHover={{ 
                scale: 1.03, 
                y: -6,
                transition: { duration: 0.3, ease: "easeOut" }
              }}
              whileTap={{ scale: 0.98 }}
            >
              {/* Outer glow background border container */}
              <div className="card-border-glow" />
              
              <div className="feature-card-content">
                <div className="feature-icon-wrapper">
                  <Icon size={20} strokeWidth={1.5} className="feature-icon" />
                </div>
                <h3>{feat.title}</h3>
                <p>{feat.description}</p>
              </div>
            </motion.div>
          );
        })}
      </motion.div>
    </motion.section>
  );
}
