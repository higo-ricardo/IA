# Diretrizes de Geração — Níveis, Fórmulas e Métricas

> Carregar antes da Fase 2 (Roteamento) e durante a geração de questões.

---

## Composição por Nível

| Nível | Composição | Lógica | Desafio |
|-------|------------|--------|--------|
| **Básico** | 60% Fontes + 40% LLM | Conceitos claros e verificáveis | Baixo |
| **Intermediário** | 35% Fontes + 25% Verbetes + 40% LLM | Norma + súmula + síntese LLM | Médio |
| **Avançado** | 20% Fontes + 20% Verbetes + 30% Doutrina + 30% LLM | 3 camadas: norma, jurisprudência, análise | Alto |
| **Sênior** | 15% Fontes + 15% Verbetes + 25% Doutrina + 45% LLM | LLM sintetiza conflitos doutrinários/precedentes | Crítico |

---

## Fórmulas de Geração por Nível

| Nível | Fórmula | Complexidade |
|-------|---------|-------------|
| **Básico** | `CONCEITO + DEFINIÇÃO_LEGAL + DISTRATOR_SIMPLES` | Enunciado direto, sem casos |
| **Intermediário** | `CASO + NORMA + VERBETE + 3 DISTRATORES + GABARITO_RAND` | Caso fático + norma + súmula |
| **Avançado** | `CASO_COMPLEXO + NORMA_LITERAL + DOUTRINA + JURISPRUDÊNCIA + 4 DISTRATORES + MODALIDADE_VARIADA` | 2+ elementos em tensão |
| **Sênior** | `CONFLITO_NORMATIVO + VERBETE + DOUTRINA_DIVERGENTE + REDAÇÃO_LITERAL + 4 DISTRATORES + DEMANDA_ANALÍTICA` | 3+ elementos, distratores quase idênticos |

---

## Protocolo de Roteamento

1. Identificar nível configurado
2. Selecionar fonte primária de acordo com % do nível
3. `web_fetch` na URL da disciplina (fallback: prosseguir sem, Confidence máx. 8/10)
4. Extrair fragmentos (1–3 linhas) quando usar fontes/verbetes
5. Permitir que LLM sintetize enunciado e alternativas
6. Garantir Confidence ≥ 7 antes de exibir
7. **Nunca bloquear** por falha na busca — sempre aplicar fallback

---

## Distratores Inteligentes

### 7 Tipos de Distratores

| Tipo | Nome | Descrição | Diferença Semântica | Exemplo (norma: "Pai autoriza filho") |
|------|------|-----------|--------------------:|----------------------------------------|
| 1 | Oposição Simples | Nega o gabarito completamente | 90% | "Pai proíbe filho" |
| 2 | Negação simples | Adiciona NÃO quando afirmativa ou remove NÃO quando negativa | 70% | "Pai não autoriza filho" |
| 3 | Inversão Sujeito/Objeto | Inverte sujeito ↔ objeto da norma | 65% | "Filho autoriza pai" |
| 4 | Elemento Periférico | Muda detalhe secundário | 50% | "Pai autoriza neto" |
| 5 | Confusão Normativa | Mistura norma correta com outra | 40% | "Pai autoriza, como em arrendamento rural" |
| 6 | Pré-requisito Ausente | Remove 1 pré-requisito do gabarito | 35% | "Pai autoriza (sem atingir maioridade)" |
| 7 | Qualificador Falso | Adiciona qualificador que inverte significado | 25% | "Pai autoriza, desde que o filho discorde" |

**Regra:** cada distrator deve ter diferença semântica ≥ 25%

### Distribuição por Nível

- **Básico**: 1, 2, 4 (óbvios)
- **Intermediário**: 1, 2, 4, 5, 6 (moderados)
- **Avançado**: 2, 3, 5, 6, 7 (desafiadores)
- **Sênior**: 3, 5, 6, 7 (complexos)

### Regras de Validação

- Nenhum absurdo óbvio
- Gabarito aleatório A–E
- Máx. 1 técnica repetida por questão
- Validar tipos 2 e 3 para evitar contradições ambíguas

---

## Confidence Score

Exibir em **todas** as questões, antes do enunciado:

```
[Confidence: X/10]
```

| Score | Significado |
|-------|-------------|
| 9–10 | Extraída do material ou conhecimento consolidado sólido |
| 7–8 | Bem fundamentada com pequena inferência |
| 5–6 | Inferência moderada — **nunca exibir** (mínimo: 7) |
| 1–4 | Alta inferência — **nunca exibir** (reformular) |

> **Regra**: Nunca exibir questão com Confidence < 7. Reformular ou substituir.

---

## Controle de Tempo

- **Timer real**: registrar `T0` no início com Python `datetime.now(timezone(timedelta(hours=-3)))`. Ao final, `Tmédio = (TFim − T0) / N`.
- **Fallback**: se Python indisponível → estimar por troca de mensagens (30–90s por questão). Indicar "(estimado)" no relatório.
- Exibir `⏱️ ref. [T]s` em cada questão.

---

