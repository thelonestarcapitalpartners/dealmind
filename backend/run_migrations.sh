#!/usr/bin/env bash
set -e

# Try alembic upgrade first
if command -v alembic >/dev/null 2>&1; then
  alembic upgrade head || true
else
  # Fallback to SQLAlchemy create_all
  python -m app.utils.manage_db init
fi
