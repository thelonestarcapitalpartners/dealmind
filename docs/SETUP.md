# Development Setup Guide

## Prerequisites

- Node.js 18+ 
- Python 3.10+
- PostgreSQL 14+
- Docker & Docker Compose (optional but recommended)

## Backend Setup (FastAPI)

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Set Up Database

```bash
# Create PostgreSQL database
createdb dealmind

# Run migrations
alembic upgrade head
```

### 5. Run Backend

```bash
python -m uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

---

## Frontend Setup (React Native / Expo)

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env.local
# Edit .env.local with your API URL and Supabase config
```

### 3. Run Development Server

```bash
npx expo start
```

Then:
- Press `i` for iOS simulator
- Press `a` for Android emulator
- Press `w` for web

---

## Web Setup (Next.js)

### 1. Install Dependencies

```bash
cd web
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env.local
# Edit .env.local with your API URL and Supabase config
```

### 3. Run Development Server

```bash
npm run dev
```

Web app runs at: `http://localhost:3000`

---

## Full Stack with Docker Compose

```bash
# From project root
docker-compose up -d

# This starts:
# - PostgreSQL on port 5432
# - FastAPI backend on port 8000
# - Redis on port 6379
```

---

## Project Structure

```
DealMind/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── models/           # SQLAlchemy models
│   │   ├── services/         # Business logic
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── utils/            # Utilities
│   │   ├── rules/            # Country/state rules
│   │   └── main.py           # FastAPI app
│   ├── config/               # Settings
│   ├── migrations/           # Alembic migrations
│   ├── tests/                # Tests
│   ├── requirements.txt      # Dependencies
│   └── .env.example          # Environment template
│
├── frontend/                 # React Native (Expo)
│   ├── app/
│   │   ├── screens/          # Mobile screens
│   │   ├── components/       # Reusable components
│   │   ├── services/         # API services
│   │   └── App.tsx           # Entry point
│   ├── assets/               # Images, fonts
│   ├── app.json              # Expo config
│   ├── package.json
│   └── .env.example
│
├── web/                      # Next.js web app
│   ├── app/
│   │   ├── layout.tsx        # Root layout
│   │   ├── page.tsx          # Home page
│   │   ├── globals.css       # Global styles
│   ├── components/           # React components
│   ├── lib/                  # Utilities
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── package.json
│   └── .env.example
│
├── docs/
│   ├── DATABASE.md
│   ├── API.md
│   ├── SETUP.md
│   └── ARCHITECTURE.md
│
└── SPECIFICATION.md          # Full product spec
```

---

## Key Services & Credentials

### Supabase
1. Create a Supabase project at https://supabase.com
2. Get your `SUPABASE_URL` and `SUPABASE_KEY`
3. Add to both backend and frontend `.env` files

### OpenAI
1. Create API key at https://platform.openai.com/api-keys
2. Add `OPENAI_API_KEY` to backend `.env`

### Stripe (for payments)
1. Create account at https://stripe.com
2. Get test API keys
3. Add `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` to backend

### Google Maps/Geocoding
1. Enable APIs in Google Cloud Console
2. Create API keys
3. Add to backend `.env`

---

## First Run Checklist

- [ ] Backend database created and migrations run
- [ ] Backend starts without errors (`http://localhost:8000/health`)
- [ ] Frontend dependencies installed
- [ ] Frontend `.env.local` configured with backend URL
- [ ] Web dependencies installed
- [ ] Web `.env.local` configured with backend URL
- [ ] Can view API docs at `http://localhost:8000/docs`

---

## Useful Commands

### Backend
```bash
# Format code
black app/

# Run linter
flake8 app/

# Run tests
pytest

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

### Frontend/Web
```bash
# Format
npm run format

# Lint
npm run lint

# Type check (web)
npm run type-check

# Test
npm test
```

---

## Common Issues

**Backend won't start: "Database connection failed"**
- Check PostgreSQL is running
- Verify DATABASE_URL in `.env`
- Run migrations: `alembic upgrade head`

**Frontend can't connect to backend**
- Ensure backend is running on `http://localhost:8000`
- Check `EXPO_PUBLIC_API_URL` in frontend `.env`
- Check CORS configuration in backend

**Dependency conflicts**
- Delete `node_modules` and `package-lock.json`, then reinstall
- Delete Python venv and recreate

---

## Next Steps

1. Review the [Full Specification](../SPECIFICATION.md)
2. Start with [Backend API Structure](./API.md)
3. Implement core underwriting calculations
4. Build frontend screens
5. Integrate with OpenAI for data extraction and chat
