# Backend (FastAPI)

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
