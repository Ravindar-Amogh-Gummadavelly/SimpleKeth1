# SimpleKeth — Architecture & Deployment Guide

## 1. System Overview
SimpleKeth is designed as a highly modular, decoupled AI MVP framework tailored for agricultural analytics.
It is built with an **Offline-First Next.js frontend** and a **FastAPI Microservice backend**, completely scalable via Docker and Kubernetes.

![Architecture Flow](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Farm_in_the_Netherlands.jpg/1200px-Farm_in_the_Netherlands.jpg)

### Core Tiers:
1. **Frontend (Next.js 15, React 19, Tailwind CSS v4)**: App Router serving ISR & Static generation for rapid load speeds (<3s constraint). Uses Zustand for global state and IndexedDB for offline data persistence.
2. **Backend Services (FastAPI)**: 
    - `prediction_service` (Port 8001): Price forecasting (XGBoost/LSTM/Prophet definitions).
    - `recommendation_service` (Port 8002): High-level Haversine net-profit calculations indicating "SELL/HOLD".
    - `notification_service` (Port 8003): Mock SMS/Push alerting router.
    - `profile_service` (Port 8004): Farmer profile CRUD.
3. **Storage (PostgreSQL + TimescaleDB + Redis)**: Scaffolding generated for long-tail metrics (Prisma Schema).
4. **DevOps**: Docker Compose, localized native Python orchestrator (`start_services.py`), Prometheus metrics endpoint mapping, and Helm Charts.

---

## 2. Running Locally (Native Mode)
If you don't have Docker installed, you can orchestrate the system seamlessly from two basic terminals:

### Launch APIs
```bash
# Terminal 1
python backend/start_services.py
```
*This will spin up all 4 microservices on ports 8001->8004 synchronously.*

### Launch Frontend
```bash
# Terminal 2
npm run dev:frontend
```
*The `next.config.ts` rewrites will proxy all outgoing API requests gracefully connecting the UI to the Python intelligence layers.*

---

## 3. Extending the ML Models
The Phase-1 MVP provides the skeleton arrays for `XGBoostPredictor`, `LSTMPredictor`, and `ProphetPredictor` inside the `backend/ml/models/` tree.
To graduate from the baseline generated statistics to real intelligence:
1. Fetch live APIs/CSVs from *Agmarknet* and deposit them inside `ml/data/`.
2. Map your schemas into `ml/preprocessing/pipeline.py` to extract seasonality factors.
3. Train via `python ml/training/train.py` which will output `.joblib` / `.pth` artifacts.
4. Replace the static `PredictionEngine` generator inside `prediction_service/services.py` with your serialized payload arrays!

---

## 4. Multi-lingual Support
English (`en`), Hindi (`hi`), and Telugu (`te`) are currently embedded via custom JSON bindings located in:
`frontend/src/i18n/`

Any new strings generated for the application must be mapped out across all 3 dictionary files and utilized via the `t("key", locale)` custom hook available across the React framework.
