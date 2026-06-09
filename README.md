# Automated Invoice & Service Tracker

Full-stack enterprise application to automate recurring IT client billing, secure access with JWT + RBAC, and prevent service disruption due to manual oversight.

## Stack

### Frontend
- **Framework**: React 18.3.1 (SPA with functional components & hooks)
- **Build Tool**: Vite 5.3.1 (fast bundler and dev server)
- **HTTP Client**: Axios 1.7.2 (API communication)
- **Routing**: React Router DOM 6.24.1 (client-side navigation)
- **Styling**: CSS3 (responsive design with CSS Grid & Flexbox)

### Backend
- **Framework**: FastAPI 0.115.0 (async Python web framework)
- **Server**: Uvicorn 0.30.0 (ASGI server)
- **ORM**: SQLAlchemy 2.0.31 (database abstraction & queries)
- **Database Migrations**: Alembic 1.13.2 (schema versioning)
- **Authentication**: python-jose 3.3.0 + cryptography (JWT tokens)
- **Password Hashing**: Passlib 1.7.4 + bcrypt<5 (secure password storage)
- **Validation**: Pydantic 2.3.4 (request/response validation)
- **Scheduling**: APScheduler 3.10.4 (task automation & overdue detection)
- **Email**: Built-in smtplib (SMTP mail dispatch)
- **Configuration**: Pydantic Settings 2.3.4 (environment management)

### Database
- **Primary**: PostgreSQL (relational data persistence)
- **Testing**: SQLite (in-memory fixtures for tests)
- **Driver**: psycopg2-binary 2.9.9 (PostgreSQL adapter)

### Development & Testing
- **Testing Framework**: pytest 8.2.2 (unit & integration tests)
- **Async Testing**: pytest-asyncio 0.23.8 (async test support)
- **HTTP Testing**: httpx 0.27.0 (async HTTP client for testing)
- **Form Parsing**: python-multipart 0.0.9 (multipart form data)
- **Email Validation**: email-validator 2.2.0 (email format validation)

### Security
- **Authentication**: JWT (JSON Web Tokens)
- **Authorization**: RBAC (Role-Based Access Control) - ADMIN, FINANCE, CLIENT
- **Hashing**: bcrypt (password encryption)
- **HTTPS**: Ready for production HTTPS deployment

## Project Structure

- `backend/` FastAPI app, ORM models, migrations, tests
  - `app/api/v1/` API endpoints (admin, auth, clients, invoices, services, users)
  - `app/models/` SQLAlchemy ORM models
  - `app/schemas/` Pydantic request/response schemas
  - `app/services/` Business logic (billing, mailer)
- `frontend/` React single-page app with role-guarded routing
  - `src/pages/` Dashboard pages for Admin, Finance, and Client roles
  - `src/components/` Reusable UI components (DashboardCard, TopBar)
  - `src/auth/` Authentication context and JWT handling
  - `src/api/` Axios client for backend communication

## Quick Start

1. Backend setup
   - `cd backend`
   - `pip install -e .`
   - Copy `.env.example` to `.env`
   - `alembic upgrade head`
   - `uvicorn app.main:app --reload --port 8000`

2. Frontend setup
   - `cd frontend`
   - `npm install`
   - Copy `.env.example` to `.env`
   - `npm run dev`

## Run Full Project

Use two terminals:

1. Backend
   - `python backend/scripts/seed_demo_data.py`
   - `uvicorn app.main:app --app-dir "a:\projects\AutomatedInvoiceandServiceTracker\backend" --host 127.0.0.1 --port 8000`
2. Frontend
   - `npm install --prefix "a:\projects\AutomatedInvoiceandServiceTracker\frontend"`
   - `npm run dev --prefix "a:\projects\AutomatedInvoiceandServiceTracker\frontend"`

Open the app at:

- Frontend: `http://localhost:5173`
- Backend health: `http://127.0.0.1:8000/health`

Demo login credentials after seeding:

- `admin` / `admin123`
- `finance` / `finance123`
- `client1` / `client123`

## Default Roles

- `ADMIN`: full access (users, clients, services, invoices) + system-wide analytics dashboard
- `FINANCE`: invoice and payment management with read access to service/client data + financial dashboard
- `CLIENT`: isolated invoice visibility for assigned client scope + personal dashboard

## Dashboards

Role-specific dashboards provide comprehensive analytics and management interfaces:

### Admin Dashboard
- System-wide statistics (total clients, services, invoices, users)
- Financial summary (revenue, pending, overdue)
- Invoice metrics and status breakdown
- Recent invoices tracking
- **Endpoint**: `GET /admin/dashboard`

### Finance Dashboard
- Revenue tracking and financial overview
- Overdue invoice alerts with days calculation
- Invoice status summary and metrics
- Recent invoice history
- **Endpoint**: `GET /admin/dashboard/finance`

### Client Dashboard
- Personal account information
- Invoice summary with balance due
- Invoice history with due date indicators
- Active services overview
- **Endpoint**: `GET /clients/{client_id}/dashboard`

*See [DASHBOARDS.md](DASHBOARDS.md) for detailed documentation.*

## Test Matrix Coverage

- `TC-SEC-01`: SQL injection attempt in login returns 401
- `TC-SEC-02`: missing JWT on guarded admin route returns 403
- `TC-CALC-01`: billing total scales correctly at boundary quantities
- `TC-AUTO-01`: overdue automation marks invoice and triggers mail dispatcher

## CV Summary

### Automated Invoice & Service Tracker - Full-Stack Developer & QA

- System Engineering: Architected and deployed a decoupled web application using React, a RESTful Python API (FastAPI), and a PostgreSQL relational database.
- Access Security: Implemented token-based authentication with JWT and bcrypt hashing, enforcing RBAC on both frontend route guards and backend endpoints.
- Dashboard & Analytics: Engineered role-specific dashboards for ADMIN, FINANCE, and CLIENT roles with real-time financial analytics, overdue detection, and invoice tracking.
- Business Automation: Developed dynamic billing logic with SQLAlchemy ORM and scheduled overdue detection with SMTP email dispatch routines.
- Quality Assurance: Implemented pytest-based verification covering security behavior, route guarding, boundary calculations, and automation triggers.
- UI/UX Design: Created responsive, professional dashboard interfaces with status indicators, financial summaries, and data visualization tables.
