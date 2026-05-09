# Protocolo de Validação Restritiva

> **Carregar antes de exibir qualquer questão.**
> **Validação obrigatória — falha = auto-correction (máx. 3) ou descartar.**

---

## Regra 0 — Validação em Cinco Etapas Sequenciais

Toda questão passa por **cinco filtros sequenciais** antes de ser exibida:

```
ETAPA 1 → ICC (Índice de Complexidade Cognitiva)
   ↓ SE APROVADA
ETAPA 2 → Validação de Fonte (obrigatória)
   ↓ SE APROVADA
ETAPA 3 → Validação de Distrator (tipos por nível)
   ↓ SE APROVADA
ETAPA 4 → Matriz Anti-Padrão (não-repetição recente)
   ↓ SE APROVADA
ETAPA 5 → Confidence Score
   ↓ SE APROVADA
EXIBIR QUESTÃO
   ↓ SE REPROVADA EM QUALQUER ETAPA
AUTO-CORRECTION (máx. 3 tentativas) → REVALIDAR
   ↓ SE LIMITE ATINGIDO
DESCARTAR TOTALMENTE → GERAR NOVA → REINICIAR VALIDAÇÃO
```

> **Nunca exibir questão sem passar por todas as 5 etapas.**
> **Auto-Correction:** reescrever APENAS o componente defeituoso antes de descartar totalmente.

---

## Etapa 1 — Validação de ICC (Índice de Complexidade Cognitiva)

> 📂 **Ver `geracao.md`** — Fórmula de cálculo do ICC e faixas esperadas por nível.

### Critério Obrigatório

**Após gerar a questão, calcular o ICC (1-5). Se divergir da faixa do nível configurado, aplicar auto-correction.**

| Nível Configurado | ICC Esperado | Ação se Divergir |
|-------------------|--------------|------------------|
| **Básico** | 1–2 | ICC ≥ 3 → ❌ Auto-Correction (simplificar enunciado) |
| **Intermediário** | 2–3 | ICC ≤ 1 ou ICC ≥ 4 → ❌ Auto-Correction (ajustar complexidade) |
| **Avançado** | 3–4 | ICC ≤ 2 ou ICC = 5 → ❌ Auto-Correction (ajustar complexidade) |
| **Sênior** | 4–5 | ICC ≤ 3 → ❌ Auto-Correction (complexificar enunciado) |

### Fórmula de Cálculo

```
ICC = (N_conceitos + N_normas + N_inferências + N_conflitos) / 2

Onde:
- N_conceitos = número de conceitos jurídicos distintos necessários
- N_normas = número de artigos/súmulas citados ou implícitos
- N_inferências = saltos lógicos necessários (não explícitos no enunciado)
- N_conflitos = tensões normativas/doutrinárias presentes
```

### Checklist de Validação

Antes de avançar para Etapa 2, responder **SIM**:

- [ ] O ICC calculado está dentro da faixa esperada para o nível configurado?

**Se NÃO → ❌ AUTO-CORRECTION #1:** simplificar ou complexificar enunciado mantendo tema e fundamento.

### Exemplos

#### ✅ ICC Correto (Nível Intermediário)

```
Questão: "João, servidor público, praticou ato de improbidade. 
Conforme a Lei 8.429/92 e a Súmula 347 do STF, qual a sanção aplicável?"

Operações: 1 conceito + 2 normas + 1 inferência + 0 conflitos = 4
ICC = 4 / 2 = 2 → Dentro da faixa Intermediário (2-3) → ✅ Aprovado
```

#### ❌ ICC Incorreto (Nível Básico)

```
Questão: "Analise o conflito entre o art. 5º, LXVII, CF/88 e a 
Súmula Vinculante 11, considerando a divergência doutrinária..."

Operações: 1 conceito + 2 normas + 2 inferências + 1 conflito = 6
ICC = 6 / 2 = 3 → Fora da faixa Básico (máx. 2) → ❌ Auto-Correction

[AÇÃO] Simplificar enunciado: remover menção a divergência doutrinária,
       focar apenas em conceito + 1 norma → ICC esperado: 1-2
```

---

## Etapa 2 — Validação de Fonte

### Critério Obrigatório

**Toda questão DEVE citar pelo menos 1 fonte de `fontes.md` ou arquivo de súmula.**

| Elemento | Verificação | Ação se Falhar |
|----------|-------------|----------------|
| Lei federal | URL em `fontes.md` correspondente à disciplina | ❌ Descartar |
| Súmula STF/STJ/Vinculante | Arquivo local (`VerbetesSTF.md`, `VerbetesSTJ.md`, `SumulasVinculantes.md`) | ❌ Descartar |
| Norma técnica (CPC, NBC) | URL em `fontes.md` | ❌ Descartar |
| Doutrina consolidada | Referência implícita a princípio reconhecido | ⚠️ Aceitar apenas se nível ≥ Avançado |

### Checklist de Validação

Antes de exibir, responder **SIM** a todas:

