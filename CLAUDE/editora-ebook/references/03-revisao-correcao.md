# 03 — Revisão e Correção

**Agente**: REVISOR  
**Estágio**: M5

---

## Objetivo
Entregar texto limpo, correto e coeso, com diff comentado das alterações.

---

## Níveis de Revisão

O usuário pode solicitar um dos 3 níveis:

| Nível | Foco | Tempo |
|---|---|---|
| **Rápida** | Ortografia e gramática apenas | Rápido |
| **Padrão** | Ortografia + gramática + fluidez + coesão | Médio |
| **Profunda** | Tudo + estilo + consistência + normas ABNT | Detalhado |

Se não especificado, usar **Padrão**.

---

## Checklist de Revisão Padrão

### Ortografia e Gramática
- [ ] Ortografia (incluindo novo acordo ortográfico 2009)
- [ ] Concordância verbal (sujeito ↔ verbo)
- [ ] Concordância nominal (substantivo ↔ adjetivo)
- [ ] Regência verbal e nominal
- [ ] Crase (aplicação correta)
- [ ] Pontuação (vírgulas, ponto e vírgula, dois-pontos, travessão)
- [ ] Uso correto de aspas, parênteses, colchetes
- [ ] Maiúsculas e minúsculas (nomes próprios, títulos, início de frase)

### Coesão e Coerência
- [ ] Conectivos adequados entre frases e parágrafos
- [ ] Pronomes sem ambiguidade de referência
- [ ] Repetição excessiva de palavras (verificar e variar)
- [ ] Parágrafos com unidade temática
- [ ] Sequência lógica das ideias

### Estilo e Fluidez
- [ ] Frases muito longas (quebrar acima de 3 orações subordinadas)
- [ ] Voz passiva excessiva (converter para ativa quando possível)
- [ ] Nominalização excessiva ("fazer a realização de" → "realizar")
- [ ] Pleonasmos e redundâncias
- [ ] Jargão sem explicação (verificar contra o nível do público)

---

## Checklist ABNT (revisão profunda)

- [ ] Citações diretas curtas (até 3 linhas): entre aspas no corpo do texto
- [ ] Citações diretas longas (mais de 3 linhas): recuo 4cm, fonte 10, sem aspas
- [ ] Citações indiretas: sem aspas, com referência autor-data
- [ ] Notas de rodapé: numeração sequencial, fonte 10
- [ ] Referências bibliográficas: ordem alfabética, formatação ABNT NBR 6023
- [ ] Figuras e tabelas: título acima (tabela) ou abaixo (figura), fonte indicada
- [ ] Sumário: alinhamento e numeração das seções

---

## Formato de Output do REVISOR

### Opção A — Diff Comentado
```
[ORIGINAL]: "As pessoas que trabalha na empresa..."
[CORRIGIDO]: "As pessoas que trabalham na empresa..."
[NOTA]: Concordância verbal — sujeito "pessoas" (plural) exige "trabalham".
```

### Opção B — Texto Limpo + Resumo
Entregar o texto já corrigido, seguido de:
```
## Resumo das Correções
- X erros ortográficos corrigidos
- Y problemas de concordância resolvidos
- Z trechos reestruturados para melhor fluidez
- Principais alterações: [lista dos 3-5 mais relevantes]
```

### Opção C — Revisão Inline (Markdown)
Usar marcação para indicar alterações:
- ~~texto removido~~
- **texto adicionado** (em negrito)
- > [Nota do revisor] em blockquote

---

## Funcionalidades Extras

### Detector de Voz Passiva
Varrer o texto e listar todas as ocorrências de voz passiva,
com sugestão de reescrita em voz ativa para cada uma.

### Analisador de Legibilidade
Calcular e reportar:
- Média de palavras por frase
- Média de sílabas por palavra
- Índice Flesch adaptado para português
- Classificação: fácil / médio / difícil

### Padronizador de Estilo
Dado um guia de estilo (ex: sempre usar "e-mail" não "email",
sempre numerais por extenso até dez), aplicar consistentemente no texto.

### Revisão por Seção
Para ebooks longos, revisar capítulo por capítulo com relatório
consolidado ao final, apontando problemas recorrentes.
