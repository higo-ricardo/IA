# Checklist de Segurança Expandido — Code Reviewer PT

Use este arquivo quando o nível for L4/L5 ou quando a revisão tiver foco explícito em segurança.

---

## Checklist Universal (todos os níveis ≥ L2)

### Entradas
- [ ] Todos os inputs externos são validados antes do uso?
- [ ] Valores de tamanho/comprimento têm limite máximo?
- [ ] Inputs numéricos verificam overflow/underflow?
- [ ] Uploads de arquivo validam tipo MIME e tamanho?

### Autenticação e Autorização
- [ ] Toda rota/endpoint sensível verifica autenticação?
- [ ] Verificação de permissão é explícita (não apenas "se chegou aqui, está autorizado")?
- [ ] Tokens têm expiração definida?
- [ ] Refresh tokens são rotativos?
- [ ] Falha de auth retorna 401/403 (não 200 com mensagem de erro)?

### Dados em Trânsito e Repouso
- [ ] Senhas são armazenadas com hash + salt (bcrypt, argon2, scrypt)?
- [ ] Dados sensíveis não aparecem em URLs (query string)?
- [ ] Cookies sensíveis têm `HttpOnly`, `Secure`, `SameSite`?
- [ ] HTTPS é enforçado (sem fallback para HTTP)?

### Secrets e Configuração
- [ ] Zero secrets no código-fonte ou arquivos versionados?
- [ ] `.env` está no `.gitignore`?
- [ ] Chaves de prod são diferentes das de dev/staging?
- [ ] Secrets são rotacionados periodicamente?

### Erros e Logs
- [ ] Mensagens de erro para o cliente são genéricas (não vazam stack trace)?
- [ ] Stack traces vão apenas para logs internos?
- [ ] Logs não contêm PII, senhas ou tokens?
- [ ] Rate limiting existe em endpoints de autenticação?

---

## Checklist por Paradigma

### Web (HTTP APIs)

- [ ] CORS configurado com origens explícitas (não `*` em prod)?
- [ ] CSRF protection em endpoints que modificam estado (se cookie-based auth)?
- [ ] Headers de segurança presentes: `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`?
- [ ] SQL/NoSQL queries usam prepared statements ou ORM seguro?
- [ ] Respostas de lista têm paginação (não retornam todos os registros)?
- [ ] IDs expostos na API são opacos (UUID) ou ao menos não sequenciais em recursos sensíveis?

### Banco de Dados

- [ ] Usuário do banco tem apenas permissões necessárias (princípio do menor privilégio)?
- [ ] Backups são testados regularmente?
- [ ] Migrations são reversíveis?
- [ ] Conexões usam SSL?

### Frontend (JavaScript/TypeScript)

- [ ] `innerHTML` com dado externo sanitizado via DOMPurify ou equivalente?
- [ ] `eval()` ausente (ou justificado com sandboxing)?
- [ ] Dependências verificadas com `npm audit` / `yarn audit`?
- [ ] Content Security Policy configurada?
- [ ] Dados sensíveis não armazenados em `localStorage` sem criptografia?

### Mobile (iOS/Android)

- [ ] Certificate pinning implementado para APIs críticas?
- [ ] Keychain/Keystore usado para dados sensíveis (não SharedPreferences/UserDefaults)?
- [ ] Jailbreak/root detection para apps financeiros?
- [ ] Dados sensíveis não logados no console de debug?

### Sistemas (Rust/Go/C/C++)

- [ ] Buffer bounds verificados explicitamente?
- [ ] Input de rede tem tamanho máximo definido?
- [ ] Ponteiros/referências nulas têm proteção?
- [ ] Recursos (arquivos, conexões, memória) liberados em todos os caminhos de erro?

### Infraestrutura / Scripts

- [ ] Scripts não expõem credenciais em argumentos CLI (visíveis em `ps aux`)?
- [ ] Permissões de arquivo são restritivas (não 777)?
- [ ] Dependências externas têm versão pinada?
- [ ] Imagens Docker não rodam como root?

---

## Matriz de Severidade por Contexto

| Vetor | App Interno (L3) | API Pública (L4) | Finanças/Saúde (L5) |
|---|---|---|---|
| SQL Injection | 🔴 Crítico | 🔴 Crítico | 🔴 Crítico + bloqueante |
| Auth bypass | 🔴 Crítico | 🔴 Crítico | 🔴 Crítico + bloqueante |
| Secret hardcoded | 🔴 Crítico | 🔴 Crítico | 🔴 Crítico + bloqueante |
| XSS stored | 🟡 Importante | 🔴 Crítico | 🔴 Crítico |
| XSS reflected | ⚪ Omitir | 🟡 Importante | 🔴 Crítico |
| Log de PII | 🟡 Importante | 🔴 Crítico | 🔴 Crítico |
| CORS permissivo | ⚪ Omitir | 🟡 Importante | 🔴 Crítico |
| Falta de rate limiting | ⚪ Omitir | 🟡 Importante | 🟡 Importante |
| Dependência com CVE | 🟡 Importante | 🔴 Crítico | 🔴 Crítico |
