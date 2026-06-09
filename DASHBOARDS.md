# Dashboard Implementation Guide

## Overview

Comprehensive dashboards have been added to the Automated Invoice & Service Tracker application for all three user roles: ADMIN, FINANCE, and CLIENT. Each dashboard provides role-specific data visualization and analytics.

## Backend Endpoints

### 1. Admin Dashboard
**Endpoint**: `GET /admin/dashboard`
**Authentication**: ADMIN role required
**Description**: Comprehensive system overview with key metrics and statistics

**Response Structure**:
```json
{
  "statistics": {
    "total_clients": number,
    "total_services": number,
    "total_invoices": number,
    "total_users": number
  },
  "invoice_metrics": {
    "unpaid_count": number,
    "overdue_count": number,
    "paid_count": number,
    "unpaid_total": number,
    "overdue_total": number,
    "paid_total": number
  },
  "financial_summary": {
    "total_revenue": number,
    "pending_revenue": number,
    "overdue_revenue": number
  },
  "recent_invoices": [
    {
      "invoice_id": string,
      "client_id": string,
      "total_amount": number,
      "issue_date": string (ISO),
      "due_date": string (ISO),
      "status": string
    }
  ]
}
```

**Dashboard Sections**:
- **Key Statistics**: Total clients, services, invoices, and users
- **Financial Summary**: Total revenue, pending, and overdue amounts
- **Invoice Status Breakdown**: Paid, unpaid, and overdue invoice counts with totals
- **Recent Invoices**: Table showing the 5 most recent invoices

---

### 2. Finance Dashboard
**Endpoint**: `GET /admin/dashboard/finance`
**Authentication**: ADMIN or FINANCE role required
**Description**: Detailed financial and invoice management overview

**Response Structure**:
```json
{
  "summary": {
    "total_revenue": number,
    "pending_revenue": number,
    "overdue_revenue": number,
    "paid_invoices": number,
    "unpaid_invoices": number,
    "overdue_invoices": number
  },
  "overdue_invoices": [
    {
      "invoice_id": string,
      "client_id": string,
      "total_amount": number,
      "due_date": string (ISO),
      "days_overdue": number,
      "status": string
    }
  ],
  "recent_invoices": [
    {
      "invoice_id": string,
      "client_id": string,
      "total_amount": number,
      "issue_date": string (ISO),
      "due_date": string (ISO),
      "status": string
    }
  ]
}
```

**Dashboard Sections**:
- **Financial Overview**: Total revenue, pending revenue, and overdue revenue
- **Invoice Status Summary**: Count of paid, unpaid, and overdue invoices
- **Overdue Invoices Alert**: Detailed table of all overdue invoices with days overdue
- **Recent Invoices**: Table showing 10 most recent invoices

---

### 3. Client Dashboard
**Endpoint**: `GET /clients/{client_id}/dashboard`
**Authentication**: CLIENT (self-access only) or ADMIN/FINANCE (any client)
**Description**: Client-specific invoice and service overview

**Response Structure**:
```json
{
  "client_info": {
    "client_id": string,
    "company_name": string,
    "contact_person": string,
    "email": string,
    "phone": string
  },
  "invoice_summary": {
    "total_invoices": number,
    "paid_invoices": number,
    "unpaid_invoices": number,
    "overdue_invoices": number,
    "total_paid": number,
    "total_unpaid": number,
    "total_overdue": number
  },
  "active_services": number,
  "total_services": number,
  "invoices": [
    {
      "invoice_id": string,
      "total_amount": number,
      "issue_date": string (ISO),
      "due_date": string (ISO),
      "status": string,
      "days_until_due": number
    }
  ],
  "services": [
    {
      "service_id": string,
      "service_name": string,
      "description": string,
      "hourly_rate": number,
      "active": boolean
    }
  ]
}
```

**Dashboard Sections**:
- **Account Information**: Client company details
- **Invoice Summary**: Balance due, total paid, and overdue amounts
- **Invoice Status Breakdown**: Counts of paid, unpaid, and overdue invoices
- **Active Services**: List of all services assigned to the client
- **Your Invoices**: Comprehensive invoice table with days until due

---

## Frontend Components

### File Structure
```
frontend/src/
├── components/
│   └── DashboardCard.jsx          (Reusable statistic card component)
├── pages/
│   ├── AdminDashboard.jsx         (Admin role dashboard)
│   ├── AdminPage.jsx              (Wrapper for AdminDashboard)
│   ├── FinanceDashboard.jsx       (Finance role dashboard)
│   ├── FinancePage.jsx            (Wrapper for FinanceDashboard)
│   ├── ClientDashboard.jsx        (Client role dashboard)
│   └── ClientPage.jsx             (Wrapper for ClientDashboard)
└── styles.css                      (Dashboard styling)
```

### DashboardCard Component
**Props**:
- `title` (string): Card title
- `value` (string | number): Main value to display
- `subtitle` (string, optional): Secondary text
- `variant` (string, optional): "default", "danger", or "success" for styling

