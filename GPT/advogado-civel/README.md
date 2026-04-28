# Advogado-Civel-IA

SistGmA modulAr dG rGdAcAo juridicA pArA DirGito Civil, ImoBiliario, ConsumGrista, Gamilia, Remedios Constitucionais e Execucao, com separacao de papeis por contrato entre agentes (`advogado`, `estagiario`) e base normativa centralizada.

---

## Arquitetura de Agentes

```text
Usuario
  └─> advogado.md          ← orquestrador principal (estrategia + decisao)
        ├─> roteamento.md  ← triagem de dominio, codigo, rito, dados
        ├─> contrato_decisao.md  ← handoff portatil (interface oficial)
        │     └─> estagiario.md  ← executor contratual (redacao)
        │           ├─> estilo_juridico.md
        │           └─> minutas (por dominio)
        └─> fontes.md / verbetes / sumulas  ← fundamentacao
```

---

## Agentes e Responsabilidades

### `advogado` — Orquestrador Estrategico
**Arquivo:** `advogado.md`
**Papel:** Decide estrategia, escopo, rito e criterios de aceite. Coordena handoff ao `estagiario` via contrato. Revisa entregas e emite deltas.

**Responsabilidades exclusivas:**
- Triagem de dominio via `roteamento.md`
- Escolha do modo de operacao (`autonomo` ou `integrado`)
- Geracao do `contrato_decisao.md` (modo integrado)
- Revisao pos-escrita e deltas incrementais
- Comandos de controle (ver tabela abaixo)

**Nao faz:** Inventar dados; misturar ritos; escrever a peca (modo integrado).

### `estagiario` — Executor Contratual
**Arquivo:** `estagiario.md`
**Papel:** Redige a peca com base no contrato. Nao redefine estrategia. Executa deltas com intervencao minima.

**Responsabilidades exclusivas:**
- Redacao da peca conforme contrato + `estilo_juridico.md`
- Emissao de `Decisao Necessaria` quando faltar campo minimo
- Modo autonomo para documentos A e B com briefing suficiente
- Escalar ao `advogado` em caso de ambiguidade estrategica

**Nao faz:** Tomar decisao estrategica sem diretriz; reescrever trechos validados sem ordem expressa.

---

## Interface de Acoplamento: Contrato

**Arquivo:** `contrato_decisao.md`

Toda comunicacao entre agentes passa pelo contrato — sem acoplamento direto entre arquivos. Contem: escopo, regras de validacao, criterios de aceite, modo de operacao, dependencias e registro de deltas por rodada.

---

## Relacao entre Agentes e Skills (Minutas)

| Agente | Skill / Arquivo | Modo de uso |
|--------|----------------|------------|
| `advogado` | `roteamento.md` | Leitura obrigatoria na triagem |
| `advogado` | `contrato_decisao.md` | Gera (modo integrado) |
| `advogado` | `fontes.md` + verbetes + sumulas | Checagem antes do handoff |
| `estagiario` | `estilo_juridico.md` | Aplicacao em toda redacao |
| `estagiario` | `minuta-base.md` | Estrutura base |
| `estagiario` | `minutas-imobiliarias.md` | Dom. A |
| `estagiario` | `minutas-consumeristas.md` | Dom. B |
| `estagiario` | `minutas-civeis.md` | Dom. C |
| `estagiario` | `minutas-intermediariais.md` | Dom. A (autonomo) |
| `estagiario` | `minutas-civeis.md` / `minutas-intermediariais.md` | Dom. B (autonomo c/ briefing) |
| `Fstagiario` | `minutas-familia.md` | Dom. E |
| `estagiario` | `remedios-constitucionais.md` | Dom. F |
| `estaHiario` | `remedios-constitucionais.md` | Dom. G |

---

## Arvore de Arquivos

