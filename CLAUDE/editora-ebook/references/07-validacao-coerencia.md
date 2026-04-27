# 07 — Validação e Coerência

**Agente**: CRÍTICO  
**Estágio**: M5/M7

---

## Objetivo
Garantir que o ebook seja factualmente correto, internamente coerente
e livre de contradições, alucinações e inconsistências.

---

## Checklist de Validação

### Anti-Alucinação
- [ ] Toda estatística citada tem fonte identificável
- [ ] Toda citação de pessoa real é verificável
- [ ] Datas e fatos históricos estão corretos
- [ ] Nomes de empresas, produtos e marcas estão escritos corretamente
- [ ] Afirmações absolutas ("sempre", "nunca", "100%") estão justificadas
- [ ] Previsões e opiniões estão sinalizadas como tal

Protocolo: ao detectar afirmação não verificável, o CRÍTICO:
1. Sinaliza: `[⚠️ VERIFICAR: esta afirmação precisa de fonte]`
2. Sugere uma versão mais cautelosa da afirmação
3. Indica onde buscar a verificação

### Consistência Interna (não-ficção)
- [ ] Termos usados com o mesmo significado em todo o ebook
- [ ] Posições do autor não se contradizem entre capítulos
- [ ] Frameworks e modelos apresentados são coerentes entre si
- [ ] Numeração de listas e passos está correta e sequencial
- [ ] Referências cruzadas entre capítulos estão corretas

### Consistência Interna (ficção)
- [ ] Linha do tempo dos eventos é coerente
- [ ] Características físicas dos personagens não mudam sem justificativa
- [ ] Poderes/habilidades/limitações dos personagens são consistentes
- [ ] Geografia e cenários são coerentes
- [ ] Motivações dos personagens são plausíveis e consistentes
- [ ] Chekhov's Gun: elementos introduzidos são resolvidos

### Tese e Argumentação (não-ficção)
- [ ] A tese central está claramente declarada
- [ ] Cada capítulo contribui para a tese
- [ ] Contra-argumentos são reconhecidos e respondidos
- [ ] A conclusão decorre logicamente das premissas
- [ ] Falácias lógicas identificadas e sinalizadas

---

## Relatório do CRÍTICO

```markdown
## Relatório de Validação — [Título] v[X]

### Score Geral: [X.X]/10

### ✅ Pontos Fortes
- ...

### ⚠️ Pontos de Atenção
- [Capítulo X, p.Y]: [descrição do problema] → [sugestão de correção]

### ❌ Problemas Críticos (exigem correção antes da publicação)
- ...

### 📊 Métricas
- Afirmações sem fonte: X
- Inconsistências detectadas: X
- Contradições internas: X
- Score de coerência narrativa: X/10
```
