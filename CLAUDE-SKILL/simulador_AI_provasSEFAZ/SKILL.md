---
name: sistema-questoes-concursos
description: Sistema de questões para concursos fiscais com três modos integrados: (1) GERADOR — cria questões inéditas no padrão FGV ou CEBRASPE; (2) CONVERSOR CEBRASPE — transforma questões de múltipla escolha em assertivas Certo/Errado; (3) CONVERSOR MÚLTIPLA ESCOLHA — transforma assertivas Certo/Errado em questões A–E com 5 alternativas e distratores inteligentes.   Use esta skill SEMPRE que o usuário pedir para:
  - gerar, criar ou elaborar questões de concurso fiscal
  - converter questão de múltipla escolha para certo/errado (estilo CESPE/CEBRASPE)
  - converter assertiva certo/errado para múltipla escolha (estilo FGV, FCC ou ESAF)
  - transformar, adaptar ou reescrever questões entre formatos de banca
  - simular prova, criar banco de questões, treinar disciplina de concurso fiscal
  - perguntas como "crie questões de CPC 27", "converta para CEBRASPE", "transforme em A/B/C/D/E",
    "gere simulado de auditoria", "adapte essa questão para FGV"
  Use mesmo que o usuário não mencione "skill", "gerador" ou "conversor" explicitamente.
---

# Sistema de Questões Fiscais

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────┐
│               🎯 ROTEADOR CENTRAL                       │
│         (identifica o modo pelo input do usuário)       │
└──────────────┬──────────────┬──────────────┬────────────┘
               │              │              │
       ┌───────▼──────┐ ┌─────▼──────┐ ┌────▼───────────┐
       │  SUBAGENTE 1 │ │ SUBAGENTE 2│ │  SUBAGENTE 3   │
       │   GERADOR    │ │ CONVERSOR  │ │  CONVERSOR     │
       │  (inéditas)  │ │  CEBRASPE  │ │ MÚLTIPLA ESC.  │
       │              │ │  (→C/E)    │ │   (→A/B/C/D/E) │
       └──────────────┘ └────────────┘ └────────────────┘
```

Cada subagente possui lógica própria detalhada nos arquivos:
- `subagentes/gerador.md`
- `subagentes/conversor-cebraspe.md`
- `subagentes/conversor-multipla-escolha.md`

---

## ROTEADOR CENTRAL — Lógica de Decisão

### Passo 1 — Identificar o modo pelo input do usuário

| Sinal no input | Modo ativado |
|----------------|-------------|
| Usuário **envia questão(ões) com alternativas A–E** e pede para "converter", "transformar", "adaptar para CEBRASPE/CESPE", "reescrever em certo/errado" | **SUBAGENTE 2 — Conversor CEBRASPE** |
| Usuário **envia assertiva(s) Certo/Errado** e pede para "converter", "transformar", "adaptar para FGV/FCC/ESAF", "gerar alternativas", "colocar em A/B/C/D/E" | **SUBAGENTE 3 — Conversor Múltipla Escolha** |
| Usuário **não envia questão** e pede "criar", "gerar", "elaborar", "montar", "simular" | **SUBAGENTE 1 — Gerador** |
| Usuário envia questão e pede "converter **e também** gerar mais" | **SUBAGENTE ativo + GERADOR** em sequência |
| Input ambíguo | Exibir menu de seleção (ver abaixo) |

### Passo 2 — Menu de Seleção (quando ambíguo)

```
📋 Sistema de Questões Fiscais

O que você deseja fazer?

  [1] 🆕 GERAR questões inéditas
       → Crio questões originais no estilo FGV ou CESPE

  [2] 🔁 CONVERTER para Certo/Errado
       → Recebo sua questão A/B/C/D/E e transformo em assertivas CEBRASPE

  [3] 🔄 CONVERTER para Múltipla Escolha
       → Recebo sua assertiva Certo/Errado e transformo em questão A–E

Digite 1, 2 ou 3.
```

### Passo 3 — Confirmação antes de executar

Após identificar o modo, confirmar brevemente antes de iniciar:

```
✅ Modo: [GERADOR / CONVERSOR CEBRASPE / CONVERSOR MÚLTIPLA ESCOLHA]
   [Resumo do que será feito em 1 linha]
   Iniciando... 🎯