**Example Usage**:
```jsx
<DashboardCard 
  title="Total Revenue" 
  value="$50,000"
  variant="success"
/>
```

### Dashboard Components

#### AdminDashboard.jsx
Displays comprehensive admin statistics:
- Key statistics grid (clients, services, invoices, users)
- Financial summary with revenue breakdown
- Invoice status breakdown
- Recent invoices table

#### FinanceDashboard.jsx
Displays financial and invoice management data:
- Financial overview cards
- Invoice status summary
- Overdue invoices alert (highlighted in red)
- Recent invoices table

#### ClientDashboard.jsx
Displays client-specific information:
- Account information card
- Invoice summary with balance due
- Invoice status breakdown
- Active services list
- Personal invoice history table

---

## Styling

### New CSS Classes

**Dashboard Grid**:
- `.dashboard-grid`: Responsive grid layout for cards

**Cards**:
- `.dashboard-card`: Base card styling
- `.dashboard-card--danger`: Red-themed card
- `.dashboard-card--success`: Green-themed card
- `.dashboard-card-value`: Large value text
- `.dashboard-card-subtitle`: Secondary text

**Tables**:
- `.dashboard-table`: Styled table with proper spacing
- `.table-responsive`: Horizontal scroll for mobile
- `.table-row--danger`: Red background for highlighted rows
- `.monospace`: Monospace font for IDs

**Status Badges**:
- `.status-badge`: Base badge styling
- `.status-paid`: Green badge
- `.status-unpaid`: Yellow badge
- `.status-overdue`: Red badge
- `.status-active`: Green badge
- `.status-inactive`: Gray badge

**Text**:
- `.danger-text`: Red colored text

**Client Info**:
- `.client-info`: Client information container
- `.services-list`: Grid of service items
- `.service-item`: Individual service card

---

## Features

### Admin Dashboard Features
✅ System-wide statistics overview
✅ Financial summary and analytics
✅ Invoice status breakdown
✅ Recent invoice tracking
✅ Role-based access control

### Finance Dashboard Features
✅ Revenue tracking and metrics
✅ Overdue invoice alerts with days calculation
✅ Invoice status summary
✅ Detailed recent invoice history
✅ Financial forecasting data

### Client Dashboard Features
✅ Personal account information
✅ Balance due tracking
✅ Paid vs. unpaid invoice breakdown
✅ Overdue amount calculation
✅ Active services visibility
✅ Invoice history with due date indicators

---

## Usage Instructions

### Access the Dashboards

1. **Admin Dashboard**:
   - Log in with ADMIN role
   - Automatically redirected to `/admin`
   - View system-wide metrics and recent invoices

2. **Finance Dashboard**:
   - Log in with ADMIN or FINANCE role
   - Navigate to `/finance` for FINANCE users
   - ADMIN users can access both Admin and Finance dashboards

3. **Client Dashboard**:
   - Log in with CLIENT role
   - Automatically redirected to `/client`
   - View personal invoices and services

### Demo Credentials
After running `python scripts/seed_demo_data.py`:
- Admin: `admin` / `admin123`
- Finance: `finance` / `finance123`
- Client: `client1` / `client123`

---

## API Integration

All dashboards use the `axiosClient` for API communication with proper error handling:

```jsx
try {
  const response = await axiosClient.get("/admin/dashboard");
  setDashboard(response.data);
} catch (err) {
  setError(err.response?.data?.detail || "Failed to load dashboard");
}
```

---

## Performance Considerations

- **Caching**: Dashboards fetch fresh data on component mount
- **Optimization**: Uses React hooks for state management
- **Responsive**: Grid layouts adapt to different screen sizes
- **Error Handling**: Comprehensive error states with user feedback
- **Loading States**: Loading indicators during data fetch

---

## Future Enhancements

Potential improvements for dashboard functionality:
- 📊 Chart visualizations (bar, pie, line charts)
- 📈 Historical trends and forecasting
- 🔄 Real-time data refresh with WebSockets
- 📧 Email report generation
- 📱 Mobile app dashboard views
- 🎯 Custom dashboard widgets
- ⚙️ Dashboard configuration options
- 📊 Advanced analytics and reporting

---

## Testing

To test the dashboards:

1. Start the backend:
   ```bash
   cd backend
   python scripts/seed_demo_data.py
   uvicorn app.main:app --reload --port 8000
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access at `http://localhost:5173`

4. Log in with different roles and verify:
   - Admin dashboard displays all system metrics
   - Finance dashboard shows financial overview and overdue alerts
   - Client dashboard shows personal account information

---

## Summary

Comprehensive dashboards have been successfully implemented across the application:
- **3 backend API endpoints** providing role-specific data
- **3 frontend dashboard components** with full data visualization
- **Professional styling** with responsive design
- **Error handling** and loading states
- **Role-based access control** enforced on both backend and frontend
