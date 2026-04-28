# Exemplos de uso no Codex para busca de risco

## Exemplo 1: localizar possivel segredo hardcoded
```powershell
rg -n -i "password|senha|secret|token" src
```

## Exemplo 2: localizar SQL concatenado
```powershell
rg -n "SELECT.*\+|\+.*SELECT|query\s*=\s*\"" src
```

## Exemplo 3: localizar console.log em producao
```powershell
rg -n "console\\.log" src -g "!**/tests/**"
```

## Exemplo 4: localizar uso de any em TypeScript
```powershell
rg -n "\bany\b" src -g "*.ts" -g "*.tsx"
```
