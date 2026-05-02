# Database — SQLAlchemy, Prisma, Redis, Migrações

Carregue quando a tarefa envolver modelagem de dados, ORM, cache, migrações ou queries complexas.

---

## SQLAlchemy 2 — Modelos Completos

```python
from sqlalchemy import (
    String, Text, Integer, Boolean, DateTime, ForeignKey,
    UniqueConstraint, Index, func, event
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, validates
)
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker
)
from datetime import datetime, timezone
from typing import Optional

class Base(DeclarativeBase):
    """Base com campos de auditoria automáticos."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        Index("ix_users_is_active", "is_active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relacionamentos
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    profile: Mapped[Optional["UserProfile"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    @validates("email")
    def validate_email(self, key, value: str) -> str:
        return value.lower().strip()

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    total_cents: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
```

---

## SQLAlchemy — Session Factory e Conexão

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,          # verifica conexão antes de usar
    echo=settings.DEBUG,
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,      # evita lazy load após commit
    autoflush=False,
)

# Dependency FastAPI
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
```

---

## Queries Avançadas

```python
from sqlalchemy import select, update, delete, exists, and_, or_, case
from sqlalchemy.orm import selectinload, joinedload, contains_eager

# Eager loading — evitar N+1
async def get_users_with_orders(db: AsyncSession) -> list[User]:
    stmt = (
        select(User)
        .options(
            selectinload(User.orders).selectinload(Order.items),
            joinedload(User.profile),
        )
        .where(User.is_active == True)
    )
    result = await db.execute(stmt)
    return result.unique().scalars().all()

# Update em massa — sem carregar objetos na memória
async def deactivate_users(db: AsyncSession, user_ids: list[int]) -> int:
    stmt = (
        update(User)
        .where(User.id.in_(user_ids))
        .values(is_active=False)
        .returning(User.id)
    )
    result = await db.execute(stmt)
    await db.commit()
    return len(result.fetchall())

# Subquery e exists
async def users_with_pending_orders(db: AsyncSession) -> list[User]:
    pending_subq = (
        select(Order.user_id)
        .where(Order.status == "pending")
        .correlate(User)
        .exists()
    )
    result = await db.execute(select(User).where(pending_subq))
    return result.scalars().all()

# CASE / condicional
from sqlalchemy import case
status_label = case(
    (Order.status == "pending", "Aguardando"),
    (Order.status == "shipped", "Enviado"),
    else_="Outro",
).label("status_label")
```

---

## Alembic — Migrações

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base          # importa todos os models
from app.core.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL).replace("+asyncpg", ""))

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

```bash
# Comandos Alembic
alembic revision --autogenerate -m "add users table"
alembic upgrade head
alembic downgrade -1
alembic history --verbose
```

---

## Redis — Cache, Sessions, Pub/Sub

```python
from redis.asyncio import Redis, ConnectionPool
from functools import wraps
import json
import hashlib
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

# Pool compartilhado
pool = ConnectionPool.from_url(str(settings.REDIS_URL), decode_responses=True)

async def get_redis() -> Redis:
    return Redis(connection_pool=pool)

# Cache decorator para async functions
def redis_cache(ttl: int = 300, prefix: str = "cache"):
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            redis = await get_redis()
            key_data = json.dumps({"args": args, "kwargs": kwargs}, default=str, sort_keys=True)
            cache_key = f"{prefix}:{func.__name__}:{hashlib.md5(key_data.encode()).hexdigest()}"

            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)

            result = await func(*args, **kwargs)
            await redis.setex(cache_key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

# Pub/Sub para eventos em tempo real
class EventBus:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def publish(self, channel: str, event: dict) -> None:
        await self._redis.publish(channel, json.dumps(event))

    async def subscribe(self, channel: str):
        async with self._redis.pubsub() as pubsub:
            await pubsub.subscribe(channel)
            async for message in pubsub.listen():
                if message["type"] == "message":
                    yield json.loads(message["data"])

# Rate limiting com sliding window
async def is_rate_limited(redis: Redis, key: str, limit: int, window: int) -> bool:
    now = int(time.time())
    pipe = redis.pipeline()
    pipe.zremrangebyscore(key, 0, now - window)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, window)
    results = await pipe.execute()
    return results[2] > limit
```

---

## Prisma (JavaScript/TypeScript)

```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  orders    Order[]
  profile   Profile?

  @@map("users")
  @@index([email])
}

model Order {
  id         Int         @id @default(autoincrement())
  userId     Int         @map("user_id")
  status     OrderStatus @default(PENDING)
  totalCents Int         @default(0) @map("total_cents")
  user       User        @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("orders")
  @@index([userId])
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}
```

```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const db = globalForPrisma.prisma ?? new PrismaClient({ log: ['query'] });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;

// Query com include e paginação
async function getOrdersWithUser(page: number = 1, perPage: number = 20) {
  const [orders, total] = await db.$transaction([
    db.order.findMany({
      include: { user: { select: { id: true, name: true, email: true } } },
      skip: (page - 1) * perPage,
      take: perPage,
      orderBy: { createdAt: 'desc' },
    }),
    db.order.count(),
  ]);
  return { orders, total, pages: Math.ceil(total / perPage) };
}
```
