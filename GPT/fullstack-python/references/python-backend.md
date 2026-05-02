# Python Backend — Referência de Frameworks

Carregue quando a tarefa envolver FastAPI, Django, Flask, autenticação, middleware ou configuração de projeto Python.

---

## FastAPI — Estrutura Completa

```
backend/
├── app/
│   ├── main.py              # criação do app, lifespan, middleware
│   ├── api/
│   │   ├── deps.py          # Depends: db, current_user, paginação
│   │   └── v1/
│   │       ├── router.py    # include_router de todos os módulos
│   │       ├── users.py
│   │       ├── auth.py
│   │       └── ...
│   ├── core/
│   │   ├── config.py        # Settings via pydantic-settings
│   │   ├── security.py      # JWT, hashing
│   │   └── exceptions.py    # handlers globais
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas (request/response)
│   ├── services/            # Business logic (sem acesso direto à DB)
│   ├── repositories/        # Acesso à DB (padrão Repository)
│   └── workers/             # Celery tasks
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── alembic/
│   ├── versions/
│   └── env.py
├── pyproject.toml
└── .env.example
```

### main.py — Configuração do App
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.db.session import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
setup_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")
```

### config.py — Settings com pydantic-settings
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn, AnyHttpUrl
from typing import Annotated

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # App
    PROJECT_NAME: str = "My API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ALLOWED_ORIGINS: list[AnyHttpUrl] = []

    # Database
    DATABASE_URL: PostgresDsn

    # Redis
    REDIS_URL: RedisDsn = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

settings = Settings()
```

### deps.py — Dependências Reutilizáveis
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.core.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await db.get(User, payload["sub"])
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

# Reutilização: get_current_active_superuser
async def get_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
```

---

## Django REST Framework

```
project/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── users/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       └── tests/
├── manage.py
└── requirements/
    ├── base.txt
    └── production.txt
```

### ViewSet com permissões customizadas
```python
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("profile").all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(id=self.request.user.id)

    @action(detail=False, methods=["get"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
```

---

## Flask — Estrutura com Blueprints e Application Factory

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api.users import users_bp
    from app.api.auth import auth_bp
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
```

---

## Autenticação JWT — FastAPI

```python
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: int | str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return jwt.encode(
        {"sub": str(subject), "exp": expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
```

---

## Dependências Python por Caso de Uso

```toml
# pyproject.toml (FastAPI stack)
[project]
dependencies = [
  "fastapi>=0.111",
  "uvicorn[standard]>=0.29",
  "pydantic[email]>=2.7",
  "pydantic-settings>=2.2",
  "sqlalchemy>=2.0",
  "asyncpg>=0.29",          # driver async para PostgreSQL
  "alembic>=1.13",
  "redis[hiredis]>=5.0",
  "celery[redis]>=5.3",
  "python-jose[cryptography]>=3.3",
  "passlib[bcrypt]>=1.7",
  "httpx>=0.27",            # cliente HTTP async (testes + calls externas)
]

[project.optional-dependencies]
dev = [
  "pytest>=8",
  "pytest-asyncio>=0.23",
  "pytest-cov>=5",
  "ruff>=0.4",
  "mypy>=1.10",
  "black>=24",
]
```

---

## Variáveis de Ambiente — `.env.example`

```env
# App
DEBUG=false
PROJECT_NAME=MyAPI
SECRET_KEY=change-me-in-production

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mydb

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]

# Email (opcional)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=
```
