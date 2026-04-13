---
name: conversor-cebraspe
description: >
  Converte questões de múltipla escolha (FGV, FCC, VUNESP, ESAF, AOCP e outras bancas)
  em 1 ou 2 assertivas no estilo CEBRASPE/CESPE (Certo ou Errado), preservando o conteúdo
  técnico original e adaptando o enunciado para o padrão assertivo da banca.
  Use esta skill SEMPRE que o usuário pedir para:
  - converter questão de múltipla escolha para certo/errado
  - transformar questão FGV, FCC, VUNESP, ESAF em estilo CESPE ou CEBRASPE
  - adaptar questão de concurso para o formato assertivo
  - reescrever questão A/B/C/D/E no estilo afirmativa única
  - "converta essa questão para CEBRASPE", "transforme em certo/errado", "adapte para CESPE"
  - gerar variações de uma questão no formato afirmativo
  Use mesmo que o usuário não mencione "skill" ou "conversor" explicitamente.
---

# Skill: Conversor de Questões — Múltipla Escolha → Estilo CEBRASPE

## Princípios Fundamentais

| Princípio | Aplicação |
|-----------|-----------|
| **Fidelidade técnica** | O conteúdo e o conceito da questão original são preservados integralmente |
| **Tom assertivo** | A afirmativa substitui a pergunta — o candidato julga verdadeiro ou falso |
| **Economia de palavras** | CEBRASPE é direto; frases longas são cortadas e reescritas em linguagem objetiva |
| **Gabarito fundamentado** | Toda assertiva gerada vem com gabarito (CERTO/ERRADO) e justificativa técnica |
| **Densidade de erro** | Assertivas ERRADAS exploram confusões técnicas reais, não distorções absurdas |

---

## Fase 1 — Recebimento da Questão

O usuário pode fornecer a questão de três formas. A skill identifica automaticamente:

| Forma | Descrição | Ação |
|-------|-----------|------|
| **Questão completa** | Enunciado + alternativas A–E | Processar direto |
| **Enunciado apenas** | Sem alternativas | Solicitar o gabarito ou inferir pelo contexto |
| **Bloco de questões** | 2 ou mais questões em sequência | Converter cada uma individualmente, numerando as assertivas por origem |

> Se o gabarito não for informado, a skill **infere a alternativa correta** pelo raciocínio
> técnico e indica: `[Gabarito inferido — verificar antes de usar]`

---

## Fase 2 — Análise da Questão Original

Antes de converter, a skill classifica internamente a questão:

### 2.1 — Tipo de Enunciado

| Tipo | Padrão Identificado | Estratégia de Conversão |
|------|---------------------|------------------------|
| **Interpretativo** | "De acordo com o CPC X, assinale..." | Transformar a alternativa correta em afirmação direta |
| **Calculativo** | Dados numéricos → pedir valor | Construir assertiva com o valor correto OU com valor errado calibrado |
| **Situação-Problema** | Empresa + eventos + pergunta de resultado | Resumir o contexto e afirmar a conclusão certa ou errada |
| **Proposições (I, II, III)** | Enunciado com itens numerados | Extrair cada proposição como assertiva CEBRASPE independente |
| **Conceitual direto** | Pergunta sobre definição ou classificação | Afirmar o conceito correto ou invertê-lo para ERRADO |
| **Negação ("à exceção de")** | "Assinale o que NÃO é..." | Inverter a lógica: afirmar o incorreto como se fosse correto → assertiva ERRADA |

### 2.2 — Extração do Conteúdo Central

A skill identifica:
- **Conceito-chave**: o que a questão testa (ex: NBC TA 530, método PEPS, lógica condicional)
- **Alternativa correta**: o gabarito informado ou inferido
- **Principal distrator**: a alternativa errada mais sedutora (usada para gerar a 2ª assertiva, quando solicitado)

---

## Fase 3 — Regras de Conversão por Tipo de Questão

### 3.1 — Questão Interpretativa / Normativa

