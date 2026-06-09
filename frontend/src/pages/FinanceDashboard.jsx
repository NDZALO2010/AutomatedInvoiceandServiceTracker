import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import TopBar from "../components/TopBar";
import DashboardCard from "../components/DashboardCard";

export default function FinanceDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axiosClient.get("/admin/dashboard/finance");
        setDashboard(response.data);
        setError(null);
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <main className="page-shell">
        <TopBar title="Finance Dashboard" />
        <div className="card">
          <p>Loading dashboard...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="page-shell">
        <TopBar title="Finance Dashboard" />
        <div className="card error-text">
          <p>Error: {error}</p>
        </div>
      </main>
    );
  }

  if (!dashboard) return null;

  const { summary, overdue_invoices, recent_invoices } = dashboard;

  return (
    <main className="page-shell">
      <TopBar title="Finance Dashboard" />

      {/* Financial Summary */}
      <section className="card">
        <h2>Financial Overview</h2>
        <div className="dashboard-grid">
          <DashboardCard
            title="Total Revenue"
            value={`$${summary.total_revenue.toFixed(2)}`}
            variant="success"
          />
          <DashboardCard
            title="Pending Revenue"
            value={`$${summary.pending_revenue.toFixed(2)}`}
            subtitle={`${summary.unpaid_invoices} unpaid`}
          />
          <DashboardCard
            title="Overdue Revenue"
            value={`$${summary.overdue_revenue.toFixed(2)}`}
            subtitle={`${summary.overdue_invoices} overdue`}
            variant="danger"
          />
        </div>
      </section>

      {/* Invoice Status Summary */}
      <section className="card">
        <h2>Invoice Status Summary</h2>
        <div className="dashboard-grid">
          <DashboardCard
            title="Paid Invoices"
            value={summary.paid_invoices}
            variant="success"
          />
          <DashboardCard
            title="Unpaid Invoices"
            value={summary.unpaid_invoices}
          />
          <DashboardCard
            title="Overdue Invoices"
            value={summary.overdue_invoices}
            variant="danger"
          />
        </div>
      </section>

      {/* Overdue Invoices */}
      {overdue_invoices.length > 0 && (
        <section className="card">
          <h2>Overdue Invoices Alert</h2>
          <div className="table-responsive">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Invoice ID</th>
                  <th>Amount</th>
                  <th>Due Date</th>
                  <th>Days Overdue</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {overdue_invoices.map((invoice) => (
                  <tr key={invoice.invoice_id} className="table-row--danger">
                    <td className="monospace">{invoice.invoice_id.substring(0, 8)}...</td>
                    <td>${invoice.total_amount.toFixed(2)}</td>
                    <td>{new Date(invoice.due_date).toLocaleDateString()}</td>
                    <td className="danger-text">{invoice.days_overdue} days</td>
                    <td>
                      <span className="status-badge status-overdue">
                        {invoice.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {/* Recent Invoices */}
      <section className="card">
        <h2>Recent Invoices</h2>
        {recent_invoices.length > 0 ? (
          <div className="table-responsive">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Invoice ID</th>
                  <th>Amount</th>
                  <th>Issued</th>
                  <th>Due Date</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recent_invoices.map((invoice) => (
                  <tr key={invoice.invoice_id}>
                    <td className="monospace">{invoice.invoice_id.substring(0, 8)}...</td>
                    <td>${invoice.total_amount.toFixed(2)}</td>
                    <td>{new Date(invoice.issue_date).toLocaleDateString()}</td>
                    <td>{new Date(invoice.due_date).toLocaleDateString()}</td>
                    <td>
                      <span className={`status-badge status-${invoice.status.toLowerCase()}`}>
                        {invoice.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No invoices yet.</p>
        )}
      </section>
    </main>
  );
}
