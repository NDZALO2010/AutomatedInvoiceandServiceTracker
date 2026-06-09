import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await login(username, password);
      navigate("/", { replace: true });
    } catch {
      setError("Invalid credentials");
    }
  };

  return (
    <main className="center-layout">
      <form className="card login-card" onSubmit={handleSubmit}>
        <h1>Invoice & Service Tracker</h1>
        <p>Secure sign-in for administrators, finance, and clients.</p>
        <label>
          Username
          <input value={username} onChange={(e) => setUsername(e.target.value)} required />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {error && <p className="error-text">{error}</p>}
        <button className="btn-primary" type="submit">
          Sign In
        </button>
      </form>
    </main>
  );
}
