import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, Lock, Sparkles, ArrowRight, ShieldCheck, BrainCircuit, Check, X } from "lucide-react";
import axios from "axios";

export default function AuthPage({ onAuthSuccess }) {
  const [mode, setMode] = useState("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [isSigningIn, setIsSigningIn] = useState(false);

  // Password validation criteria (W3Schools pattern reference)
  const isLengthValid = password.length >= 8;
  const isLowerValid = /[a-z]/.test(password);
  const isUpperValid = /[A-Z]/.test(password);
  const isNumberValid = /\d/.test(password);
  const isPasswordValid = isLengthValid && isLowerValid && isUpperValid && isNumberValid;

  const handleLocalSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!email || !password || (mode === "signup" && !name)) {
      setError("Please fill in all fields.");
      return;
    }

    if (mode === "signup" && !isPasswordValid) {
      setError("Please ensure your password meets all complexity requirements.");
      return;
    }

    setIsSigningIn(true);
    try {
      const url = `${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}/auth/${mode === "signup" ? "signup" : "login"}`;
      const payload = mode === "signup"
        ? { name, email, password, provider: "local" }
        : { email, password, provider: "local" };

      const response = await axios.post(url, payload);

      if (!response.data?.authenticated) {
        throw new Error(response.data?.error || "Authentication failed.");
      }

      const user = response.data.user;
      localStorage.setItem("langpal_user", JSON.stringify(user));
      onAuthSuccess(user);
    } catch (authError) {
      setError(
        authError.response?.data?.error ||
        authError.response?.data?.message ||
        authError.message ||
        "Authentication failed. Please try again."
      );
    } finally {
      setIsSigningIn(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #0b0f19 0%, #111827 50%, #1e1b4b 100%)", padding: "2rem" }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} style={{ width: "100%", maxWidth: "1050px", background: "rgba(17, 24, 39, 0.85)", backdropFilter: "blur(20px)", borderRadius: "30px", border: "1px solid rgba(255, 255, 255, 0.12)", boxShadow: "0 25px 80px rgba(0,0,0,0.6)", overflow: "hidden", display: "grid", gridTemplateColumns: "1.1fr 0.9fr" }}>
        <div style={{ background: "linear-gradient(135deg, #0f172a 0%, #3730a3 50%, #6366f1 100%)", color: "white", padding: "2.8rem", display: "flex", flexDirection: "column", justifyContent: "center", gap: "1.2rem" }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: "0.6rem", width: "fit-content", background: "rgba(255,255,255,0.16)", padding: "0.45rem 0.85rem", borderRadius: "999px" }}>
            <Sparkles size={16} />
            <span style={{ fontSize: "0.88rem", fontWeight: 600 }}>AI-Powered Language Agent</span>
          </div>
          <h1 style={{ margin: 0, fontSize: "2.1rem", lineHeight: 1.25, color: "#ffffff" }}>Learn English faster with your personal AI Coach.</h1>
          <p style={{ margin: 0, fontSize: "1.02rem", lineHeight: 1.6, color: "rgba(255,255,255,0.85)" }}>
            Practice real conversation scenarios, track your progress automatically, and build fluency with personalized roadmaps.
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: "0.8rem", marginTop: "0.5rem", fontSize: "0.95rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.65rem" }}><ShieldCheck size={18} color="#34d399" /> Personalized guidance</div>
            <div style={{ display: "flex", alignItems: "center", gap: "0.65rem" }}><BrainCircuit size={18} color="#818cf8" /> Smart feedback & 30-day plans</div>
          </div>
        </div>

        <div style={{ padding: "2.5rem", display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "0.8rem", marginBottom: "1.6rem" }}>
            <div style={{ width: "46px", height: "46px", borderRadius: "50%", background: "linear-gradient(135deg, #6366f1, #8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center", color: "white", boxShadow: "0 0 20px rgba(99, 102, 241, 0.5)" }}>
              <Sparkles size={22} />
            </div>
            <div>
              <h2 style={{ margin: 0, fontSize: "1.35rem", color: "#f8fafc" }}>Language Learning Pal</h2>
              <p style={{ margin: 0, color: "#94a3b8", fontSize: "0.92rem" }}>{mode === "signin" ? "Welcome back" : "Create your account"}</p>
            </div>
          </div>

          {error ? <div style={{ background: "rgba(239, 68, 68, 0.15)", color: "#f87171", border: "1px solid rgba(239, 68, 68, 0.3)", padding: "0.75rem", borderRadius: "12px", marginBottom: "1rem", fontSize: "0.9rem" }}>{error}</div> : null}

          <form onSubmit={handleLocalSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {mode === "signup" ? (
              <div style={{ display: "flex", alignItems: "center", gap: "0.7rem", background: "rgba(30, 41, 59, 0.6)", border: "1px solid rgba(255, 255, 255, 0.12)", borderRadius: "14px", padding: "0.85rem 1.1rem" }}>
                <Mail size={18} color="#94a3b8" />
                <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Full name" style={{ border: 0, outline: 0, width: "100%", background: "transparent", color: "#f8fafc", fontSize: "0.95rem" }} required />
              </div>
            ) : null}

            <div style={{ display: "flex", alignItems: "center", gap: "0.7rem", background: "rgba(30, 41, 59, 0.6)", border: "1px solid rgba(255, 255, 255, 0.12)", borderRadius: "14px", padding: "0.85rem 1.1rem" }}>
              <Mail size={18} color="#94a3b8" />
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email address" style={{ border: 0, outline: 0, width: "100%", background: "transparent", color: "#f8fafc", fontSize: "0.95rem" }} required />
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: "0.7rem", background: "rgba(30, 41, 59, 0.6)", border: "1px solid rgba(255, 255, 255, 0.12)", borderRadius: "14px", padding: "0.85rem 1.1rem" }}>
              <Lock size={18} color="#94a3b8" />
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" style={{ border: 0, outline: 0, width: "100%", background: "transparent", color: "#f8fafc", fontSize: "0.95rem" }} required />
            </div>

            {mode === "signup" ? (
              <div style={{ background: "rgba(30, 41, 59, 0.5)", border: "1px solid rgba(255, 255, 255, 0.1)", borderRadius: "14px", padding: "0.9rem 1.1rem", fontSize: "0.85rem" }}>
                <p style={{ margin: "0 0 0.5rem 0", fontWeight: 600, color: "#cbd5e1" }}>Password must contain:</p>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.45rem" }}>
                  <div style={{ color: isLowerValid ? "#34d399" : "#f87171", display: "flex", alignItems: "center", gap: "0.35rem", fontWeight: 500 }}>
                    {isLowerValid ? <Check size={14} /> : <X size={14} />} Lowercase letter (a-z)
                  </div>
                  <div style={{ color: isUpperValid ? "#34d399" : "#f87171", display: "flex", alignItems: "center", gap: "0.35rem", fontWeight: 500 }}>
                    {isUpperValid ? <Check size={14} /> : <X size={14} />} Uppercase letter (A-Z)
                  </div>
                  <div style={{ color: isNumberValid ? "#34d399" : "#f87171", display: "flex", alignItems: "center", gap: "0.35rem", fontWeight: 500 }}>
                    {isNumberValid ? <Check size={14} /> : <X size={14} />} Number (0-9)
                  </div>
                  <div style={{ color: isLengthValid ? "#34d399" : "#f87171", display: "flex", alignItems: "center", gap: "0.35rem", fontWeight: 500 }}>
                    {isLengthValid ? <Check size={14} /> : <X size={14} />} Minimum 8 characters
                  </div>
                </div>
              </div>
            ) : null}

            <button type="submit" disabled={isSigningIn} style={{ background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)", color: "white", border: 0, borderRadius: "14px", padding: "1rem", fontWeight: 600, fontSize: "0.98rem", cursor: isSigningIn ? "wait" : "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: "0.5rem", boxShadow: "0 0 20px rgba(99, 102, 241, 0.4)", opacity: isSigningIn ? 0.8 : 1 }}>
              {mode === "signin" ? (isSigningIn ? "Signing In..." : "Sign In") : (isSigningIn ? "Creating Account..." : "Sign Up")}
              <ArrowRight size={18} />
            </button>
          </form>

          <p style={{ marginTop: "1.4rem", textAlign: "center", color: "#94a3b8", fontSize: "0.92rem" }}>
            {mode === "signin" ? "Don’t have an account?" : "Already have an account?"}{" "}
            <button onClick={() => { setMode(mode === "signin" ? "signup" : "signin"); setError(""); }} style={{ background: "none", border: 0, color: "#818cf8", cursor: "pointer", fontWeight: 600, padding: 0 }}>
              {mode === "signin" ? "Sign up" : "Sign in"}
            </button>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
