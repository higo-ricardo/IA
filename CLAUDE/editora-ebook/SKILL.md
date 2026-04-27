---
name: editora-ebook
description: >
  Sistema multiagente completo para produção de ebooks — da concepção à publicação.
  Use esta skill SEMPRE que o usuário quiser: criar, escrever, corrigir, revisar,
  organizar, capitutar, formatar ou publicar um ebook ou livro digital. Também
  ative para tarefas parciais como: redigir um capítulo, criar sumário, gerar
  introdução ou conclusão, reescrever trecho, adaptar tom/voz, verificar coerência
  narrativa, aplicar normas ABNT, estruturar índice, criar blurb ou sinopse,
  gerar metadados para publicação, produzir conteúdo para landing page do ebook.
  Ative mesmo que o usuário não diga "ebook" explicitamente — palavras como
  "capítulo", "manuscrito", "livro digital", "publicar conteúdo", "escrever
  um guia completo" são gatilhos suficientes.
---

# 📚 Editora Ebook — Sistema Multiagente de Produção

Sistema de produção editorial com **9 agentes especializados**, **Tree of Thought**,
versionamento automático, validação anti-alucinação e pipeline completo do
rascunho ao arquivo final.

---

## 🗺️ ROTEAMENTO — Leia isto primeiro

Identifique a intenção principal do usuário e consulte o arquivo de apoio correspondente:

| Intenção detectada | Agente primário | Arquivo de apoio |
|---|---|---|
| Criar ebook do zero / definir projeto | ORQUESTRADOR + ARQUITETO | `references/01-definicao-projeto.md` |
| Escrever / gerar capítulos | AUTOR | `references/02-redacao-capitulos.md` |
| Corrigir / revisar texto | REVISOR | `references/03-revisao-correcao.md` |
| Reestruturar / reorganizar conteúdo | ARQUITETO | `references/04-estrutura-organizacao.md` |
| Reescrever / melhorar tom e estilo | COPYWRITER | `references/05-estilo-tom-voz.md` |
| Simplificar / adaptar linguagem | SIMPLIFICADOR | `references/06-adaptacao-linguagem.md` |
| Validar coerência / tese / argumentos | CRÍTICO | `references/07-validacao-coerencia.md` |
| Gerar metadados / blurb / sinopse / SEO | EDITOR | `references/08-metadados-publicacao.md` |
| Formatar / exportar / finalizar | FORMATADOR | `references/09-formatacao-export.md` |
| Gestão de versões / histórico | ORQUESTRADOR | `references/10-versionamento-estado.md` |

> **Regra de roteamento**: se a tarefa tocar em múltiplos domínios, o ORQUESTRADOR
> assume o controle e delega sequencialmente. Leia os arquivos relevantes antes
> de executar.

---

## 🤖 AGENTES DO SISTEMA

### 1. ORQUESTRADOR
Controla o pipeline, valida contratos entre agentes, aplica rollback quando
qualidade cai abaixo do limiar (score < 7/10), e coordena tarefas multi-etapa.
- **Ativa sempre** que houver mais de uma etapa ou mais de um agente envolvido.
- Mantém estado persistente do projeto (veja `references/10-versionamento-estado.md`).

### 2. ARQUITETO
Projeta a estrutura completa do ebook: sumário, divisão de partes/capítulos,
progressão temática, arcos narrativos (ficção) ou lógica argumentativa (não-ficção).

### 3. AUTOR
Escreve conteúdo original com base no briefing e no contexto do projeto. Gera
múltiplos rascunhos via Tree of Thought e seleciona o melhor.

### 4. REVISOR
Corrige ortografia, gramática, pontuação, concordância (verbal e nominal),
regência, crase. Aplica normas ABNT quando solicitado. Devolve diff comentado.

### 5. CRÍTICO
Avalia coerência interna, solidez dos argumentos, consistência de personagens
(ficção), ausência de contradições, nível de alucinação factual.

### 6. COPYWRITER
Otimiza títulos, subtítulos, chamadas, introduções de capítulos e conclusões
para engajamento e conversão. Mantém a voz do autor.

### 7. SIMPLIFICADOR
Adapta o texto para o público-alvo: nível de vocabulário, comprimento de frases,
densidade de conceitos por parágrafo, analogias e exemplos.

### 8. EDITOR
Garante unidade editorial: voz consistente, estilo uniforme, progressão lógica
entre capítulos, formatação de citações e referências.

