#!/usr/bin/env bash
set -e
# Start backend via Docker and instruct how to start frontends
if command -v docker >/dev/null 2>&1 && command -v docker-compose >/dev/null 2>&1; then
  echo "Starting backend services with Docker Compose..."
  docker compose up --build -d
  echo "Backend should be at http://localhost:8000"
else
  echo "Docker not found. To run backend locally, do:\n  cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python -m app.utils.manage_db init && uvicorn app.main:app --reload --port 8000"
fi

echo "To start web frontend(s):"
echo "  cd web && npm install && npm run dev  # Next.js"
echo "  cd frontend && npm install && npm run web  # Expo / React Native"
