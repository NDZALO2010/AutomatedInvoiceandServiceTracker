import { useEffect, useState } from "react";

import axiosClient from "../api/axiosClient";
import TopBar from "../components/TopBar";

export default function FinancePage() {
  const [invoices, setInvoices] = useState([]);

  useEffect(() => {
    axiosClient.get("/invoices").then((res) => setInvoices(res.data)).catch(() => setInvoices([]));
  }, []);

  return (
    <main className="page-shell">
      <TopBar title="Finance Dashboard" />
      <section className="card">
        <h2>Invoices</h2>
        <p>Tracked invoices: {invoices.length}</p>
      </section>
    </main>
  );
}
