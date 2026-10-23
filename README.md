# Feature Flag Management System

FastAPI + SQLAlchemy + PostgreSQL backend (React + TypeScript frontend coming in Milestone 6).

## Milestone 1 — Project Setup & Database ✅
- FastAPI app with health endpoints
- PostgreSQL connection + SQLAlchemy configuration
- 9 models: users, environments, flags, flag_versions, user_groups,
  user_group_memberships, targeting_rules, audit_log, evaluation_stats
- Alembic migration + sample-record / FK verification script

## Setup

### 1. Create the PostgreSQL database
```sql
CREATE USER ff_user WITH PASSWORD 'ff_password';
CREATE DATABASE feature_flags OWNER ff_user;
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env
alembic upgrade head            # creates all tables
python -m app.seed              # verifies tables + inserts sample records
uvicorn app.main:app --reload
```

- API docs: http://localhost:8000/docs
- App check: http://localhost:8000/health
- DB check: http://localhost:8000/health/db

## Project structure
```
backend/app/{models,schemas,routers,services,database}, main.py, config.py, seed.py
backend/alembic/        # migrations
frontend/               # placeholder
```
