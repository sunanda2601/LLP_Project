import React from "react";
import { motion } from "framer-motion";
import "./Footer.css";

export default function Footer() {
  return (
    <motion.footer 
      className="footer"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8 }}
    >
      <div className="footer-content">
        <div className="footer-branding">
          <h4>Language Learning Pal</h4>
          <p>AI-Powered Language Learning Partner</p>
        </div>
        <div className="footer-details">
          <span className="footer-copyright">
            &copy; 2026 Language Learning Pal. All Rights Reserved.
          </span>
        </div>
      </div>
    </motion.footer>
  );
}
