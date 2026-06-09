# Backend (FastAPI)

## Technology Stack

### Framework & Server
- **FastAPI 0.115.0**: Modern, fast Python web framework with automatic OpenAPI documentation
- **Uvicorn 0.30.0**: ASGI server for async request handling

### Database & ORM
- **SQLAlchemy 2.0.31**: Powerful ORM for database abstraction and query building
- **Alembic 1.13.2**: Database migration tool for schema versioning
- **PostgreSQL**: Primary production database
- **psycopg2-binary 2.9.9**: PostgreSQL database adapter

### Authentication & Security
- **python-jose 3.3.0** + **cryptography**: JWT token generation and validation
- **Passlib 1.7.4** + **bcrypt<5**: Secure password hashing and verification
- **python-multipart 0.0.9**: Multipart form data handling

### Validation & Configuration
- **Pydantic 2.3.4**: Request/response schema validation
- **Pydantic Settings 2.3.4**: Environment configuration management
- **email-validator 2.2.0**: Email format validation

### Automation & Communication
- **APScheduler 3.10.4**: Task scheduling for overdue invoice detection
- **smtplib** (built-in): Email dispatch for notifications

### Testing & Quality
- **pytest 8.2.2**: Unit and integration testing framework
- **pytest-asyncio 0.23.8**: Async test support
- **httpx 0.27.0**: Async HTTP client for API testing

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -e .`
3. Copy `.env.example` to `.env` and update values.
4. Run migrations (optional starter flow):
   - `alembic upgrade head`
5. Start API:
   - `uvicorn app.main:app --reload --port 8000`

## Run full project

Use two terminals:

1. Backend
   - `python scripts/seed_demo_data.py`
   - `uvicorn app.main:app --app-dir "a:\projects\AutomatedInvoiceandServiceTracker\backend" --host 127.0.0.1 --port 8000`
2. Frontend
   - `npm install`
   - `npm run dev --prefix "a:\projects\AutomatedInvoiceandServiceTracker\frontend"`

Open the app at:

- Frontend: `http://localhost:5173`
- Backend health: `http://127.0.0.1:8000/health`

## Demo bootstrap

Seed the database with demo accounts and a sample client:

- `python scripts/seed_demo_data.py`

Demo login credentials:

- `admin` / `admin123`
- `finance` / `finance123`
- `client1` / `client123`

## API prefix

- `/api/v1`
