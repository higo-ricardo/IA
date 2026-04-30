---
name: equity-analyst-B3
description: |
  Executa análise técnica completa de ações brasileiras (B3) para swing trade no gráfico diário, estruturada em 5 seções obrigatórias: Tendência Atual, Suportes e Resistências, Ponto de Entrada, Stop Loss e Preço Alvo. Utiliza dados reais via yfinance + indicadores técnicos (médias móveis, IFR/RSI, MACD, Bandas de Bollinger, Fibonacci). Use esta skill SEMPRE que o usuário pedir para:
  - analisar tecnicamente uma ação da B3 (ex: CMIG4, PETR4, VALE3, ITUB4)
  - identificar suporte, resistência, entrada, stop loss ou alvo de uma ação
  - fazer análise gráfica diária ou semanal de qualquer papel
  - sugerir pontos de compra ou venda para swing trade ou position trade
  - descrever a tendência atual de uma ação brasileira
  - perguntas como "onde comprar CMIG4?", "qual o stop de VALE3?", "PETR4 está em alta?"
  Use mesmo que o usuário não mencione "análise técnica" explicitamente.
compatibility:
  python_libs: [yfinance, pandas, numpy, pandas_ta, matplotlib]
---

# Skill: Análise Técnica de Ações Brasileiras (Swing Trade — Gráfico Diário)

## Objetivo
Produzir análise técnica estruturada em **5 seções obrigatórias**, com dados reais, indicadores calculados via código Python, e interpretação fundamentada para operações de swing trade no gráfico diário (timeframe 1D).

---

## Fluxo de Execução

### 1. Coleta de Dados
- Fonte: **Yahoo Finance via `yfinance`** — ticker no formato `XXXX4.SA`
- Período mínimo: **2 anos** de dados diários (garante médias longas + Fibonacci confiável)
- Colunas necessárias: `Open`, `High`, `Low`, `Close`, `Volume`

### 2. Cálculo dos Indicadores Técnicos

| Indicador | Parâmetro padrão | Finalidade |
|---|---|---|
| MM9 (EMA curta) | 9 períodos | Tendência de curto prazo |
| MM21 (EMA média) | 21 períodos | Tendência de médio prazo |
| MM50 (SMA) | 50 períodos | Tendência intermediária |
| MM200 (SMA) | 200 períodos | Tendência de longo prazo |
| RSI/IFR | 14 períodos | Sobrecompra/sobrevenda |
| MACD | 12/26/9 | Momentum e cruzamentos |
| Bandas de Bollinger | 20/2 | Volatilidade e compressão |
| Volume médio | 20 dias | Confirmação de movimentos |
| Fibonacci | Swing mais recente | Suporte/resistência dinâmica |

### 3. Identificação Automática de S/R
- **Suportes**: mínimas locais com ≥2 toques, MM200, MM50, retração Fibonacci (38.2%, 50%, 61.8%)
- **Resistências**: máximas locais com ≥2 toques, topo histórico, extensão Fibonacci (127.2%, 161.8%)
- **Prioridade**: nível testado mais vezes + coincidência com MM ou Fibonacci = nível mais forte

### 4. Lógica de Sinalização para Swing Trade

#### Cenário de Compra
- Preço > MM9 > MM21 > MM50 → tendência de alta confirmada
- RSI acima 30 e subindo (momentum positivo sem sobrecompra extrema)
- MACD acima da linha de sinal e acima do zero
- Volume na última sessão acima da média de 20 dias
- **Entrada**: pullback em suporte próximo ou rompimento de resistência com volume

#### Cenário de Venda/Short
- Preço < MM9 < MM21 → tendência de baixa
- RSI abaixo de 50 e caindo
- MACD abaixo da linha de sinal
- **Entrada**: repique em resistência sem volume

#### Cenário Lateral
- Preço oscilando entre MM50 e MM200 sem direção clara
- RSI entre 45–55
- MACD próximo do zero com cruzamentos frequentes
- **Estratégia**: aguardar rompimento com volume antes de operar

### 5. Cálculo de Stop Loss e Alvo

| Tipo de operação | Stop Loss | Alvo mínimo | Relação R/R |
|---|---|---|---|
| Compra em suporte | Abaixo do suporte -1% | Próxima resistência | ≥ 1:2 |
| Compra em rompimento | Abaixo do nível rompido -1% | Projeção da figura/canal | ≥ 1:2 |
| Venda em resistência | Acima da resistência +1% | Próximo suporte | ≥ 1:2 |

**Regra obrigatória**: só sugerir a operação se a relação Risco/Retorno for ≥ 1:2.

---

## Template de Código Python

