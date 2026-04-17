# 🌾 SimpleKeth — AI-Powered Crop Decision Assistant

> **Know exactly when & where to sell your crops for maximum profit.**

SimpleKeth is an AI-powered decision assistant that predicts mandi prices and recommends when/where to sell to maximize net profit for small and medium Indian farmers.

---

## 🏗️ Architecture

```
Frontend (Next.js 15 + TypeScript)
          ↓
Backend (FastAPI Microservices)
  ├── Prediction Service  :8001
  ├── Recommendation Service :8002
  ├── Notification Service :8003
  └── Profile Service     :8004
          ↓
ML Layer (XGBoost + LSTM + Prophet Ensemble)
          ↓
Database (PostgreSQL + TimescaleDB) + Redis Cache
          ↓
External: OpenWeatherMap, Twilio (SMS/Voice), Firebase (Push)
```

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.12+
- Docker & Docker Compose (for full stack)
- PostgreSQL 16 + TimescaleDB (or use Docker)
- Redis 7+ (or use Docker)

### 1. Clone & Setup

```bash
git clone <repo-url> SimpleKeth
cd SimpleKeth
cp .env.example .env
# Edit .env with your API keys
```

### 2. Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

### 3. Backend Services

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Start each service (in separate terminals)
uvicorn prediction_service.main:app --port 8001 --reload
uvicorn recommendation_service.main:app --port 8002 --reload
uvicorn notification_service.main:app --port 8003 --reload
uvicorn profile_service.main:app --port 8004 --reload
```

### 4. Docker Compose (Full Stack)

```bash
docker compose -f infra/docker-compose.yml up --build
# → Frontend: http://localhost:3000
# → API Gateway: http://localhost:8000
# → Prediction API: http://localhost:8001
# → Recommendation API: http://localhost:8002
```

---

## 📁 Project Structure

```
SimpleKeth/
├── frontend/           # Next.js 15 App Router (TypeScript)
│   ├── src/app/        # Pages (dashboard, market, trends, simulator, alerts, profile)
│   ├── src/components/ # DecisionCard, MultiMandiList, PriceChart, InputModule
│   ├── src/i18n/       # Translations (EN, HI, TE)
│   ├── src/lib/        # API client, Zustand stores, utilities, offline/IndexedDB
│   └── public/         # PWA manifest, service worker, icons
├── backend/
│   ├── prediction_service/     # POST /predict — price forecasting + Redis cache
│   ├── recommendation_service/ # POST /recommend — SELL NOW / HOLD decisions
│   ├── notification_service/   # POST /notify — Twilio SMS/Voice + Firebase push
│   ├── profile_service/        # CRUD /farmers — farmer profile management
│   └── shared/                 # Config, DB, auth, SQLAlchemy models
├── ml/
│   ├── models/         # XGBoost, LSTM, Prophet, Ensemble
│   ├── preprocessing/  # Feature engineering pipeline
│   ├── training/       # Training orchestrator + evaluation
│   ├── explainability/ # SHAP feature importance
│   └── data/           # Sample Agmarknet CSV
├── prisma/             # Schema, migrations, seed script
├── infra/              # Docker Compose, Nginx, Helm, Prometheus, Grafana
└── .github/workflows/  # CI/CD (GitHub Actions)
```

---

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `API_BEARER_TOKEN` | Static auth token for MVP | `sk-simpleketh-dev-token-2026` |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | (provided) |
| `TWILIO_ACCOUNT_SID` | Twilio SID for SMS/voice | `mock_sid` |
| `TWILIO_AUTH_TOKEN` | Twilio auth token | `mock_token` |
| `FIREBASE_PROJECT_ID` | Firebase project for push notifications | `simpleketh-dev` |

---

## 📡 API Endpoints

### Prediction Service (`:8001`)
```bash
POST /predict
{
  "crop": "onion",
  "mandiId": "M001",
  "date": "2026-07-01",
  "quantityKg": 500
}
# → { predictions: [...], modelVersion, generatedAt }
```

### Recommendation Service (`:8002`)
```bash
POST /recommend
{
  "farmerProfile": {
    "location": { "lat": 28.61, "lng": 77.20 },
    "transportCostPerKg": 1.5,
    "storageCostPerKgPerDay": 0.5,
    "estimatedLossPct": 5
  },
  "crop": "onion",
  "quantityKg": 500
}
# → { decision: "SELL NOW", recommendedMandi, expectedNetProfit, ... }
```

### Notification Service (`:8003`)
```bash
POST /notify
{ "farmerId": "f1", "channel": "sms", "message": "Price spike alert!" }
```

### Profile Service (`:8004`)
```bash
POST /farmers         # Create farmer
GET  /farmers/{id}    # Get farmer
PUT  /farmers/{id}    # Update farmer
PUT  /farmers/{id}/profile  # Update profile
GET  /mandis          # List mandis
GET  /crops           # List crops
```

---

## 🌍 Internationalization

Supports **English**, **Hindi (हिन्दी)**, and **Telugu (తెలుగు)**.

Language can be switched from the navbar globe icon. All UI strings, crop names, and labels are translated.

---

## 📱 PWA & Offline Support

- Service Worker caches static assets and API responses
- IndexedDB stores farmer profile, last 7 predictions, and latest recommendation
- Offline users see cached data with an offline banner
- Twilio SMS/voice fallback for no-network scenarios

---

## 🤖 ML Models

| Model | Purpose | Framework |
|-------|---------|-----------|
| XGBoost | Tabular feature regression | xgboost |
| LSTM | Time-series price sequences | PyTorch |
| Prophet | Seasonal trend decomposition | prophet |
| Ensemble | Weighted combination | Custom |

Train models:
```bash
cd ml
pip install -r requirements.txt
python training/train.py
```

---

## 🧪 Testing

```bash
# Frontend unit tests
cd frontend && npm test

# Backend tests
cd backend && pytest

# E2E tests
cd frontend && npx playwright test
```

---

## 📜 License

MIT
