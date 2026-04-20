# Exemplos de Uso do `/codesearch`

## Introdução
O `/codesearch` é uma ferramenta poderosa para encontrar **exemplos de código**, **melhores práticas**, **padrões de projeto** e **soluções para problemas comuns**. Este guia fornece exemplos práticos de como usá-lo em diferentes cenários.

---

## 📌 Pré-requisitos
- Ferramenta `/codesearch` disponível no ambiente (Claude Chat, Copilot Code, Qwen Code).
- Acesso a uma base de código ou repositório (local ou remoto).

---

## 🚀 Exemplos de Uso

### **Exemplo 1: Encontrar Melhores Práticas para Funções Puras em JavaScript**
```
/codesearch "melhores práticas função pura JavaScript"
```
**Resultado esperado:**
```
📚 Melhores práticas para funções puras em JavaScript:

1. **Função pura básica:**
```javascript
function add(a, b) {
  return a + b;
}
```

2. **Função pura com validação:**
```javascript
function add(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new Error('Parâmetros devem ser números');
  }
  return a + b;
}
```

3. **Função pura com imutabilidade:**
```javascript
function updateUser(user, updates) {
  return { ...user, ...updates };
}
```

🔍 Fonte: [https://github.com/facebook/react/wiki/Guides](https://github.com/facebook/react/wiki/Guides)
```

---

### **Exemplo 2: Encontrar Padrões de Projeto (Design Patterns) em Python**
```
/codesearch "design patterns Python Singleton Factory"
```
**Resultado esperado:**
```
📚 Padrões de Projeto em Python:

1. **Singleton:**
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

2. **Factory:**
```python
class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Tipo de animal desconhecido")
```

🔍 Fonte: [https://refactoring.guru/design-patterns](https://refactoring.guru/design-patterns)
```

---

### **Exemplo 3: Encontrar Soluções para Validação de CPF em JavaScript**
```
/codesearch "validação CPF JavaScript"
```
**Resultado esperado:**
```
📚 Validação de CPF em JavaScript:

1. **Função de validação:**
```javascript
function validateCPF(cpf) {
  // Remove caracteres não numéricos
  cpf = cpf.replace(/[^0-9]/g, '');
  
  // Verifica se o CPF tem 11 dígitos
  if (cpf.length !== 11) return false;
  
  // Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
  if (/^(\d)\1{10}$/.test(cpf)) return false;
  
  // Calcula o primeiro dígito verificador
  let sum = 0;
  for (let i = 0; i < 9; i++) {
    sum += parseInt(cpf.charAt(i)) * (10 - i);
  }
  let firstDigit = 11 - (sum % 11);
  if (firstDigit >= 10) firstDigit = 0;
  
  // Calcula o segundo dígito verificador
  sum = 0;
  for (let i = 0; i < 10; i++) {
    sum += parseInt(cpf.charAt(i)) * (11 - i);
  }
  let secondDigit = 11 - (sum % 11);
  if (secondDigit >= 10) secondDigit = 0;
  
  // Verifica se os dígitos calculados batem com os do CPF
  return firstDigit === parseInt(cpf.charAt(9)) && 
         secondDigit === parseInt(cpf.charAt(10));
}
```

2. **Uso da função:**
```javascript
console.log(validateCPF("123.456.789-09")); // false
console.log(validateCPF("111.444.777-35")); // true
```

🔍 Fonte: [https://www.devmedia.com.br/validando-o-cpf-em-javascript/23693](https://www.devmedia.com.br/validando-o-cpf-em-javascript/23693)
```

---

### **Exemplo 4: Encontrar Exemplos de Refatoração em TypeScript**
```
/codesearch "refatoração TypeScript remover duplicação"
```
**Resultado esperado:**
```
📚 Exemplos de Refatoração em TypeScript:

1. **Antes (código duplicado):**
```typescript
function calculateTotal(items: { price: number }[]) {
  let total = 0;
  for (const item of items) {
    total += item.price;
  }
  return total;
}

function calculateAverage(items: { price: number }[]) {
  let total = 0;
  for (const item of items) {
    total += item.price;
  }
  return total / items.length;
}
```

2. **Depois (código reutilizado):**
```typescript
function getTotal(items: { price: number }[]) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

function calculateTotal(items: { price: number }[]) {
  return getTotal(items);
}

function calculateAverage(items: { price: number }[]) {
  return getTotal(items) / items.length;
}
```

🔍 Fonte: [https://refactoring.guru/pt-br/refactoring](https://refactoring.guru/pt-br/refactoring)
```

---

### **Exemplo 5: Encontrar Soluções para Autenticação com JWT em Node.js**
```
/codesearch "autenticação JWT Node.js"
```
**Resultado esperado:**
```
📚 Autenticação com JWT em Node.js:

1. **Instalação do pacote:**
```bash
npm install jsonwebtoken
```

2. **Código de exemplo:**
```javascript
const jwt = require('jsonwebtoken');

