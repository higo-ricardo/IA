# 📝 Simulador de Prova — Área Jurídica

> **Skill para simulação interativa de provas e questões de concurso na área jurídica.**
> Timer configurável, 4 níveis de dificuldade, feedback pedagógico em 3 campos, 6 formatos de questão, correção por espelho e relatório de desempenho com diagnóstico por faixas.

| Metadado | Valor |
|----------|-------|
| **Nome** | `simulador-prova` |
| **Versão** | 2.0.0 |
| **Autor** | Higo Ricardo |
| **Foco** | Área jurídica geral (Civil, Tributário, Administrativo, etc.) |
| **Arquitetura** | Modular — core orquestrador + 8 módulos externos carregados sob demanda |
| **Modos** | Simulado interativo |

---

## 🎯 Propósito

Simular um **exame real** do início ao fim: configuração interativa, timer (real ou estimado), uma questão por vez, feedback configurável, política de desistência com relatório parcial e gabarito final com métricas separadas para objetivas e discursivas.

---

## 📋 Fluxo de Configuração (7 passos)

```
Passo 1 → Disciplina
Passo 2 → Nível (Básico | Intermediário | Avançado | Sênior)
Passo 3 → Nº de questões (padrão: 10)
Passo 4 → Tempo por questão (s) (padrão: 60s | 120s para discursivas)
Passo 5 → Feedback (com / sem)
Passo 6 → Tipo de questão (A–F)
Passo 7 → Material de estudo (opcional)
→ Prova começa
```

---

## 🎓 4 Níveis de Dificuldade

| Nível | Fórmula de Geração | Fontes |
|-------|-------------------|--------|
| **Básico** | Conceito + Definição Legal + Distrator Simples | Sem busca externa |
| **Intermediário** | Caso + Norma + Verberte + 3 Distratores | `web_fetch` + súmulas |
| **Avançado** | Caso Complexo + Norma Literal + Doutrina + Jurisprudência + 4 Distratores | `web_fetch` + súmulas |
| **Sênior** | Conflito Normativo + Doutrina Divergente + Redação Literal + 4 Distratores | `web_fetch` multi-URLs + súmulas |

---

## 🧩 6 Formatos de Questão

| # | Formato | Exemplo de uso |
|---|---------|----------------|
| 1 | **Certo / Errado** | Afirmativa para julgamento binário |
| 2 | **Múltipla Escolha (A–E)** | Enunciado com 5 alternativas |
| 3 | **Tipo A (Proposições)** | Itens I, II, III com combinação de corretas |
| 4 | **Exceto / Incorreto** | "Assinale a alternativa INCORRETA" |
| 5 | **Discursiva** | Resposta livre — corrigida por espelho |
| 6 | **Estudo de Caso** | Narrativa de situação-problema com perguntas aplicadas |

> **Variação automática**: não repete o mesmo formato em questões consecutivas.

---

## ⏱️ Controle de Tempo

| Cenário | Comportamento |
|---------|---------------|
| **Timer disponível** | Python `datetime.now()` → `T0` no início, `Tmédio = (TFim − T0) / N` |
| **Fallback** | Estimativa por troca de mensagens (30–90s). Indicar "(estimado)" no relatório. |

Exibir `⏱️ ref. [T]s` em cada questão.

---

## ✅ Correção e Feedback

### Questões Objetivas (Formatos 1–4)

| Modo | Comportamento |
|------|---------------|
| **COM feedback** | 3 campos: **Fundamento** + **Por que errou** + **Insight** |
| **SEM feedback** | "Resposta registrada" → gabarito só no final |

### Questões Discursivas e Estudo de Caso (Formatos 5–6)

Correção por **espelho de resposta** com 4 critérios ponderados:

| Critério | Peso | Pergunta |
|----------|------|----------|
| Conceito-chave | 30% | Mencionou o princípio/conceito central? |
| Fundamento legal/doutrinário | 30% | Citou norma, artigo, lei ou doutrina? |
| Raciocínio aplicado | 25% | Aplicou ao caso de forma lógica? |
| Clareza e estrutura | 15% | Resposta organizada e com linguagem técnica? |

#### Regras de Correção

| Situação | Regra |
|----------|-------|
| Sem fundamento legal citado | Máximo 8/10 (nunca 10) |
| Esforço argumentativo | Mínimo 2/10 |
| Em branco | 0/10 |
| Fora do tema | 1/10 |

---

## 📊 Confidence Score

Exibido em **todas** as questões antes do enunciado:

| Score | Significado |
|-------|-------------|
| 9–10 | Extraída do material ou conhecimento consolidado sólido |
| 7–8 | Bem fundamentada com pequena inferência |
| < 7 | **Nunca exibida** — reformular ou substituir |

---

## 🎯 6 Técnicas de Distratores

| Técnica | Exemplo |
|---------|---------|
| **Inversão de polo** | "credor" por "devedor" |
| **Falso absoluto** | "sempre" onde há exceções |
| **Troca de prazo** | 5 anos por 3 anos |
| **Norma próxima** | art. 186 por art. 187 |
| **Súmula revogada** | indicar como vigente |
| **Terminologia errada** | "nulidade" por "anulabilidade" |

**Regras**: nenhum absurdo óbvio; gabarito aleatório A–E; máx. 1 técnica repetida por questão.

---

## 🛑 Comandos do Usuário Durante a Prova

| Comando | Ação |
|---------|------|
| `PARAR`, `ENCERRAR`, `DESISTIR` | Encerrar prova → relatório parcial |
| `PULAR`, `PRÓXIMA` | Pular questão atual → próxima |
| `REINICIAR`, `RECOMEÇAR` | Descartar progresso → recomeçar do zero |

### Política de Desistência

1. Confirmação obrigatória: `"CONFIRMAR" para encerrar`
2. Se confirmar → **Relatório Parcial**
3. Se voltar atrás → retoma sem penalidade
4. Se nenhuma respondida → "Não há dados para relatório parcial"

---

## 📈 Relatórios de Desempenho

### Resultado Final (prova completa)

```
📋 RESULTADO FINAL
├─ GABARITO: Q01 ✅/❌ | Q02 📝 Nota X/10 | ...
├─ DESEMPENHO OBJETIVAS: Acertos N/total (%) | Erros N/total (%)
├─ DESEMPENHO DISCURSIVAS: Média X/10 | Melhor Q[N] | Menor Q[N]
├─ DESEMPENHO GERAL: Tempo médio/q | Tempo total
└─ DIAGNÓSTICO: Fortes (≥70%), Atenção (40-69%), Crítico (<40%)
```

### Resultado Parcial (desistência)

```
📋 RESULTADO PARCIAL (Prova encerrada)
├─ GABARITO PARCIAL: respondidas ✅/❌/📝 | não respondidas —
├─ DESEMPENHO OBJETIVAS: Acertos/Erros sobre respondidas
├─ DESEMPENHO DISCURSIVAS: Média das notas
├─ DESEMPENHO GERAL: Não respondidas | Tempo médio/total
└─ OPÇÕES: 1→Retomar | 2→Recomeçar | 3→Mudar disciplina
```

---

## 📚 Fontes Normativas Consultadas

> Todas as URLs estão em `fontes.md` — carregado sob demanda.

| Área | Temas Cobertos |
|------|---------------|
| **Constitucional** | CF/88, ADPF, ADC, ADI, Mandado de Injunção |
| **Civil** | Código Civil, LINDB, Estatuto PcD, Registros Públicos |
| **Processo Civil** | CPC/15, Mandado de Segurança |
| **Tributário** | CTN, EC 132/2023 (IBS/CBS), Lei Kandir, Execução Fiscal |
| **Administrativo** | Lei 9.784/99, Improbidade, LAI, LRF, Licitações (14.133/21) |
| **Penal** | CP, Organizações Criminosas, Lavagem, Crimes Hediondos, Abuso de Autoridade |
| **Processo Penal** | CPP, Tribunal do Júri |
| **Contabilidade** | CPCs, NBCs TA, Lei das S.A., NBC TSP 34 |

### Súmulas e Jurisprudência

| Arquivo | Conteúdo |
|---------|----------|
| `VerbetesSTF.md` | Súmulas do STF (1–739) |
| `VerbetesSTJ.md` | Súmulas do STJ (1–679) |
| `SumulasVinculantes.md` | Súmulas Vinculantes do STF (1–115) |

**Prioridade**: Material do usuário > `fontes.md` + súmulas > Conhecimento + inferência (50/50)

---

## 🔀 Comparação com simulador_AI_provasSEFAZ

| Dimensão | provasJURIDICAS (modular) | provasSEFAZ |
|----------|:---:|:---:|
| UX do usuário final | ⭐ 9.0 | ⭐ 7.0 |
| Versatilidade funcional | ⭐ 8.0 | ⭐ 9.5 |
| Arquitetura/manutenibilidade | ⭐ 9.5 | ⭐ 9.0 |
| Robustez/fallbacks | ⭐ 9.0 | ⭐ 7.0 |
| Métricas e diagnóstico | ⭐ 9.0 | ⭐ 5.0 |
| System Prompt | ✅ ~7.9k chars | ❌ > 8k |
| **MÉDIA** | **8.9** | **7.5** |