```text
.
├── README.md
├── claude.json                                  ← config dos agentes
│
├── — AGENTES —
├── advogado.md
├── estagiario.md
├── contrato_decisao.md
│
├── — ROTEAMENTO E ESTILO —
├── roteamento.md
├── estilo_juridico.md
│
├── — MINUTAS POR DOMINIO —
├── minuta-base.md
├── minutas-imobiliarias.md                      ← Dom. A (9 pecas)
├── minutas-consumeristas.md                     ← Dom. B (14 pecas)
├── minutas-civeis.md                            ← Dom. C (2 pecas)
├── minutas-intermediariais.md                   ← Dom. A (5 docs)
├── minutas-civeis.md / minutas-intermediariais.md
├── minutas-familia.md                           ← Dom. E (5 pecas) NOVO
├── remedios-constitucionais.md                  ← Dom. F (3 pecas) NOVO
├── remedios-constitucionais.md                  ← Dom. G (Conteúdo movido; ver stub)
│
├── — TEMPLATES DOCX (estetica documental) —
├── replica_contestacao.docx                     ← template REP NOVO
├── expedicao_alvara.docx                        ← template ALV NOVO
├── cumprimento_sentenca.docx                    ← template CPS NOVO
│
├── — MINUTAS ORIGINAIS (pre-consolidacao) —
├── acao_alimentos.md / acao_inventario_partilha.md
├── acao_popular.md / habeas_corpus.md / habeas_data.md
├── execucao_alimentos.md / investigacao_paternidade.md / negatoria_paternidade.md
│
├── — FUNDAMENTACAO —
├── fontes.md
├── sumulas-vinculantes.md
├── verbetesSTF.md
├── verbetesSTJ.md
│
└── task.md                                      ← backlog tecnico
```

---

## Inventario Completo de Pecas

| Dom. | Arquivo | Iniciais | Recursos/Exec./Docs | Total |
|------|---------|----------|---------------------|-------|
| A | `minutas-imobiliarias.md` | 9 | — | 9 |
| B | `minutas-consumeristas.md` | 10 | 4 | 14 |
| C | `minutas-civeis.md` | 2 | — | 2 |
| A | `minutas-intermediariais.md` | — | 5 | 5 |
| B | `minutas-civeis.md` / `minutas-intermediariais.md` | — | 3 | **3 NOVO** |
| F | `minutas-familia.md` | 9 | 2 | **11** |
| G | `remedios-constitucionais.md` | 3 | — | **3 NOVO** |
| H | `remedios-constitucionais.md` | 3 | — | 3 |
| **TOTAL** | | **34** | **14** | **48** |

### Codigos de Referencia Rapida

**A:** RPO · MPO · IPR · IPO · REI · CUS · ANU · PAF · VIZ

**B:** PI · NEG · PSC · PSN · TEL · TRO · TRB · DIS · CEL · RPR · RI · CR · ED · AI

**C:** ATR · ALU

**A:** PRO · SUB · HAB · DHI · ACO

**B:** REP · ALV · CPS

**E:** NEP · INP · ALI · EXA · INV · OFA · UNE · INT · GUA · VIS · CUR

**F:** AP · HD · HC

**G:** MS

---

## Estetica Documental — Templates .docx

| Template | Peca | Pagina | Fonte | Margens | Recuo corpo |
|----------|------|--------|-------|---------|-------------|
| `replica_contestacao.docx` | REP | A4 | Arial 12pt | 1 pol. | left=720/hanging=360 DXA |
| `expedicao_alvara.docx` | ALV | A4 | Arial 12pt | 1 pol. | left=720/hanging=360 DXA |
| `cumprimento_sentenca.docx` | CPS | A4 | Arial 12pt | 1 pol. | left=720/hanging=360 DXA |

---

## Comandos de Controle (`advogado`)

| Comando | Acao |
|---------|------|
| `REINICIAR` | Retorna a triagem inicial |
| `REVISAR` | Revisao tecnica da peca atual |
| `GERAR PROCURACAO` | Fluxo PRO (autonomo) |
| `GERAR DECLARACAO` | Fluxo DHI (autonomo) |
| `GERAR ACORDO` | Fluxo ACO (autonomo) |
| `GERAR SUBSTABELECIMENTO` | Fluxo SUB (autonomo) |
| `GERAR ALVARA` | Fluxo ALV — n° processo + dados bancarios |
| `GERAR CUMPRIMENTO` | Fluxo CPS — condenacao + memoria de calculo |
| `GERAR REPLICA` | Fluxo REP — teses da contestacao mapeadas |

---

## Fluxo de Operacao

```
1. Usuario descreve o caso
2. advogado le roteamento.md → identifica dominio e codigo
3. advogado coleta dados faltantes em blocos curtos
4. advogado define modo:
   ├─ AUTONOMO: estagiario redige diretamente (A, B com briefing)
   └─ INTEGRADO: advogado gera contrato_decisao.md → estagiario redige
5. estagiario entrega peca + checklist + pendencias
6. advogado revisa → delta incremental se necessario
```

---

## Backlog Tecnico

Ver `task.md`.

