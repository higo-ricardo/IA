# Referência Completa de Regras — Code Reviewer PT

Baseado em 350+ regras de três fontes fundamentais.

| Prefixo | Fonte | Regras |
|---|---|---|
| **PP-##** | The Pragmatic Programmer (Thomas & Hunt) | PP-1 a PP-100 |
| **CC-##** | Clean Code (Robert C. Martin) | CC-1 a CC-202 |
| **CA-##** | Clean Architecture (Robert C. Martin) | CA-1 a CA-48 |

---

## Índice

1. [Segurança — Referência de Vetores](#1-segurança--referência-de-vetores)
2. [Performance — Padrões e Anti-padrões](#2-performance--padrões-e-anti-padrões)
3. [The Pragmatic Programmer (PP)](#3-the-pragmatic-programmer-pp)
4. [Clean Code (CC) — Princípios Chave](#4-clean-code-cc--princípios-chave)
5. [Clean Architecture (CA) — Referência Completa](#5-clean-architecture-ca--referência-completa)
6. [Métricas e Isenções](#6-métricas-e-isenções)

> Para snippets de código ❌/✅, consulte `references/examples-pt.md`.

---

## 1. Segurança — Referência de Vetores

| ID | Vetor | Regra | Sinal de Violação |
|---|---|---|---|
| S1 | SQL Injection | PP-72, CC-130 | Concatenação direta de input em query |
| S2 | XSS | PP-72 | `innerHTML`/`eval()` com dado externo |
| S3 | Secrets hardcoded | PP-72 | Credenciais literais no código-fonte |
| S4 | Auth bypass | CA-29 | Acesso a dado sensível sem verificação |
| S5 | Path traversal | PP-72 | Caminho de arquivo com input não sanitizado |
| S6 | SSRF | PP-72 | URL construída com input sem allowlist |
| S7 | Deserialização insegura | PP-72 | `pickle.loads`/`eval` em dado externo |
| S8 | Condição de corrida | PP-48 | Estado mutável compartilhado sem lock |
| S9 | Dependência vulnerável | PP-5 | Pacote com CVE conhecido importado |
| S10 | Log de dado sensível | CC-86 | PII/token/senha em log statement |

---

## 2. Performance — Padrões e Anti-padrões

| Anti-padrão | Impacto | Solução |
|---|---|---|
| N+1 Queries | Alto — cresce linearmente com dados | JOIN ou eager loading |
| Loop com I/O síncrono | Alto — bloqueia por iteração | Batch requests, async/await |
| Alocação em hot path | Médio — pressão de GC | Pool de objetos, reutilização |
| Busca linear em coleção grande | Médio — O(n) evitável | HashMap, índice, sorted search |
| Recálculo sem cache | Médio — CPU desperdiçada | Memoização, cache com TTL |
| Serialização desnecessária | Médio — CPU + memória | Lazy loading, streaming |

---

## 3. The Pragmatic Programmer (PP)

### Princípios Essenciais

| Regra | Nome | Ponto de Revisão |
|---|---|---|
| PP-5 | Broken Windows | Código ruim tolerado? Cada "janela quebrada" degrada o entorno? |
| PP-14 | ETC — Easy To Change | A mudança mais provável seria fácil de fazer? |
| PP-15 | DRY — Don't Repeat Yourself | Conhecimento duplicado além da tolerância do nível? |
| PP-20 | Tracer Bullets | Caminho end-to-end funciona antes de otimizar? |
| PP-37 | Design by Contract | Pré/pós-condições definidas? Invariantes documentadas? |
| PP-43 | YAGNI | Complexidade adicionada sem necessidade atual comprovada? |
| PP-46 | Lei de Demeter | Objeto acessa internals de outro objeto diretamente? |
| PP-47 | Estado Global | Variáveis globais mutáveis causando acoplamento oculto? |
| PP-48 | Acoplamento Temporal | Operações dependem de ordem não documentada? |
| PP-51 | Herança Profunda | Hierarquia > 2 níveis sem justificativa clara? |
| PP-72 | KISS + Minimizar Superfície de Ataque | Código simples? Exposição a entrada externa minimizada? |

---

## 4. Clean Code (CC) — Princípios Chave

### Nomenclatura (CC-4 a CC-18)

| Regra | Princípio | Sinal de Violação |
|---|---|---|
| CC-4 | Use nomes que revelam intenção | `d`, `data`, `temp`, `x`, `val` sem contexto |
| CC-7 | Evite desinformação | `accountList` que não é lista; `hp` ambíguo |
| CC-10 | Distinções significativas | `getData()` vs `getDataNew()` vs `getData2()` |
| CC-13 | Nomes pronunciáveis | `genymdhms` vs `generationTimestamp` |
| CC-15 | Nomes buscáveis | Constante `7` vs `MAX_CLASSES_PER_STUDENT` |
| CC-17 | Nomes de classes — substantivos | `Manager`, `Processor`, `Data` são vagos demais |
| CC-18 | Nomes de métodos — verbos | `save()`, `deleteRecord()`, `get*()`, `set*()`, `is*()` |

### Funções (CC-20 a CC-45)

| Regra | Princípio | Sinal de Violação |
|---|---|---|
| CC-20 | Funções pequenas | Excede limite do nível? |
| CC-21 | Faça uma coisa | Múltiplos níveis de abstração na mesma função? |
| CC-22 | Um nível de abstração por função | Mix de lógica de alto e baixo nível |
| CC-26 | Argumentos de função | Excede limite do nível? Booleanos como parâmetro? |
| CC-28 | Sem argumentos de flag | `render(true)` — o que significa true? |
| CC-31 | Sem efeitos colaterais ocultos | Função modifica estado não declarado em sua assinatura? |
| CC-37 | DRY em funções | Lógica duplicada acima da tolerância? |
| CC-40 | Prefira exceções a códigos de erro | `if (deletePage(page) == E_OK)` espalhado? |

### Comentários (CC-55 a CC-65)

| Regra | Princípio |
|---|---|
| CC-55 | Comentários compensam código ruim — prefira melhorar o código |
| CC-58 | Bons comentários: intenção, esclarecimento de API externa, warning, TODO |
| CC-59 | TODO comments são aceitáveis — desde que rastreados |
| CC-62 | Comentários redundantes são ruído: `i++; // incrementa i` |
| CC-63 | Comentário enganoso é pior que nenhum — verifique se ainda está correto |
| CC-64 | Código comentado deve ser removido — use controle de versão |
| CC-65 | Comentários de fechamento de bloco são sinal de função longa demais |

### Formatação (CC-70 a CC-82)

| Regra | Princípio | Sinal de Violação |
|---|---|---|
| CC-75 | Distância vertical — declare perto do uso | Variável declarada no topo, usada 50 linhas abaixo |
| CC-78 | Funções dependentes — próximas no arquivo | Caller antes do callee |
| CC-80 | LoD — Lei de Demeter | `a.getB().getC().doSomething()` |
| CC-81 | Trem de carga | Cadeia de métodos com mais de 2–3 saltos |

### Tratamento de Erro (CC-86 a CC-97)

| Regra | Princípio | Sinal de Violação |
|---|---|---|
| CC-86 | Use exceções, não códigos de retorno | `if err != nil` espalhado sem estrutura |
| CC-88 | Crie contexto de erro | Exception sem mensagem informativa |
| CC-90 | Não retorne null | Prefira Optional, lista vazia, ou exceção específica |
| CC-91 | Não passe null | Null como argumento obriga verificações em toda parte |
| CC-95 | Não ignore exceções capturadas | `except: pass` / `catch (e) {}` sem logging ou handling |

### Testes (CC-120 a CC-130)

| Regra | Princípio |
|---|---|
| CC-120 | Um conceito por teste — falha deve indicar o que quebrou |
| CC-121 | Um assert por teste (regra de ouro, exceções aceitáveis) |
| CC-124 | Testes devem ser F.I.R.S.T.: Fast, Independent, Repeatable, Self-validating, Timely |
| CC-126 | Testes limpos são tão importantes quanto código de produção |
| CC-128 | Testes habilitam mudança — sem teste, refatorar é arriscado |
| CC-130 | KISS nos testes também — teste simples e legível é melhor |

### Code Smells Relevantes (CC-155 a CC-202)

| Regra | Smell | Detecção |
|---|---|---|
| CC-162 | Imports/variáveis não utilizados | Pego por linter — **não reporte** |
| CC-164 | Feature Envy | Método usa mais dados de outra classe que da própria |
| CC-168 | Intimidade inadequada | Classes que acessam partes privadas umas das outras |
| CC-170 | Classe alternativa com interface diferente | Duas classes fazem a mesma coisa com nomes diferentes |
| CC-175 | Números mágicos | `if status == 7` → `if status == Status.PENDING` |
| CC-178 | Aninhamento profundo | Excede limite do nível? Early return resolve? |
| CC-180 | Switch statements repetidos | Mesmo switch em múltiplos lugares = oportunidade de polimorfismo |
| CC-185 | Método morto | Código nunca chamado — delete; use controle de versão |
| CC-190 | Generalidade especulativa | Abstração existindo apenas para "e se no futuro?" |

---

## 5. Clean Architecture (CA) — Referência Completa

### Parte 1 — Introdução

| Regra | Nome | Ponto de Revisão |
|---|---|---|
| CA-1 | Design = Arquitetura | Decisões consistentes em todos os níveis? |
| CA-2 | Objetivo: minimizar recursos humanos | Arquitetura reduz custo de manutenção? |
| CA-3 | Comportamento vs Estrutura | Sacrificando estrutura por features? |
| CA-4 | Maior valor = capacidade de mudar | Sistema fácil de evoluir sem reescritas? |

### Parte 2 — Paradigmas

| Regra | Nome | Ponto de Revisão |
|---|---|---|
| CA-5 | Programação Estruturada | Fluxo de controle claro? Evitando GOTOs e jumps? |
| CA-6 | OOP | Polimorfismo usado para inverter dependências? |
| CA-7 | Funcional | Imutabilidade usada? Efeitos colaterais contidos em borda? |

### Parte 3 — SOLID

| Regra | Princípio | Uma-Linha | Sinal de Violação |
|---|---|---|---|
| CA-8 | SRP | Uma razão para mudar | Classe serve múltiplos stakeholders diferentes |
| CA-9 | OCP | Aberto para extensão, fechado para modificação | Adicionar feature exige editar código existente |
| CA-10 | LSP | Subtipos substituíveis pelo tipo base | Verificações `instanceof` em código polimórfico |
| CA-11 | ISP | Sem dependências não usadas | Cliente importa interface com métodos que nunca usa |
| CA-12 | DIP | Dependa de abstrações | Lógica de negócio importa classe concreta de infra |

### Parte 4 — Princípios de Componente

#### Coesão

| Regra | Princípio | Pergunta |
|---|---|---|
| CA-14 | REP — Equivalência Reuso/Lançamento | Pode ser lançado e versionado independentemente? |
| CA-15 | CCP — Fechamento Comum | Coisas que mudam juntas vivem juntas? |
| CA-16 | CRP — Reuso Comum | Usar este componente força dependências desnecessárias? |

#### Acoplamento

| Regra | Princípio | Pergunta |
|---|---|---|
| CA-18 | ADP — Dependências Acíclicas | Há ciclos entre componentes/módulos? |
| CA-19 | SDP — Dependências Estáveis | Dependemos de componentes menos estáveis que nós? |
| CA-20 | SAP — Abstrações Estáveis | Componentes estáveis são abstratos o suficiente para permitir extensão? |

### Parte 5 — Arquitetura

| Regra | Nome | Ponto de Revisão |
|---|---|---|
| CA-21 | O que é Arquitetura | Decisões de tech bloqueadas cedo demais? |
| CA-22 | Independência | Independência de casos de uso, operações e deploy? |
| CA-25 | Duplicação | Duplicação verdadeira ou similaridade acidental? |
| CA-29 | Regras de Negócio | Lógica de negócio separada de detalhes técnicos? |
| CA-30 | Arquitetura Gritante | Estrutura revela casos de uso, não frameworks? |
| CA-31 | Clean Architecture | Dependências apontam apenas para dentro (camadas internas)? |

**A Regra de Dependência:**
```
Frameworks & Drivers (web, DB, UI)
        ↓
Interface Adapters (controllers, gateways, presenters)
        ↓
Application Business Rules (use cases)
        ↓
Enterprise Business Rules (entities)

Violações críticas (CA-31):
  ❌ Entity importa Controller
  ❌ Use Case importa classe Database concreta
  ❌ Regra de negócio depende de anotação de framework

Correto:
  ✅ Controller importa interface do Use Case
  ✅ Database implementa interface Repository definida pelo Use Case
  ✅ Entity é POJO/POCO sem dependências externas
```

### Parte 6 — Detalhes como Plugins

| Regra | Nome | Sinal Ruim |
|---|---|---|
| CA-36 | Database é detalhe | SQL diretamente em lógica de negócio |
| CA-37 | Web é detalhe | Lógica de negócio dentro de controllers/handlers |
| CA-38 | Framework é detalhe | Anotações de framework em entidades de domínio |
| CA-46 | Humble Object | Partes difíceis de testar não isoladas em objeto simples |
| CA-47 | Plugin Architecture | Núcleo do sistema não é independente de detalhes |
| CA-48 | Fronteira de Teste | Testes unitários exigem database/network para rodar |

**Checklist de testabilidade arquitetural:**

| Pergunta | Sinal bom | Sinal ruim |
|---|---|---|
| Posso trocar o banco sem mudar negócio? | Interface Repository | SQL em lógica de negócio |
| Posso trocar a UI sem mudar negócio? | Padrão Presenter/ViewModel | Negócio em controller |
| Posso testar o domínio sem infra? | Testes unitários puros | Testes requerem DB/rede |
| Posso rodar sem framework? | Core em classes puras | Core depende de Spring/Django/Rails |

---

## 6. Métricas e Isenções

### Diretrizes por Nível

| Métrica | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| Linhas/função | N/A | ≤80 | ≤50 | ≤30 | ≤20 |
| Parâmetros | N/A | ≤7 | ≤5 | ≤3 | ≤2 |
| Aninhamento | N/A | ≤5 | ≤4 | ≤3 | ≤2 |
| Tamanho PR | N/A | ≤800 | ≤500 | ≤300 | ≤200 |
| Cobertura testes | N/A | 30% | 60% | 80% | 95% |
| Tolerância DRY | N/A | 4× | 3× | 2× | 1× |

### Isenções

**Tamanho de função:** função de responsabilidade única não decomponível, switch/match grande, construtor de dados puro, mapeamento de configuração. Uma função clara de 60 linhas vence três funções confusas de 20.

**Parâmetros:** maioria com valores padrão (conte só obrigatórios), funções de configuração, Factory/Builder controlado por framework.

**DRY:** código similar com conhecimento de negócio diferente (teste: "se um muda, o outro SEMPRE deve mudar?" — se não → mantenha separado). Duplicação no mesmo arquivo é menor risco em L1–L3.

### Referência Rápida de Code Smells

| Smell | Regra | Detecção |
|---|---|---|
| Função longa | CC-20 | Excede limite do nível? |
| Muitos parâmetros | CC-26 | Excede limite do nível? |
| Números mágicos | CC-175 | Constantes não nomeadas? |
| Classe Deus | CA-8 | Múltiplas responsabilidades? |
| Feature Envy | CC-164 | Usa mais dados de outra classe? |
| Trem de Carga | CC-81 | `a.b().c().d()` em cadeia? |
| Estado global | PP-47 | Globais mutáveis? |
| Herança profunda | PP-51 | Hierarquia > 2 níveis? |
| Switch duplicado | CC-180 | Mesmo switch em múltiplos lugares? |
| Generalidade especulativa | CC-190 | Código para "e se no futuro"? |
| Acoplamento temporal | PP-48 | Depende de ordem não documentada? |
