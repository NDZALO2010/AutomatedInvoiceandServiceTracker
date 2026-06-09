import { createContext, useContext, useEffect, useMemo, useState } from "react";

import axiosClient from "../api/axiosClient";

const AuthContext = createContext(null);

function parseJwt(token) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("access_token"));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (!token) {
      setUser(null);
      return;
    }
    const payload = parseJwt(token);
    if (!payload || !payload.sub || !payload.role) {
      localStorage.removeItem("access_token");
      setToken(null);
      setUser(null);
      return;
    }
    setUser({ username: payload.sub, role: payload.role });
  }, [token]);

  const login = async (username, password) => {
    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);
    const response = await axiosClient.post("/auth/login", body, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    localStorage.setItem("access_token", response.data.access_token);
    setToken(response.data.access_token);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
  };

  const value = useMemo(() => ({ token, user, login, logout }), [token, user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}
