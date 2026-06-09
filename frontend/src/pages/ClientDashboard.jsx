import { useEffect, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import axiosClient from "../api/axiosClient";
import TopBar from "../components/TopBar";
import DashboardCard from "../components/DashboardCard";

export default function ClientDashboard() {
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      if (!user?.client_id) {
        setError("User client ID not found");
        setLoading(false);
        return;
      }

      try {
        const response = await axiosClient.get(`/clients/${user.client_id}/dashboard`);
        setDashboard(response.data);
        setError(null);
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [user]);

  if (loading) {
    return (
      <main className="page-shell">
        <TopBar title="My Dashboard" />
        <div className="card">
          <p>Loading dashboard...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="page-shell">
        <TopBar title="My Dashboard" />
        <div className="card error-text">
          <p>Error: {error}</p>
        </div>
      </main>
    );
  }

  if (!dashboard) return null;

  const { client_info, invoice_summary, active_services, total_services, invoices, services } = dashboard;

  return (
    <main className="page-shell">
      <TopBar title="My Dashboard" />

      {/* Client Information */}
      <section className="card">
        <h2>Account Information</h2>
        <div className="client-info">
          <p>
            <strong>Company:</strong> {client_info.company_name}
          </p>
          <p>
            <strong>Contact:</strong> {client_info.contact_person}
          </p>
          <p>
            <strong>Email:</strong> {client_info.email}
          </p>
          <p>
            <strong>Phone:</strong> {client_info.phone}
          </p>
        </div>
      </section>

      {/* Invoice Summary */}
      <section className="card">
        <h2>Invoice Summary</h2>
        <div className="dashboard-grid">
          <DashboardCard
            title="Total Balance Due"
            value={`$${invoice_summary.total_unpaid.toFixed(2)}`}
            variant={invoice_summary.total_unpaid > 0 ? "danger" : "default"}
          />
          <DashboardCard
            title="Total Paid"
            value={`$${invoice_summary.total_paid.toFixed(2)}`}
            variant="success"
          />
          <DashboardCard
            title="Overdue Amount"
            value={`$${invoice_summary.total_overdue.toFixed(2)}`}
            subtitle={`${invoice_summary.overdue_invoices} invoices`}
            variant={invoice_summary.total_overdue > 0 ? "danger" : "default"}
          />
        </div>
      </section>

      {/* Invoice Status Breakdown */}
      <section className="card">
        <h2>Your Invoices Status</h2>
        <div className="dashboard-grid">
          <DashboardCard
            title="Paid"
            value={invoice_summary.paid_invoices}
            variant="success"
          />
          <DashboardCard
            title="Unpaid"
            value={invoice_summary.unpaid_invoices}
          />
          <DashboardCard
            title="Overdue"
            value={invoice_summary.overdue_invoices}
            variant="danger"
          />
        </div>
      </section>

      {/* Services */}
      <section className="card">
        <h2>Active Services</h2>
        <p>Active Services: {active_services} of {total_services}</p>
        {services.length > 0 ? (
          <div className="services-list">
            {services.map((service) => (
              <div key={service.service_id} className="service-item">
                <h4>{service.service_name}</h4>
                <p>{service.description}</p>
                <p>
                  <strong>Rate:</strong> ${service.hourly_rate.toFixed(2)}/hour
                </p>
                <span className={`status-badge ${service.active ? "status-active" : "status-inactive"}`}>
                  {service.active ? "Active" : "Inactive"}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p>No services assigned.</p>
        )}
      </section>

      {/* Recent Invoices */}
      <section className="card">
        <h2>Your Invoices</h2>
        {invoices.length > 0 ? (
          <div className="table-responsive">
            <table className="dashboard-table">
              <thead>
                <tr>
                  <th>Invoice ID</th>
                  <th>Amount</th>
                  <th>Issued</th>
                  <th>Due Date</th>
                  <th>Days Until Due</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {invoices.map((invoice) => (
                  <tr key={invoice.invoice_id}>
                    <td className="monospace">{invoice.invoice_id.substring(0, 8)}...</td>
                    <td>${invoice.total_amount.toFixed(2)}</td>
                    <td>{new Date(invoice.issue_date).toLocaleDateString()}</td>
                    <td>{new Date(invoice.due_date).toLocaleDateString()}</td>
                    <td className={invoice.days_until_due < 0 ? "danger-text" : ""}>
                      {invoice.days_until_due < 0
                        ? `${Math.abs(invoice.days_until_due)} days overdue`
                        : `${invoice.days_until_due} days`}
                    </td>
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
