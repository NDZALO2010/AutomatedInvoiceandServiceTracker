import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import TopBar from "../components/TopBar";
import DashboardCard from "../components/DashboardCard";

export default function AdminDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axiosClient.get("/admin/dashboard");
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
        <TopBar title="Admin Dashboard" />
        <div className="card">
          <p>Loading dashboard...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="page-shell">
        <TopBar title="Admin Dashboard" />
        <div className="card error-text">
          <p>Error: {error}</p>
        </div>
      </main>
    );
  }

  if (!dashboard) return null;

  const { statistics, invoice_metrics, financial_summary, recent_invoices } = dashboard;

  return (
    <main className="page-shell">
      <TopBar title="Admin Dashboard" />

      {/* Key Statistics */}
      <section className="card">
        <h2>Key Statistics</h2>
        <div className="dashboard-grid">
          <DashboardCard title="Total Clients" value={statistics.total_clients} />
          <DashboardCard title="Total Services" value={statistics.total_services} />
          <DashboardCard title="Total Invoices" value={statistics.total_invoices} />
          <DashboardCard title="Total Users" value={statistics.total_users} />
        </div>
      </section>

      {/* Financial Summary */}
      <section className="card">
        <h2>Financial Summary</h2>
        <div className="dashboard-grid">
          <DashboardCard
            title="Total Revenue"
            value={`$${financial_summary.total_revenue.toFixed(2)}`}
            variant="success"
          />
          <DashboardCard
            title="Pending Revenue"
            value={`$${financial_summary.pending_revenue.toFixed(2)}`}
            subtitle={`${invoice_metrics.unpaid_count} invoices`}
          />
          <DashboardCard
            title="Overdue Revenue"
            value={`$${financial_summary.overdue_revenue.toFixed(2)}`}
            subtitle={`${invoice_metrics.overdue_count} invoices`}
            variant="danger"
          />
        </div>
      </section>

      {/* Invoice Breakdown */}
      <section className="card">
        <h2>Invoice Status Breakdown</h2>
        <div className="dashboard-grid">
          <DashboardCard
            title="Paid Invoices"
            value={invoice_metrics.paid_count}
            subtitle={`$${invoice_metrics.paid_total.toFixed(2)}`}
            variant="success"
          />
          <DashboardCard
            title="Unpaid Invoices"
            value={invoice_metrics.unpaid_count}
            subtitle={`$${invoice_metrics.unpaid_total.toFixed(2)}`}
          />
          <DashboardCard
            title="Overdue Invoices"
            value={invoice_metrics.overdue_count}
            subtitle={`$${invoice_metrics.overdue_total.toFixed(2)}`}
            variant="danger"
          />
        </div>
      </section>

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
