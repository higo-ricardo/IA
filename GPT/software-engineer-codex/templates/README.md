# Templates da Skill `software-engineer-codex`

Este diretorio e o indice de templates para uso no fluxo da skill no GPT Codex.

## Estado atual
Atualmente, esta pasta contem os seguintes templates reais:
- `templates/README.md`
- `templates/criacao/classe-abstrata-python.py`
- `templates/manutencao/template-manutencao.md`
- `templates/analise/template-analise.md`
- `templates/analise/contrato-dashboard-handoff.json`
- `templates/analise/validacao-dashboard-handoff.md`
- `templates/refatoracao/template-refatoracao.md`

## Como usar no estado atual
1. Defina o modo operacional (CRIACAO, MANUTENCAO, ANALISE, REFATORACAO).
2. Use os exemplos em `../exemplos/` para guiar busca, validacao e testes.
3. Parta dos templates existentes e adapte apenas o necessario.

## Convencao para novos templates
Quando criar templates nesta pasta, usar estrutura minima:
- `templates/criacao/`
- `templates/manutencao/`
- `templates/analise/`
- `templates/refatoracao/`

Cada template novo deve incluir:
- objetivo do arquivo
- entrada e saida esperadas
- comandos de validacao aplicaveis
- exemplo curto de uso