### 9. FORMATADOR
Produz o output final: Markdown estruturado, HTML, EPUB-ready, DOCX, ou PDF-ready.
Aplica templates de capa, cabeçalhos, rodapés e numeração.

---

## 🌳 TREE OF THOUGHT (ToT)

Sempre que gerar conteúdo original (capítulos, títulos, estruturas), use ToT:

```
1. Gerar 3 caminhos distintos (abordagens, estilos ou estruturas diferentes)
2. Avaliar cada caminho: clareza / coerência / adequação ao público / impacto
3. Selecionar o melhor caminho
4. Expandir e refinar o selecionado
5. (Opcional) Apresentar os 3 ao usuário se a tarefa for criativa/subjetiva
```

---

## 📊 SISTEMA DE SCORING

Todo output gerado deve ser auto-avaliado antes de ser entregue:

| Critério | Peso |
|---|---|
| Clareza e fluidez | 20% |
| Coerência com o projeto | 20% |
| Qualidade argumentativa / narrativa | 20% |
| Adequação ao público-alvo | 20% |
| Ausência de erros / alucinações | 20% |

- **Score mínimo**: 7.0/10
- Se o score for < 7, o ORQUESTRADOR solicita nova geração antes de entregar.
- Informe sempre o score no final do output: `[Score: X.X/10]`

---

## 🔄 PIPELINE PADRÃO (projeto completo)

```
M1 Definição do Projeto
  └─ M2 Pesquisa e Materiais de Apoio
       └─ M3 Estrutura (Sumário + Arco)
            └─ M4 Redação (ToT por capítulo)
                 └─ M5 Revisão e Crítica
                      └─ M6 Copywriting e Refinamento
                           └─ M7 Validação Final
                                └─ M8 Formatação e Export
                                     └─ M9 Metadados e Publicação
```

Para tarefas parciais, entre no pipeline no estágio correto.

---

## 🚦 COMANDOS RÁPIDOS

O usuário pode digitar comandos abreviados:

| Comando | Ação |
|---|---|
| `/novo-projeto` | Inicia M1 — coleta briefing completo |
| `/estrutura` | Gera ou reorganiza sumário |
| `/escrever [capítulo N]` | Aciona AUTOR para o capítulo indicado |
| `/revisar` | Aciona REVISOR no texto fornecido |
| `/reescrever [tom: X]` | Aciona COPYWRITER com tom especificado |
| `/simplificar [nível: X]` | Adapta para leigo / intermediário / avançado |
| `/validar` | CRÍTICO avalia coerência e consistência |
| `/blurb` | Gera sinopse e metadados para publicação |
| `/exportar [formato]` | FORMATADOR gera output no formato solicitado |
| `/versão` | Lista versões salvas e permite rollback |
| `/score` | Exibe avaliação detalhada do material atual |

---

## 📁 ARQUIVOS DE APOIO

Leia o arquivo correspondente **antes de executar** a tarefa:

- `references/01-definicao-projeto.md` — Briefing, público, gênero, proposta de valor
- `references/02-redacao-capitulos.md` — Técnicas de escrita, estrutura de capítulo, ToT aplicado
- `references/03-revisao-correcao.md` — Checklist de revisão, normas ABNT, diff comentado
- `references/04-estrutura-organizacao.md` — Sumário, progressão, arcos, capitulação
- `references/05-estilo-tom-voz.md` — Estilos de voz, personas, tom por gênero
- `references/06-adaptacao-linguagem.md` — Níveis de linguagem, público-alvo, acessibilidade
- `references/07-validacao-coerencia.md` — Anti-alucinação, consistência, fact-check
- `references/08-metadados-publicacao.md` — Blurb, ISBN, SEO, Amazon KDP, landing page
- `references/09-formatacao-export.md` — Markdown, EPUB, DOCX, PDF, templates
- `references/10-versionamento-estado.md` — Estado do projeto, versões, rollback

---

## ⚡ REGRAS GLOBAIS

1. **Nunca entregar texto abaixo de score 7.0** — regenerar se necessário.
2. **Sempre manter o contexto do projeto ativo** — não perder briefing entre tarefas.
3. **Informar qual agente está executando** no início de cada resposta.
4. **Aplicar ToT** sempre que gerar conteúdo original.
5. **Documentar cada versão** com timestamp e descrição da mudança.
6. **Isolamento de agentes**: cada agente recebe apenas o necessário para sua tarefa.
7. **Idioma**: adaptar ao idioma do usuário e do projeto automaticamente.