## Índice de Complexidade Cognitiva (ICC)

> **Meta-instrução obrigatória pós-geração.** Carregar antes de validar fonte e distratores.

### Definição

O **Índice de Complexidade Cognitiva (ICC)** mede a quantidade de operações mentais necessárias para resolver a questão, em escala de 1 a 5.

| ICC | Operações Mentais | Descrição | Nível Esperado |
|-----|-------------------|-----------|----------------|
| **1** | 1 operação | Reconhecimento/recordação simples | Básico |
| **2** | 2 operações | Compreensão + aplicação direta | Básico/Intermediário |
| **3** | 3 operações | Aplicação + análise de 2 elementos | Intermediário |
| **4** | 4 operações | Análise + síntese + avaliação de conflito | Avançado |
| **5** | 5+ operações | Avaliação crítica + criação de solução para cenário complexo | Sênior |

### Fórmula de Cálculo

```
ICC = (N_conceitos + N_normas + N_inferências + N_conflitos) / 2

Onde:
- N_conceitos = número de conceitos jurídicos distintos necessários
- N_normas = número de artigos/súmulas citados ou implícitos
- N_inferências = saltos lógicos necessários (não explícitos no enunciado)
- N_conflitos = tensões normativas/doutrinárias presentes
```

### Validação de Alinhamento

**Regra Restritiva:** Após gerar a questão, calcular o ICC. Se divergir do nível configurado, **descartar e regenerar**.

| Nível Configurado | ICC Esperado | Ação se Divergir |
|-------------------|--------------|------------------|
| **Básico** | 1–2 | ICC ≥ 3 → ❌ Descartar |
| **Intermediário** | 2–3 | ICC ≤ 1 ou ICC ≥ 4 → ❌ Descartar |
| **Avançado** | 3–4 | ICC ≤ 2 ou ICC = 5 → ❌ Descartar |
| **Sênior** | 4–5 | ICC ≤ 3 → ❌ Descartar |

### Exemplos de Cálculo

#### ✅ ICC Correto (Nível Intermediário, ICC=3)

```
Questão: "João, servidor público, praticou ato de improbidade. 
Conforme a Lei 8.429/92 e a Súmula 347 do STF, qual a sanção aplicável?"

Operações:
1. Identificar conceito de improbidade (1 conceito)
2. Localizar Lei 8.429/92 (1 norma)
3. Consultar Súmula 347 do STF (1 norma)
4. Aplicar sanção ao caso concreto (1 inferência)

Cálculo: (1 + 2 + 1 + 0) / 2 = 2 → ICC=2 (aceitável para Intermediário: 2-3)
→ ✅ Aprovado
```

#### ❌ ICC Incorreto (Nível Básico, ICC=4)

```
Questão: "Analise o conflito entre o art. 5º, LXVII, CF/88 e a 
Súmula Vinculante 11, considerando a divergência doutrinária 
entre Roberto Barroso e Gilmar Mendes sobre prisão civil..."

Operações:
1. Conceito de prisão civil (1)
2. Art. 5º, LXVII, CF/88 (1 norma)
3. Súmula Vinculante 11 (1 norma)
4. Divergência doutrinária (1 conflito)
5. Síntese crítica da posição de cada ministro (2 inferências)

Cálculo: (1 + 2 + 2 + 1) / 2 = 3 → ICC=3 (inaceitável para Básico: máx. 2)
→ ❌ Descartar e simplificar
```

### Registro Interno (não exibir)

```
[ICC Calculado: X] | [Nível Esperado: Y-Z] | [Status: ✅ Aprovado / ❌ Reprovado]
```

---

## Auto-Correction Loop (Loop de Autocorreção)

> **Protocolo de reescrita inteligente.** Quando uma questão falha na validação, reescrever corrigindo o erro específico em vez de gerar do zero.

### Fluxo de Auto-Correction

```
1. Gerar questão completa
2. Executar validação (fonte → distrator → ICC)
   ↓ SE REPROVADA
3. Identificar causa raiz da falha
4. Reescrever APENAS o componente defeituoso
   - Fonte inválida → substituir fundamento por outro de fontes.md
   - Distrator inadequado → recalculaar distratores mantendo enunciado
   - ICC divergente → simplificar ou complexificar enunciado
5. Revalidar questão reescrita
6. Repetir até aprovação ou limite de 3 tentativas de reescrita
   ↓ SE LIMITE ATINGIDO
7. Descartar totalmente e gerar nova questão do zero
```

### Vantagens vs. Regeneração Total

| Estratégia | Tokens Gastos | Coerência Temática | Tempo de Processamento |
|------------|---------------|--------------------|------------------------|
| **Regeneração Total** | Alto (~100% novo) | Baixa (novo tema) | Alto |
| **Auto-Correction** | Médio (~40% novo) | Alta (mesmo tema) | Baixo |

### Exemplo de Auto-Correction

#### Tentativa 1 (Falha: Fonte Inválida)

