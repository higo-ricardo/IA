# ⚖️ Sistema de Questões Fiscais

> **Skill para geração e conversão de questões entre formatos de banca (FGV, CEBRASPE, FCC, ESAF).**

| Metadado | Valor |
|----------|-------|
| **Nome** | `sistema-questoes-concursos` |
| **Versão** | — |
| **Autor** | — |
| **Foco** | Concursos fiscais (Contabilidade, CPCs, NBCs, CTN, Lei das S.A.) |

---

## 🎯 Propósito

**Produzir material de estudo**: gerar questões inéditas, converter entre formatos de banca (múltipla escolha ↔ certo/errado) e adaptar questões a diferentes estilos examinadores.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│               🎯 ROTEADOR CENTRAL                       │
│         (identifica o modo pelo input do usuário)       │
└──────────────┬──────────────┬──────────────┬────────────┘
               │              │              │
       ┌───────▼──────┐ ┌─────▼──────┐ ┌────▼───────────┐
       │  SUBAGENTE 1 │ │ SUBAGENTE 2│ │  SUBAGENTE 3   │
       │   GERADOR    │ │ CONVERSOR  │ │  CONVERSOR     │
       │  (inéditas)  │ │  CEBRASPE  │ │ MÚLTIPLA ESC.  │
       │              │ │  (→C/E)    │ │   (→A–E)       │
       └──────────────┘ └────────────┘ └────────────────┘
```

| Característica | Detalhe |
|----------------|---------|
| **Tipo** | Modular — roteador central + 3 subagentes com arquivos próprios |
| **Modos de operação** | 3 (GERADOR, CONVERSOR CEBRASPE, CONVERSOR MÚLTIPLA ESCOLHA) |
| **Interatividade** | Média — configuração inicial + geração em bloco |
| **Encadeamento** | Cadeia entre subagentes (gerar → converter → reconverter) |

---

## ✨ Funcionalidades

### Subagente 1 — GERADOR

| Recurso | Detalhe |
|---------|---------|
| Cria questões inéditas | Sim, originais por disciplina e tópico |
| Bancas suportadas | FGV, CEBRASPE, FCC |
| Dificuldade | Fácil, Médio, Difícil |
| Confidence Score | Interno (não exibido) — controla publicação |
| Formato de saída | Bloco de questões + gabarito comentado |

### Subagente 2 — CONVERSOR CEBRASPE

| Recurso | Detalhe |
|---------|---------|
| Entrada | Questão múltipla escolha (A–E) |
| Saída | Assertivas Certo / Errado |
| Quantidade | 1 a 4 assertivas por questão |
| Tipos suportados | Interpretativo, calculativo, proposições, situação-problema, negativa |
| Sintaxe | Sujeito explícito, verbo no presente, 1–3 linhas |

### Subagente 3 — CONVERSOR MÚLTIPLA ESCOLHA

| Recurso | Detalhe |
|---------|---------|
| Entrada | Assertiva Certo / Errado |
| Saída | Questão A–E com 5 alternativas |
| Bancas suportadas | FGV (padrão), FCC, ESAF |
| Distratores | Exploram confusões técnicas reais da disciplina |

### Flags Globais

| Flag | Significado |
|------|-------------|
| `[Gabarito inferido]` | Gabarito deduzido pela skill |
| `[Verificar cálculo]` | Questão numérica complexa — conferir |
| `[Norma não identificada]` | Sem referência normativa clara |
| `[Confidence baixo — conceitual]` | Inferência moderada |
| `[Distrator reaproveitado]` | Erro da assertiva original virou distrator |
| `[Estilo FGV aplicado por padrão]` | Banca não especificada |

---

## 📚 Fontes Normativas Consultadas

| Disciplina | Fonte | URL |
|------------|-------|-----|
| CPCs | CPC Online | https://www.cpc.org.br/CPC/Documentos-Emitidos/Pronunciamentos |
| NBCs TA | CFC | https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/ |
| Lei das S.A. | Planalto | https://www.planalto.gov.br/ccivil_03/leis/l6404consol.htm |
| CTN | Planalto | https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm |
| NBC TSP 34 | CFC | https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/ |

---

## 📊 Avaliação por Critérios

| Critério | Nota (0–10) |
|----------|:-----------:|
| UX do usuário final | 7.0 |
| Versatilidade funcional | 9.5 |
| Arquitetura / Manutenibilidade | 9.0 |
| Robustez / Fallbacks | 7.0 |
| Métricas e diagnóstico | 5.0 |
| **MÉDIA** | **7.5** |

### Pontos Fortes
- ✅ 3 modos operacionais (gerar + 2 conversores)
- ✅ Arquitetura modular com subagentes independentes
- ✅ Encadeamento entre modos (gerar → converter → reconverter)
- ✅ Distratores técnicos específicos por tipo de questão
- ✅ Flags globais para sinalizar limitações internas
- ✅ Adaptação por banca (FGV, FCC, ESAF, CEBRASPE)

### Pontos de Melhoria
- 🔧 Sem timer / controle de tempo
- 🔧 Sem política de desistência ou relatório parcial
- 🔧 Sem métricas agregadas de desempenho
- 🔧 Sem versionamento da skill
- 🔧 Tratamento de resposta inválida (ex: "F" em vez de "A–E")
- 🔧 Banco de questões persistente entre sessões

---

## 🔀 Comparação com simulador_AI_provasJURIDICAS

| Dimensão | provasSEFAZ | provasJURIDICAS |
|----------|:---:|:---:|
| UX do usuário final | ⭐ 7.0 | ⭐ 9.0 |
| Versatilidade funcional | ⭐ 9.5 | ⭐ 7.0 |
| Arquitetura/manutenibilidade | ⭐ 9.0 | ⭐ 7.5 |
| Robustez/fallbacks | ⭐ 7.0 | ⭐ 8.0 |
| Métricas e diagnóstico | ⭐ 5.0 | ⭐ 8.0 |

> **provasSEFAZ** = produzir material (gerar e converter questões)
> **provasJURIDICAS** = treinar (experiência de prova real)
> **São complementares, não concorrentes.**

---

## 📁 Estrutura do Projeto

```
simulador_AI_provasSEFAZ/
├── SKILL.md                    # Definição principal da skill
├── readme.md                   # Documentação original
├── subagentes/
│   ├── gerador.md              # Subagente 1 — Questões inéditas
│   ├── conversor-cebraspe.md   # Subagente 2 → CEBRASPE
│   └── conversor-multipla-escolha.md  # Subagente 3 → A–E
└── banco-questoes/             # Questões geradas/conversões
```
