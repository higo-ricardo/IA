---
name: conversor-multipla-escolha
description: >
  Converte questões de julgamento Certo/Errado (estilo CESPE/CEBRASPE) em questões de
  múltipla escolha (A–E) no padrão FGV, FCC, ESAF ou VUNESP, com enunciado expandido,
  5 alternativas com distratores inteligentes e gabarito comentado.
  Use esta skill SEMPRE que o usuário pedir para:
  - converter questão certo/errado para múltipla escolha
  - transformar assertiva CESPE ou CEBRASPE em questão A/B/C/D/E
  - adaptar questão de julgamento para estilo FGV, FCC ou ESAF
  - expandir uma assertiva em questão de concurso com alternativas
  - "converta para múltipla escolha", "transforme em A/B/C/D/E", "adapte para FGV"
  - gerar banco de questões múltipla escolha a partir de assertivas
  Use mesmo que o usuário não mencione "skill" ou "conversor" explicitamente.
---

# Skill: Conversor de Questões — Estilo CEBRASPE → Múltipla Escolha

## Princípios Fundamentais

| Princípio | Aplicação |
|-----------|-----------|
| **Expansão fiel** | O conceito da assertiva original é preservado — o enunciado é enriquecido, não distorcido |
| **5 alternativas sempre** | Toda questão gerada tem exatamente A, B, C, D, E |
| **Distratores inteligentes** | Alternativas erradas exploram confusões técnicas reais da disciplina |
| **Gabarito fundamentado** | Toda questão gerada vem com gabarito e justificativa normativa |
| **Estilo de banca configurável** | FGV (situação-problema), FCC (direta/conceitual), ESAF (proposições) |

---

## Fase 1 — Recebimento da Questão

O usuário pode fornecer:

| Forma | Descrição | Ação |
|-------|-----------|------|
| **Assertiva + gabarito** | "A NBC TA 530 veda... ERRADO" | Processar direto |
| **Assertiva sem gabarito** | Só o texto | Inferir o gabarito e sinalizar `[Gabarito inferido]` |
| **Bloco de assertivas** | 2 ou mais | Converter cada uma individualmente, numerando Q1, Q2... |
| **Tema sem assertiva** | "Crie questão de CPC 27 estilo FGV" | Gerar do zero com base no tema |

---

## Fase 2 — Análise da Assertiva Original

Antes de converter, a skill classifica internamente:

### 2.1 — Status da Assertiva

| Status | O que fazer |
|--------|-------------|
| **CERTA** | A alternativa correta da questão gerada afirma exatamente o que a assertiva diz |
| **ERRADA** | A alternativa correta da questão gerada **corrige** o erro da assertiva — o texto errado vira um distrator |

### 2.2 — Tipo de Conteúdo

| Tipo | Estratégia de Expansão |
|------|------------------------|
| **Normativo/interpretativo** | Construir enunciado com "De acordo com [norma]..." + 5 interpretações da norma |
| **Conceitual** | Enunciado pede definição, classificação ou distinção entre conceitos |
| **Calculativo** | Enunciado traz dados numéricos + evento → pede resultado específico |
| **Situação-problema** | Enunciado descreve empresa/auditor + evento → pede conclusão ou classificação |
| **Processual/sequencial** | Enunciado descreve etapas → pede a correta ou a que está fora de lugar |

---

## Fase 3 — Regras de Expansão do Enunciado

### 3.1 — De Assertiva Curta para Enunciado FGV

A assertiva CEBRASPE é tipicamente curta (1–3 linhas). O enunciado FGV exige **contexto, sujeito e situação**. A skill expande seguindo este modelo:

```
[CONTEXTO: empresa, auditor, entidade ou situação que justifica a pergunta]
[EVENTO ou DADO que ancora o problema]
[PERGUNTA DIRETA ao final: "Assinale a opção correta." / "Assinale a opção que indica..."]
```

**Exemplo de expansão:**

*Assertiva original (CEBRASPE — ERRADA):*
```
A variância amostral é obtida dividindo-se a soma dos quadrados
dos desvios pela quantidade total de observações da amostra.
```

*Enunciado FGV gerado:*
```
Uma analista fiscal coletou a seguinte amostra de tempos de
tramitação de processos (em dias): {2, 5, 5, 6, 6, 7, 7, 10}.
Para calcular a dispersão dos dados, ela decidiu apurar a
variância amostral da série.

Assinale a opção que indica o procedimento correto para o cálculo
da variância amostral.
```

---

### 3.2 — De Assertiva Curta para Enunciado FCC

FCC é mais direta e conceitual. O enunciado não precisa de situação-empresa — pode ser direto:

```
"Acerca de [tema], assinale a opção correta."
"Em relação a [norma/conceito], é correto afirmar que"
"Sobre [tema], assinale a alternativa que apresenta conceito correto."
```

---

### 3.3 — De Assertiva Curta para Estilo ESAF (Proposições)

Quando o usuário pede estilo ESAF, a skill transforma a assertiva em questão com proposições:

```
Analise as afirmativas a seguir sobre [tema]:

I.   [proposição — verdadeira]
II.  [proposição — falsa, baseada no erro da assertiva original]
III. [proposição — verdadeira]

Estão corretas:
(A) Apenas I
(B) Apenas II
(C) I e III
(D) II e III
(E) I, II e III
```

---

## Fase 4 — Construção das 5 Alternativas

### 4.1 — Estrutura Obrigatória

```
(A) [alternativa]
(B) [alternativa]
(C) [alternativa — GABARITO, em posição variável]
(D) [alternativa]
(E) [alternativa]
```

**Regras de posicionamento:**
- O gabarito deve variar entre A e E ao longo de um bloco — nunca fixar sempre em (A) ou sempre em (E)
- Em bloco de 5+ questões, distribuir gabarito: pelo menos 1 vez em cada letra

### 4.2 — Tipos de Distratores por Disciplina

#### Contabilidade Geral / CPCs
| Distrator | Técnica |
|-----------|---------|
| Trocar método de avaliação | PEPS no lugar de custo médio, custo no lugar de valor justo |
| Inverter grupo contábil | Ativo no lugar de passivo, resultado no lugar de PL |
| Trocar demonstração | DRE no lugar de DMPL, DFC no lugar de DVA |
| Aplicar CPC errado | CPC 27 no lugar de CPC 06, CPC 46 no lugar de CPC 12 |
| Erro de alíquota ou base | 25% no lugar de 34%, base contábil no lugar de fiscal |

#### Auditoria (NBCs TA)
| Distrator | Técnica |
|-----------|---------|
| Trocar NBC TA | NBC TA 500 no lugar de NBC TA 530, NBC TA 705 no lugar de NBC TA 700 |
| Inverter risco | Risco inerente no lugar de risco de controle |
| Confundir opinião | Opinião com ressalva no lugar de abstenção de opinião |
| Trocar objetivo | Testes de controle no lugar de testes substantivos |
| Erro de escopo | "eliminar" o risco no lugar de "reduzir a nível aceitável" |

#### Custos
| Distrator | Técnica |
|-----------|---------|
| Incluir despesa no custo | Despesa administrativa classificada como custo de produção |
| Confundir custeio | Custeio variável no lugar de absorção (ou vice-versa) |
| Erro no PE | Usar margem de contribuição bruta no lugar da unitária |
| Trocar classificação | Custo fixo classificado como variável |
| Erro no divisor | Dividir por unidades vendidas no lugar das produzidas |

#### Raciocínio Lógico
| Distrator | Técnica |
|-----------|---------|
| Afirmar a recíproca | "Se P→Q, então Q→P" (inválido) |
| Negar incorretamente | Negar antecedente em vez de consequente |
| Confundir "alguns" com "todos" | "Alguns X são Y" → distrator: "Todo X é Y" |
| Inverter conclusão | Afirmar o contraditório da conclusão válida |

#### Estatística
| Distrator | Técnica |
|-----------|---------|
| Trocar divisor | n no lugar de n−1 (variância amostral vs populacional) |
| Confundir Z e t | Usar Z quando n < 30 sem variância conhecida |
| Erro na probabilidade | P(A ∪ B) sem subtrair P(A ∩ B) |
| Trocar parâmetros | Média no lugar de mediana, desvio no lugar de variância |

---

## Fase 5 — Exemplos Completos de Conversão

### Exemplo 1 — Assertiva ERRADA → Questão FGV

**Assertiva original (CEBRASPE — ERRADA):**
```
Conforme o CPC 46, quando não existe mercado principal para um
ativo, o valor justo deve ser mensurado com base em fatos
históricos mais recentes relacionados a esse ativo.
```

**Questão FGV gerada:**
```
Questão X — CPC 46 / Mensuração do Valor Justo

De acordo com o Pronunciamento Técnico CPC 46 — Mensuração do
Valor Justo, a mensuração do valor justo presume que a transação
para a venda do ativo ou a transferência do passivo ocorre no
mercado principal. Na ausência de mercado principal, o CPC 46
estabelece que a transação deve ocorrer:

(A) no mercado em que a entidade adquiriu originalmente o ativo.
(B) com base em fatos históricos mais recentes relacionados ao ativo.
(C) no mercado mais vantajoso para o ativo ou passivo.
(D) com base nos preços cotados em mercados internacionais equivalentes.
(E) no mercado de maior volume de negociações nos últimos 12 meses.

Gabarito: C
Fundamento: CPC 46, itens 16–17 — na ausência de mercado principal,
presume-se o mercado mais vantajoso. "Fatos históricos" (B) não é
critério previsto na norma — era o erro da assertiva original.
```

---

### Exemplo 2 — Assertiva CERTA → Questão FCC

**Assertiva original (CEBRASPE — CERTA):**
```
O auditor independente, ao identificar flutuações inconsistentes
nos procedimentos analíticos, deve investigá-las por meio de
indagação à administração e obtenção de evidência adicional.
```

