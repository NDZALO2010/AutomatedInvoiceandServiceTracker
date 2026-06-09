export default function DashboardCard({ title, value, subtitle, variant = "default" }) {
  const variantClass = variant === "danger" ? "dashboard-card--danger" : variant === "success" ? "dashboard-card--success" : "";

  return (
    <div className={`dashboard-card ${variantClass}`}>
      <h3>{title}</h3>
      <p className="dashboard-card-value">{value}</p>
      {subtitle && <p className="dashboard-card-subtitle">{subtitle}</p>}
    </div>
  );
}
