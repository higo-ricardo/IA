# Advogado-Civel-IA

Sistema modular de redacao juridica para Direito Civil, Imobiliario e Consumerista, com separacao de papeis por contrato entre `advogado` (estrategia) e `estagiario` (execucao textual).

## Arquitetura Atual

```text
Usuario
  -> advogado.md (orquestracao, estrategia, criterios de aceite)
      -> roteamento.md (fonte unica de triagem, codigo e dados obrigatorios)
      -> contrato_decisao.md (handoff portatil e versionavel)
          -> estagiario.md (executor contratual)
              -> estilo_juridico.md (padrao de linguagem)
              -> minutas e base
```

## Arvore de Arquivos

```text
.
├── README.md
├── advogado.md
├── estagiario.md
├── contrato_decisao.md
├── roteamento.md
├── estilo_juridico.md
├── task.md
├── minuta-base.md
├── minutas-civeis.md
├── minutas-consumeristas.md
├── minutas-imobiliarias.md
├── minutas-intermediariais.md
├── fontes.md
├── sumulas-vinculantes.md
├── verbetesSTF.md
├── verbetesSTJ.md
└── VerbetesSTF_new.md
```

## Componentes Principais

### 1) Orquestrador: `advogado.md`
- Decide estrategia e modo de operacao (`autonomo` ou `integrado`).
- Define briefing e criterios de aceite.
- Revisa entrega do `estagiario` e emite deltas incrementais.

### 2) Executor: `estagiario.md`
- Executa redacao com base no `contrato_decisao.md`.
- Nao redefine estrategia quando houver diretriz do `advogado`.
- Opera em modo autonomo para documentos intermediarios (`PRO`, `SUB`, `HAB`, `DHI`, `ACO`) quando o fluxo for claro.

### 3) Interface de Acoplamento: `contrato_decisao.md`
- Artefato unico de handoff entre `advogado` e `estagiario`.
- Contem escopo, regras de validacao, criterios de aceite, dependencias e deltas por rodada.

### 4) Triagem e Coleta: `roteamento.md`
- Fonte unica para dominio, codigo de peca, rito e dados obrigatorios.
- Inclui dominios A (Imobiliario), B (Consumerista/JEC), C (Civel) e D (Intermediarios).

### 5) Estilo: `estilo_juridico.md`
- Guia de padrao textual do escritorio.
- Separado da execucao para reduzir acoplamento e custo de contexto.

### 6) Minutas e Base
- `minuta-base.md`
- `minutas-imobiliarias.md`
- `minutas-consumeristas.md`
- `minutas-civeis.md`
- `minutas-intermediariais.md`

### 7) Fundamentacao e Apoio
- `fontes.md`
- `sumulas-vinculantes.md`
- `verbetesSTF.md`
- `verbetesSTJ.md`

### 8) Backlog Tecnico
- `task.md` (controle de manutencao/refatoracao; nao e interface de execucao)

## Fluxo Recomendado

1. Usuario descreve o caso.
2. `advogado` consulta `roteamento.md`, coleta dados e define estrategia.
3. Em modo integrado, `advogado` gera `contrato_decisao.md`.
4. `estagiario` redige a peca conforme contrato + estilo.
5. `advogado` revisa e solicita deltas incrementais quando necessario.

## Modos de Operacao

### Modo Integrado
- Usar quando houver ambiguidade estrategica ou necessidade de validacao forte.
- `advogado` decide; `estagiario` executa.

### Modo Autonomo do Estagiario
- Usar para documentos simples e padronizados (intermediarios), sem disputa de estrategia.
- Escalar para `advogado` se houver ambiguidade relevante.

## Objetivo da Estrutura

- Baixo acoplamento entre estrategia e execucao.
- Reducao de retrabalho por deltas incrementais.
- Melhor performance de contexto (arquivos com responsabilidades bem separadas).
- Manutencao mais simples e rastreavel.
