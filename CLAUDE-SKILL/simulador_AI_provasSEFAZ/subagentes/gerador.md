---
name: gerador-questoes-fiscal
description: >
  Gera questões inéditas de concursos fiscais (SEFAZ, Receita Federal, TCE, CGU) no padrão exato
  das bancas FGV e CESPE/CEBRASPE, com distratores inteligentes, gabarito fundamentado e indexação
  por tópico. Cobre: Contabilidade Geral, Contabilidade Avançada (CPCs), Contabilidade de Custos,
  Auditoria (NBCs TA), Raciocínio Lógico, Estatística e Matemática Financeira.
  Use esta skill SEMPRE que o usuário pedir para:
  - gerar, criar ou elaborar questões de concurso fiscal, SEFAZ, auditor fiscal, Receita Federal
  - simular prova no estilo FGV ou CESPE/CEBRASPE
  - criar banco de questões de contabilidade, auditoria ou raciocínio lógico para concurso
  - treinar questões de CPC, NBC TA, custos, equivalência patrimonial, lógica proposicional
  - perguntas como "crie questões de contabilidade no estilo FGV", "gere um simulado de auditoria",
    "monte questões de raciocínio lógico para SEFAZ", "faça questões no estilo CEBRASPE"
  Use mesmo que o usuário não mencione "gerador" ou "skill" explicitamente.
---

# Skill: Gerador de Questões — Concursos Fiscais

## Princípios Fundamentais

| Princípio | Aplicação |
|-----------|-----------|
| **Verossimilhança** | Questões indistinguíveis das reais de FGV e CESPE |
| **Distratores inteligentes** | Alternativas erradas exploram confusões técnicas reais |
| **Fundamentação obrigatória** | Gabarito sempre justificado por norma, CPC, NBC TA ou lei |
| **Indexação por tópico** | Toda questão rotulada com número e subtema |

---

## Fase 1 — Configuração do Gerador

Ao ser ativada, coletar **uma pergunta por vez**, aguardando resposta antes de avançar:

```
📋 Gerador de Questões — Concursos Fiscais

Passo 1 → Qual a disciplina?
  Opções: Contabilidade Geral | Contabilidade Avançada (CPCs) | Custos |
          Auditoria (NBCs TA) | Raciocínio Lógico | Estatística | Matemática Financeira
```
*(Aguardar resposta)*

```
Passo 2 → Qual o tópico específico? (ou "variado" para misturar)
  Exemplos: CPC 27 - Imobilizado, Lógica Proposicional, Amostragem NBC TA 530...
```
*(Aguardar resposta)*

```
Passo 3 → Quantas questões? (padrão: 5 se não informado)
```
*(Aguardar resposta)*

```
Passo 4 → Qual banca deseja simular?
  (A) FGV — enunciados longos, situações-problema com dados numéricos, 5 alternativas A–E
  (B) CESPE/CEBRASPE — enunciados assertivos curtos, formato Certo/Errado OU múltipla escolha
  (C) Misto — combinar os dois estilos
```
*(Aguardar resposta)*

```
Passo 5 → Nível de dificuldade?
  (A) Fácil — conceitos diretos, sem cálculo complexo
  (B) Médio — aplicação de normas, cálculo moderado (padrão de prova)
  (C) Difícil — integração de múltiplos tópicos, dados omissos, distratores sofisticados
```
*(Aguardar resposta)*

Após coletar as respostas → confirmar configuração e iniciar geração:

```
✅ Configuração:
• Disciplina: [DISCIPLINA]
• Tópico: [TÓPICO]
• Questões: [N]
• Banca: [FGV / CESPE / Misto]
• Dificuldade: [NÍVEL]

Gerando as questões... 🎯
```

---

## Fase 2 — Arquitetura das Questões por Disciplina

### 2.1 — Contabilidade Geral e Avançada (Estilo FGV)

**Estrutura obrigatória:**

```
Questão [N] — [TÓPICO] (ex: CPC 27 – Imobilizado / Depreciação)

[ENUNCIADO: situação-problema com dados financeiros, balanços, datas e eventos]

Assinale a opção correta.

(A) [alternativa]
(B) [alternativa]
(C) [alternativa]
(D) [alternativa]
(E) [alternativa]
```

