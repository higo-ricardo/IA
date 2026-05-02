# DevOps — Docker, CI/CD, Deploy

Carregue quando a tarefa envolver containerização, pipelines de CI/CD, deploy ou infraestrutura.

---

## Docker

### Dockerfile Python (FastAPI) — multi-stage, otimizado
```dockerfile
# ---- build stage ----
FROM python:3.12-slim AS builder
WORKDIR /app

RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

# ---- runtime stage ----
FROM python:3.12-slim AS runtime
WORKDIR /app

# Usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /app/.venv /app/.venv
COPY ./app ./app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER appuser
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Dockerfile Next.js — standalone output
```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN yarn build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

---

## Docker Compose — Stack Completa

```yaml
# docker-compose.yml
version: "3.9"

services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-appdb}
      POSTGRES_USER: ${POSTGRES_USER:-appuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?required}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

  backend:
    build:
      context: ./backend
      target: runtime
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY:?required}
    ports:
      - "8000:8000"
    volumes:
      - ./backend/app:/app/app   # hot reload em dev

  worker:
    build:
      context: ./backend
      target: runtime
    command: celery -A app.workers.celery_app worker --loglevel=info --concurrency=4
    restart: unless-stopped
    depends_on:
      - backend
      - redis
    environment:
      REDIS_URL: redis://redis:6379/0

  frontend:
    build:
      context: ./frontend
      target: runner
    restart: unless-stopped
    depends_on:
      - backend
    environment:
      NEXT_PUBLIC_API_URL: http://backend:8000/api/v1
    ports:
      - "3000:3000"

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    depends_on:
      - frontend
      - backend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro

volumes:
  postgres_data:
  redis_data:
```

---

## GitHub Actions — CI/CD Python + Node

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v4
        with:
          version: "0.4"

      - name: Install dependencies
        working-directory: ./backend
        run: uv sync --frozen

      - name: Lint (ruff + mypy)
        working-directory: ./backend
        run: |
          uv run ruff check .
          uv run mypy app/

      - name: Run tests
        working-directory: ./backend
        env:
          DATABASE_URL: postgresql+asyncpg://testuser:testpass@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key
        run: uv run pytest --cov=app --cov-report=xml -q

      - uses: codecov/codecov-action@v4
        with:
          file: ./backend/coverage.xml

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: yarn
          cache-dependency-path: frontend/yarn.lock

      - run: yarn install --frozen-lockfile
        working-directory: ./frontend

      - run: yarn lint && yarn type-check && yarn test --ci
        working-directory: ./frontend

  deploy:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ghcr.io/${{ github.repository }}/backend:${{ github.sha }}

      - name: Deploy to Fly.io
        uses: superfly/flyctl-actions@v1
        with:
          args: deploy --image ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

---

## Makefile — Atalhos de Desenvolvimento

```makefile
.PHONY: dev test lint migrate seed

# Iniciar tudo em dev
dev:
	docker compose up --build

# Apenas banco e redis (backend local)
infra:
	docker compose up db redis -d

# Backend
backend-dev:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

backend-test:
	cd backend && uv run pytest -v --cov=app

backend-lint:
	cd backend && uv run ruff check . && uv run mypy app/

# Migrações
migrate:
	cd backend && uv run alembic upgrade head

migration:
	cd backend && uv run alembic revision --autogenerate -m "$(msg)"

# Frontend
frontend-dev:
	cd frontend && yarn dev

frontend-build:
	cd frontend && yarn build

# Reset completo
reset:
	docker compose down -v
	docker compose up db redis -d
	sleep 3
	make migrate
```

---

## Plataformas de Deploy Recomendadas

| Serviço | Caso de Uso | Custo |
|---------|-------------|-------|
| **Fly.io** | APIs Python / Node com Docker | Free tier generoso |
| **Railway** | Full-stack com banco incluído | $5/mês |
| **Render** | APIs + workers + cron | Free tier |
| **Vercel** | Next.js frontend | Free tier |
| **Supabase** | PostgreSQL gerenciado + Auth + Storage | Free tier |
| **Upstash** | Redis serverless | Free tier |

### Configuração básica Fly.io (FastAPI)
```toml
# fly.toml
app = "my-fastapi-app"
primary_region = "gru"   # São Paulo

[build]
dockerfile = "Dockerfile"

[env]
PORT = "8000"

[http_service]
internal_port = 8000
force_https = true
auto_stop_machines = true
auto_start_machines = true

[[vm]]
memory = "512mb"
cpu_kind = "shared"
cpus = 1
```
