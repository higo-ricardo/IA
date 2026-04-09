# Guia de Contribuição

Obrigado pelo interesse em contribuir com o **equity-analyst-B3**! Este documento explica como ajudar a melhorar essa ferramenta de forma eficiente.

---

## Como reportar um problema

Use a aba **Issues** do GitHub. Ao abrir uma issue, inclua:

1. **Descrição do comportamento esperado** — o que você esperava que a análise contivesse.
2. **Descrição do comportamento atual** — o que a análise apresentou.
3. **Prompt utilizado** — o trecho da conversa que gerou o problema.
4. **Ticker da ação** — qual ação foi analisada (ex: PETR4, VALE3)

### Labels disponíveis

| Label | Quando usar |
|---|---|
| `bug` | Análise incorreta ou erro no cálculo de indicadores |
| `melhoria` | Sugestão de aprimoramento em indicadores ou lógica |
| `novo-recurso` | Proposta de novo indicador ou funcionalidade |
| `documentação` | Correção ou melhoria nos docs |
| `discussão` | Questão aberta sobre análise técnica |

---

## Como propor melhorias

1. Abra uma issue com o label `melhoria` ou `novo-recurso` **antes** de abrir um PR.
2. Descreva o problema que a melhoria resolve na análise técnica — não apenas a solução.
3. Aguarde feedback do patrono do projeto antes de implementar.

Para mudanças pequenas (correções de texto, exemplos), pode abrir um PR direto.

---

## Fluxo de contribuição (Pull Request)

```bash
# 1. Fork e clone
git clone https://github.com/seu-usuario/equity-analyst-B3.git
cd equity-analyst-B3

# 2. Crie uma branch descritiva
git checkout -b melhoria/novo-indicador-stochastico

# 3. Faça suas alterações
# Edite equity-analyst-B3.md, README.md, etc.

# 4. Commit com mensagem clara
git commit -m "feat: adiciona indicador estocástico à análise técnica"

# 5. Push e abra o PR
git push origin melhoria/novo-indicador-stochastico
```

---

## Padrão de commits

Use o formato [Conventional Commits](https://www.conventionalcommits.org/):

| Prefixo | Quando usar |
|---|---|
| `feat:` | Novo indicador ou funcionalidade na análise |
| `fix:` | Correção de cálculo incorreto ou lógica errada |
| `docs:` | Mudança apenas em documentação |
| `refactor:` | Reorganização sem mudança no comportamento |
| `test:` | Adição de exemplos de análise ou casos de teste |

---

## O que pode ser alterado

### `equity-analyst-B3.md` (arquivo principal)
- Mudanças aqui afetam diretamente o comportamento do Claude na análise.
- Todo PR que altere o `equity-analyst-B3.md` deve incluir pelo menos um exemplo de análise antes/depois mostrando a diferença.


### `README.md`
- Melhorias de clareza, exemplos de análises adicionais, correções de português — sempre bem-vindos.
- Não altere os diagramas ASCII sem propor a versão nova na issue primeiro.

### Novos arquivos
- Se propor recursos bundled (scripts, referências), abra uma issue de discussão primeiro — isso altera a estrutura do repositório.

---

## O que NÃO alterar sem discussão prévia

- O código python é o core da skill, logo as mudanças nele afeta na qualidade do resultado. 
- A ordem das 5 seções — mudanças aqui têm impacto sistêmico
- O frontmatter YAML do `equity-analyst-B3.md` (especialmente `name` e `description`) — afeta o triggering

---

## Dúvidas?

Abra uma issue com o label `discussão` ou use as Discussions do repositório.
