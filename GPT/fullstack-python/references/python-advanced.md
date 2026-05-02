# Python Avançado — Referência de Recursos

Carregue este arquivo quando a tarefa envolver recursos avançados de Python:
classes, herança, metaclasses, ABCs, decoradores, generators, async, type system, protocolos.

---

## 1. Classes e Herança

### Dataclasses — objetos de valor sem boilerplate
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)          # imutável; hashável
class Money:
    amount: float
    currency: str = "BRL"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

@dataclass
class Order:
    id: int
    items: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    total: Optional[Money] = None
```

### ABCs — contratos de interface
```python
from abc import ABC, abstractmethod
from typing import AsyncIterator

class Repository[T](ABC):
    """Interface genérica de repositório."""

    @abstractmethod
    async def get(self, id: int) -> T | None: ...

    @abstractmethod
    async def save(self, entity: T) -> T: ...

    @abstractmethod
    async def delete(self, id: int) -> bool: ...

    @abstractmethod
    def list_all(self) -> AsyncIterator[T]: ...

class UserRepository(Repository["User"]):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get(self, id: int) -> "User | None":
        return await self._db.get(User, id)

    async def save(self, entity: "User") -> "User":
        self._db.add(entity)
        await self._db.commit()
        await self._db.refresh(entity)
        return entity

    async def delete(self, id: int) -> bool:
        user = await self.get(id)
        if not user:
            return False
        await self._db.delete(user)
        await self._db.commit()
        return True

    async def list_all(self) -> AsyncIterator["User"]:
        result = await self._db.execute(select(User))
        for user in result.scalars():
            yield user
```

### Metaclasses — controle de criação de classes
```python
from typing import Any

class SingletonMeta(type):
    """Metaclass para o padrão Singleton thread-safe."""
    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabasePool(metaclass=SingletonMeta):
    def __init__(self, url: str):
        self.url = url
        self._pool = None  # inicializado lazy

# Uso:
pool1 = DatabasePool("postgresql://...")
pool2 = DatabasePool("qualquer-coisa")
assert pool1 is pool2  # True — mesma instância

# Registry automático via metaclass
class PluginMeta(type):
    registry: dict[str, type] = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:  # não registra a base em si
            mcs.registry[name.lower()] = cls
        return cls

class Plugin(metaclass=PluginMeta): ...
class CSVExporter(Plugin): ...   # registrado automaticamente
class JSONExporter(Plugin): ...  # idem

# PluginMeta.registry == {"csvexporter": CSVExporter, "jsonexporter": JSONExporter}
```

---

## 2. Decoradores

### Decorador de classe com estado
```python
import functools
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def cache_result(ttl_seconds: int = 60):
    """Cache em memória com TTL."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        cache: dict = {}

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in cache:
                result, ts = cache[key]
                if now - ts < ttl_seconds:
                    return result
            result = await func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def require_permission(permission: str):
    """Decorator de autorização — integra com FastAPI."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # extrai `current_user` dos kwargs (injetado via Depends)
            current_user = kwargs.get("current_user")
            if not current_user or permission not in current_user.permissions:
                raise HTTPException(status_code=403, detail="Forbidden")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### Classe-decorador (via `__call__`)
```python
class RateLimiter:
    """Limita chamadas a N por janela de segundos."""
    def __init__(self, max_calls: int, window: float):
        self.max_calls = max_calls
        self.window = window
        self._calls: list[float] = []

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            now = time.monotonic()
            self._calls = [t for t in self._calls if now - t < self.window]
            if len(self._calls) >= self.max_calls:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            self._calls.append(now)
            return await func(*args, **kwargs)
        return wrapper

@RateLimiter(max_calls=10, window=1.0)
async def send_email(to: str, subject: str) -> None: ...
```

---

## 3. Generators e Iteradores

```python
from typing import Generator, Iterator
from collections.abc import AsyncGenerator

def paginate_query(
    query,
    db: Session,
    page_size: int = 100,
) -> Generator[list, None, None]:
    """Itera sobre resultados em pages — evita carregar tudo na memória."""
    offset = 0
    while True:
        batch = db.execute(query.offset(offset).limit(page_size)).scalars().all()
        if not batch:
            return
        yield batch
        if len(batch) < page_size:
            return
        offset += page_size

# Pipeline de transformação lazy
def parse_csv_rows(path: str) -> Iterator[dict]:
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def validate_rows(rows: Iterator[dict]) -> Iterator[dict]:
    for row in rows:
        if row.get("email"):
            yield row

def transform_rows(rows: Iterator[dict]) -> Iterator[dict]:
    for row in rows:
        yield {**row, "name": row["name"].strip().title()}

# Composição de pipeline (zero alocação intermediária):
pipeline = transform_rows(validate_rows(parse_csv_rows("users.csv")))
for record in pipeline:
    db.save(record)

# Async generator — streaming de SSE / WebSocket
async def stream_events(channel: str) -> AsyncGenerator[dict, None]:
    async with redis.subscribe(channel) as sub:
        async for message in sub:
            yield json.loads(message.data)
```