- [ ] A questão menciona artigo, parágrafo, inciso ou alínea de lei listada em `fontes.md`?
- [ ] OU cita número de súmula (ex: "Súmula 347 do STF") presente nos arquivos locais?
- [ ] OU referencia norma técnica (CPC, NBC) da tabela `fontes.md`?
- [ ] O fundamento jurídico é verificável (não inventado)?

**Se qualquer resposta for NÃO → ❌ DESCARTAR E GERAR NOVA.**

### Exemplos

#### ✅ VÁLIDA

```
Fundamento: Art. 5º, LXVII, CF/88
→ CF/88 está em fontes.md (Direito Constitucional)
```

```
Fundamento: Súmula 347 do STF
→ VerbetesSTF.md carregado e súmula 347 existe
```

```
Fundamento: Art. 487, CPC/2015
→ CPC/2015 está em fontes.md (Processo Civil)
```

#### ❌ INVÁLIDA (Descartar)

```
Fundamento: "Conforme entendimento majoritário dos tribunais..."
→ Sem citação específica de fonte verificável
```

```
Fundamento: "Lei 9.999/99, art. 10"
→ Lei não existe em fontes.md (provavelmente inventada)
```

```
Fundamento: "Princípio da boa-fé objetiva"
→ Sem artigo do CC/2002 citado (nível Básico/Intermediário)
```

### Fallback para Níveis Avançado/Sênior

Para níveis **Avançado** e **Sênior**, admite-se:

- Questões baseadas em **conflito doutrinário** sem lei específica
- **Precedentes hipotéticos** baseados em jurisprudência consolidada

**Condição:** deve haver menção explícita a "divergência doutrinária" ou "jurisprudência dominante" + Confidence ≥ 8.

---

## Etapa 3 — Validação de Distrator (Tipos por Nível)

### Critério Obrigatório

**Os distratores DEVEM seguir a distribuição por nível definida em `geracao.md`.**

| Nível | Tipos Permitidos | Mínimo de Técnicas Diferentes |
|-------|------------------|-------------------------------|
| **Básico** | 1, 2, 4 | 2 técnicas distintas |
| **Intermediário** | 1, 2, 4, 5, 6 | 3 técnicas distintas |
| **Avançado** | 2, 3, 5, 6, 7 | 4 técnicas distintas |
| **Sênior** | 3, 5, 6, 7 | 4 técnicas distintas (priorizar 6 e 7) |

### Checklist de Validação

Antes de avançar para Etapa 4, responder **SIM** a todas:

- [ ] Cada distrator usa um tipo da lista permitida para o nível?
- [ ] Há pelo menos N técnicas diferentes (conforme tabela acima)?
- [ ] Nenhum distrator é absurdo óbvio (diferença semântica ≥ 25%)?
- [ ] Gabarito está aleatorizado (A–E, não viciar para C/D)?
- [ ] Máximo de 1 técnica repetida por questão?

**Se qualquer resposta for NÃO → ❌ AUTO-CORRECTION #2:** recalcular distratores mantendo enunciado e gabarito.

### Validação de Diferença Semântica

Para cada distrator, aplicar teste:

```
Distrator é plausível para candidato despreparado?
   SIM → diferença semântica provavelmente ≥ 25% → ✅
   NÃO → muito óbvio ou muito sutil → ❌ auto-correction
```

### Exemplos

#### ✅ VÁLIDA (Nível Intermediário)

```
Gabarito: "Pai autoriza filho menor a viajar"
Distratores:
A) "Pai proíbe filho menor" → Tipo 1 (Oposição)
B) "Pai não autoriza filho" → Tipo 2 (Negação)
C) "Pai autoriza neto" → Tipo 4 (Elemento Periférico)
D) "Pai autoriza, como em arrendamento" → Tipo 5 (Confusão Normativa)
E) "Pai autoriza (sem maioridade)" → Tipo 6 (Pré-requisito Ausente)

→ 5 técnicas distintas (1, 2, 4, 5, 6) → ✅ Aprovado
```

#### ❌ INVÁLIDA (Nível Intermediário)

```
Gabarito: "Pai autoriza filho menor a viajar"
Distratores:
A) "Pai proíbe filho menor" → Tipo 1
B) "Mãe autoriza filho menor" → Tipo 1 (repetido!)
C) "Pai proíbe filha menor" → Tipo 1 (repetido!)
D) "Pai autoriza filho maior" → Tipo 4
E) "Pai proíbe filho maior" → Tipo 1 (repetido!)

→ Apenas 2 técnicas distintas (1 e 4), mínimo era 3 → ❌ Auto-Correction

[AÇÃO] Recalcular distratores B, C, E usando tipos 2, 5, 6
       Manter enunciado e gabarito originais
```

---

## Etapa 4 — Matriz Anti-Padrão (Não-Repetição Recente)

> 📂 **Ver `geracao.md`** — Protocolo de rastreamento dos últimos 5 distratores.

### Critério Obrigatório