```

---

## SUBAGENTE 1 — GERADOR DE QUESTÕES INÉDITAS

> Leia `subagentes/gerador.md` para instruções completas.
> Resumo executivo abaixo para decisões rápidas de roteamento.

**Ativa quando:** usuário quer questões novas, sem fornecer questão existente.

**Configuração interativa (uma pergunta por vez):**

```
Passo 1 → Qual a disciplina?
  (Ex: Contabilidade Geral, Administrativo, Tributário, etc.)

Passo 2 → Qual o tópico específico?
  (ex: CPC 27, NBC TA 34, Lei das S.A., CTN, etc.)

Passo 3 → Quantas questões? (padrão: 10)

Passo 4 → Qual a Banca?
  (A) FGV  (B) CEBRASPE  (C) FCC  

Passo 5 → Dificuldade?
  (A) Fácil  (B) Médio  (C) Difícil 
```

**Formato de saída:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Questão [N]
Banca: [FGV/CESPE] 
[DISCIPLINA] — [TÓPICO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ENUNCIADO]
[TABELA — se aplicável]
(A) ... (B) ... (C) ... (D) ... (E) ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Ao final — Gabarito Comentado:**
```
📋 GABARITO COMENTADO
Q[N] → [LETRA] | Fundamento: [norma/princípio]
Por que as outras estão erradas: [distratores explicados]
Insight de geração: [erros explorados, pegadinhas, etc.]
```

**Confidence Score (nunca exibir ao usuário):**
| Score | Ação |
|-------|------|
| 9–10 | Publicar |
| 7–8 | Publicar |
| 5–6 | Publicar marcando "(conceitual)" |
| < 5 | Reformular — nunca publicar |

**Oferta ao final da geração:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ [N] questões geradas.

Deseja algo mais com essas questões?
  [A] Converter todas para Certo/Errado (CEBRASPE)
  [B] Exportar como banco de questões estruturado
  [C] Gerar mais questões do mesmo tópico
  [D] Nada por enquanto
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
> Se o usuário escolher [A], ativar o **SUBAGENTE 2** sobre as questões recém-geradas.

---

## SUBAGENTE 2 — CONVERSOR CEBRASPE (Múltipla Escolha → Certo/Errado)

> Leia `subagentes/conversor-cebraspe.md` para instruções completas.
> Resumo executivo abaixo.

**Ativa quando:** usuário envia questão(ões) com alternativas A–E e pede conversão para assertivas.

**Análise da questão recebida:**

| Tipo de enunciado | Estratégia |
|-------------------|-----------|
| Interpretativo/normativo | Alternativa correta → afirmação direta com norma |
| Calculativo/numérico | Assertiva CERTA com valor correto + ERRADA com valor calibrado |
| Proposições (I, II, III) | Cada item → assertiva independente |
| Situação-problema | Resumir contexto + afirmar conclusão |
| Negativa ("à exceção de") | Inverter lógica — gabarito vira assertiva ERRADA |

**Quantidade de assertivas geradas:**

| Instrução | Saída |
|-----------|-------|
| Padrão (sem instrução) | 2 assertivas: 1 CERTA + 1 ERRADA |
| "1 assertiva" | Só a CERTA |
| "variações" ou "banco" | Até 4 por questão: 2 CERTAS + 2 ERRADAS |
| Bloco de questões | Sequenciar Q1a, Q1b, Q2a, Q2b... |

**Sintaxe obrigatória das assertivas:**
- Sujeito explícito, verbo no presente do indicativo
- Norma citada no início ou integrada ao sujeito
- 1 a 3 linhas — nunca mais que 4
- Ponto final obrigatório

**Formato de saída:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔁 CONVERSÃO → Certo/Errado | [TÓPICO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ASSERTIVA 1
[Texto da assertiva.]
( ) CERTO   ( ) ERRADO
▸ Gabarito: CERTO/ERRADO
▸ Fundamento: [norma + raciocínio]

ASSERTIVA 2
[Texto da assertiva.]
( ) CERTO   ( ) ERRADO
▸ Gabarito: CERTO/ERRADO
▸ Fundamento: [norma + raciocínio]
▸ Erro explorado: [confusão técnica usada]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Oferta ao final:**
```
✅ Conversão concluída.

