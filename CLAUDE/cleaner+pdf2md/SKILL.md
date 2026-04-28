---
name: markdown-cleaner
description: >
  Pipeline completo de limpeza, normalização e processamento de documentos Markdown em português.
  Use esta skill SEMPRE que o usuário quiser: limpar ou normalizar arquivos .md, corrigir encoding
  de documentos (UTF-8, Latin-1, CP1252), remover espaços duplos/triplos ou linhas em branco
  excessivas, extrair e classificar questões jurídicas por área do direito, validar consistência
  de numerais (súmulas, artigos, parágrafos, incisos) em documentos Markdown, processar lotes de
  arquivos .md de uma pasta, gerar relatórios de qualidade de documentos. Ative também para:
  "limpar meu markdown", "corrigir caracteres estranhos", "encoding quebrado", "caracteres
  embaralhados", "organizar questões por matéria", "extrair questões do meu arquivo", "validar
  súmulas", "normalizar documento", "processar meus .md".
---

# Markdown Cleaner — Skill de Processamento de Documentos

Pipeline modular para limpeza, correção de encoding, validação e extração de conteúdo em documentos Markdown jurídicos e gerais em português.

---

## Arquitetura da Skill

```
md-cleaner-skill/
├── SKILL.md                  ← este arquivo (roteador + visão geral)
├── scripts/
│   ├── md_cleaner.py         ← pipeline principal (limpeza + extração + encoding)
│   └── md_validator.py       ← validador de numerais e consistência
└── references/
    ├── encoding_guide.md     ← referência: mapeamento de caracteres e estratégias
    └── areas_juridicas.md    ← referência: áreas, keywords e padrões de classificação
```

**Regra de carregamento:**
- Leia `references/encoding_guide.md` se a tarefa envolve caracteres quebrados, encoding ou pt-BR corrompido
- Leia `references/areas_juridicas.md` se a tarefa envolve classificação ou extração de questões jurídicas
- Execute `scripts/md_cleaner.py` para pipeline de limpeza/extração em lote
- Execute `scripts/md_validator.py` para validação de numerais e consistência

---

## Capacidades Disponíveis

| Módulo | Funcionalidade | Quando usar |
|---|---|---|
| **Limpeza Geral** | Remove espaços duplos/triplos, linhas em branco excessivas, caracteres de controle, trailing whitespace, BOM | Normalizar qualquer .md |
| **Correção de Encoding** | Detecta e corrige UTF-8, Latin-1, CP1252, ISO-8859-1; repara pt-BR corrompido (ã, ç, á, é...) | Caracteres embaralhados ou `â`, `Ã`, `\x82` no texto |
| **Limpeza Markdown** | Normaliza headers (#), remove espaços antes de `**bold**`, padroniza listas, corrige links quebrados `[]()` | Markdown mal formatado |
| **Extração de Questões** | Extrai questões numeradas de arquivos .md e classifica por área jurídica | Banco de questões misturado |
| **Classificação Jurídica** | Distribui questões entre tributário, administrativo, civil, penal, processual | Organizar questões por matéria |
| **Validação de Numerais** | Verifica consistência de súmulas, artigos, parágrafos, incisos entre sumário e seções | Documentos com numeração inconsistente |
| **Processamento em Lote** | Processa todos os .md de uma pasta em pipeline de duas fases | Limpeza de diretório inteiro |

---

## Fluxo de Decisão

```
Usuário pede processamento de Markdown
         │
         ├─ Caracteres embaralhados / encoding?
         │      └─ Leia encoding_guide.md → use módulo EncodingDetector
         │
         ├─ Questões jurídicas / classificar por matéria?
         │      └─ Leia areas_juridicas.md → use módulo QuestionProcessor
         │
         ├─ Validar súmulas / artigos / numerais?
         │      └─ Use scripts/md_validator.py com padrão adequado
         │
         ├─ Limpeza geral (espaços, linhas, formatação)?
         │      └─ Use MarkdownCleaner diretamente (sem arquivos externos)
         │
         └─ Tudo junto / lote de arquivos?
                └─ Use PipelineOrchestrator em duas fases
```

---

## Como Executar

### Limpeza geral de um diretório:
```bash
python scripts/md_cleaner.py /caminho/para/pasta
```

### Limpeza com relatório JSON:
```bash
python scripts/md_cleaner.py /caminho/para/pasta --relatorio relatorio.json
```

### Validação de numerais:
```bash
# Auto-detectar todos os .md
python scripts/md_validator.py --auto

# Validar padrão específico
python scripts/md_validator.py --pattern sumulas arquivo.md

# Gerar relatório JSON
python scripts/md_validator.py --auto --format json -o relatorio.json

# Modo correção (reescreve com encoding corrigido)
python scripts/md_validator.py --fix arquivo.md
```

---

## Limpezas Realizadas pelo Pipeline

O `MarkdownCleaner` aplica as seguintes transformações, nesta ordem:

1. **Encoding** → detecta e corrige cp1252/latin-1/UTF-8 corrompido
2. **BOM** → remove `\ufeff` do início do arquivo
3. **CRLF → LF** → normaliza quebras de linha Windows
4. **Caracteres de controle** → remove `\x00-\x08`, `\x0b`, `\x0c`, `\x0e-\x1f`
5. **Espaços duplos/triplos** → `" +"` → `" "` (preserva indentação de código)
6. **Espaços ao final de linha** → trailing whitespace removido
7. **Linhas em branco excessivas** → máximo 2 consecutivas permitidas
8. **Espaço antes de pontuação** → `" ,"` `" ."` `" ;"` → normalizado
9. **Headers Markdown** → garante espaço após `#` (`##Titulo` → `## Titulo`)
10. **Negrito/itálico** → remove espaços internos `** texto **` → `**texto**`
11. **Links quebrados** → detecta `[texto]()` vazio e sinaliza
12. **Linhas em branco finais** → uma única `\n` no final do arquivo

---

## Notas de Implementação

- Todos os arquivos de saída são salvos em **UTF-8** independentemente do encoding original
- Arquivos gerados por extração de questões seguem o padrão `questoes_{area}.md`
- Arquivos limpos recebem sufixo `_limpo.md` por padrão (configurável)
- O pipeline **nunca sobrescreve** o arquivo original; sempre cria cópia
- Questões com menos de 50 ou mais de 10.000 caracteres são ignoradas na extração
- Classificação jurídica requer score ≥ 3 (2 pts/keyword + 10 pts/header de seção)