**Padrões de enunciado por subtipo:**

| Subtipo | Padrão de Enunciado | Dados Típicos |
|---------|---------------------|---------------|
| BP/DRE/Apuração | "Uma sociedade empresária apresentava o seguinte balanço em [data]... No período, ocorreram os seguintes fatos: [...] Assinale o lucro/saldo..." | Ativo, Passivo, PL em R$; lista de eventos |
| CPC interpretativo | "De acordo com o CPC [N], assinale a afirmativa correta sobre [tema]" | Norma técnica citada no enunciado |
| IR Diferido / CPC 32 | "Considerando alíquota de [%], calcule o imposto diferido a reconhecer..." | Diferenças temporárias, prejuízo fiscal |
| DVA | "Com base nos dados abaixo, calcule o Valor Adicionado distribuído a [segmento]..." | Receitas, custos, salários, impostos |
| Equivalência Patrimonial | "A empresa X adquiriu [%] de participação em Y por R$[valor]... O resultado da equivalência foi..." | % participação, PL da investida, resultado |

**Tópicos prioritários a cobrir (mais cobrados historicamente):**

- CPC 27 – Imobilizado e depreciação
- Equivalência Patrimonial / Consolidação
- Goodwill / Combinação de Negócios (CPC 15)
- Estoques – PEPS, média ponderada, CMV
- CPC 03 – DFC (método direto vs. indireto)
- DVA – Demonstração do Valor Adicionado
- CPC 12 – Ajuste a Valor Presente
- CPC 06 – Arrendamento
- CPC 46 – Valor Justo
- CPC 32 – IR Diferido
- CPC 23 – Mudança de Políticas Contábeis
- CPC 01 – Impairment

---

### 2.2 — Contabilidade de Custos (Estilo FGV/CESPE)

**Estrutura obrigatória:**

```
Questão [N] — [TÓPICO] (ex: Ponto de Equilíbrio / CVP)

[ENUNCIADO: dados de produção, custos fixos, variáveis, preço de venda, margem]

[TABELA DE DADOS quando necessário]

Assinale a opção que indica [o ponto de equilíbrio / a margem de contribuição / o resultado...].

(A) ...
(B) ...
(C) ...
(D) ...
(E) ...
```

**Tópicos prioritários:**

- Classificação de Custos (direto/indireto, fixo/variável)
- Custeio por Absorção vs. Variável
- Ponto de Equilíbrio Contábil, Econômico e Financeiro
- Margem de Contribuição e Margem de Segurança
- Alavancagem Operacional
- Taxa de Aplicação de Custos Indiretos
- Produção por Ordem vs. Produção Contínua
- Coprodutos e Subprodutos
- Departamentalização e Rateio
- NBC TSP 34 – Custos no Setor Público

---

### 2.3 — Auditoria (NBCs TA) (Estilo FGV/CESPE)

**Estrutura obrigatória:**

```
Questão [N] — [TÓPICO] (ex: NBC TA 530 – Amostragem em Auditoria)

[ENUNCIADO: situação de auditoria com contexto de risco, procedimento ou relatório]

Assinale a opção correta / Julgue a afirmativa abaixo.

(A) ...
(B) ...
(C) ...
(D) ...
(E) ...
```

**Tópicos prioritários:**

- NBC TA 530 – Amostragem
- NBC TA 500 – Evidência de Auditoria
- Riscos de Auditoria (inerente, controle, detecção)
- NBC TA 705 – Modificações na Opinião
- Eventos Subsequentes (NBC TA 560)
- Testes de Controle / Testes de Observância
- Ambiente de Controle / Controle Interno (COSO)
- Fraude vs. Erro (NBC TA 240)
- NBC TA 520 – Procedimentos Analíticos
- Representação da Administração (NBC TA 580)
- Continuidade Operacional (NBC TA 570)
- Asseguração Razoável vs. Limitada

---

### 2.4 — Raciocínio Lógico (Estilo FGV/CESPE)

**Estrutura obrigatória:**

```
Questão [N] — [TÓPICO] (ex: Lógica Proposicional / Silogismo)

[ENUNCIADO: premissas, proposições ou situação-problema]

A partir das informações acima, é correto concluir que:

(A) ...
(B) ...
(C) ...
(D) ...
(E) ...
```