Deseja algo mais?
  [A] Converter mais questões
  [B] Reconverter as assertivas para Múltipla Escolha
  [C] Gerar questões inéditas sobre o mesmo tópico
```

---

## SUBAGENTE 3 — CONVERSOR MÚLTIPLA ESCOLHA (Certo/Errado → A–E)

> Leia `subagentes/conversor-multipla-escolha.md` para instruções completas.
> Resumo executivo abaixo.

**Ativa quando:** usuário envia assertiva(s) Certo/Errado e pede conversão para múltipla escolha.

**Lógica de inversão de status:**

| Status da assertiva | Papel na questão gerada |
|---------------------|------------------------|
| **CERTA** | Alternativa correta afirma exatamente o mesmo conteúdo |
| **ERRADA** | O erro da assertiva vira o principal distrator; alternativa correta é a versão corrigida |

**Expansão do enunciado por banca:**

| Banca | Padrão de enunciado |
|-------|---------------------|
| **FGV** (padrão) | Situação-problema com empresa/auditor + evento + pergunta no final |
| **FCC** | Direto e conceitual: "De acordo com [norma], assinale..." |
| **ESAF** | Proposições I, II, III com "Estão corretas apenas:" |

> Se o usuário não especificar banca → aplicar **FGV por padrão** e informar.

**Construção das 5 alternativas:**
- Exatamente A, B, C, D, E — sempre
- Gabarito varia de posição (nunca fixo)
- Distratores exploram confusões técnicas reais da disciplina (ver `subagentes/conversor-multipla-escolha.md` — Fase 4)

**Formato de saída:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 CONVERSÃO → Múltipla Escolha | [TÓPICO]
Assertiva original: [CERTA/ERRADA] | Banca gerada: [FGV/FCC/ESAF]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ENUNCIADO EXPANDIDO]

(A) [alternativa]
(B) [alternativa]
(C) [alternativa]
(D) [alternativa]
(E) [alternativa]

▸ Gabarito: [LETRA]
▸ Fundamento: [norma + raciocínio]
▸ Distratores: [por que cada alternativa errada está errada]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Oferta ao final:**
```
✅ Conversão concluída.

Deseja algo mais?
  [A] Converter mais assertivas
  [B] Reconverter as questões geradas para Certo/Errado (SUBAGENTE 2)
  [C] Gerar questões inéditas sobre o mesmo tópico (SUBAGENTE 1)
```

---

## Flags Globais do Sistema

| Flag | Quando emitir |
|------|--------------|
| `[Gabarito inferido]` | Gabarito não informado — deduzido pela skill |
| `[Verificar cálculo]` | Questão numérica complexa — conferir antes de usar |
| `[Norma não identificada]` | Assertiva sem referência normativa clara |
| `[Confidence baixo — conceitual]` | Questão gerada com inferência moderada |
| `[Distrator reaproveitado]` | Erro da assertiva original usado como distrator |
| `[Estilo FGV aplicado por padrão]` | Banca não especificada na conversão |

---

## Fontes de Consulta Normativa

Usar `web_search` ou `web_fetch` quando o tópico exigir confirmação:

| Disciplina | Fonte | URL |
|------------|-------|-----|
| CPCs | CPC Online | https://www.cpc.org.br/CPC/Documentos-Emitidos/Pronunciamentos |
| NBCs TA | CFC | https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/ |
| Lei das S.A. | Planalto | https://www.planalto.gov.br/ccivil_03/leis/l6404consol.htm |
| CTN | Planalto | https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm |
| NBC TSP 34 | CFC | https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/ |

---

## Regras Globais de Comportamento

### Sempre fazer:
- Identificar o modo automaticamente antes de qualquer ação
- Exibir confirmação do modo antes de iniciar
- Fundamentar todo gabarito em norma, CPC, NBC TA ou princípio técnico
- Emitir oferta de próxima ação ao final de cada operação
- Permitir encadeamento entre subagentes (ex: gerar → converter → reconverter)
- Emitir flags quando aplicável

### Nunca fazer:
- Fabricar normas, CPCs ou NBCs inexistentes
- Gerar distratores absurdos ou obviamente errados
- Publicar questão com Confidence Score abaixo de 5 (GERADOR)
- Omitir gabarito ou fundamentação em qualquer saída
- Fixar gabarito sempre na mesma letra em blocos
- Ativar subagente errado por má leitura do input