**O sistema deve rastrear os últimos 5 distratores utilizados na sessão ativa. É proibido utilizar o mesmo tipo de distrator duas vezes seguidas na mesma área jurídica.**

### Checklist de Validação

Antes de avançar para Etapa 5, responder **SIM** a todas:

- [ ] Nenhum dos distratores da questão atual repete o tipo usado na questão anterior (mesma disciplina)?
- [ ] Pelo menos 50% dos distratores usam tipos diferentes dos últimos 5 registrados?
- [ ] Se nível = Sênior, pelo menos 1 distrator usa tipo 6 ou 7 (mais complexos)?

**Se qualquer resposta for NÃO → ❌ AUTO-CORRECTION #3:** diversificar tipos de distratores.

### Rastreamento de Estado

```
Estado Interno (por disciplina):
{
  "disciplina": "Direito Constitucional",
  "ultimos_5_distratores": [1, 4, 2, 5, 1],
  "tipos_disponiveis_proxima": [2, 3, 6, 7]
}
```

### Exemplo de Aplicação

#### ❌ Violação de Anti-Padrão

```
Questão Anterior (Direito Constitucional):
Distratores usados: [Tipo 1, Tipo 4, Tipo 1, Tipo 2, Tipo 4]

Próxima Questão (mesma disciplina):
Distratores propostos: [Tipo 1, Tipo 4, Tipo 1, Tipo 2, Tipo 4]

→ Violação: Tipo 1 e 4 repetidos da questão anterior
→ Ação: Auto-Correction #3 → substituir por Tipos 3, 5, 6, 7
```

#### ✅ Conformidade com Anti-Padrão

```
Questão Anterior (Direito Constitucional):
Distratores usados: [1, 4, 2, 5, 1]

Próxima Questão (mesma disciplina):
Distratores propostos: [3, 6, 7, 5, 2]

→ Tipos 3, 6, 7 não estavam nos últimos 5 → ✅ Aprovado
```

### Reset de Estado

- **Mudança de disciplina:** resetar contador para nova disciplina
- **Nova sessão de simulado:** resetar todos os contadores
- **Após 10 questões sem repetição:** permitir repetição controlada (máx. 1 tipo repetido)

---

## Etapa 5 — Confidence Score

Além das quatro etapas anteriores, validar:

- [ ] Confidence Score ≥ 7/10?

**Se NÃO → ❌ AUTO-CORRECTION #4:** reformular questão para aumentar fundamentação ou descartar total se após 3 tentativas ainda < 7.
```

---

## Protocolo de Descarte e Regeneração

### Fluxo

```
1. Gerar questão completa (enunciado + alternativas + gabarito + fundamento)
2. Executar Etapa 1 (Fonte)
   → REPROVADA: registrar motivo, descartar, voltar ao passo 1
   → APROVADA: continuar
3. Executar Etapa 2 (Distrator)
   → REPROVADA: registrar motivo, descartar, voltar ao passo 1
   → APROVADA: exibir questão
```

### Limite de Tentativas

- **Máximo: 5 tentativas** por questão
- Se após 5 tentativas nenhuma passar → **fallback**:
  - Reduzir complexidade (ex: mudar de Sênior para Avançado temporariamente)
  - Usar questão pré-validada do banco (`bq/`)
  - Informar usuário: "Questão em revisão técnica. Próxima questão."

### Registro de Logs (interno, não exibir)

```
[Tentativa 1] ❌ Fonte inválida: Lei 9.999/99 não encontrada
[Tentativa 2] ❌ Distrator inválido: apenas 2 técnicas distintas (mín. 3)
[Tentativa 3] ✅ Aprovada → Exibida
```

---

## Confidence Score Mínimo

Além das duas etapas, validar:

- [ ] Confidence Score ≥ 7?
- [ ] Se < 7 → ❌ Descartar e regenerar

---

## Resumo das Regras Restritivas

| Regra | Validação | Ação se Falhar |
|-------|-----------|----------------|
| **Fonte obrigatória** | Lei/súmula/norma de `fontes.md` citada | ❌ Descartar |
| **Distrator por nível** | Tipos conforme `geracao.md` | ❌ Descartar |
| **Diferença semântica** | ≥ 25% entre gabarito e distratores | ❌ Descartar |
| **Confidence Score** | ≥ 7/10 | ❌ Descartar |
| **Técnicas distintas** | Mínimo por nível (2/3/4/4) | ❌ Descartar |
| **Gabarito aleatório** | Distribuição uniforme A–E | ⚠️ Ajustar e revalidar |
| **Máx. 1 técnica repetida** | Não repetir >1 vez mesma técnica | ❌ Descartar |

---

## Mensagem ao Usuário (se fallback acionado)

Nunca revelar falha interna. Usar:

```
⚠️ Questão em revisão técnica. Avançando para próxima...
```

Ou, se múltiplas falhas consecutivas:

```
🔄 Ajustando parâmetros de dificuldade. Por favor, aguarde...
```

---

> **IMPORTANTE:** Este protocolo é **obrigatório**. Ignorar qualquer etapa = violação das regras da skill.