**Questão original (FGV):**
```
De acordo com o CPC 46 – Mensuração do Valor Justo, a mensuração do
valor justo presume que a transação para a venda do ativo ocorre no
mercado principal para o ativo ou, em sua ausência:

(A) em fatos históricos mais recentes.
(B) no mercado mais similar para o ativo.
(C) no mercado mais vantajoso para o ativo.    ← GABARITO
(D) com base nos preços cotados no mercado internacional.
(E) no mercado em que a empresa comprou o bem no passado.
```

**Assertiva CEBRASPE gerada (CERTA):**
```
Questão — CPC 46 / Valor Justo

Conforme o CPC 46, quando não existe mercado principal para determinado
ativo, a mensuração do valor justo presume que a transação ocorre no
mercado mais vantajoso para esse ativo.

( ) CERTO   ( ) ERRADO
```
**Gabarito: CERTO**
**Fundamento: CPC 46 – item 16 e 17 — ausência de mercado principal → mercado mais vantajoso.**

---

**Assertiva CEBRASPE gerada (ERRADA — baseada no principal distrator):**
```
Questão — CPC 46 / Valor Justo

Na ausência de mercado principal, o CPC 46 determina que o valor
justo deve ser mensurado com base em fatos históricos mais recentes
relacionados ao ativo.

( ) CERTO   ( ) ERRADO
```
**Gabarito: ERRADO**
**Fundamento: O CPC 46 não usa fatos históricos como referência subsidiária — usa o mercado mais vantajoso.**

---

### 3.2 — Questão Calculativa / Numérica

**Questão original (FGV):**
```
Uma amostra de valores forneceu os seguintes dados: 2, 5, 5, 6, 6, 7, 7, 10.
A variância amostral é igual a:

(A) 4,5  (B) 5,1  (C) 5,5  (D) 5,8  (E) 6,2
Gabarito: (B) 5,1
```

**Assertiva CEBRASPE gerada (CERTA):**
```
Questão — Estatística / Variância Amostral

Com base na amostra {2, 5, 5, 6, 6, 7, 7, 10}, a variância
amostral calculada é igual a 5,1.

( ) CERTO   ( ) ERRADO
```
**Gabarito: CERTO**
**Fundamento: Média = 6; soma dos quadrados dos desvios = 35,75; variância amostral = 35,75 / 7 ≈ 5,1.**

---

**Assertiva CEBRASPE gerada (ERRADA — valor calibrado):**
```
Questão — Estatística / Variância Amostral

A variância amostral da série {2, 5, 5, 6, 6, 7, 7, 10} é igual
a 5,5, valor obtido dividindo-se a soma dos quadrados dos desvios
pelo número total de observações.

( ) CERTO   ( ) ERRADO
```
**Gabarito: ERRADO**
**Fundamento: O erro está no divisor — variância AMOSTRAL divide por (n−1) = 7, não por n = 8. O valor 5,5 corresponderia à variância populacional.**

---

### 3.3 — Questão com Proposições (I, II, III)

**Questão original (FGV — Auditoria):**
```
Em relação aos testes de observância, analise:

I. Inspeção: verificação de registros, documentos e ativos tangíveis.
II. Observação: acompanhamento de processo quando de sua execução.
III. Investigação e confirmação: obtenção de informações perante pessoas.

Está correto o que se afirma em:
(A) I, somente.  (B) I e II, somente.  (C) I e III, somente.
(D) II e III, somente.  (E) I, II e III.   ← GABARITO
```

**Assertivas CEBRASPE geradas:**

```
Questão 1 — NBC TI 01 / Testes de Observância

A inspeção, como procedimento de auditoria interna, consiste na
verificação de registros, documentos e ativos tangíveis.

( ) CERTO   ( ) ERRADO
```
**Gabarito: CERTO** | *Proposição I — correta conforme NBC TI 01.*

```
Questão 2 — NBC TI 01 / Testes de Observância

A investigação e confirmação, como técnica de auditoria interna,
limita-se à obtenção de informações de fontes internas à entidade,
excluindo pessoas físicas ou jurídicas externas.

( ) CERTO   ( ) ERRADO
```
**Gabarito: ERRADO** | *A norma inclui fontes externas à entidade — a restrição é fabricada.*

---

### 3.4 — Questão de Situação-Problema (BP/DRE/Resultado)

