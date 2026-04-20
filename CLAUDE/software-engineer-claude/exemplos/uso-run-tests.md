# Exemplos de Uso do `/run-tests`

## Introdução
O `/run-tests` é uma ferramenta poderosa para validar a qualidade do código, executando testes unitários e medindo a cobertura de código. Este guia fornece exemplos práticos de como usá-lo em diferentes cenários.

---

## 📌 Pré-requisitos
- Projeto configurado com um framework de testes (ex: Jest, Mocha, PyTest).
- Ferramenta `/run-tests` disponível no ambiente (Claude Chat, Copilot Code, Qwen Code).

---

## 🚀 Exemplos de Uso

### **Exemplo 1: Executar Todos os Testes**
```
/run-tests
```
**Resultado esperado:**
```
📊 Testes Unitários
✅ 20/20 testes passaram
⏱️ Tempo de execução: 1.2s
📈 Cobertura de código: 85%

🎉 Todos os testes passaram!
```

---

### **Exemplo 2: Executar Testes com Cobertura**
```
/run-tests --coverage
```
**Resultado esperado:**
```
📊 Testes Unitários
✅ 20/20 testes passaram
⏱️ Tempo de execução: 1.2s

📈 Cobertura de Código
- src/auth.js: 100%
- src/utils.js: 80%
- src/api.js: 70%

📉 Arquivos com cobertura baixa:
- src/api.js (70%): Adicione testes para as funções `fetchData` e `postData`.

🎉 Todos os testes passaram, mas a cobertura pode ser melhorada!
```

---

### **Exemplo 3: Executar Testes Específicos**
```
/run-tests src/auth.test.js
```
**Resultado esperado:**
```
📊 Testes Unitários para src/auth.test.js
✅ 5/5 testes passaram
⏱️ Tempo de execução: 0.5s

🎉 Todos os testes específicos passaram!
```

---

### **Exemplo 4: Executar Testes em Modo Verbose**
```
/run-tests --verbose
```
**Resultado esperado:**
```
📊 Testes Unitários (Modo Verbose)

🔹 Teste 1: Validação de Login
✅ PASSOU
   - Entrada: { email: 'user@example.com', password: '123456' }
   - Saída esperada: { success: true, token: 'abc123' }

🔹 Teste 2: Login Inválido
✅ PASSOU
   - Entrada: { email: 'user@example.com', password: 'wrong' }
   - Saída esperada: { success: false, error: 'Invalid credentials' }

⏱️ Tempo de execução: 1.2s
📈 Cobertura de código: 85%

🎉 Todos os testes passaram!
```

---

### **Exemplo 5: Executar Testes e Gerar Relatório em JSON**
```
/run-tests --json
```
**Resultado esperado:**
```json
{
  "totalTests": 20,
  "passedTests": 20,
  "failedTests": 0,
  "executionTime": "1.2s",
  "coverage": {
    "src/auth.js": 100,
    "src/utils.js": 80,
    "src/api.js": 70
  },
  "message": "Todos os testes passaram!"
}
```

---

### **Exemplo 6: Executar Testes e Parar em Caso de Falha**
```
/run-tests --fail-fast
```
**Resultado esperado:**
```
📊 Testes Unitários
❌ 1/5 testes falharam
   - Teste: Validação de Email
   - Erro: Email inválido não foi rejeitado

⏱️ Tempo de execução: 0.3s

🚨 Fail-fast ativado. Parando a execução.
```

---

## 🛠️ Configuração do Ambiente

### **Jest (JavaScript/TypeScript)**
1. Instale o Jest:
   ```bash
   npm install --save-dev jest
   ```

2. Adicione um script no `package.json`:
   ```json
   {
     "scripts": {
       "test": "jest"
     }
   }
   ```

3. Execute os testes:
   ```bash
   npm test
   ```
   Ou diretamente com `/run-tests`.

---

### **Mocha (JavaScript/TypeScript)**
1. Instale o Mocha:
   ```bash
   npm install --save-dev mocha
   ```

2. Adicione um script no `package.json`:
   ```json
   {
     "scripts": {
       "test": "mocha"
     }
   }
   ```

3. Execute os testes:
   ```bash
   npm test
   ```
   Ou diretamente com `/run-tests`.

---

### **PyTest (Python)**
1. Instale o PyTest:
   ```bash
   pip install pytest
   ```

2. Crie testes no diretório `tests/`:
   ```python
   # tests/test_auth.py
   def test_login():
       assert login("user", "password") == {"success": True}
   ```

3. Execute os testes:
   ```bash
   pytest
   ```
   Ou diretamente com `/run-tests`.

---

## 📊 Interpretando os Resultados

| Resultado               | Descrição                                                                 | Ação Recomendada                          |
|-------------------------|---------------------------------------------------------------------------|--------------------------------------------|
| ✅ Todos os testes passaram | Nenhum erro encontrado.                                                  | Prosseguir com confiança.                 |
| ⚠️ Cobertura baixa       | Alguns trechos do código não estão cobertos por testes.                  | Adicione testes para as funções críticas. |
| ❌ Testes falharam       | Um ou mais testes falharam.                                               | Corrigir o código ou os testes.           |
| ⏱️ Execução lenta        | Os testes estão demorando muito para rodar.                              | Otimize os testes ou divida em suítes.    |

---

## 🔧 Solução de Problemas

### **Problema: Ferramenta `/run-tests` não encontrada**
**Solução:**
- Verifique se o ambiente suporta a ferramenta (Claude Chat, Copilot Code, Qwen Code).
- Se estiver usando um ambiente local, instale a ferramenta manualmente.

---

### **Problema: Testes falham aleatoriamente**
**Solução:**
- Verifique se os testes são **determinísticos** (mesma entrada sempre produz mesma saída).
- Evite dependências externas nos testes (ex: chamadas a APIs, acesso a banco de dados).
- Use **mocks** para simular dependências.

---

### **Problema: Cobertura de código muito baixa**
**Solução:**
- Adicione testes para as funções ou módulos com baixa cobertura.
- Use ferramentas como `Istanbul` (JavaScript) ou `Coverage.py` (Python) para medir a cobertura.
- Priorize testes para funções críticas (ex: autenticação, validação de entrada).

---

## 📚 Referências
- [Documentação do Jest](https://jestjs.io/)
- [Documentação do Mocha](https://mochajs.org/)
- [Documentação do PyTest](https://docs.pytest.org/)
- [Claude Chat - Ferramentas](https://claude.ai/)