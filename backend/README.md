# KenyaPOS Backend

FastAPI backend for a lightweight, offline-capable POS for SMEs in Kenya.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment
Create `.env` in `backend/`:

```
SECRET_KEY=change-this-secret
DATABASE_URL=sqlite+aiosqlite:///./kenyapos.db
CORS_ORIGINS=["http://localhost:5173"]
MPESA_CONSUMER_KEY=
MPESA_CONSUMER_SECRET=
MPESA_PASSKEY=
MPESA_SHORT_CODE=
MPESA_CALLBACK_URL=http://localhost:8000/mpesa/callback
```
