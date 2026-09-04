import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_URL,
});

export default api;

const getUserId = () => {
  const storedUserStr = localStorage.getItem("langpal_user");
  if (storedUserStr) {
    try {
      const user = JSON.parse(storedUserStr);
      return user.email || user.id || "test_user";
    } catch (e) {
      console.error("Error parsing user from localStorage", e);
    }
  }
  return "test_user";
};

/**
 * Sends a chat message to the Language Learning Pal API backend.
 */
export const sendMessage = async (message) => {
  try {
    const response = await api.post("/chat/", {
      user_id: getUserId(),
      message: message,
    });
    return response.data;
  } catch (error) {
    console.error("Language Learning Pal API network error:", error);
    return {
      success: false,
      error: "Unable to connect to the Language Learning Pal backend service.",
    };
  }
};

/**
 * Fetches current user progress dashboard and memory profile statistics.
 */
export const fetchDashboardData = async () => {
  try {
    const response = await api.get("/dashboard-data", {
      params: {
        user_id: getUserId(),
      },
    });
    return response.data;
  } catch (error) {
    console.error("Language Learning Pal API dashboard-data fetch error:", error);
    return {
      success: false,
      error: "Unable to connect to the Language Learning Pal backend service.",
    };
  }
};

/**
 * Saves task completion states.
 */
export const updateCompletedTasks = async (completedTasks) => {
  try {
    const response = await api.post("/update-tasks", {
      user_id: getUserId(),
      completed_tasks: completedTasks,
    });
    return response.data;
  } catch (error) {
    console.error("Language Learning Pal API update-tasks error:", error);
    return {
      success: false,
      error: "Unable to connect to the Language Learning Pal backend service.",
    };
  }
};

/**
 * Advances the user to the next day.
 */
export const completeDay = async () => {
  try {
    const response = await api.post("/complete-day", {
      user_id: getUserId(),
    });
    return response.data;
  } catch (error) {
    console.error("Language Learning Pal API complete-day error:", error);
    return {
      success: false,
      error: "Unable to connect to the Language Learning Pal backend service.",
    };
  }
};
