import { Link } from "react-router-dom";

export default function UnauthorizedPage() {
  return (
    <main className="center-layout">
      <section className="card">
        <h1>Access Forbidden</h1>
        <p>Your current role does not have permission for this route.</p>
        <Link to="/" className="btn-primary inline-btn">
          Return Home
        </Link>
      </section>
    </main>
  );
}
