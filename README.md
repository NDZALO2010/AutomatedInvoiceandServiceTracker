# Automated Invoice & Service Tracker

Full-stack enterprise application to automate recurring IT client billing, secure access with JWT + RBAC, and prevent service disruption due to manual oversight.

## Stack

- Frontend: React SPA (Vite, Axios, React Router)
- Backend: FastAPI, SQLAlchemy, Alembic
- Database: PostgreSQL
- Security: JWT, Passlib bcrypt
- Automation: APScheduler, SMTP mail dispatch
- QA: pytest matrix for security, route-guarding, calculation boundaries, and overdue automation

## Project Structure

- `backend/` FastAPI app, ORM models, migrations, tests
- `frontend/` React single-page app with role-guarded routing

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

- `ADMIN`: full access (users, clients, services, invoices)
- `FINANCE`: invoice and payment management with read access to service/client data
- `CLIENT`: isolated invoice visibility for assigned client scope

## Test Matrix Coverage

- `TC-SEC-01`: SQL injection attempt in login returns 401
- `TC-SEC-02`: missing JWT on guarded admin route returns 403
- `TC-CALC-01`: billing total scales correctly at boundary quantities
- `TC-AUTO-01`: overdue automation marks invoice and triggers mail dispatcher

## CV Summary

### Automated Invoice & Service Tracker - Full-Stack Developer & QA

- System Engineering: Architected and deployed a decoupled web application using React, a RESTful Python API (FastAPI), and a PostgreSQL relational database.
- Access Security: Implemented token-based authentication with JWT and bcrypt hashing, enforcing RBAC on both frontend route guards and backend endpoints.
- Business Automation: Developed dynamic billing logic with SQLAlchemy ORM and scheduled overdue detection with SMTP email dispatch routines.
- Quality Assurance: Implemented pytest-based verification covering security behavior, route guarding, boundary calculations, and automation triggers.
