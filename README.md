# KenyaPOS (Backend + Frontend)

Fast, secure, offline-capable POS for SMEs in Kenya.

## Prerequisites
- Python 3.13
- Node.js 22+, npm 10+

## Backend (FastAPI)

Setup and run:
```bash
cd backend
pip3 install -r requirements.txt
python3 -m app.db.create_db
python3 -m app.db.init_data
python3 -m app.db.sample_data
uvicorn app.main:app --reload --port 8000
```

Environment (copy `.env.example` to `.env` in `backend/` and fill values):
- `SECRET_KEY`
- `DATABASE_URL` (defaults to `sqlite+aiosqlite:///./kenyapos.db`)
- `CORS_ORIGINS`
- `MPESA_*` (sandbox creds)

Postman collection:
- `backend/postman_collection.json`

## Frontend (React + Vite + Tailwind)

Install and run:
```bash
cd backend/frontend
npm install
npm run dev
```

Build:
```bash
npm run build
```

## Features Implemented
- Auth (JWT), roles (admin, manager, cashier)
- Modules: products, customers, sales, purchases, reports, settings, users
- M-Pesa STK push endpoint and callback (sandbox)
- DB init + sample data
- Postman collection
- React scaffold with basic navigation and Tailwind styling

## Next
- Frontend auth + protected routes
- Offline support with service worker + IndexedDB
- Robust M-Pesa transaction state tracking and verification