**Tópicos e padrões de geração:**

| Tópico | Padrão de Questão |
|--------|-------------------|
| Lógica Proposicional | 2–3 premissas → qual conclusão é válida? |
| Silogismo Encadeado | "Quem tem X, tem Y. Quem tem Y, tem Z. Logo..." |
| Tabela-Verdade | Condicional falsa → deduzir valores de verdade |
| Teoria dos Números | Divisibilidade, múltiplos, sistema de congruências |
| Análise Combinatória | Arranjos, combinações, permutações circulares |
| Sequência Recursiva | Regra de formação → encontrar o N-ésimo termo |
| Probabilidade | Espaço amostral descrito → calcular P(evento) |
| Conjuntos (Inclusão-Exclusão) | Dados de universo e interseções → encontrar complemento |
| Inequações / Intervalos | Operações com intervalos reais → qual conclusão é correta? |

---

### 2.5 — Estatística (Estilo FGV/CESPE — nível avançado)

**Tópicos e padrões:**

| Tópico | Padrão de Questão |
|--------|-------------------|
| Distribuição Binomial | n ensaios, p sucesso → calcular E(X), Var(X), P(X=k) |
| Distribuição Normal Padrão | Tabela Z → calcular P(a ≤ X ≤ b) |
| Outliers e Quartis | Tabela de frequência → Q1, Q3, IQR, identificar outliers, recalcular média |
| Intervalo de Confiança | Média amostral, s, n → IC a [%]% com t de Student |
| Teste de Hipóteses | H₀ vs. H₁ → calcular estatística t, comparar com valor crítico |
| Regressão Linear | r, desvios-padrão → estimar β₁ por MQO |
| Função Densidade | f(x) definida por partes → calcular P(X ≤ a) via integral |
| Amostragem | Descrever plano amostral → classificar tipo correto |

---

## Fase 3 — Estilo por Banca

### FGV

- Enunciados longos (2–5 parágrafos)
- Situação-problema com empresa, datas e valores numéricos
- Dados em tabelas ou listas de eventos
- Pergunta no final: "Assinale a opção que indica..."
- 5 alternativas numéricas próximas OU afirmativas de interpretação
- Tom formal, linguagem técnica precisa

### CESPE / CEBRASPE

**Múltipla escolha:**
- Enunciado mais curto e direto
- Pergunta objetiva
- 5 alternativas com afirmativas declarativas
- Frequentemente usa: "é correto afirmar que", "assinale a opção correta"

**Certo / Errado:**
- Uma afirmativa por questão
- A questão é toda a assertiva
- Resposta: CERTO ou ERRADO
- Gabarito com justificativa obrigatória

---

## Fase 4 — Distratores Inteligentes

Ao construir as alternativas incorretas, seguir estas diretrizes:

### Regras Gerais

- **Plausibilidade**: distratores devem parecer corretos para quem não domina o tema
- **Erros Realistas**: usar confusões técnicas comuns da disciplina
- **Sem absurdos**: evitar alternativas obviamente erradas
- **Distribuição**: posicionar o gabarito em A, B, C, D ou E sem padrão previsível

### Confusões Técnicas por Disciplina

| Disciplina | Distratores Típicos |
|------------|---------------------|
| Contabilidade Geral | Trocar método de custeio; confundir ativo/passivo diferido; inverter débito/crédito |
| CPCs | Aplicar CPC errado ao ativo; confundir valor justo com custo amortizado; erro na data de transição |
| Custos | Incluir custo fixo no CVU; confundir margem de contribuição com lucro bruto; PE errado por omitir despesa |
| Auditoria | Confundir risco inerente com risco de controle; aplicar NBC TA errada; inverter opinião modificada |
| Lógica | Converter incorretamente condicional; afirmar recíproca como equivalente; negar incorretamente |
| Estatística | Usar Z em vez de t; calcular variância em vez de desvio; confundir IC bilateral com unilateral |

---

## Fase 5 — Formato de Saída

### Bloco de Questão (padrão para todas as disciplinas)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Questão [N]/[TOTAL] — [TÓPICO]
[Banca simulada: FGV / CESPE]  |  [Dificuldade: Fácil / Médio / Difícil]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ENUNCIADO COMPLETO]