```python
import yfinance as yf
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# === PARÂMETROS ===
TICKER = "CMIG4.SA"   # Altere conforme necessário
PERIODO = "2y"

# === COLETA ===
df = yf.download(TICKER, period=PERIODO, auto_adjust=True, progress=False)
df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
df = df.dropna()
print(f"Total de pregões: {len(df)} | Último preço: R$ {df['Close'].iloc[-1]:.2f}")

# === MÉDIAS MÓVEIS ===
df['MM9']   = df['Close'].ewm(span=9).mean()
df['MM21']  = df['Close'].ewm(span=21).mean()
df['MM50']  = df['Close'].rolling(50).mean()
df['MM200'] = df['Close'].rolling(200).mean()

# === RSI ===
delta = df['Close'].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()
rs = gain / loss
df['RSI'] = 100 - (100 / (1 + rs))

# === MACD ===
ema12 = df['Close'].ewm(span=12).mean()
ema26 = df['Close'].ewm(span=26).mean()
df['MACD']   = ema12 - ema26
df['Signal'] = df['MACD'].ewm(span=9).mean()
df['Hist']   = df['MACD'] - df['Signal']

# === BOLLINGER BANDS ===
df['BB_mid']   = df['Close'].rolling(20).mean()
df['BB_upper'] = df['BB_mid'] + 2 * df['Close'].rolling(20).std()
df['BB_lower'] = df['BB_mid'] - 2 * df['Close'].rolling(20).std()

# === VOLUME MÉDIO ===
df['Vol_med20'] = df['Volume'].rolling(20).mean()

# === ÚLTIMOS VALORES ===
ultimo = df.iloc[-1]
preco_atual = ultimo['Close']

print(f"""
╔══════════════════════════════════════════════╗
║  INDICADORES — {TICKER} (último pregão)
╠══════════════════════════════════════════════╣
║  Preço atual:  R$ {preco_atual:.2f}
║  MM9  (EMA):   R$ {ultimo['MM9']:.2f}   {'✅ Acima' if preco_atual > ultimo['MM9'] else '❌ Abaixo'}
║  MM21 (EMA):   R$ {ultimo['MM21']:.2f}  {'✅ Acima' if preco_atual > ultimo['MM21'] else '❌ Abaixo'}
║  MM50 (SMA):   R$ {ultimo['MM50']:.2f}  {'✅ Acima' if preco_atual > ultimo['MM50'] else '❌ Abaixo'}
║  MM200 (SMA):  R$ {ultimo['MM200']:.2f} {'✅ Acima' if preco_atual > ultimo['MM200'] else '❌ Abaixo'}
║  RSI (14):     {ultimo['RSI']:.1f}  {'⚡ Sobrecomprado' if ultimo['RSI'] > 70 else ('🔵 Sobrevendido' if ultimo['RSI'] < 30 else '🟢 Neutro')}
║  MACD:         {ultimo['MACD']:.4f} | Signal: {ultimo['Signal']:.4f}
║  BB Upper:     R$ {ultimo['BB_upper']:.2f} | Lower: R$ {ultimo['BB_lower']:.2f}
║  Volume:       {ultimo['Volume']:,.0f} | Média20: {ultimo['Vol_med20']:,.0f}
╚══════════════════════════════════════════════╝
""")

# === FIBONACCI (último swing) ===
janela = 60  # pregões
recente = df.tail(janela)
topo = recente['High'].max()
fundo = recente['Low'].min()
retracao = {
    '0%':     topo,
    '23.6%':  topo - 0.236 * (topo - fundo),
    '38.2%':  topo - 0.382 * (topo - fundo),
    '50.0%':  topo - 0.500 * (topo - fundo),
    '61.8%':  topo - 0.618 * (topo - fundo),
    '100%':   fundo,
}
print("Retrações de Fibonacci (últimos 60 pregões):")
for nivel, preco in retracao.items():
    print(f"  {nivel:6s} → R$ {preco:.2f}")
```

---

## Estrutura de Saída Obrigatória

A análise deve sempre ser entregue com **exatamente estas 5 seções**, em português, com os títulos em negrito:

```
**1. Tendência Atual**
Descreva alta / baixa / lateral com base nas MMs e no padrão de topos/fundos.
Informe se preço está acima/abaixo de MM9, MM21, MM50, MM200.

**2. Principais Níveis de Suporte e Resistência**
Mínimo: 2 suportes + 2 resistências com valores em R$ e justificativa técnica.
Associar cada nível a: mínima/máxima histórica, MM, Fibonacci ou toque múltiplo.

**3. Ponto de Entrada**
Valor específico em R$ com justificativa (ex: "pullback na MM21 em R$ X,XX").
Indicar se é compra ou venda e qual o gatilho de entrada (candle, volume, rompimento).

**4. Preço de Stop Loss**
Valor específico em R$ abaixo/acima do suporte/resistência de referência.
Justificar o nível escolhido tecnicamente.

**5. Preço Alvo**
Valor(es) em R$ com justificativa (ex: "resistência histórica em R$ X,XX").
Calcular e informar a relação Risco/Retorno (R/R).
```

---

## Avisos Obrigatórios na Saída

Incluir sempre ao final:
> ⚠️ *Esta análise é de caráter educacional e não constitui recomendação de investimento. Opere sempre com gestão de risco adequada ao seu perfil. Dados obtidos via Yahoo Finance.*

---

## Limitações e Boas Práticas

1. **Análise técnica não prevê o futuro** — indica probabilidades baseadas em padrões históricos
2. **Confirmar volume** em rompimentos: sem volume, o sinal é fraco
3. **Não operar contra a tendência** do gráfico semanal sem confirmação clara
4. **Atualizar a análise diariamente** para swing trade — níveis mudam com o mercado
5. **Gestão de risco**: nunca arriscar mais que 2% do capital por operação

---

## Referências Complementares
Para análise avançada com múltiplos timeframes, padrões de candles (price action) e análise de volume (OBV, VWAP), consulte:
`references/price_action_avancado.md`