```
❌ Fonte inválida: "Lei 9.999/99" não encontrada em fontes.md

[AÇÃO: Auto-Correction #1]
→ Manter enunciado e distratores
→ Substituir fundamento por "Art. 5º, LXVII, CF/88" (fontes.md: Direito Constitucional)
→ Revalidar
```

#### Tentativa 2 (Falha: Distrator)

```
❌ Distrator inválido: apenas 2 técnicas distintas (mín. 3 para Intermediário)

[AÇÃO: Auto-Correction #2]
→ Manter enunciado e gabarito
→ Recalcular distratores A, B, C usando tipos 1, 4, 5 (geracao.md)
→ Revalidar
```

#### Tentativa 3 (Aprovada)

```
✅ Todas as validações aprovadas → Exibir questão
```

### Limite de Tentativas

- **Auto-Correction:** Máximo de **3 reescritas** por questão
- **Se após 3 reescritas ainda falhar:** descartar totalmente e gerar nova questão do zero
- **Fallback final:** se 5 questões consecutivas falharem → usar banco `bq/`

### Registro de Logs (interno)

```
[Tentativa 1] ❌ Fonte inválida → Auto-Correction #1 (substituir fundamento)
[Tentativa 2] ❌ Distrator inválido → Auto-Correction #2 (recalcular distratores)
[Tentativa 3] ✅ Aprovada → Exibida (economia: ~60% tokens vs. regeneração total)
```

---

## Matriz de Distratores Dinâmica (Anti-Padrão)

> **Regra de Não-Repetição Recente.** Evitar vícios de geração e forçar exploração completa dos 7 tipos de distratores.

### Protocolo Anti-Padrão

**Regra:** O sistema deve rastrear os últimos **5 distratores utilizados na sessão ativa**. É **proibido** utilizar o mesmo tipo de distrator duas vezes seguidas na mesma área jurídica.

### Rastreamento de Estado

```
Estado Interno (por disciplina):
{
  "disciplina": "Direito Constitucional",
  "ultimos_5_distratores": [1, 4, 2, 5, 1],  // Tipos usados nas últimas 5 questões
  "tipos_disponiveis_proxima": [2, 3, 6, 7]   // Tipos não repetidos recentemente
}
```

### Validação de Diversidade

Antes de exibir a questão, validar:

- [ ] Nenhum dos distratores da questão atual repete o tipo usado na questão anterior?
- [ ] Pelo menos 50% dos distratores usam tipos diferentes dos últimos 5?
- [ ] Se nível = Sênior, pelo menos 1 distrator usa tipo 6 ou 7 (mais complexos)?

**Se qualquer resposta for NÃO → ❌ Auto-Correction (recalcular distratores).**

### Exemplo de Aplicação

#### ❌ Violação de Anti-Padrão

```
Questão Anterior (Direito Constitucional):
Distratores usados: Tipo 1 (Oposição), Tipo 4 (Elemento Periférico), Tipo 1 (Oposição), Tipo 2 (Negação), Tipo 4 (Elemento Periférico)

Próxima Questão (mesma disciplina):
Distratores propostos: Tipo 1, Tipo 4, Tipo 1, Tipo 2, Tipo 4

→ Violação: Tipo 1 e 4 repetidos da questão anterior
→ Ação: Auto-Correction → substituir por Tipos 3, 5, 6, 7
```

#### ✅ Conformidade com Anti-Padrão

```
Questão Anterior (Direito Constitucional):
Distratores usados: [1, 4, 2, 5, 1]

Próxima Questão (mesma disciplina):
Distratores propostos: [3, 6, 7, 5, 2]

→ Tipos 3, 6, 7 não estavam nos últimos 5 → ✅ Aprovado
→ Tipos 5 e 2 aparecem, mas não são repetição imediata → ✅ Aprovado
```

### Reset de Estado

- **Mudança de disciplina:** resetar contador para nova disciplina
- **Nova sessão de simulado:** resetar todos os contadores
- **Após 10 questões sem repetição:** permitir repetição controlada (máx. 1 tipo repetido)

---

## Resumo das Validações Pós-Geração

| Validação | Ordem | Critério | Ação se Falhar |
|-----------|-------|----------|----------------|
| **ICC (Complexidade)** | 1ª | ICC dentro da faixa do nível | ❌ Auto-Correction (simplificar/complexificar) |
| **Fonte** | 2ª | Lei/súmula/norma de `fontes.md` citada | ❌ Auto-Correction (substituir fundamento) |
| **Distrator (Nível)** | 3ª | Tipos conforme `geracao.md` | ❌ Auto-Correction (recalcular distratores) |
| **Distrator (Anti-Padrão)** | 4ª | Não-repetição recente (últimas 5) | ❌ Auto-Correction (diversificar tipos) |
| **Confidence Score** | 5ª | ≥ 7/10 | ❌ Auto-Correction ou descarte total |

**Fluxo Completo:**
```
Gerar → Calcular ICC → Validar Fonte → Validar Distratores → Validar Anti-Padrão → Confidence → Exibir
   ↓          ↓             ↓                ↓                   ↓              ↓
Reescrever  Reescrever   Reescrever      Reescrever         Reescrever    Descarte/Reescrever
```
