# 10 — Versionamento e Estado do Projeto

**Agente**: ORQUESTRADOR  
**Estágio**: M7/M8

---

## Objetivo
Manter controle de versões do projeto, histórico de alterações,
possibilidade de rollback e estado persistente entre sessões.

---

## Estrutura de Estado do Projeto

O ORQUESTRADOR mantém um **Bloco de Estado** que deve ser incluído
no início de cada sessão de trabalho:

```markdown
## 📋 ESTADO DO PROJETO — [TÍTULO]

**Versão atual**: v[X.Y]  
**Última atualização**: [data]  
**Estágio atual no pipeline**: M[X] — [nome do estágio]  
**Score atual**: [X.X]/10  

### Sumário de Progresso
| Capítulo | Status | Score | Versão |
|---|---|---|---|
| Introdução | ✅ Completo | 8.2 | v1.3 |
| Cap. 1 | ✅ Completo | 7.8 | v1.1 |
| Cap. 2 | 🔶 Em revisão | 6.5 | v0.2 |
| Cap. 3 | ❌ Pendente | — | — |

### Histórico de Versões
| Versão | Data | Agente | Descrição da mudança |
|---|---|---|---|
| v1.3 | [data] | COPYWRITER | Reescrita do gancho da Introdução |
| v1.2 | [data] | REVISOR | Correção ortográfica Cap. 1 e 2 |
| v1.1 | [data] | AUTOR | Expansão do Cap. 1 (+800 palavras) |
| v1.0 | [data] | ARQUITETO | Estrutura inicial aprovada |

### Decisões Editoriais Registradas
- Tom: [descrição]
- Público-alvo: [descrição]
- Estilo de citação: [ABNT / Chicago / APA / informal]
- Persona do leitor: [nome/descrição]
- Voz autoral: [descrição]
```

---

## Sistema de Versionamento

### Numeração
```
v1.0 — Versão base (estrutura aprovada)
v1.1, v1.2... — Revisões menores (correções, adições pontuais)
v2.0 — Revisão maior (reestruturação, novo capítulo, mudança de tom)
vX.Y-draft — Rascunho não aprovado
vX.Y-final — Versão aprovada para publicação
```

### Política de Rollback
Se o score de qualquer versão cair abaixo de 7.0 em relação à versão anterior:
1. ORQUESTRADOR detecta regressão
2. Notifica o usuário com comparação side-by-side
3. Oferece: manter nova versão / reverter / mesclar melhor de cada
4. Registra o rollback no histórico

---

## Retomada de Sessão

Para retomar trabalho em uma sessão nova, o usuário deve fornecer:

```
/retomar-projeto
[Cole aqui o Bloco de Estado da última sessão]
```

O ORQUESTRADOR irá:
1. Carregar o estado
2. Identificar o próximo passo no pipeline
3. Perguntar: "Deseja continuar de onde paramos (M[X]) ou
   há alguma tarefa específica que precisa de atenção?"

---

## Comandos de Versionamento

| Comando | Ação |
|---|---|
| `/salvar-estado` | Gera o Bloco de Estado atual para copiar |
| `/histórico` | Lista todas as versões com datas e descrições |
| `/rollback v[X.Y]` | Restaura descrição e decisões da versão indicada |
| `/comparar v[X] v[Y]` | Compara dois capítulos em versões diferentes |
| `/diff` | Mostra o que mudou desde a última versão salva |

---

## Exportação do Projeto

O ORQUESTRADOR pode gerar um **arquivo de projeto** completo:

```markdown
# PROJETO: [TÍTULO]
## Exportado em: [data]

### ESTADO
[Bloco de Estado completo]

### DOCUMENTO DE PROJETO
[Briefing e decisões editoriais]

### SUMÁRIO APROVADO
[Sumário atual]

### CONTEÚDO
[Todo o conteúdo por capítulo, com versão indicada]

### HISTÓRICO COMPLETO
[Todas as versões e mudanças]
```

Este arquivo pode ser salvo pelo usuário e colado em uma nova
sessão para retomar o trabalho sem perda de contexto.
