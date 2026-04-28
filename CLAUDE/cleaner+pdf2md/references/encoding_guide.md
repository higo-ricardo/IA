# Guia de Encoding — Referência da Skill markdown-cleaner

Leia este arquivo quando a tarefa envolver caracteres embaralhados, encoding corrompido
ou texto em português com acentuação quebrada.

---

## Estratégia de Detecção

O `EncodingDetector` tenta os encodings nesta ordem:

1. `utf-8` — padrão moderno, maioria dos editores atuais
2. `utf-8-sig` — UTF-8 com BOM (common no Windows Notepad)
3. `latin-1` — superset do ISO-8859-1, nunca levanta exceção (lê qualquer byte)
4. `cp1252` — Windows-1252, variante do latin-1 com caracteres extras
5. `iso-8859-1` — padrão ISO, sinônimo de latin-1 na maioria dos casos
6. **Fallback binário** — lê como bytes e decodifica com `errors='replace'`

---

## Sintomas e Diagnóstico

| Sintoma no texto | Causa provável | Solução |
|---|---|---|
| `Ã£` no lugar de `ã` | UTF-8 lido como latin-1 | PT_BR_CORRECT |
| `Ã©` no lugar de `é` | UTF-8 lido como latin-1 | PT_BR_CORRECT |
| `â\x80\x99` no lugar de `'` | UTF-8 quebrado (apóstrofo) | REPLACEMENTS |
| `\x82`, `\x84`, `\x91` | cp1252 lido errado | REPLACEMENTS |
| `\xa0` (espaço duro) | latin-1 NBSP | Substituído por espaço normal |
| `\xc3\xa7` como string literal | UTF-8 bytes como texto | PT_BR_CORRECT |
| `?` ou `▯` no texto | Decodificação com `errors='replace'` | Revisar encoding original |

---

## Mapeamento de Caracteres pt-BR Críticos

### Sequências duplas (UTF-8 mal decodificado como latin-1):

```
Ã¡ → á      Ã© → é      Ã­ → í      Ã³ → ó      Ãº → ú
Ã£ → ã      Ãµ → õ      Ã¢ → â      Ãª → ê      Ã´ → ô
Ã§ → ç      Ã‡ → Ç      Ã… → à
```

### Caracteres cp1252 problemáticos:

```
\x91 → '    \x92 → '    \x93 → "    \x94 → "
\x95 → •    \x96 → -    \x97 → —    \x85 → ...
\xa0 → ' '  \xaa → ª    \xba → º    \xb0 → °
```

---

## BOM (Byte Order Mark)

O BOM `\ufeff` aparece no início de arquivos UTF-8-SIG (gerados pelo Excel ou
Notepad do Windows). O cleaner o remove automaticamente.

**Detectar manualmente:**
```python
with open("arquivo.md", "rb") as f:
    inicio = f.read(3)
print(inicio)  # b'\xef\xbb\xbf' indica BOM
```

---

## Caracteres de Controle Removidos

O pipeline remove automaticamente os bytes `\x00–\x08`, `\x0b`, `\x0c`, `\x0e–\x1f`,
que são caracteres de controle ASCII inválidos em texto. Os bytes `\x09` (tab),
`\x0a` (newline) e `\x0d` (carriage return) são **preservados** pois têm uso legítimo.

---

## Uso no Código

```python
from scripts.md_cleaner import EncodingDetector

# Detectar e corrigir automaticamente
encoding_usado, conteudo_corrigido = EncodingDetector.detect_and_correct("arquivo.md")

# Apenas corrigir string já em memória
conteudo_ok = EncodingDetector.correct_characters(conteudo_bruto)
```

---

## Diagnóstico Rápido via CLI

```bash
# Ver encoding atual do arquivo (Linux/Mac)
file -i meu_arquivo.md

# Ver primeiros bytes (detectar BOM)
xxd meu_arquivo.md | head -1

# Converter manualmente com iconv
iconv -f cp1252 -t utf-8 entrada.md > saida.md
```
