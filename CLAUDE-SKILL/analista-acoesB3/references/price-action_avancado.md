# Price Action Avançado, Padrões de Candles e Volume

## Padrões de Candles de Reversão (Alta Relevância para Swing Trade)

### Reversão de Alta (fundo)
| Padrão | Descrição | Confirmação |
|---|---|---|
| Martelo (Hammer) | Corpo pequeno, sombra inferior longa (≥2x corpo), pouca sombra superior | Próximo candle fecha em alta |
| Engolfo de Alta | Candle de alta engole completamente o anterior de baixa | Volume acima da média |
| Estrela da Manhã | 3 candles: baixa / indecisão / alta | Após queda prolongada em suporte |
| Doji em suporte | Abertura = fechamento, sombras longas | Indecisão — aguardar confirmação |
| Piercing Line | Alta fecha acima da metade do candle de baixa anterior | Em suporte com volume |

### Reversão de Baixa (topo)
| Padrão | Descrição | Confirmação |
|---|---|---|
| Shooting Star | Corpo pequeno, sombra superior longa, pouca sombra inferior | Em resistência com volume |
| Engolfo de Baixa | Candle de baixa engole completamente o anterior de alta | Volume acima da média |
| Estrela da Tarde | 3 candles: alta / indecisão / baixa | Após alta prolongada em resistência |
| Harami de Baixa | Candle menor contido no anterior maior de alta | Confirma desaceleração |

---

## Análise de Volume

### OBV (On-Balance Volume)
```python
df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
# OBV subindo com preço subindo = tendência forte (confirmação)
# OBV caindo com preço subindo = divergência bearish (fraqueza)
# OBV subindo com preço caindo = divergência bullish (acumulação)
```

### VWAP (Volume Weighted Average Price)
```python
df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
# Preço acima do VWAP = pressão compradora
# Preço abaixo do VWAP = pressão vendedora
# Útil como suporte/resistência dinâmico
```

### Confirmação por Volume em Rompimentos
```python
vol_atual = df['Volume'].iloc[-1]
vol_med = df['Volume'].rolling(20).mean().iloc[-1]
fator = vol_atual / vol_med
if fator >= 1.5:
    print(f"✅ Rompimento com volume forte ({fator:.1f}x a média)")
elif fator >= 1.0:
    print(f"⚠️ Volume moderado ({fator:.1f}x a média) — aguardar confirmação")
else:
    print(f"❌ Sem volume no rompimento — sinal fraco")
```

---

## Análise Multi-Timeframe

### Hierarquia de Análise (top-down)
1. **Gráfico Semanal (1W)**: determinar a tendência primária
2. **Gráfico Diário (1D)**: identificar setup de entrada
3. **Gráfico de 4h (4H)**: timing preciso da entrada (opcional)

### Regra prática
- Só operar na direção da tendência **semanal**
- No diário: entrar em pullbacks contra-tendência dentro da tendência maior
- Evitar operações contra a MM200 semanal

```python
# Buscar dados semanais
df_semanal = yf.download("CMIG4.SA", period="5y", interval="1wk", auto_adjust=True, progress=False)
df_semanal['MM50w'] = df_semanal['Close'].rolling(50).mean()
df_semanal['MM200w'] = df_semanal['Close'].rolling(200).mean()

tendencia_semanal = "ALTA" if df_semanal['Close'].iloc[-1] > df_semanal['MM50w'].iloc[-1] else "BAIXA"
print(f"Tendência no gráfico semanal: {tendencia_semanal}")
```

---

## Padrões Gráficos de Continuação

### Figuras de Alta Relevância
| Figura | O que indica | Alvo projetado |
|---|---|---|
| Bandeira de Alta | Consolidação após impulso de alta | Entrada + altura do mastro |
| Triângulo Ascendente | Acumulação com topo plano e fundos crescentes | Largura da base projetada para cima |
| Canal de Alta | Topos e fundos ascendentes | Próxima linha superior do canal |
| Cup and Handle | Fundo arredondado + pequena correção | Profundidade da "xícara" projetada |

### Figuras de Reversão
| Figura | O que indica | Alvo projetado |
|---|---|---|
| Topo Duplo (M) | Falha em romper resistência 2x | Distância neckline-topo para baixo |
| Ombro-Cabeça-Ombro | Padrão clássico de reversão | Altura da cabeça projetada para baixo |
| Fundo Duplo (W) | Suporte testado 2x sem rompimento | Distância neckline-fundo para cima |

---

## Gestão de Risco — Fórmulas

### Tamanho de posição pelo risco fixo
```python
capital_total = 10000       # R$ disponível
risco_por_operacao = 0.02   # 2% do capital por operação
entrada = 10.84
stop_loss = 10.49

risco_unitario = entrada - stop_loss
max_perda = capital_total * risco_por_operacao
quantidade = int(max_perda / risco_unitario)

print(f"Risco unitário: R$ {risco_unitario:.2f}")
print(f"Máx perda tolerada: R$ {max_perda:.2f}")
print(f"Quantidade máxima de ações: {quantidade}")
print(f"Capital alocado: R$ {quantidade * entrada:.2f}")
```

### Relação Risco/Retorno
```python
entrada = 10.84
stop = 10.49
alvo = 11.50

risco = entrada - stop
retorno = alvo - entrada
rr = retorno / risco

print(f"R/R: 1:{rr:.1f} {'✅ Válido' if rr >= 2 else '❌ Não operar (R/R insuficiente)'}")
```

---

## Checklist Pré-Operação

- [ ] Tendência diária identificada (alta / baixa / lateral)
- [ ] Tendência semanal confirmada (não operar contra)
- [ ] Nível de entrada próximo a suporte/resistência forte
- [ ] Stop definido abaixo/acima de nível técnico
- [ ] Relação R/R ≥ 1:2 calculada
- [ ] Volume no rompimento/pullback confirmado
- [ ] RSI não em sobrecompra (>70) para compra ou sobrevenda (<30) para venda
- [ ] MACD alinhado com a direção da operação
- [ ] Aviso de risco incluído na análise