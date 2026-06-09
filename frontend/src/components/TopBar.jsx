import { useAuth } from "../auth/AuthContext";

export default function TopBar({ title }) {
  const { user, logout } = useAuth();

  return (
    <header className="topbar">
      <div>
        <h1>{title}</h1>
        <p>Signed in as {user?.username} ({user?.role})</p>
      </div>
      <button className="btn-secondary" onClick={logout}>
        Logout
      </button>
    </header>
  );
}
