---
name: code-reviewer-pt
description: |
  Revisão de código rigorosa em português, combinando Clean Code, Clean Architecture e The Pragmatic Programmer com foco em segurança, performance e qualidade. Use SEMPRE que o usuário pedir para: revisar código ou pull request, auditar segurança, verificar qualidade ou dívida técnica, preparar código para merge ou produção, detectar code smells ou violações de SOLID/DRY/YAGNI/KISS, refatorar código existente. Também dispara em: "este código está bom?", "pronto para merge?", "encontrar bugs", "verificar problemas", "code smell", "revisão de PR", "olhar meu código", "dívida técnica", "melhores práticas", "está seguro?", "está pronto para produção?", "tem algum problema aqui?", "me fala o que melhorar", "pode revisar?", "que tal esse código?". Use mesmo que o usuário não diga "revisão de código" explicitamente.
---

# Code Reviewer PT

Revisão pragmática de código em português seguindo Clean Code (CC), Clean Architecture (CA) e The Pragmatic Programmer (PP).

**Princípio central:** Máquinas cuidam de formatação. Humanos focam em lógica, segurança e design.

**Arquivos de referência disponíveis:**
- `references/rules-pt.md` — 350+ regras PP/CC/CA com exemplos detalhados por categoria
- `references/examples-pt.md` — Snippets ❌/✅ por vulnerabilidade, performance e smell
- `references/security-checklist.md` — Checklist de segurança expandido por paradigma

> Leia o arquivo relevante **somente quando** precisar de detalhes além do que está neste SKILL.md.

---

## PASSO 1 — Posicionamento do Projeto (OBRIGATÓRIO)

Antes de revisar qualquer código, determine o nível de rigidez com o questionário 3+4+2:

**Q1: Quem usa este código?**
- `D1` 🧑 Solo — só eu
- `D2` 👥 Interno — equipe/empresa
- `D3` 🌍 Externo — usuários externos / open source

**Q2: Que padrão?**
- `R1` 🚀 Lançar — só fazer funcionar
- `R2` 📦 Normal — qualidade básica
- `R3` 🛡️ Cuidadoso — revisão criteriosa
- `R4` 🔒 Rigoroso — padrão máximo

**Q3: Quão crítico?** *(perguntar apenas se D2/D3 + R3/R4)*
- `C1` 🔧 Normal — pode aguardar correção
- `C2` 💎 Crítico — interrompe se quebrar

**Tabela de níveis:**

| D | R | C | Nível | Exemplo |
|---|---|---|---|---|
| D1 | R1 ou R2 | — | **L1** 🧪 Laboratório | Scripts, experimentos, protótipos |
| D1 | R3/R4 ou D2 | R1/R2 | **L2** 🛠️ Ferramenta | Utilitários pessoais/internos |
| D2 | R3/R4 | C1 | **L3** 🤝 Equipe | Projetos de equipe |
| D2 | R3/R4 | C2 ou D3 | R1-R3 | **L4** 🚀 Infra | SDKs internos, APIs críticas |
| D3 | R4 | C2 | **L5** 🏛️ Crítico | Finanças, saúde, auditável |

**Quando o usuário não fornecer contexto:** pergunte Q1 e Q2. Se D1+R1/R2, assuma L1 e prossiga. Para qualquer outro caso, espere a resposta antes de revisar.

---

## PASSO 2 — Identificar Linguagem e Paradigma

Ajuste as regras ao paradigma detectado:

| Paradigma | Linguagens típicas | Ajuste principal |
|---|---|---|
| OOP Puro | Java, C# | Regras SOLID completas; interfaces em tudo |
| Multi-paradigma | Python, TypeScript, Kotlin, Swift | SOLID ajustado — funções de primeira classe são válidas |
| Funcional | Haskell, Elixir, F#, Clojure | Imutabilidade > SRP clássico; efeitos em borda |
| Sistemas | Rust, Go, Zig, C/C++ | Segurança de memória, lifetimes, ownership |
| Script/Glue | Bash, Python scripts, Ruby | KISS dominante; DRY mínimo aceitável |

