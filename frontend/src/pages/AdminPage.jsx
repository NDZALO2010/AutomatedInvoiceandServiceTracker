import { useEffect, useState } from "react";

import axiosClient from "../api/axiosClient";
import TopBar from "../components/TopBar";

export default function AdminPage() {
  const [clients, setClients] = useState([]);

  useEffect(() => {
    axiosClient.get("/clients").then((res) => setClients(res.data)).catch(() => setClients([]));
  }, []);

  return (
    <main className="page-shell">
      <TopBar title="Admin Dashboard" />
      <section className="card">
        <h2>Client Directory</h2>
        <p>Total clients: {clients.length}</p>
      </section>
    </main>
  );
}
