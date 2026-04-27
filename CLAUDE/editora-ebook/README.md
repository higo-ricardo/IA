# 📚 Editora Ebook — Skill para Claude

Sistema multiagente completo de produção editorial para ebooks, do briefing à publicação.

---

## Instalação

1. Acesse **claude.ai → Settings → Skills**
2. Clique em **"Install Skill"**
3. Faça upload do arquivo `editora-ebook.skill`
4. Confirme a instalação

---

## O que esta skill faz

Transforma o Claude em uma **editora completa com 9 agentes especializados**,
capaz de cobrir todo o ciclo de produção de um ebook:

| Agente | Responsabilidade |
|---|---|
| **ORQUESTRADOR** | Controla o pipeline, versões e rollback |
| **ARQUITETO** | Estrutura, sumário, progressão temática |
| **AUTOR** | Redação original com Tree of Thought |
| **REVISOR** | Correção ortográfica, gramatical e ABNT |
| **CRÍTICO** | Coerência, anti-alucinação, consistência |
| **COPYWRITER** | Títulos, ganchos, tom e engajamento |
| **SIMPLIFICADOR** | Adaptação por nível de público |
| **EDITOR** | Unidade editorial e voz consistente |
| **FORMATADOR** | Export em Markdown, EPUB, DOCX, PDF |

---

## Comandos Rápidos

| Comando | Ação |
|---|---|
| `/novo-projeto` | Inicia o briefing completo |
| `/estrutura` | Gera ou reorganiza o sumário |
| `/escrever [capítulo N]` | Escreve o capítulo indicado |
| `/revisar` | Revisa o texto fornecido |
| `/reescrever [tom: X]` | Reescreve com novo tom |
| `/simplificar [nível: X]` | Adapta a linguagem ao público |
| `/validar` | Verifica coerência e consistência |
| `/blurb` | Gera sinopse e metadados |
| `/exportar [formato]` | Formata para EPUB, PDF, DOCX... |
| `/versão` | Lista versões e permite rollback |
| `/score` | Avalia o material atual (0-10) |
| `/salvar-estado` | Exporta estado para retomar depois |

---

## Estrutura de Arquivos

```
editora-ebook/
├── SKILL.md                          ← Roteador principal
├── README.md                         ← Este arquivo
├── agents/
│   └── critico.md                    ← Persona do agente Crítico
├── references/
│   ├── 01-definicao-projeto.md       ← Briefing e proposta de valor
│   ├── 02-redacao-capitulos.md       ← Técnicas de escrita e ToT
│   ├── 03-revisao-correcao.md        ← Checklist revisão e ABNT
│   ├── 04-estrutura-organizacao.md   ← Modelos de sumário e arco
│   ├── 05-estilo-tom-voz.md          ← Estilos, tons e ghostwriting
│   ├── 06-adaptacao-linguagem.md     ← Níveis de público e analogias
│   ├── 07-validacao-coerencia.md     ← Anti-alucinação e consistência
│   ├── 08-metadados-publicacao.md    ← Blurb, KDP, landing page
│   ├── 09-formatacao-export.md       ← Markdown, EPUB, DOCX, PDF
│   └── 10-versionamento-estado.md    ← Controle de versões e rollback
└── templates/
    └── capitulos-e-estruturas.md     ← Templates prontos para uso
```

---

## Como usar — Exemplos

### Começar um ebook do zero
```
/novo-projeto
```
O Claude vai coletar o briefing completo e gerar o Documento de Projeto.

### Escrever apenas um capítulo
```
Escreva o Capítulo 3 sobre gestão do tempo para um público iniciante,
tom conversacional, com exemplos práticos.
```

### Revisar um texto existente
```
/revisar

[cole seu texto aqui]
```

### Gerar materiais de venda
```
/blurb

Meu ebook é sobre produtividade para mães empreendedoras...
```

### Retomar um projeto
```
/retomar-projeto

[cole o Bloco de Estado salvo anteriormente]
```

---

## Sistema de Scoring

Todo conteúdo gerado é auto-avaliado antes da entrega:

| Critério | Peso |
|---|---|
| Clareza e fluidez | 20% |
| Coerência com o projeto | 20% |
| Qualidade argumentativa/narrativa | 20% |
| Adequação ao público-alvo | 20% |
| Ausência de erros/alucinações | 20% |

**Score mínimo para entrega: 7.0/10.**
Se o conteúdo não atingir esse limiar, o sistema regenera automaticamente.

---

## Funcionalidades Avançadas

- 🌳 **Tree of Thought** — gera 3 abordagens e seleciona a melhor para cada capítulo
- 👻 **Modo Fantasma** — detecta sua voz autoral e escreve no seu estilo
- 📊 **Análise de Legibilidade** — índice Flesch adaptado para português
- 🔄 **Versionamento com Rollback** — histórico completo de alterações
- 🎨 **Prompt de Capa** — gera prompt para Midjourney/DALL-E/Stable Diffusion
- 🛒 **Copy de Vendas** — blurb, landing page e metadados para KDP/Hotmart
- 📐 **Calculadora de Equilíbrio** — detecta capítulos desproporcionais
- 🔍 **Análise de Gap** — identifica lacunas no conteúdo planejado

---

## Compatibilidade

- ✅ Claude Sonnet (recomendado)
- ✅ Claude Opus
- ✅ Português e outros idiomas (auto-detectado)
- ✅ Ficção e não-ficção
- ✅ Ebooks curtos (10p) a longos (300p+)

---

## Versão

**v1.0** — Abril 2026  
Criado com o sistema de Skills do Claude (claude.ai)
