# Exemplos de Uso do `/grep`

## Introdução
O `/grep` é uma ferramenta poderosa para **buscar padrões de texto** em arquivos, como **código-fonte**, **logs**, **configurações** e **documentação**. Este guia fornece exemplos práticos de como usá-lo para identificar **riscos de segurança**, **padrões de código problemáticos**, **boas práticas** e muito mais.

---

## 📌 Pré-requisitos
- Ferramenta `/grep` disponível no ambiente (Claude Chat, Copilot Code, Qwen Code).
- Acesso a uma base de código ou diretório com arquivos de texto.

---

## 🚀 Exemplos de Uso

### **Exemplo 1: Buscar por Uso de `eval` (Risco de Segurança)**
```
/grep "eval(" src/
```
**Resultado esperado:**
```
🔍 Arquivos com uso de `eval` (risco de segurança):
- src/unsafe.js: linha 42 → eval(userInput);
- src/legacy.js: linha 15 → eval(config.dynamicCode);

⚠️ Risco identificado: Uso de `eval` pode permitir injeção de código malicioso!
🔧 Sugestão: Substituir por funções seguras ou bibliotecas de sanitização.
```

---

### **Exemplo 2: Buscar por Senhas em Plaintext (Risco de Segurança)**
```
/grep -i "password\|senha\|secret" src/
```
**Resultado esperado:**
```
🔍 Arquivos com possíveis senhas em plaintext:
- src/config.js: linha 5 → const password = "123456";
- src/database.js: linha 10 → db.connect("user:admin,pass:admin123");

⚠️ Risco identificado: Senhas armazenadas em plaintext!
🔧 Sugestão: Usar variáveis de ambiente ou um gerenciador de segredos.
```

---

### **Exemplo 3: Buscar por SQL Injection (Risco de Segurança)**
```
/grep -i "concat\|+.*select\|'.*\+" src/
```
**Resultado esperado:**
```
🔍 Arquivos com possíveis vulnerabilidades de SQL Injection:
- src/users.js: linha 20 → query = "SELECT * FROM users WHERE name = '" + userName + "'";

⚠️ Risco identificado: Concatenção direta de entrada do usuário em queries SQL!
🔧 Sugestão: Usar prepared statements ou ORMs (ex: Sequelize, TypeORM).
```

---

### **Exemplo 4: Buscar por Uso de `console.log` em Código de Produção**
```
/grep "console\.log" src/ --exclude-dir=tests
```
**Resultado esperado:**
```
🔍 Arquivos com `console.log` em código de produção:
- src/api.js: linha 45 → console.log("Request received:", req.body);
- src/utils.js: linha 12 → console.log("Calculating total:", total);

⚠️ Aviso: `console.log` pode expor dados sensíveis ou afetar performance!
🔧 Sugestão: Remover ou substituir por um logger configurável (ex: Winston, Pino).
```

---

### **Exemplo 5: Buscar por Funções Não Utilizadas (Dead Code)**
```
/grep -r "function [a-zA-Z_][a-zA-Z0-9_]*(" src/ | grep -v "export\|import"
```
**Resultado esperado:**
```
🔍 Funções não exportadas ou não utilizadas:
- src/utils.js: linha 30 → function oldHelper() { ... }
- src/legacy.js: linha 5 → function deprecatedFunction() { ... }

⚠️ Aviso: Código morto pode aumentar a complexidade e dificultar a manutenção!
🔧 Sugestão: Remover ou documentar funções não utilizadas.
```

---

### **Exemplo 6: Buscar por Importação de Bibliotecas Inseguras**
```
/grep "require.*eval\|require.*child_process\|import.*child_process" src/
```
**Resultado esperado:**
```
🔍 Arquivos com importação de bibliotecas potencialmente inseguras:
- src/setup.js: linha 3 → const { exec } = require('child_process');

⚠️ Risco identificado: `child_process` pode executar comandos arbitrários no sistema!
🔧 Sugestão: Validar entrada do usuário e restringir permissões.
```

---

### **Exemplo 7: Buscar por Comentários Temporários ou Depuradores**
```
/grep -r "TODO\|FIXME\|DEBUG\|HACK\|XXX" src/
```
**Resultado esperado:**
```
🔍 Comentários temporários ou depuradores:
- src/api.js: linha 60 → // TODO: Validar token JWT
- src/auth.js: linha 25 → // DEBUG: console.log(token)
- src/utils.js: linha 40 → // HACK: Ignorar erro de validação

🔧 Sugestão: Resolver ou documentar os itens marcados como TODO/FIXME.
```

---