**Para linguagens tipadas estaticamente** (Java, TypeScript, C#, Kotlin, Rust): type hints/anotações ausentes são reportáveis a partir de L3.

---

## PASSO 3 — Varredura de Segurança (SEMPRE PRIMEIRO)

Antes da checklist de 15 pontos, execute esta varredura rápida. Qualquer hit é automaticamente **Crítico**.

### Varredura Rápida de Segurança

| # | Vetor | Sinal de Alerta |
|---|---|---|
| S1 | **SQL Injection** | Concatenação de string com input do usuário em query |
| S2 | **XSS** | `innerHTML`, `dangerouslySetInnerHTML`, `eval()` com input externo |
| S3 | **Secrets hardcoded** | API keys, senhas, tokens literais no código-fonte |
| S4 | **Auth bypass** | Função de dado sensível sem verificação de identidade/permissão |
| S5 | **Path traversal** | Caminhos de arquivo construídos com input não sanitizado |
| S6 | **SSRF** | URLs construídas com input do usuário sem allowlist |
| S7 | **Deserialização insegura** | `pickle.loads`, `eval`, `unserialize` em dado externo |
| S8 | **Condição de corrida** | Estado compartilhado mutável sem lock em contexto concorrente |
| S9 | **Dependência vulnerável** | Import de pacote com CVE conhecido |
| S10 | **Log de dado sensível** | PII, senha ou token aparecendo em log statement |

> Para snippets ❌/✅ de cada vetor, consulte `references/examples-pt.md` → Seção 1.

---

## PASSO 4 — Lista de Verificação de 15 Pontos

Execute em ordem de prioridade. Documente cada problema encontrado.

### 🔴 Correção e Segurança (CRÍTICO)
1. **Vulnerabilidades de segurança** — resultado da varredura S1–S10
2. **Lógica incorreta** — off-by-one, condições invertidas, comparações erradas (== vs ===, is vs ==)
3. **Tratamento de erro ausente** — exceções ignoradas, crashes em produção (CC-86, CC-95)
4. **Validação de entrada** — inputs externos não validados/sanitizados antes de uso
5. **Condições de corrida** — estado compartilhado sem sincronização (PP-48)

### 🟡 Design e Performance (IMPORTANTE)
6. **SRP / Responsabilidade única** — classe ou função com múltiplas razões para mudar (CA-8)
7. **DRY** — duplicação de *conhecimento* acima da tolerância do nível (PP-15, CC-37)
8. **Direção de dependência** — lógica de negócio importando infraestrutura concreta (CA-12, CA-31)
9. **N+1 queries** — loops gerando queries por iteração sem batch/join
10. **Métricas fora do limite** — tamanho de função, contagem de parâmetros, aninhamento (ver PASSO 6)

### 📝 Manutenibilidade (IMPORTANTE quando nível ≥ L3)
11. **Nomenclatura** — nomes que não revelam intenção; abreviações sem contexto (CC-4, CC-7)
12. **Efeitos colaterais ocultos** — função modifica estado não declarado em sua assinatura (CC-31)
13. **Números mágicos** — constantes literais sem nome e sem contexto (CC-175)
14. **Cobertura de testes** — abaixo do mínimo do nível; lógica crítica sem teste
15. **YAGNI / over-engineering** — abstração, parametrização ou generalidade sem caso de uso atual (PP-43)

---

## PASSO 5 — Classificação de Severidade

| Nível | Critério | Exemplos |
|---|---|---|
| 🔴 **Crítico** | Segurança, perda de dados, crash em produção, bug lógico que afeta correção | SQL injection, auth não validada, off-by-one financeiro, exception silenciada |
| 🟡 **Importante** | Violação de princípio, métrica fora do limite, testabilidade comprometida | SRP violado, 8 params em L3, sem teste para lógica central, N+1 em endpoint |

**Regras fixas:**
- Problemas de segurança (S1–S10) são **sempre** Críticos, independente do nível
- Severidade é determinada pela natureza do problema, **não** pelo esforço de correção
- Problemas abaixo do limiar Importante são **omitidos completamente** do relatório
- Em L1, apenas Críticos de segurança e bugs lógicos são reportados

---

## PASSO 6 — Avaliação de Esforço e Benefício

Para cada problema Crítico e Importante:

**Esforço:**
- **Baixo** — poucas linhas, 1 arquivo, < 30 min
- **Médio** — refator moderado, múltiplos arquivos, 30 min–4 h
- **Alto** — mudança arquitetural, impacto amplo, > 4 h

**Benefício:**
- **Alto** — caminho quente + consequência severa (dados, segurança, disponibilidade)
- **Médio** — caminho comum + impacto moderado, ou caso extremo + consequência severa
- **Baixo** — caso extremo + impacto menor (glitch de UI, experiência ligeiramente degradada)

**Regra de desempate:** se incerto entre Baixo e Médio, ou Médio e Alto → escolha o extremo conservador. Médio é escolha deliberada, não fallback.

---

## PASSO 7 — Métricas por Nível

> Iniciadores de conversa, não portões duros. Uma função clara de 60 linhas vence três funções confusas de 20.

| Métrica | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| Linhas por função | N/A | ≤80 | ≤50 | ≤30 | ≤20 |
| Parâmetros | N/A | ≤7 | ≤5 | ≤3 | ≤2 |
| Profundidade aninhamento | N/A | ≤5 | ≤4 | ≤3 | ≤2 |
| Tamanho PR | N/A | ≤800 | ≤500 | ≤300 | ≤200 |
| Cobertura de testes | N/A | 30% | 60% | 80% | 95% |
| Tolerância DRY (repetições) | N/A | 4× | 3× | 2× | 1× |

**Conte apenas linhas lógicas** — exclua comentários, docstrings e linhas em branco.

**Isenções de tamanho de função:** responsabilidade única não decomponível, switch/match grandes, construtores de dados puros, mapeamentos de configuração.

**Isenções de parâmetros:** maioria com valor padrão (conte só obrigatórios), funções de configuração, padrões Factory/Builder do framework.

**Isenções de DRY:** duplicação acidental — conhecimento de negócio *diferente* (teste: "se um muda, o outro SEMPRE muda?" — se não → mantenha separado). Duplicação no mesmo arquivo é menor risco em L1–L3.

---

## PASSO 8 — Formato do Relatório

> Omita seções sem problemas. Não adicione seções extras além das listadas abaixo.

```markdown
## 📋 Relatório de Revisão de Código

**Posicionamento:** L[N] [Nome]
**Linguagem/Paradigma:** [linguagem detectada]
**Escopo:** [arquivos/commits revisados]

### 🔴 Problemas Críticos (Deve Corrigir)

- **[arquivo:linha] Título curto do problema**
  - Regra: XX-## (Nome da Regra)
  - Princípio: por que importa em uma frase
  - Sugestão: como corrigir (com snippet ❌/✅ quando útil)
  - Esforço: [Baixo/Médio/Alto] — [razão em uma linha]
  - Benefício: [Baixo/Médio/Alto] — [razão em uma linha]

### 🟡 Problemas Importantes (Deve Corrigir)

- **[arquivo:linha] Título curto do problema**
  - Regra: XX-## (Nome da Regra)
  - Princípio: por que importa em uma frase
  - Sugestão: como corrigir
  - Esforço: [Baixo/Médio/Alto] — [razão em uma linha]
  - Benefício: [Baixo/Médio/Alto] — [razão em uma linha]

---

### 📝 Veredicto
[✅ Pronto para merge / ⚠️ Precisa correções / 🚫 Retrabalho maior necessário]

**Resumo:** [1–2 frases sobre o estado geral do código]
```

**Critérios de veredicto** (aplique o primeiro que corresponder):

| Veredicto | Condição |
|---|---|
| 🚫 Retrabalho maior | ≥3 Críticos OU problema arquitetural fundamental (CA-31 violado sistematicamente) |
| ⚠️ Precisa correções | Qualquer Crítico OU >2 Importantes |
| ✅ Pronto para merge | Zero Críticos E ≤2 Importantes |

---

## O que NÃO revisar (trabalho de máquina)

Linter e formatter cuidam disso — não reporte, jamais:
- Indentação e espaçamento
- Convenções de nomenclatura capturadas por linter (camelCase vs snake_case)
- Imports/variáveis não utilizados (CC-162 — pego por linter)
- Erros de sintaxe, ponto e vírgula faltante, chaves
- Ordenação de imports

**Foque no que máquinas não fazem:** correção lógica, intenção de design, alinhamento arquitetural, segurança semântica, legibilidade humana.

---

## Referência Rápida de Regras

| Acrônimo | Regra | Fonte |
|---|---|---|
| DRY | Don't Repeat Yourself | PP-15, CC-37 |
| YAGNI | You Aren't Gonna Need It | PP-43 |
| KISS | Keep It Simple | CC-130, PP-72 |
| ETC | Easy To Change | PP-14 |
| SRP | Single Responsibility Principle | CA-8 |
| OCP | Open-Closed Principle | CA-9 |
| LSP | Liskov Substitution Principle | CA-10 |
| ISP | Interface Segregation Principle | CA-11 |
| DIP | Dependency Inversion Principle | CA-12 |
| LoD | Law of Demeter | PP-46, CC-80 |

Para regras completas com todos os números, consulte: `references/rules-pt.md`
Para exemplos de código ❌/✅: `references/examples-pt.md`

---

## Code Smells de Referência Rápida

| Smell | Regra | Detecção |
|---|---|---|
| Função longa | CC-20 | Excede limite do nível? |
| Muitos parâmetros | CC-26 | Excede limite do nível? |
| Números mágicos | CC-175 | Constantes literais sem nome? |
| Classe Deus | CA-8 | Múltiplas responsabilidades não relacionadas? |
| Inveja de Feature | CC-164 | Método usa mais dados de outra classe que da própria? |
| Trem de Carga | CC-81 | Cadeia `a.b().c().d()` violando LoD? |
| Estado global mutável | PP-47 | Variáveis globais modificadas em múltiplos lugares? |
| Herança profunda | PP-51 | Hierarquia > 2 níveis sem justificativa? |
| Aninhamento profundo | CC-178 | Excede limite do nível? |
| Switch duplicado | CC-180 | Mesmo switch em múltiplos lugares? |
| Acoplamento temporal | PP-48 | Operações dependem de ordem não documentada? |
| Broken Window | PP-5 | Código ruim tolerado que degrada o entorno? |
