import { useEffect, useState } from "react";

import axiosClient from "../api/axiosClient";
import TopBar from "../components/TopBar";

export default function ClientPage() {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    axiosClient.get("/invoices").then((res) => setInvoices(res.data)).catch(() => setInvoices([]));
  }, []);

  return (
    <main className="page-shell">
      <TopBar title="Client Portal" />
      <section className="card">
        <h2>Your Statements</h2>
        <p>Visible invoices: {invoices.length}</p>
      </section>
    </main>
  );
}