### **Exemplo 8: Buscar por Configurações de Ambiente Padrão**
```
/grep -i "localhost\|127\.0\.0\.1\|test\|dev\|staging" .env*
```
**Resultado esperado:**
```
🔍 Configurações de ambiente com valores padrão:
- .env: linha 5 → DB_HOST=localhost
- .env.example: linha 3 → API_URL=http://127.0.0.1:3000

⚠️ Aviso: Configurações padrão podem ser inseguras em produção!
🔧 Sugestão: Sempre sobrescrever valores padrão em ambientes de produção.
```

---

### **Exemplo 9: Buscar por Uso de `any` em TypeScript (Tipo Inseguro)**
```
/grep "any" src/ --include="*.ts" --include="*.tsx"
```
**Resultado esperado:**
```
🔍 Arquivos TypeScript com uso de `any`:
- src/types.ts: linha 10 → let data: any = fetchData();

⚠️ Aviso: Uso de `any` desativa a verificação de tipos do TypeScript!
🔧 Sugestão: Usar tipos específicos ou genéricos para melhorar a segurança e manutenção.
```

---

### **Exemplo 10: Buscar por Linhas Muito Longas (Acima de 80 caracteres)**
```
/grep -r ".\{81,\}" src/ --include="*.js" --include="*.ts"
```
**Resultado esperado:**
```
🔍 Linhas com mais de 80 caracteres:
- src/utils.js: linha 15 → const longFunctionName = (param1, param2, param3, param4) => { ... }

⚠️ Aviso: Linhas muito longas podem dificultar a leitura e manutenção!
🔧 Sugestão: Reformatar o código para quebrar linhas longas.
```

---

## 🔍 Dicas para Usar o `/grep`

1. **Buscas simples**: Use palavras-chave ou padrões básicos.
   - ✅ `/grep "password" src/`

2. **Buscas com expressões regulares**: Use padrões avançados para encontrar estruturas específicas.
   - ✅ `/grep -r "function [a-zA-Z_][a-zA-Z0-9_]*(" src/`

3. **Buscas recursivas**: Use a flag `-r` para buscar em subdiretórios.
   - ✅ `/grep -r "eval(" .`

4. **Excluir diretórios**: Use `--exclude-dir` para ignorar pastas como `node_modules` ou `tests`.
   - ✅ `/grep "console.log" src/ --exclude-dir=tests`

5. **Buscas case-insensitive**: Use a flag `-i` para ignorar maiúsculas/minúsculas.
   - ✅ `/grep -i "password\|senha" src/`

6. **Buscas por tipo de arquivo**: Use `--include` para buscar apenas em arquivos específicos.
   - ✅ `/grep "any" src/ --include="*.ts"`

7. **Buscas por tamanho de linha**: Use expressões regulares para encontrar linhas muito longas ou curtas.
   - ✅ `/grep -r ".\{120,\}" src/` (linhas com mais de 120 caracteres)

8. **Buscas por padrões complexos**: Combine múltiplas expressões regulares.
   - ✅ `/grep -r "SELECT.*FROM.*WHERE.*\+" src/` (SQL Injection)

---

## 🛠️ Solução de Problemas

### **Problema: Nenhum resultado encontrado**
**Solução:**
- Verifique se o padrão de busca está correto.
- Tente usar uma expressão regular mais simples.
- Verifique se o diretório ou arquivo existe.

---

### **Problema: Muitos resultados (overload de informações)**
**Solução:**
- Seja mais específico no padrão de busca.
- Use flags como `--include` ou `--exclude-dir` para limitar o escopo.
- Combine múltiplas buscas para refinar os resultados.

---

### **Problema: Ferramenta `/grep` não encontrada**
**Solução:**
- Verifique se o ambiente suporta a ferramenta (Claude Chat, Copilot Code, Qwen Code).
- Se estiver usando um ambiente local, instale o `grep` manualmente:
  - **Linux/macOS**: Geralmente já está instalado.
  - **Windows**: Instale via [Git Bash](https://git-scm.com/) ou [WSL](https://learn.microsoft.com/pt-br/windows/wsl/install).

---

### **Problema: Busca muito lenta**
**Solução:**
- Limite o escopo da busca (ex: `--include="*.js"`).
- Exclua diretórios desnecessários (ex: `--exclude-dir=node_modules`).
- Use ferramentas mais rápidas como `ripgrep` (rg) ou `ag` (se disponível).

---

## 📚 Referências
- [Manual do `grep`](https://www.gnu.org/software/grep/manual/)
- [Expressões Regulares - MDN](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Guide/Regular_Expressions)
- [Guia de Segurança em Node.js](https://nodejs.org/en/docs/guides/security)
- [OWASP - SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [TypeScript - Tipos Seguros](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html)