---

## 4. Context Managers

```python
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator

@asynccontextmanager
async def transaction(db: AsyncSession) -> AsyncIterator[AsyncSession]:
    """Context manager de transação com rollback automático."""
    async with db.begin():
        try:
            yield db
        except Exception:
            await db.rollback()
            raise

# Uso:
async with transaction(db) as session:
    await session.execute(...)  # rollback automático se raise

@contextmanager
def temporary_directory() -> Iterator[Path]:
    """Cria e remove diretório temporário."""
    tmp = Path(tempfile.mkdtemp())
    try:
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
```

---

## 5. Async / Await — Padrões Avançados

```python
import asyncio
from typing import TypeVar, Coroutine, Any

T = TypeVar("T")

async def gather_with_limit(
    *coros: Coroutine[Any, Any, T],
    limit: int = 10,
) -> list[T]:
    """Executa coroutines com concorrência limitada (semaphore)."""
    sem = asyncio.Semaphore(limit)

    async def bounded(coro: Coroutine[Any, Any, T]) -> T:
        async with sem:
            return await coro

    return await asyncio.gather(*[bounded(c) for c in coros])

# Background tasks — FastAPI / Starlette
from fastapi import BackgroundTasks

@router.post("/send-report")
async def send_report(
    background_tasks: BackgroundTasks,
    report_id: int,
    db: AsyncSession = Depends(get_db),
):
    background_tasks.add_task(generate_and_email_report, report_id, db)
    return {"status": "queued"}
```

---

## 6. Type System Avançado

```python
from typing import TypeVar, Generic, Protocol, runtime_checkable, overload, Literal
from typing import TypeAlias

# Generics
T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

class Result(Generic[T]):
    """Either/Result type para tratamento funcional de erros."""
    def __init__(self, value: T | None = None, error: Exception | None = None):
        self._value = value
        self._error = error

    @classmethod
    def ok(cls, value: T) -> "Result[T]":
        return cls(value=value)

    @classmethod
    def err(cls, error: Exception) -> "Result[T]":
        return cls(error=error)

    @property
    def is_ok(self) -> bool:
        return self._error is None

    def unwrap(self) -> T:
        if self._error:
            raise self._error
        return self._value  # type: ignore

# Protocols — duck typing com verificação estática
@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> "Serializable": ...

# TypeAlias legível
UserId: TypeAlias = int
Email: TypeAlias = str

# Overload para funções polimórficas
@overload
def parse_id(value: str) -> int: ...
@overload
def parse_id(value: int) -> int: ...

def parse_id(value: str | int) -> int:
    return int(value)

# Literal types para enumerações simples
Status: TypeAlias = Literal["active", "inactive", "pending"]
```

---

## 7. Pydantic v2 — Validação e Serialização

```python
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from pydantic import EmailStr, AnyHttpUrl
from typing import Annotated

PositiveInt = Annotated[int, Field(gt=0)]

class UserBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, str_to_lower=True)

    email: EmailStr
    name: str = Field(min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(min_length=8)
    confirm_password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreate":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)  # compatível com ORM

    id: PositiveInt
    is_active: bool = True
```

---

## 8. SQLAlchemy 2 — Async ORM

```python
from sqlalchemy import String, ForeignKey, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

class Base(DeclarativeBase): ...

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="user", lazy="select")

# Query builder seguro (sem SQL raw)
async def get_active_users_with_orders(db: AsyncSession) -> list[User]:
    stmt = (
        select(User)
        .where(User.is_active == True)
        .join(User.orders)
        .group_by(User.id)
        .having(func.count() > 0)
        .order_by(User.name)
    )
    result = await db.execute(stmt)
    return result.scalars().unique().all()
```

---

## 9. Celery — Background Jobs

```python
from celery import Celery, Task
from celery.utils.log import get_task_logger

app = Celery("worker", broker="redis://localhost:6379/0")
logger = get_task_logger(__name__)

class DatabaseTask(Task):
    """Task base com sessão de banco."""
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

@app.task(bind=True, base=DatabaseTask, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, user_id: int) -> dict:
    try:
        user = self.db.get(User, user_id)
        if not user:
            return {"status": "user_not_found"}
        email_service.send_welcome(user.email, user.name)
        return {"status": "sent", "to": user.email}
    except Exception as exc:
        logger.error(f"Failed to send email to user {user_id}: {exc}")
        raise self.retry(exc=exc)
```

---

## 10. pytest — Testes Avançados

```python
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(app, db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users/", json={"email": "test@example.com", "name": "Test"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"

@pytest.mark.parametrize("email,valid", [
    ("valid@example.com", True),
    ("invalid-email", False),
    ("", False),
])
async def test_email_validation(client, email, valid):
    response = await client.post("/users/", json={"email": email, "name": "Test"})
    assert (response.status_code == 201) == valid
```
