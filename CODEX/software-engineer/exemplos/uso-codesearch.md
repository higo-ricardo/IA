# Exemplos de uso no Codex para busca de codigo

## Exemplo 1: localizar uso de eval
```powershell
rg "eval\(" src
```

## Exemplo 2: localizar padrao de validacao de CPF
```powershell
rg -n "cpf|validateCPF|validarCPF" src
```

## Exemplo 3: localizar design patterns em TypeScript
```powershell
rg -n "Factory|Singleton|Observer" -g "*.ts" -g "*.tsx" src
```

## Observacao
Use `rg --files` para mapear arquivos antes da busca textual.