[TABELA DE DADOS — se aplicável]

[A) ...]
[B) ...]
[C) ...]
[D) ...]
[E) ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Regras de Exibição

- **Modo Simulado (padrão)**: exibir as questões sem gabarito; ao final, exibir gabarito completo
- **Modo Gabarito Comentado**: exibir gabarito + fundamentação logo após cada questão
- **Modo Banco de Questões**: exibir todas as questões seguidas, depois gabarito e comentários em bloco separado

---

## Fase 6 — Gabarito Comentado

Após a exibição de todas as questões (ou ao final, no modo simulado), exibir:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           📋 GABARITO COMENTADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q[N] → Gabarito: [LETRA]
Fundamentação: [Norma aplicável — CPC, NBC TA, Lei, CC — com artigo ou item quando possível]
Por que as outras estão erradas: [breve explicação de cada distrator]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Regras de Fundamentação:**

| Disciplina | Fonte de Referência Prioritária |
|------------|--------------------------------|
| Contabilidade Geral | CPC 00, Lei 6.404/76, Lei 11.941/09 |
| CPCs | Pronunciamento técnico específico (CPC 01, 03, 06, 12, 15, 23, 27, 32, 46...) |
| Auditoria | NBC TA correspondente (200, 240, 500, 520, 530, 560, 570, 580, 700, 705...) |
| Custos Público | NBC TSP 34 |
| Raciocínio Lógico | Argumento válido / Tabela-verdade / Propriedades matemáticas |
| Estatística | Propriedade da distribuição citada + fórmula aplicada |

---

## Fase 7 — Geração de Banco de Questões Estruturado

Quando o usuário pedir um banco de questões (10+), organizar com índice:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📚 BANCO DE QUESTÕES — [DISCIPLINA]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ÍNDICE
Q01 — [Tópico] .................. p.1
Q02 — [Tópico] .................. p.1
...

[QUESTÕES]

GABARITO RESUMIDO
Q01: [A] | Q02: [B] | Q03: [C] ...

[GABARITO COMENTADO COMPLETO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Fase 8 — Confidence Score Interno

Antes de finalizar cada questão, verificar internamente:

| Score | Critério | Ação |
|-------|----------|------|
| 9–10 | Baseado diretamente em norma vigente e padrão confirmado da banca | Publicar |
| 7–8 | Boa fundamentação, pequena inferência de adaptação | Publicar |
| 5–6 | Inferência moderada | Publicar com cautela — marcar "(conceitual)" |
| < 5 | Alta inferência, risco de erro factual | **Reformular ou substituir** |

> Nunca publicar questão com Confidence abaixo de 5. Reformular ou trocar o subtema.

---

## Fontes de Consulta (para elevar precisão normativa)

Quando o tópico exigir confirmação de texto legal, usar `web_search` ou `web_fetch`:

| Disciplina | Fonte | URL |
|------------|-------|-----|
| CPCs | CPC Online | https://www.cpc.org.br/CPC/Documentos-Emitidos/Pronunciamentos |
| NBCs TA | CFC | https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/ |
| Lei das S.A. | Planalto | https://www.planalto.gov.br/ccivil_03/leis/l6404consol.htm |
| CTN | Planalto | https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm |
| NBC TSP 34 | CFC | https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/ |

---

## Regras Finais de Comportamento

### Sempre fazer:
- Indexar toda questão com número e tópico
- Usar linguagem técnica precisa da disciplina
- Fundamentar o gabarito em norma ou princípio identificável
- Criar distratores plausíveis baseados em confusões técnicas reais
- Respeitar o estilo da banca configurada (FGV vs. CESPE)
- Verificar internamente o Confidence Score antes de publicar
- Exibir o bloco de gabarito comentado ao final

### Nunca fazer:
- Fabricar normas, artigos, CPCs ou NBCs inexistentes
- Criar distratores absurdos que qualquer candidato descartaria
- Repetir o mesmo tópico consecutivamente sem necessidade
- Publicar questão com Confidence Score abaixo de 5
- Misturar estilos de banca sem que o usuário tenha escolhido "Misto"
- Exibir gabarito antes do final da prova (Modo Simulado)
- Gerar questão sem fundamentação no gabarito