**Regra de Ouro:** Para questões com dados numéricos extensos, a skill **NÃO repete a tabela inteira**. Ela resume o contexto essencial e formula a assertiva com o resultado ou a conclusão.

**Questão original (FGV):**
```
[Balanço Patrimonial com Ativo Circulante: 102.000, Imobilizado: 30.000,
Passivo: 38.000, PL: 106.000]

Após os eventos de janeiro de X1 (pagamento de salários, venda de
estoque por R$50.000, inadimplência 3%, despesas gerais R$5.000,
depreciação e aluguel), o lucro antes do IR é:

(A) R$12.167  (B) R$22.417  (C) R$22.750  (D) R$23.167  (E) R$23.500
Gabarito: (D) R$23.167
```

**Assertiva CEBRASPE gerada (CERTA):**
```
Questão — Contabilidade Geral / Apuração de Resultado

Uma sociedade empresária vendeu seu estoque por R$ 50.000, com
50% à vista e 50% a prazo, e estimou 3% de inadimplência sobre o
valor a prazo. Considerando ainda despesas gerais de R$ 5.000,
depreciação mensal e aluguel proporcional, o lucro antes do IR
apurado no período foi de R$ 23.167.

( ) CERTO   ( ) ERRADO
```
**Gabarito: CERTO**
**Fundamento: Receita líquida R$49.250 (−R$750 PDD) − custos R$20.000 − despesas R$5.000 − depreciação R$833 − aluguel R$1.000 = R$23.167 (aprox.).**

---

### 3.5 — Questão Negativa ("à exceção de" / "NÃO é")

**Regra:** Inverter a lógica. A alternativa que era a resposta correta (o que NÃO se enquadra) vira uma assertiva **ERRADA** — porque o candidato CEBRASPE deve identificar se a afirmação está correta.

**Questão original:**
```
De acordo com a NBC TI 01, devem ser observados os seguintes
procedimentos de auditoria interna, à exceção de um. Assinale-o.

(C) A informação tempestiva é conservadora e livre de erros.   ← GABARITO
```

**Assertiva CEBRASPE gerada (ERRADA):**
```
Questão — NBC TI 01 / Auditoria Interna

Conforme a NBC TI 01, a informação tempestiva deve ser
conservadora e livre de erros.

( ) CERTO   ( ) ERRADO
```
**Gabarito: ERRADO**
**Fundamento: A NBC TI 01 define informação tempestiva como aquela fornecida em tempo hábil — não como "conservadora". "Conservadora" é característica de outro atributo ou de aplicação equivocada.**

---

## Fase 4 — Regras de Redação das Assertivas

### Sintaxe CEBRASPE Padrão

| Elemento | Regra |
|----------|-------|
| **Sujeito** | Sempre explícito. Nunca começar com "Isso", "Esse", "O referido" |
| **Verbo** | Presente do indicativo, voz ativa. Ex: "é", "deve ser", "consiste em", "classifica-se como" |
| **Norma citada** | Referenciar no início da assertiva ou integrada ao sujeito. Ex: "Conforme o CPC 27..." / "De acordo com a NBC TA 530..." |
| **Números e valores** | Sempre por extenso quando ambíguos; em algarismos para cálculos. Ex: "cinco por cento (5%)" ou "R$ 23.167" |
| **Comprimento** | 1 a 3 linhas. Assertivas com mais de 4 linhas devem ser cortadas |
| **Ponto final** | Obrigatório. Toda assertiva CEBRASPE termina com ponto final |

### Fórmulas de Abertura Mais Usadas pela Banca

```
"Conforme o [CPC/NBC TA/Lei], [sujeito] [verbo] [complemento]."
"De acordo com [norma], é correto afirmar que [sujeito] [verbo]."
"[Sujeito] [verbo] [complemento], conforme prevê o [normativo]."
"No contexto da [tema], [afirmativa técnica]."
"O [conceito] pode ser definido como [definição]."
"A [norma] estabelece que [afirmativa]."
"Em auditoria, [afirmativa técnica]."
"[Sujeito], ao [ação], deve [obrigação]."
```

### Palavras e Construções a Evitar