// Chave secreta (deve ser armazenada em variáveis de ambiente!)
const SECRET_KEY = 'sua_chave_secreta';

// Função para gerar um token
function generateToken(user) {
  return jwt.sign({ id: user.id, email: user.email }, SECRET_KEY, { expiresIn: '1h' });
}

// Função para verificar um token
function verifyToken(token) {
  try {
    return jwt.verify(token, SECRET_KEY);
  } catch (error) {
    throw new Error('Token inválido ou expirado');
  }
}

// Uso:
const token = generateToken({ id: 1, email: 'user@example.com' });
const decoded = verifyToken(token);
console.log(decoded); // { id: 1, email: 'user@example.com', iat: ..., exp: ... }
```

🔍 Fonte: [https://www.bezkoder.com/node-js-jwt-authentication/](https://www.bezkoder.com/node-js-jwt-authentication/)
```

---

### **Exemplo 6: Encontrar Exemplos de Testes Unitários com Jest**
```
/codesearch "testes unitários Jest mock axios"
```
**Resultado esperado:**
```
📚 Testes Unitários com Jest e Mock de Axios:

1. **Instalação dos pacotes:**
```bash
npm install --save-dev jest axios
```

2. **Código a ser testado:**
```javascript
// src/api.js
const axios = require('axios');

async function fetchData(url) {
  const response = await axios.get(url);
  return response.data;
}

module.exports = { fetchData };
```

3. **Teste unitário com mock:**
```javascript
// tests/api.test.js
const { fetchData } = require('../src/api');
const axios = require('axios');
const MockAdapter = require('axios-mock-adapter');

const mock = new MockAdapter(axios);

describe('fetchData', () => {
  afterEach(() => {
    mock.reset();
  });

  it('deve retornar dados quando a requisição for bem-sucedida', async () => {
    const mockData = { id: 1, name: 'Test' };
    mock.onGet('https://api.example.com/data').reply(200, mockData);

    const result = await fetchData('https://api.example.com/data');
    expect(result).toEqual(mockData);
  });

  it('deve lançar um erro quando a requisição falhar', async () => {
    mock.onGet('https://api.example.com/data').reply(500);

    await expect(fetchData('https://api.example.com/data')).rejects.toThrow();
  });
});
```

🔍 Fonte: [https://jestjs.io/docs/mock-functions](https://jestjs.io/docs/mock-functions)
```

---

## 🔍 Dicas para Usar o `/codesearch`

1. **Seja específico**: Quanto mais detalhes você fornecer na busca, melhores serão os resultados.
   - ❌ `/codesearch "função JavaScript"`
   - ✅ `/codesearch "função pura JavaScript sem efeitos colaterais"`

2. **Use aspas**: Para buscar frases exatas ou termos compostos.
   - ✅ `/codesearch "design patterns Factory Python"`

3. **Combine termos**: Use operadores lógicos como `AND`, `OR` ou `NOT` (se suportado).
   - ✅ `/codesearch "TypeScript AND validação CPF"`

4. **Busque por bibliotecas específicas**: Se você já sabe qual biblioteca ou framework usar.
   - ✅ `/codesearch "express.js middleware autenticação JWT"`

5. **Busque por padrões de projeto**: Ótimo para refatoração ou aprendizado.
   - ✅ `/codesearch "padrões de projeto Observer JavaScript"`

---

## 🛠️ Solução de Problemas

### **Problema: Nenhum resultado encontrado**
**Solução:**
- Verifique se a ferramenta `/codesearch` está disponível no ambiente.
- Tente usar termos mais genéricos na busca.
- Verifique se o código ou biblioteca que você está buscando está acessível.

---

### **Problema: Resultados irrelevantes**
**Solução:**
- Seja mais específico na busca.
- Use aspas para buscar frases exatas.
- Combine termos com operadores lógicos (se disponíveis).

---

### **Problema: Ferramenta `/codesearch` não encontrada**
**Solução:**
- Verifique se o ambiente suporta a ferramenta (Claude Chat, Copilot Code, Qwen Code).
- Se estiver usando um ambiente local, instale a ferramenta manualmente.

---

## 📚 Referências
- [Documentação do `/codesearch` (se disponível)](https://claude.ai/)
- [Refactoring Guru - Design Patterns](https://refactoring.guru/pt-br/design-patterns)
- [MDN Web Docs - JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [Real Python - Python Tutorials](https://realpython.com/)
---

## Exemplo 7: Encontrar exemplos de classe abstrata em Python (ABC)
```
/codesearch "python abstract class abc example"
```
**Resultado esperado:**
```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        raise NotImplementedError

class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"email: {message}")
```

Validacao sugerida no fluxo Claude:
- `/grep "from abc import ABC" src/`
- `/run-tests`
