# Áreas Jurídicas — Referência de Classificação

Leia este arquivo quando a tarefa envolver extração ou classificação de questões
jurídicas por matéria/área do direito.

---

## Sistema de Pontuação

A classificação usa score de relevância:
- **+2 pontos** por keyword encontrada no texto da questão
- **+10 pontos** por header de seção encontrado (`DIREITO TRIBUTÁRIO`, etc.)
- **Score mínimo:** 3 para ser classificada (filtra questões sem contexto suficiente)

Questões abaixo do score mínimo ficam **sem classificação** (não são salvas em nenhuma área).

---

## Áreas Configuradas

### 1. Direito Tributário (`direito_tributario`)

**Headers detectados:** `DIREITO TRIBUTARIO`, `TRIBUTARIO`, `DIREITO TRIBUTÁRIO`

**Keywords (peso +2 cada):**
`icms`, `iptu`, `iss`, `ipva`, `ipi`, `ir`, `cofins`, `pis`, `csll`,
`ctn`, `tributario`, `tributário`, `imposto`, `tributo`, `fisco`,
`contribuinte`, `lançamento`, `obrigação tributária`

**Arquivo de saída:** `questoes_direito_tributario.md`

---

### 2. Direito Administrativo (`direito_administrativo`)

**Headers detectados:** `DIREITO ADMINISTRATIVO`, `ADMINISTRATIVO`

**Keywords:**
`licitacao`, `licitação`, `servidor publico`, `servidor público`,
`improbidade`, `concurso`, `autarquia`, `fundação pública`,
`ato administrativo`, `poder de polícia`, `administração pública`,
`lei 8112`, `lei 8666`, `lei 14133`

**Arquivo de saída:** `questoes_direito_administrativo.md`

---

### 3. Direito Civil (`direito_civil`)

**Headers detectados:** `DIREITO CIVIL`, `CIVIL`

**Keywords:**
`codigo civil`, `código civil`, `contratos`, `obrigacoes`, `obrigações`,
`familia`, `família`, `propriedade`, `posse`, `usucapião`,
`sucessões`, `responsabilidade civil`, `dano moral`

**Arquivo de saída:** `questoes_direito_civil.md`

---

### 4. Direito Penal (`direito_penal`)

**Headers detectados:** `DIREITO PENAL`, `PENAL`

**Keywords:**
`codigo penal`, `código penal`, `crime`, `pena`, `homicidio`, `homicídio`,
`furto`, `roubo`, `estelionato`, `peculato`, `corrupção`,
`lavagem de dinheiro`, `tráfico`, `reclusão`

**Arquivo de saída:** `questoes_direito_penal.md`

---

### 5. Direito Processual (`processual`)

**Headers detectados:** `PROCESSO`, `PROCESSUAL`, `CPC`, `CPP`

**Keywords:**
`recurso`, `apelacao`, `apelação`, `embargos`, `sentenca`, `sentença`,
`liminar`, `tutela`, `mandado de segurança`, `habeas corpus`,
`agravo`, `cpc`, `cpp`, `prazo processual`

**Arquivo de saída:** `questoes_processual.md`

---

## Padrão de Detecção de Questões

```regex
(?:QUESTAO|Quest[^\d]+|QUESTÃO|Item|item|^\s*\d+[\.\)\-])\s*(\d+)
```

Detecta formatos como:
- `Questão 01`, `QUESTÃO 1`, `Quest. 15`
- `Item 3`, `item 42`
- `1.`, `2)`, `3-` no início da linha

---

## Filtros de Qualidade

Questões são **descartadas** se:
- Menos de **50 caracteres** (provavelmente fragmento ou header)
- Mais de **10.000 caracteres** (provavelmente documento inteiro mal delimitado)

---

## Adicionar Nova Área

Para adicionar uma nova área jurídica ao pipeline, edite o dicionário `AREAS`
em `scripts/md_cleaner.py`:

```python
AREAS["direito_constitucional"] = {
    "titulo": "Direito Constitucional",
    "headers": ["DIREITO CONSTITUCIONAL", "CONSTITUCIONAL"],
    "keywords": [
        "constituição", "direitos fundamentais", "mandado de segurança",
        "ação direta", "controle de constitucionalidade", "stf"
    ],
}
```

---

## Formato dos Arquivos de Saída

```markdown
# Direito Tributário

> Extraídas automaticamente pelo Markdown Cleaner

---

## nome_do_arquivo_original.md

### Questão 01

[texto completo da questão]

---
```