> **provasJURIDICAS** = treinar (experiência de prova real)
> **provasSEFAZ** = produzir material (gerar e converter questões)
> **São complementares, não concorrentes.**

---

## 📊 Avaliação por Critérios

| Critério | Nota (0–10) |
|----------|:-----------:|
| Estrutura e Organização | 9.5 |
| Especificidade e Determinismo | 9.0 |
| Interatividade e UX | 9.0 |
| Robustez e Tratamento de Erros | 9.0 |
| Precisão e Controle de Qualidade | 9.5 |
| Mensuração e Relatório | 9.0 |
| Escopo e Abrangência | 9.0 |
| Manutenibilidade e Reusabilidade | 9.5 |
| Otimização de System Prompt | 7.5 |
| **MÉDIA GERAL** | **9.0** |

### Pontos Fortes
- ✅ Arquitetura modular com **8 módulos** carregados sob demanda
- ✅ **4 níveis de dificuldade** com fórmulas de geração distintas
- ✅ **6 formatos** de questão com variação automática
- ✅ **6 técnicas de distratores** nomeadas com exemplos
- ✅ Feedback pedagógico em **3 campos**: Fundamento + Por que errou + Insight
- ✅ Correção por espelho com **4 critérios ponderados**
- ✅ **~1.532 súmulas** consultáveis (STF, STJ, Vinculantes)
- ✅ **32 URLs normativas** em 8 áreas do Direito + Contabilidade
- ✅ Desistência com confirmação, relatório parcial e opções de retomar
- ✅ Métricas separadas: objetivas vs. discursivas

### Pontos de Melhoria
- 🔧 Tratamento de resposta inválida (ex: digitar "F" em vez de "A–E")
- 🔧 Banco de questões persistente entre sessões
- 🔧 SKILL.md em ~7.9k chars — sem margem para expansão no core

---

## 📁 Estrutura do Projeto

```
simulador_AI_provasJURIDICAS/
├── SKILL.md                  ~7.900 chars  ← CORE (orquestrador)
├── fontes.md                  4.371 chars  ← 32 URLs normativas + súmulas
├── formatos.md                2.671 chars  ← 6 templates de questão
├── correcao.md                1.751 chars  ← Espelho discursivo + regras de nota
├── diretrizes.md              1.141 chars  ← 6 técnicas de distratores + confidence
├── report.md                  3.292 chars  ← Resultado final + parcial
├── VerbetesSTF.md          120.455 chars   ← Súmulas do STF (1–739)
├── VerbetesSTJ.md           97.606 chars   ← Súmulas do STJ (1–679)
├── SumulasVinculantes.md    13.436 chars   ← Súmulas Vinculantes STF (1–115)
└── README.md                 8.097 chars   ← Este arquivo
```

### Fluxo de Carga Sequencial

A skill usa **carregamento sob demanda** — apenas o core fica sempre ativo. Módulos externos são carregados apenas quando necessários.

```
[SEMPRE] SKILL.md (~7.900 chars)
    │
    ├─ Configuração → 7 passos inline (sem carga extra)
    │
    ├─ Gerar questão
    │   ├─ load formatos.md (2.671)
    │   └─ load diretrizes.md (1.141)
    │       → Pico: ~11.700 chars
    │
    ├─ Buscar legislação
    │   └─ load fontes.md (4.371)
    │       → Pico: ~12.300 chars
    │
    ├─ Corrigir discursiva
    │   └─ load correcao.md (1.751)
    │       → Pico: ~9.650 chars ✅
    │
    ├─ Finalizar prova
    │   └─ load report.md (3.292)
    │       → Pico: ~11.200 chars
    │
    └─ Consultar súmula
        └─ load VerbetesSTF.md | VerbetesSTJ.md | SumulasVinculantes.md
            → Carga pontual (não acumula no system prompt)
```

> **Nota:** O core sozinho (SKILL.md) fica em **~7.900 chars** — dentro do limite de 8k.
> Os módulos são carregados individualmente, nunca todos simultaneamente.

---

## 🚀 Como Usar

Basta mencionar qualquer um destes gatilhos:

> `simulado`, `prova`, `questões`, `gabarito`, `treinar matéria`, `testar conhecimento`, `concurso`, `quiz`, `exercícios`, `múltipla escolha`, `certo ou errado`, `discursiva`, `estudo de caso`, `redação jurídica`

A skill iniciará o diálogo de configuração **uma pergunta por vez**.
