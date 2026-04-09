# 🤖 Coleção de Skills para Claude

> Skills e ferramentas de IA prontas para uso no Claude.ai, abrangendo áreas jurídica, financeira e educacional.

[![Claude Skill](https://img.shields.io/badge/Claude-Skills-orange?logo=anthropic)](https://claude.ai)
[![Idioma](https://img.shields.io/badge/idioma-Português-green)](.)
[![Licença](https://img.shields.io/badge/licença-MIT-blue)](LICENSE)

---

## O que é isto?

Este repositório reúne **skills para o Claude (claude.ai)** — pacotes de instrução especializada que transformam o assistente em expert de diversas áreas. Cada skill é independente e pode ser instalada individualmente.

---

## Skills disponíveis

### 📜 [advogado-consumerista](CLAUDE-SKILL/advogado-consumerista/)
> Redigir petições iniciais para Juizados Especiais Cíveis com fundamentação no CDC, Código Civil, CPC e Constituição Federal.

**Funcionalidades:**
- Redação de petições iniciais estruturadas
- Fundamentação jurídica completa (CDC, CC, CPC, CF)
- Cálculo de danos materiais e morais
- Modo educativo sobre direitos do consumidor
- Minutas prontas para recursos

**Minutas incluídas:**
| Arquivo | Descrição |
|---|---|
| [`peticao_inicial.md`](CLAUDE-SKILL/advogado-consumerista/minutas/peticao_inicial.md) | Petição Inicial |
| [`recurso_inominado.md`](CLAUDE-SKILL/advogado-consumerista/minutas/recurso_inominado.md) | Recurso Inominado |
| [`embargos_declaracao.md`](CLAUDE-SKILL/advogado-consumerista/minutas/embargos_declaracao.md) | Embargos de Declaração |
| [`contrarrazoes.md`](CLAUDE-SKILL/advogado-consumerista/minutas/contrarrazoes.md) | Contrarrazões |
| [`agravo_interno.md`](CLAUDE-SKILL/advogado-consumerista/minutas/agravo_interno.md) | Agravo Interno |

---

### 📈 [analista-de-acoes-B3](CLAUDE-SKILL/analista-de-acoes-B3/)
> Análise de ações negociadas na bolsa de valores brasileira (B3).

**Arquivos:**
| Arquivo | Descrição |
|---|---|
| [`equity-analist-B3.zip`](CLAUDE-SKILL/analista-de-acoes-B3/equity-analist-B3.zip) | Pacote da skill |
| [`README.md`](CLAUDE-SKILL/analista-de-acoes-B3/README.md) | Documentação |
| [`CONTRIBUTING.md`](CLAUDE-SKILL/analista-de-acoes-B3/CONTRIBUTING.md) | Guia de contribuição |

---

### 📝 [simulador-prova](CLAUDE-SKILL/simulador-prova/)
> Simulação de provas e exercícios acadêmicos.

**Arquivos:**
| Arquivo | Descrição |
|---|---|
| [`SKILL.md`](CLAUDE-SKILL/simulador-prova/SKILL.md) | Definição da skill |

---

## Estrutura do repositório

```
IA/
├── CLAUDE-SKILL/
│   ├── advogado-consumerista/
│   │   ├── SKILL.md
│   │   └── minutas/
│   │       ├── peticao_inicial.md
│   │       ├── recurso_inominado.md
│   │       ├── embargos_declaracao.md
│   │       ├── contrarrazoes.md
│   │       └── agravo_interno.md
│   ├── analista-de-acoes-B3/
│   │   ├── README.md
│   │   ├── CONTRIBUTING.md
│   │   └── equity-analist-B3.zip
│   └── simulador-prova/
│       └── SKILL.md
├── README.md              # Esta documentação
└── .git/
```

---

## Instalação

### Pré-requisitos
- Conta no [Claude.ai](https://claude.ai)
- Acesso à funcionalidade de **Skills**

### Passo a passo

1. **Clone ou baixe este repositório:**

    ```bash
    git clone https://github.com/seu-usuario/IA.git
    ```

2. **No Claude.ai, acesse as configurações da sua conta.**

3. Acesse **CAPACIDADES**, na opção **HABILIDADES** clique em *Ir para Personalizar* e faça upload do arquivo `SKILL.md` da skill desejada.

4. **Confirme que a skill aparece na lista** de skills ativas.

5. **Teste** com um prompt adequado à skill instalada.

---

## Controle de Contribuição

Agradecemos o interesse em contribuir! Abaixo estão as diretrizes para ajudar a melhorar este repositório.

### Como reportar um problema

Use a aba **Issues** do GitHub. Ao abrir uma issue, inclua:

1. **Qual skill afetada** — advogado-consumerista, analista-de-acoes-B3 ou simulador-prova
2. **Descrição do comportamento esperado**
3. **Descrição do comportamento atual**
4. **Prompt utilizado** (se aplicável)

### Labels disponíveis

| Label | Quando usar |
|---|---|
| `bug` | Comportamento incorreto ou erro na skill |
| `melhoria` | Sugestão de aprimoramento |
| `novo-recurso` | Proposta de nova funcionalidade ou skill |
| `documentação` | Correção ou melhoria na documentação |
| `discussão` | Questão aberta ou dúvida |

### Como propor melhorias

1. Abra uma issue com o label `melhoria` ou `novo-recurso` **antes** de abrir um PR
2. Descreva o problema que a melhoria resolve
3. Aguarde feedback antes de implementar

Para mudanças pequenas (correções de texto, ajustes de formatação), pode abrir um PR direto.

### Fluxo de contribuição (Pull Request)

```bash
# 1. Fork e clone
git clone https://github.com/seu-usuario/IA.git
cd IA

# 2. Crie uma branch descritiva
git checkout -b melhoria/nova-minuta-recurso-especial

# 3. Faça suas alterações
# Edite os arquivos da skill desejada

# 4. Commit com mensagem clara
git commit -m "feat: adiciona minuta de Recurso Especial ao advogado-consumerista"

# 5. Push e abra o PR
git push origin melhoria/nova-minuta-recurso-especial
```

### Padrão de commits

Use o formato [Conventional Commits](https://www.conventionalcommits.org/):

| Prefixo | Quando usar |
|---|---|
| `feat:` | Nova funcionalidade, minuta ou skill |
| `fix:` | Correção de erro ou lógica incorreta |
| `docs:` | Mudança apenas em documentação |
| `refactor:` | Reorganização sem mudança de comportamento |
| `test:` | Adição de exemplos ou casos de teste |

### O que pode ser alterado

#### Skills individuais (`SKILL.md`, minutas)
- Mudanças aqui afetam diretamente o comportamento do Claude
- Todo PR que altere um `SKILL.md` deve incluir um exemplo de antes/depois

#### `README.md`
- Melhorias de clareza, exemplos adicionais, correções — sempre bem-vindos

#### Novas skills
- Para adicionar uma nova skill, crie uma pasta em `CLAUDE-SKILL/` com o `SKILL.md` e outros arquivos necessários
- Abra uma issue de discussão primeiro

### O que NÃO alterar sem discussão prévia
- A estrutura base do repositório sem propor na issue
- Conteúdo que afete múltiplas skills simultaneamente

### Tabela de Contribuição por Skill

| Skill | Status | Contribuições |
|---|---|---|
| advogado-consumerista | ✅ Ativa | Minutas, fundamentação, correções |
| analista-de-acoes-B3 | ✅ Ativa | Análises, indicadores, correções |
| simulador-prova | ✅ Ativa | Modelos de prova, cenários, correções |

---

## Dúvidas?

Abra uma issue com o label `discussão` ou use as Discussions do repositório.

---

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.
