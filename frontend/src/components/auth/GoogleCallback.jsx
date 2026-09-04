import { useEffect } from "react";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

export default function GoogleCallback({ onAuthSuccess }) {
  useEffect(() => {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    const accessToken = params.get("access_token");
    const error = params.get("error");

    if (error) {
      window.opener?.postMessage({ type: "google-auth-error", error }, window.location.origin);
      window.close();
      return;
    }

    if (accessToken) {
      window.opener?.postMessage({ type: "google-auth-success", accessToken }, window.location.origin);
    }

    window.close();
  }, [onAuthSuccess]);

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #f5f7ff 0%, #eef5ff 100%)", padding: "2rem" }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} style={{ width: "100%", maxWidth: "420px", background: "#fff", borderRadius: "24px", boxShadow: "0 20px 60px rgba(0,0,0,0.1)", padding: "2rem", textAlign: "center" }}>
        <div style={{ display: "inline-flex", alignItems: "center", justifyContent: "center", width: "48px", height: "48px", borderRadius: "50%", background: "#0071e3", color: "white", marginBottom: "1rem" }}>
          <Sparkles size={22} />
        </div>
        <h2 style={{ margin: 0, fontSize: "1.2rem" }}>Finishing sign-in…</h2>
        <p style={{ marginTop: "0.5rem", color: "#666" }}>You’ll be redirected back to Language Learning Pal shortly.</p>
      </motion.div>
    </div>
  );
}
