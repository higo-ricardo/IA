# Exemplos de Código — Code Reviewer PT

Snippets ❌/✅ organizados por categoria. Use como referência ao incluir sugestões no relatório.

---

## Índice

1. [Segurança — Exemplos e Correções](#1-segurança--exemplos-e-correções)
2. [Performance — Exemplos e Correções](#2-performance--exemplos-e-correções)
3. [Design — Exemplos e Correções](#3-design--exemplos-e-correções)
4. [Manutenibilidade — Exemplos e Correções](#4-manutenibilidade--exemplos-e-correções)

---

## 1. Segurança — Exemplos e Correções

### S1 — SQL Injection (PP-72, CC-130)

```python
# ❌ CRÍTICO — concatenação direta
query = f"SELECT * FROM users WHERE id = {user_id}"
db.execute(query)

# ✅ Correto — query parametrizada
query = "SELECT * FROM users WHERE id = ?"
db.execute(query, (user_id,))
```

```javascript
// ❌ CRÍTICO — template string em query
const query = `SELECT * FROM users WHERE email = '${email}'`;
await db.query(query);

// ✅ Correto — prepared statement
const query = "SELECT * FROM users WHERE email = $1";
await db.query(query, [email]);
```

---

### S2 — XSS — Cross-Site Scripting (PP-72)

```javascript
// ❌ CRÍTICO — inserção direta de input do usuário
element.innerHTML = userInput;
document.write(userInput);

// ✅ Correto — escape ou textContent
element.textContent = userInput;

// ✅ Para HTML intencional — use biblioteca de sanitização
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

```jsx
// ❌ CRÍTICO — React: bypass do escape automático
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// ✅ Correto — deixe o React escapar
<div>{userContent}</div>

// ✅ Para HTML intencional — sanitize antes
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />
```

---

### S3 — Secrets Hardcoded (PP-72)

```python
# ❌ CRÍTICO — credencial no código
API_KEY = "sk-abc123..."
DB_PASSWORD = "minha_senha_super_secreta"
JWT_SECRET = "hardcoded-jwt-secret"

# ✅ Correto — variável de ambiente
import os
API_KEY = os.environ["API_KEY"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
JWT_SECRET = os.environ["JWT_SECRET"]
```

```javascript
// ❌ CRÍTICO — token no código
const stripeKey = "sk_live_abc123...";

// ✅ Correto
const stripeKey = process.env.STRIPE_SECRET_KEY;
if (!stripeKey) throw new Error("STRIPE_SECRET_KEY não definida");
```

---

### S4 — Auth Bypass — Verificação Ausente (CA-29)

```python
# ❌ CRÍTICO — assume autenticação sem verificar
def get_admin_data(user_id):
    return db.query("SELECT * FROM admin_data")

# ✅ Correto — verificação explícita
def get_admin_data(user_id: int) -> list[dict]:
    user = db.get_user(user_id)
    if not user or not user.is_admin:
        raise PermissionError("Acesso negado")
    return db.query("SELECT * FROM admin_data")
```

---

### S5 — Path Traversal (PP-72)

```python
# ❌ CRÍTICO — caminho construído com input
def serve_file(filename: str):
    path = f"/var/www/files/{filename}"
    return open(path).read()
# Ataque: filename = "../../etc/passwd"

# ✅ Correto — resolve e valide que está dentro do diretório permitido
import os

BASE_DIR = "/var/www/files"

def serve_file(filename: str):
    safe_path = os.path.realpath(os.path.join(BASE_DIR, filename))
    if not safe_path.startswith(BASE_DIR):
        raise PermissionError("Acesso negado")
    return open(safe_path).read()
```

---

### S6 — SSRF (PP-72)

```python
# ❌ CRÍTICO — URL construída com input sem validação
def fetch_url(url: str):
    return requests.get(url).text
# Ataque: url = "http://169.254.169.254/metadata" (AWS metadata)

# ✅ Correto — allowlist de domínios
ALLOWED_DOMAINS = {"api.trusted.com", "data.trusted.com"}

def fetch_url(url: str):
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    if domain not in ALLOWED_DOMAINS:
        raise ValueError(f"Domínio não permitido: {domain}")
    return requests.get(url).text
```

---

### S7 — Deserialização Insegura (PP-72)

```python
# ❌ CRÍTICO — pickle executa código arbitrário
import pickle
data = pickle.loads(user_input)  # RCE garantido com input malicioso

# ✅ Correto — use JSON para dados não confiáveis
import json
data = json.loads(user_input)
```

---

### S8 — Condição de Corrida (PP-48)

```python
# ❌ CRÍTICO — leitura-modificação-escrita sem lock
balance = account.get_balance()
if balance >= amount:
    account.set_balance(balance - amount)  # Race condition

# ✅ Correto — operação atômica no banco ou lock explícito
with db.transaction():
    account = db.get_for_update(account_id)  # SELECT FOR UPDATE
    if account.balance >= amount:
        account.balance -= amount
        db.save(account)
    else:
        raise InsufficientFundsError()
```

---

### S10 — Log de Dado Sensível (CC-86)

```python
# ❌ CRÍTICO — senha/token no log
logger.info(f"Login: user={user.email}, password={password}")
logger.debug(f"Request headers: {request.headers}")  # pode ter Authorization

# ✅ Correto — nunca logar dado sensível
logger.info(f"Login attempt: user={user.email}")
logger.debug(f"Request to {request.path} from {request.remote_addr}")
```

---

## 2. Performance — Exemplos e Correções

### N+1 Queries

```python
# ❌ Alto — 1 query por usuário no loop
users = db.query("SELECT * FROM users")
for user in users:
    orders = db.query(f"SELECT * FROM orders WHERE user_id = {user.id}")
    print(f"{user.name}: {len(orders)} pedidos")

# ✅ Correto — JOIN único
users_with_orders = db.query("""
    SELECT u.id, u.name, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id, u.name
""")
```

```python
# ✅ Com ORM (Django/SQLAlchemy) — eager loading
users = User.objects.prefetch_related('orders').all()
# ou
users = db.query(User).options(joinedload(User.orders)).all()
```

---

### Tratamento de Erro Ausente (CC-86)

```python
# ❌ Alto — assume resultado sem verificar
def get_user(user_id: int):
    result = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return result[0]  # IndexError se vazio

# ✅ Correto — verificação antes de acessar
from typing import Optional

def get_user(user_id: int) -> Optional[dict]:
    result = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    if not result:
        return None
    return result[0]
```

---

### Exception Silenciada (CC-95)

```python
# ❌ Alto — exception engolida
try:
    process_payment(order)
except Exception:
    pass  # Falha silenciosa — pedido parece processado

# ✅ Correto — handle ou re-raise com contexto
try:
    process_payment(order)
except PaymentGatewayError as e:
    logger.error(f"Falha no pagamento order={order.id}: {e}")
    raise PaymentFailedError(f"Não foi possível processar o pagamento") from e
```

---

### Type Hints Ausentes (CC-4 — linguagens tipadas)

```python
# ❌ Médio (L3+) — sem anotações
def process(data, config):
    ...

# ✅ Correto — intenção clara
from typing import Optional
def process(data: list[dict], config: ProcessConfig) -> Optional[ProcessResult]:
    ...
```

---

## 3. Design — Exemplos e Correções

### SRP Violado (CA-8)

```python
# ❌ Importante — classe com múltiplas responsabilidades
class UserService:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...    # ← responsabilidade de notificação
    def generate_pdf_report(self, user): ...   # ← responsabilidade de relatório
    def hash_password(self, password): ...     # ← responsabilidade de segurança

# ✅ Correto — responsabilidades separadas
class UserService:
    def create_user(self, data): ...

class NotificationService:
    def send_welcome_email(self, user): ...

class ReportService:
    def generate_user_pdf(self, user): ...

class PasswordHasher:
    def hash(self, password): ...
```

---

### DIP Violado — Dependência Invertida (CA-12)

```python
# ❌ Importante — use case depende de implementação concreta
class CreateOrderUseCase:
    def __init__(self):
        self.repo = PostgresOrderRepository()  # ← concreto, não testável
        self.emailer = SendGridEmailer()       # ← concreto, não testável

# ✅ Correto — depende de abstrações (interfaces/protocolos)
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: ...

class Emailer(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None: ...

class CreateOrderUseCase:
    def __init__(self, repo: OrderRepository, emailer: Emailer):
        self.repo = repo
        self.emailer = emailer
```

---

### Números Mágicos (CC-175)

```python
# ❌ Médio — valores sem nome
if user.status == 7:
    ...
if len(items) > 100:
    ...
time.sleep(300)

# ✅ Correto — constantes nomeadas
class UserStatus:
    PENDING_VERIFICATION = 7

MAX_ITEMS_PER_PAGE = 100
CACHE_TTL_SECONDS = 300

if user.status == UserStatus.PENDING_VERIFICATION:
    ...
if len(items) > MAX_ITEMS_PER_PAGE:
    ...
time.sleep(CACHE_TTL_SECONDS)
```

---

### Aninhamento Profundo (CC-178)

```python
# ❌ Importante (L3+) — 4 níveis de aninhamento
def process_order(order):
    if order:
        if order.is_valid():
            if order.user.is_active():
                if order.items:
                    for item in order.items:
                        ...

# ✅ Correto — early returns reduzem aninhamento
def process_order(order):
    if not order:
        return
    if not order.is_valid():
        raise InvalidOrderError()
    if not order.user.is_active():
        raise InactiveUserError()
    if not order.items:
        return

    for item in order.items:
        ...
```

---

### Efeitos Colaterais Ocultos (CC-31)

```python
# ❌ Importante — nome sugere apenas leitura, mas modifica estado
def get_user_session(user_id: int) -> Session:
    session = db.get_session(user_id)
    session.last_accessed = datetime.now()  # ← efeito oculto!
    db.save(session)
    return session

# ✅ Correto — nomeie para revelar o efeito ou separe responsabilidades
def get_and_refresh_user_session(user_id: int) -> Session:
    session = db.get_session(user_id)
    session.last_accessed = datetime.now()
    db.save(session)
    return session

# ou separe em dois métodos
def get_user_session(user_id: int) -> Session:
    return db.get_session(user_id)

def refresh_session_access(session: Session) -> None:
    session.last_accessed = datetime.now()
    db.save(session)
```

---

## 4. Manutenibilidade — Exemplos e Correções

### Nomes sem Intenção (CC-4)

```python
# ❌ Médio (L3+) — nomes vazios
def calc(d, c):
    return d * c * 0.87

# ✅ Correto
TAX_RATE = 0.87

def calculate_net_price(unit_price: float, quantity: int) -> float:
    return unit_price * quantity * TAX_RATE
```

---

### DRY — Lógica Duplicada (PP-15, CC-37)

```python
# ❌ Importante (acima da tolerância do nível)
def create_admin_user(email, password):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Email inválido")
    hashed = bcrypt.hash(password)
    db.insert("users", {"email": email, "password": hashed, "role": "admin"})

def create_regular_user(email, password):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # ← duplicado
        raise ValueError("Email inválido")
    hashed = bcrypt.hash(password)                   # ← duplicado
    db.insert("users", {"email": email, "password": hashed, "role": "user"})

# ✅ Correto — conhecimento centralizado
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

def validate_email(email: str) -> None:
    if not re.match(EMAIL_REGEX, email):
        raise ValueError("Email inválido")

def create_user(email: str, password: str, role: str) -> None:
    validate_email(email)
    hashed = bcrypt.hash(password)
    db.insert("users", {"email": email, "password": hashed, "role": role})

def create_admin_user(email: str, password: str) -> None:
    create_user(email, password, role="admin")

def create_regular_user(email: str, password: str) -> None:
    create_user(email, password, role="user")
```

---

### YAGNI — Over-engineering (PP-43)

```python
# ❌ Médio — abstração sem caso de uso atual
class AbstractUserFactory(ABC):
    @abstractmethod
    def create_user(self, strategy: str, adapter: str, observer: list): ...

class ConcreteUserFactoryV1(AbstractUserFactory):
    def create_user(self, strategy: str, adapter: str, observer: list):
        # Usado em exatamente 1 lugar, de 1 forma
        return User(name="default")

# ✅ Correto — só o necessário agora
def create_user(name: str) -> User:
    return User(name=name)
```
