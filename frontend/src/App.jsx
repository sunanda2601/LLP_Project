import { useEffect, useState } from "react";
import "./styles/App.css";
import ChatPage from "./pages/ChatPage";
import AuthPage from "./components/auth/AuthPage";
import GoogleCallback from "./components/auth/GoogleCallback";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("langpal_user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const isGoogleCallback = window.location.pathname === "/auth/google/callback";

  if (isGoogleCallback) {
    return <GoogleCallback onAuthSuccess={setUser} />;
  }

  const handleSignOut = () => {
    localStorage.removeItem("langpal_user");
    setUser(null);
  };

  if (!user) {
    return <AuthPage onAuthSuccess={setUser} />;
  }

  return <ChatPage user={user} onSignOut={handleSignOut} />;
}

export default App;