| Evitar | Substituir por |
|--------|---------------|
| "A questão trata de..." | Assertiva direta |
| "Segundo os estudos..." | "Conforme o CPC X..." |
| "É importante notar que..." | Eliminar — ir direto |
| "Pode-se dizer que..." | Afirmar ou negar diretamente |
| "Na visão de especialistas..." | Citar norma |
| Frases com 5+ vírgulas | Dividir em duas assertivas |

---

## Fase 5 — Quantas Assertivas Gerar

| Instrução do Usuário | Comportamento |
|---------------------|---------------|
| Não especificou | Gerar **2 assertivas**: 1 CERTA + 1 ERRADA |
| "1 assertiva" | Gerar apenas a **CERTA** (baseada no gabarito) |
| "2 assertivas" | 1 CERTA (gabarito) + 1 ERRADA (principal distrator ou erro calibrado) |
| "variações" ou "banco" | Gerar até **4 assertivas** por questão: 2 CERTAS + 2 ERRADAS |
| Bloco de questões | Converter cada questão individualmente, sequenciando Q1a, Q1b, Q2a, Q2b... |

---

## Fase 6 — Formato de Saída

### Saída padrão (1 questão → 2 assertivas)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔁 CONVERSÃO — Questão [N] | [TÓPICO]
Banca original: [FGV / FCC / ESAF / outra]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ASSERTIVA 1 — Estilo CEBRASPE

[Texto da assertiva.]

( ) CERTO   ( ) ERRADO

▸ Gabarito: CERTO / ERRADO
▸ Fundamento: [Norma + raciocínio técnico]

---

ASSERTIVA 2 — Estilo CEBRASPE

[Texto da assertiva.]

( ) CERTO   ( ) ERRADO

▸ Gabarito: CERTO / ERRADO
▸ Fundamento: [Norma + raciocínio técnico]
▸ Erro explorado: [Qual confusão técnica foi usada para torná-la errada]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Saída em bloco (múltiplas questões)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 BANCO DE ASSERTIVAS — [DISCIPLINA]
[N] questões convertidas → [N×2] assertivas
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q1a | [TÓPICO] — [Assertiva]
( ) CERTO   ( ) ERRADO
▸ CERTO | [Fundamento]

Q1b | [TÓPICO] — [Assertiva]
( ) CERTO   ( ) ERRADO
▸ ERRADO | [Fundamento + Erro explorado]

[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GABARITO RESUMIDO
Q1a: C | Q1b: E | Q2a: C | Q2b: E ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Fase 7 — Alertas e Flags

A skill emite os seguintes alertas ao final de cada conversão:

| Flag | Quando emitir |
|------|--------------|
| `[Gabarito inferido]` | Usuário não informou o gabarito — skill deduziu pelo contexto |
| `[Verificar cálculo]` | Questão numérica com dados complexos — conferir antes de usar |
| `[Assertiva longa]` | Assertiva gerada com mais de 3 linhas — considerar enxugar |
| `[Norma não identificada]` | Questão sem referência normativa clara — fundamento pode ser genérico |
| `[Proposição extraída]` | Assertiva derivada de um item (I, II, III) da questão original |

---

## Regras Finais de Comportamento

### Sempre fazer:
- Preservar o conteúdo técnico original — nunca alterar o conceito testado
- Citar a norma ou fundamento legal na assertiva ou no fundamento
- Gerar pelo menos 1 assertiva CERTA e 1 ERRADA por padrão
- Indicar o gabarito logo após cada assertiva
- Fundamentar tecnicamente cada gabarito
- Emitir o flag `[Gabarito inferido]` quando o gabarito não foi fornecido
- Formatar a saída com separadores visuais e rótulos claros

### Nunca fazer:
- Fabricar normas, CPCs, NBCs ou artigos inexistentes no fundamento
- Reproduzir a questão original integralmente na assertiva — sempre reescrever
- Gerar assertiva ERRADA com erro absurdo que qualquer candidato descartaria
- Omitir o gabarito de qualquer assertiva gerada
- Alterar o conceito técnico correto testado pela questão original
- Repetir o mesmo erro em todas as assertivas ERRADAS de um bloco
