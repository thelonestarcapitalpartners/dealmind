#!/usr/bin/env bash
set -e

# Wait for Postgres
echo "Waiting for Postgres..."
until pg_isready -h "${POSTGRES_HOST:-postgres}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-dealmind}"; do
  sleep 1
done

# Initialize DB (create tables) using SQLAlchemy if alembic not run
echo "Initializing database schema..."
python -m app.utils.manage_db init || true

# Run the provided command (default: uvicorn)
exec "$@"
