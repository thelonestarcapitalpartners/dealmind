# Deployment Checklist and Steps

This document outlines the steps to push the repository to GitHub and deploy backend and frontend to production.

1) Prepare repo

- Ensure `.gitignore` is present (already included).
- Ensure `README.md` and `docs/DEPLOYMENT.md` exist.
- Commit all changes:

```bash
git init
git add .
git commit -m "Initial MVP commit"
```

2) Create GitHub repository

- Use GitHub UI or `gh` CLI:

```bash
gh repo create <org>/DealMind --public --source=. --remote=origin --push
```

3) Configure GitHub Secrets

- In repository settings > Secrets, add:
  - `DATABASE_URL`
  - `REDIS_URL`
  - `SUPABASE_URL`
  - `SUPABASE_KEY`
  - `OPENAI_API_KEY`
  - `GHCR_PAT` (if using GHCR with personal token)

4) CI/CD

- A CI workflow is provided at `.github/workflows/ci.yml` to run tests and build frontends.
- A container publishing workflow is at `.github/workflows/publish-image.yml` which pushes to `ghcr.io` on push to `main`.

5) Database migrations

- Generate alembic migrations locally and commit to `backend/alembic/versions`:

```bash
cd backend
alembic revision --autogenerate -m "initial"
alembic upgrade head
git add alembic/versions
git commit -m "Add alembic migrations"
```

6) Build and publish Docker image (optional)

```bash
./scripts/build_and_push_image.sh ghcr.io/<org>/dealmind-backend:latest
```

7) Deploy

- Vercel for `web` (Next.js):
  - Connect the GitHub repo to Vercel.
  - Set the project root to `web` if Vercel does not auto-detect the Next.js app.
  - Set environment variable `NEXT_PUBLIC_API_URL` to your backend URL.
  - Deploy the app.
  - If using the root `vercel.json`, Vercel should route the build to `web/package.json`.
- Render/Fly/AWS for backend: use `render.yaml` or `fly.toml` as template.

8) Post-deploy

- Run migrations on deploy or via a migration job.
- Set up backups, monitoring, and health checks.
- Point domain and enable TLS.