**Questão FCC gerada:**
```
Questão X — NBC TA 520 / Procedimentos Analíticos

Conforme a NBC TA 520 — Procedimentos Analíticos, quando o
auditor identifica flutuações ou relações inconsistentes com
outras informações relevantes, ele deve examinar essas diferenças.
Assinale a opção que indica corretamente como o auditor deve
proceder nessa situação.

(A) Emitir opinião com ressalva diretamente, sem investigação adicional.
(B) Substituir os procedimentos analíticos por testes de controle.
(C) Encerrar o trabalho e comunicar o fato ao comitê de auditoria.
(D) Realizar indagação à administração e obter evidência de auditoria
    adequada para avaliar as respostas obtidas.
(E) Solicitar confirmação externa a terceiros como único procedimento
    de investigação cabível.

Gabarito: D
Fundamento: NBC TA 520, item 7 — diante de flutuações inexplicadas,
o auditor deve indagar à administração e obter evidência adicional
para avaliar as respostas. As demais alternativas descrevem ações
não previstas ou excessivas pela norma.
```

---

### Exemplo 3 — Assertiva ERRADA → Questão com Proposições (ESAF)

**Assertiva original (CEBRASPE — ERRADA):**
```
Na amostragem em auditoria, quanto maior o risco que o auditor
aceita, maior deve ser o tamanho da amostra.
```

**Questão ESAF gerada:**
```
Questão X — NBC TA 530 / Amostragem em Auditoria

Com base na NBC TA 530 — Amostragem em Auditoria, analise as
afirmativas abaixo:

I.  O tamanho da amostra é influenciado pelo nível de risco de
    amostragem que o auditor está disposto a aceitar.
II. Quanto maior o risco de amostragem que o auditor aceita,
    maior deve ser o tamanho da amostra.
III. A amostragem estatística e a não estatística, quando
     aplicadas corretamente, podem fornecer evidências suficientes.

Estão corretas apenas:
(A) I
(B) II
(C) I e III
(D) II e III
(E) I, II e III

Gabarito: C
Fundamento: I — CERTA (NBC TA 530, item 7). II — ERRADA: a relação
é inversa — quanto menor o risco aceito, maior a amostra necessária.
III — CERTA (NBC TA 530, item 9). O erro da assertiva original estava
exatamente na proposição II.
```

---

## Fase 6 — Formato de Saída

### Saída padrão (1 assertiva → 1 questão)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔁 CONVERSÃO — Assertiva [N] | [TÓPICO]
Assertiva original: [CERTA / ERRADA]
Banca gerada: [FGV / FCC / ESAF]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ENUNCIADO EXPANDIDO]

(A) [alternativa]
(B) [alternativa]
(C) [alternativa]
(D) [alternativa]
(E) [alternativa]

▸ Gabarito: [LETRA]
▸ Fundamento: [Norma + raciocínio técnico]
▸ Distratores: [Breve explicação do erro de cada alternativa incorreta]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Saída em bloco (múltiplas assertivas)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 BANCO DE QUESTÕES — [DISCIPLINA]
[N] assertivas convertidas → [N] questões múltipla escolha
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUESTÃO 1 — [TÓPICO]
[Enunciado + alternativas A–E]
▸ Gabarito: [LETRA] | [Fundamento]

QUESTÃO 2 — [TÓPICO]
[Enunciado + alternativas A–E]
▸ Gabarito: [LETRA] | [Fundamento]

[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GABARITO GERAL
Q1: [A] | Q2: [C] | Q3: [B] | Q4: [E] | Q5: [D]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Fase 7 — Flags e Alertas

| Flag | Quando emitir |
|------|--------------|
| `[Gabarito inferido]` | Usuário não informou CERTO/ERRADO — skill deduziu |
| `[Verificar cálculo]` | Questão numérica complexa — confirmar antes de usar |
| `[Norma não identificada]` | Assertiva sem referência normativa clara |
| `[Estilo padrão FGV aplicado]` | Usuário não especificou banca — FGV usado por padrão |
| `[Distrator reaproveitado da assertiva]` | O erro da assertiva original foi usado como distrator |

---

## Configuração de Banca (quando não especificada)

Se o usuário não informar a banca desejada, aplicar **FGV por padrão** e informar:
```
ℹ️ Banca não especificada — questão gerada no padrão FGV.
   Para FCC, ESAF ou outra banca, informe na próxima mensagem.
```

---

## Regras Finais de Comportamento

### Sempre fazer:
- Preservar o conceito técnico da assertiva original
- Gerar exatamente 5 alternativas (A–E)
- Fundamentar o gabarito com norma, CPC, NBC TA ou princípio técnico
- Usar o erro da assertiva ERRADA como distrator principal
- Emitir flag quando gabarito for inferido
- Variar a posição do gabarito ao longo de blocos de questões
- Explicar brevemente o erro de cada distrator

### Nunca fazer:
- Fabricar normas, artigos ou CPCs inexistentes
- Gerar distratores absurdos ou obviamente errados
- Repetir a assertiva original literalmente no enunciado sem expandi-la
- Omitir o gabarito ou a fundamentação
- Fixar o gabarito sempre na mesma letra em blocos de questões
- Alterar o conceito técnico correto da assertiva original
