# 🤖 equity-analyst-B3

> Uma skill para Claude executar análise técnica completa de ações brasileiras (B3) para swing trade no gráfico diário, com indicadores técnicos, suportes/resistências, pontos de entrada, stop loss e alvos.

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-orange?logo=anthropic)](https://claude.ai)
[![Idioma](https://img.shields.io/badge/idioma-Português-green)](.)
[![Licença](https://img.shields.io/badge/licença-MIT-blue)](LICENSE)

---

## O que é isto?

**equity-analyst-B3** é uma skill para o Claude (claude.ai) que transforma o assistente num analista técnico especializado em ações brasileiras listadas na B3. Em vez de respostas genéricas, o Claude fornece análises estruturadas em 5 seções obrigatórias: Tendência Atual, Suportes e Resistências, Ponto de Entrada, Stop Loss e Preço Alvo, utilizando dados reais via Yahoo Finance e indicadores técnicos como médias móveis, RSI, MACD, Bandas de Bollinger e Fibonacci.

A skill foi projetada para traders e investidores que usam o Claude para análises técnicas de ações brasileiras, garantindo consistência e base em dados reais para decisões de swing trade.

---

## Funcionalidades

- **Coleta de dados reais** via Yahoo Finance (yfinance) — preços, volume e indicadores atualizados
- **Cálculo automático de indicadores técnicos** — médias móveis (EMA/SMA), RSI, MACD, Bandas de Bollinger, Fibonacci
- **Identificação de suportes e resistências** baseada em toques múltiplos, médias e retrações Fibonacci
- **Análise de tendência** com base em médias móveis e padrões de preço
- **Sugestões de entrada, stop loss e alvo** com relação risco/retorno ≥ 1:2
- **Estrutura obrigatória de saída** em 5 seções para clareza e consistência
- **Avisos educacionais** sobre riscos e caráter não-recomendatório da análise

---

## Demonstração rápida

Após instalar a skill, basta iniciar uma conversa no Claude com algo como:

```
Analise tecnicamente a ação PETR4 para swing trade.
```

ou

```
Quais os suportes e resistências da VALE3?
```

O Claude vai:
1. Coletar dados históricos da ação via Yahoo Finance
2. Calcular indicadores técnicos automaticamente
3. Identificar suportes, resistências e tendência
4. Sugerir pontos de entrada, stop loss e alvo com justificativas
5. Entregar análise em 5 seções estruturadas

---

## Instalação

### Pré-requisitos
- Conta no [Claude.ai](https://claude.ai).
- Acesso à funcionalidade de **Skills**.

### Passo a passo

1. **Clone ou baixe este repositório:**

    ```bash
    git clone https://github.com/seu-usuario/equity-analyst-B3.git
    ```

2. **No Claude.ai, acesse as configurações do seu Projeto.**

3. **Adicione uma nova skill** e faça upload do arquivo `equity-analyst-B3.md`.

4. **Confirme que a skill aparece na lista** de skills ativas.

5. **Teste** com a frase de ativação: `"analise tecnica da ação CMIG4"`.

---

## Estrutura do repositório

```
equity-analyst-B3/
├── equity-analyst-B3.md  # Definição da skill (instalável no Claude)
├── README.md             # Esta documentação
├── CONTRIBUTING.md       # Guia de contribuição
├── LICENSE               # Licença MIT
```

---

## Como funciona — as 5 seções obrigatórias

```
┌─────────────────────────────────────────────────────────┐
│  SEÇÃO 1 — Tendência Atual                              │
│                                                         │
│  Análise baseada em médias móveis e padrões de preço     │
│  Indicação de alta, baixa ou lateral                     │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  SEÇÃO 2 — Suportes e Resistências                       │
│                                                         │
│  Identificação de níveis chave com justificativas        │
│  Baseada em toques, médias e Fibonacci                   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  SEÇÃO 3 — Ponto de Entrada                              │
│                                                         │
│  Sugestão específica de preço e gatilho                  │
│  Compra ou venda com justificativa técnica               │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  SEÇÃO 4 — Stop Loss                                     │
│                                                         │
│  Nível de proteção com justificativa                     │
│  Abaixo do suporte para compras                          │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  SEÇÃO 5 — Preço Alvo                                   │
│                                                         │
│  Objetivo de lucro com relação risco/retorno            │
│  Sempre ≥ 1:2                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Regra de Ouro — Gestão de Risco

> **Nunca arrisque mais que 2% do capital por operação e sempre confirme volume em rompimentos.**

| Boas práticas | O que evitar |
|---|---|
| Usar stop loss em todas as operações | Operar sem proteção de risco |
| Confirmar rompimentos com volume | Ignorar volume em sinais |
| Atualizar análise diariamente | Usar análise antiga para decisões |
| Diversificar posições | Concentrar tudo em uma ação |

---

## Casos de uso típicos

- Analisar tecnicamente ações brasileiras para swing trade
- Identificar suportes e resistências de papéis da B3
- Sugerir pontos de entrada e saída com stop loss
- Avaliar tendência atual de uma ação específica
- Calcular alvos com relação risco/retorno adequada

---

## Limitações conhecidas

- A análise depende de dados históricos do Yahoo Finance — pode haver atrasos ou indisponibilidades
- Foco em gráfico diário para swing trade — não substitui análise intradiária ou fundamentalista
- Indicadores técnicos não garantem resultados — são ferramentas probabilísticas
- Dados em tempo real não são suportados — use para planejamento, não execução em tempo real

---

## Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para o guia completo.

Formas de contribuir:
- Reportar bugs na análise técnica via Issues
- Propor novos indicadores ou melhorias na lógica
- Adicionar exemplos de análises em diferentes cenários de mercado
- Melhorar a documentação ou tradução

---

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.

---

## Créditos
Desenvolvido como skill para o ecossistema Claude (Anthropic).  
Análises baseadas em indicadores técnicos padrão e dados do Yahoo Finance.
