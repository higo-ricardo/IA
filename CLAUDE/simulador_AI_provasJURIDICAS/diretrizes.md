# Diretrizes — Distratores e Confidence Score

> Carregar ao criar alternativas incorretas e ao exibir questões.

---

## Distratores Inteligentes

### Técnicas de Distratores (atualizado)

| Técnica | Descrição | Exemplo |
|--------:|----------|--------|
| **Oposição Simples** | Nega o gabarito de forma direta | "Pai proíbe filho" |
| **Negação simples** | Adiciona 'NÃO' quando afirmativa ou remove 'NÃO' quando negativa | "Pai não autoriza filho" |
| **Inversão Sujeito/Objeto** | Inverte sujeito e objeto da norma | "Filho autoriza pai" |
| **Elemento Periférico** | Substitui um detalhe secundário (ex.: beneficiário, prazo) | "Pai autoriza neto" |
| **Confusão Normativa** | Mistura norma correta com outra norma próxima | "Pai autoriza, como em arrendamento rural" |
| **Pré-requisito Ausente** | Remove condição necessária do gabarito | "Pai autoriza (sem atingir maioridade)" |
| **Qualificador Falso** | Adiciona condição/qualificador que inverte o sentido | "Pai autoriza, desde que o filho discorde" |

### Regras e Métricas
- Nenhum absurdo óbvio
- Gabarito aleatório A–E
- Máx. 1 técnica repetida por questão
- **Diferença semântica mínima:** todo distrator deve ter diferença ≥ 25% em relação ao gabarito (validar com métrica de similaridade)

### Observações
- Validar especialmente tipos 2 e 3 (Negação simples e Inversão Sujeito/Objeto) para evitar contradições ambíguas
- Em níveis Sênior, preferir distratores com pequenas diferenças formais (tipos 3,5,6,7) para aumentar o desafio

---

## Confidence Score

Exibir em **todas** as questões, antes do enunciado:

```
[Confidence: X/10]
```

| Score | Significado |
|-------|-------------|
| 9–10 | Extraída do material ou conhecimento consolidado sólido |
| 7–8 | Bem fundamentada com pequena inferência |
| 5–6 | Inferência moderada — **nunca exibir** (mínimo: 7) |
| 1–4 | Alta inferência — **nunca exibir** (reformular) |

> **Regra**: Nunca exibir questão com Confidence < 7. Reformular ou substituir.
