# Configuração Externa — Fontes Normativas

> Carregar quando disciplina for compatível e não houver material do usuário.
> Usar `web_fetch` na URL correspondente.

---

## Direito Constitucional

| Tema | URL |
|------|-----|
| Constituição Federal (CF/88) | https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm |
| ADPF | https://www.planalto.gov.br/ccivil_03/leis/l9882.htm |
| Mandado de Injunção | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/lei/l13300.htm |
| ADC | https://www.planalto.gov.br/ccivil_03/leis/l9868.htm |
| Ação Direta de Inconstitucionalidade (ADI) | https://www.planalto.gov.br/ccivil_03/leis/l9868.htm |

---

## Direito Civil

| Tema | URL |
|------|-----|
| Código Civil (Lei 10.406/02) | https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm |
| LINDB | https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm |
| Estatuto da Pessoa com Deficiência | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm |
| Lei de Registros Públicos | https://www.planalto.gov.br/ccivil_03/leis/l6015compilado.htm |

---

## Processo Civil

| Tema | URL |
|------|-----|
| Código de Processo Civil (CPC/15) | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm |
| Mandado de Segurança | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12016.htm |

---

## Direito Tributário

| Tema | URL |
|------|-----|
| CTN | https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm |
| EC 132/2023 (IBS, CBS, IS) | https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm |
| Lei Kandir (ICMS) | https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp87.htm |
| Execução Fiscal | https://www.planalto.gov.br/ccivil_03/leis/l6830.htm |

---

## Direito Administrativo

| Tema | URL |
|------|-----|
| Processo Adm. Federal (Lei 9.784/99) | https://www.planalto.gov.br/ccivil_03/leis/l9784.htm |
| Improbidade Administrativa | https://www.planalto.gov.br/ccivil_03/leis/l8429.htm |
| LAI (Transparência) | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm |
| LRF | https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm |
| Licitações (Lei 14.133/21) | https://www.planalto.gov.br/ccivil_03/leis/l14133.htm |

---

## Direito Penal

| Tema | URL |
|------|-----|
| Código Penal | https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm |
| Organizações Criminosas | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12850.htm |
| Lavagem de Dinheiro | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12683.htm |
| Crimes Hediondos | https://www.planalto.gov.br/ccivil_03/leis/l8072compilado.htm |
| Abuso de Autoridade | https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13869.htm |

---

## Processo Penal

| Tema | URL |
|------|-----|
| Código de Processo Penal | https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689.htm |
| Tribunal do Júri | https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689compilado.htm |

---

## Contabilidade / Auditoria

| Tema | URL |
|------|-----|
| CPCs | https://www.cpc.org.br/CPC/Documentos-Emitidos/Pronunciamentos |
| NBCs TA (Auditoria) | https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/ |
| Lei das S.A. | https://www.planalto.gov.br/ccivil_03/leis/l6404consol.htm |
| NBC TSP 34 | https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/ |
| Lei 11.941/09 | https://www.planalto.gov.br/ccivil_03/leis/l11941.htm |
| CFC | https://cfc.org.br/ |

---

## Direito Financeiro

| Tema | URL |
|------|-----|
| Normas Gerais do Direito Financeiro | https://www.planalto.gov.br/ccivil_03/leis/l4320.htm |
| Manual da Contabilidade Aplicada ao Setor Público | https://cnm.org.br/storage/noticias/2024/Links/MCASP%20-%2011%C2%AA%20Edi%C3%A7%C3%A3o.pdf |
| Constituição Federal (CF/88) | https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm |


## Súmulas e Jurisprudência (arquivos locais)

> Carregar `read_file` no arquivo correspondente para consultar enunciados completos.

| Arquivo | Conteúdo | Linhas |
|---------|----------|--------|
| `VerbetesSTF.md` | Súmulas do STF (1–739) | ~739 |
| `VerbetesSTJ.md` | Súmulas do STJ (1–679) | ~679 |
| `SumulasVinculantes.md` | Súmulas Vinculantes do STF (1–115) | ~115 |

**Quando usar:**
- Questões sobre jurisprudência dominante → consultar `VerbetesSTF.md` e `VerbetesSTJ.md`
- Questões sobre constitucionalidade com efeito vinculante → consultar `SumulasVinculantes.md`
- Confidence 9–10 quando questão derivada diretamente de súmula citada

---

## Constantes

- Timeout para consultas: 15s
- Score mínimo para publicação: 7
- Formato padrão de saída: Ver interfaces em `SKILL.md`
