# Skill: portugues-concursos

Agente gerador de questões de **Língua Portuguesa para concursos públicos**, com níveis fácil, médio e difícil. Baseado em padrões das bancas CESPE/CEBRASPE, FCC, VUNESP, FGV e IBFC.

---

## Instalação

1. Abra o Claude (claude.ai)
2. Vá em **Configurações → Skills**
3. Faça upload do arquivo `portugues-concursos.skill`
4. A skill estará disponível automaticamente nas conversas

---

## Temas Cobertos (15 temas)

| # | Tema | Arquivo de referência |
|---|---|---|
| 01 | Análise Sintática | `references/01-analise-sintatica.md` |
| 02 | Correlação de Tempos e Modos Verbais | `references/02-tempos-verbais.md` |
| 03 | Voz Verbal (ativa ↔ passiva) | `references/03-voz-verbal.md` |
| 04 | Figuras de Linguagem | `references/04-figuras-linguagem.md` |
| 05 | Paráfrase e Inferência Textual | `references/05-parafrases-inferencia.md` |
| 06 | Concordância Verbal e Nominal | `references/06-concordancia.md` |
| 07 | Regência Verbal e Nominal | `references/07-regencia.md` |
| 08 | Crase | `references/08-crase.md` |
| 09 | Pontuação | `references/09-pontuacao.md` |
| 10 | Coesão e Coerência Textual | `references/10-coesao-coerencia.md` |
| 11 | Ortografia e Acentuação Gráfica | `references/11-ortografia-acentuacao.md` |
| 12 | Orações Subordinadas | `references/12-orações-subordinadas.md` |
| 13 | Orações Coordenadas | `references/13-orações-coordenadas.md` |
| 14 | Sinonímia, Antonímia e Polissemia | `references/14-sinonimia-antonimia.md` |
| 15 | Funções da Linguagem e Tipologia Textual | `references/15-funcoes-linguagem.md` |

---

## Como Usar

A skill é ativada automaticamente ao mencionar qualquer um dos termos:

> *questões de português, treinar português, simulado de português, concurso público, gramática, análise sintática, tempos verbais, voz passiva, figuras de linguagem, paráfrase, inferência, concordância, regência, crase, pontuação, coesão, coerência, ortografia, acentuação*

**Exemplos de prompts:**

- `"Quero treinar 10 questões de análise sintática nível médio"`
- `"Gere questões de voz passiva estilo CESPE"`
- `"Simulado misto de português, 15 questões, nível difícil"`
- `"Questões sobre correlação de tempos verbais para concurso"`

---

## Níveis de Dificuldade

| Nível | Características |
|---|---|
| 🟢 **Fácil** | Frase curta, uma regra, distratores com erros grosseiros |
| 🟡 **Médio** | Estrutura complexa, duas regras interagindo, distratores sutis |
| 🔴 **Difícil** | Período composto, múltiplas regras, exceções e casos especiais |
| 🎲 **Misto** | Alternância automática de níveis |

---

## Formatos de Questão

- **Certo/Errado** — padrão CESPE/CEBRASPE
- **Múltipla escolha A–E** — padrão FCC, VUNESP, FGV
- **Reescrita/Transformação** — voz passiva, paráfrase

---

## Funcionalidades

- Feedback imediato com explicação gramatical e indicação do erro comum
- Relatório final com diagnóstico por tema
- Confidence Score em cada questão (mínimo 6/10)
- Sugestão de próximo tema com base no desempenho

---

## Base de Conhecimento

O arquivo `references/02-tempos-verbais.md` incorpora o mapa mental de **Correlação de Tempos e Modos Verbais** fornecido pelo usuário, incluindo as 3 regras condicionais, padrões de ouro e erros clássicos de prova.

---

## Versão

**v1.0** — Abril 2026  
15 temas · 3 níveis · Padrão CESPE/FCC/VUNESP/FGV · PT-BR
