# 📚 Pipeline de Extração e Análise de Questões de Concursos

Com base no fluxo de tarefas analisado, criei scripts Python dedicados para automação completa do processo: **Pré-processamento**, **Extração** e **Análise de Temas com Granularidade Fina**.

Este pipeline utiliza `pdfplumber` para extração de PDFs e um motor de classificação por palavras-chave para análise temática.

---

## 🛠️ Scripts Disponíveis

### 📜 `pdf_to_md_cleaner.py`
**Função:** Converter PDFs brutos em Markdown limpo e normalizado.

#### 🔧 Como Funciona o Motor de Limpeza:
- **Detecção Inteligente de Cabeçalhos/Rodapés:** O script varre o PDF e identifica linhas que se repetem em mais de 40% das páginas (ex: "SEFAZ-AM", "Página 2", "Tipo 1 - Branca") e as remove automaticamente.
- **Filtro de "Instruções Gerais":** Ele ignora as primeiras páginas de instruções ("Não abra antes…", "Você dispõe de 4 horas…") buscando pelo primeiro marcador real de conteúdo (ex: "LÍNGUA PORTUGUESA", "QUESTÃO 1").
- **Remoção de Ruídos:** Aplica Regex para eliminar:
  - "Espaço livre", "Rascunho".
  - Links de sites das bancas.
  - Numerações de página soltas.
- **Proteção Anti-Cópia:** Tenta contornar proteções simples extraindo o texto bruto das camadas do PDF. Se o PDF for uma imagem escaneada (sem texto selecionável), o script avisará que não foi possível extrair.

---

### 📊 `analisador_temas_fiscal.py`
**Função:** Analisar provas de concurso e extrair temas com granularidade fina (tópicos específicos por disciplina).

#### 🔧 Funcionalidades do Script
✅ Classificação automática por disciplina e tópico específico  
✅ Banco de dados com +300 patterns de palavras-chave  
✅ 20 disciplinas mapeadas com +100 tópicos específicos  
✅ 3 formatos de saída: Markdown, CSV e JSON  
✅ Relatórios consolidados e por arquivo individual  
✅ TOP 20 temas mais cobrados automaticamente  
✅ Granularidade fina (ex: "ICMS - Fato Gerador", "Simples Nacional/MEI", "NBC TA 500 - Evidência de Auditoria")

#### 🎯 Como Usar
```bash
# Executar análise completa
python analisador_temas_fiscal.py
```

#### 📁 Arquivos Gerados
- **`analise_granularidade_fina_auto.md`** → Relatório completo em Markdown com tabelas detalhadas
- **`analise_granularidade_fina_auto.csv`** → Tabela para análise no Excel/Google Sheets
- **`analise_granularidade_fina_auto.json`** → Dados estruturados para análise programática

#### 📊 Resultados da Última Análise
- **Total de questões analisadas:** 1.151 questões
- **Total de provas processadas:** 11
- **Disciplinas identificadas:** 20

**TOP 5 Disciplinas:**
1. Direito Tributário: 203 ocorrências
2. Contabilidade Geral: 143 ocorrências
3. TI / Análise de Dados: 91 ocorrências
4. Direito Civil: 77 ocorrências
5. Auditoria: 69 ocorrências

---

### 🔍 `extrator_questoes.py`
**Função:** Extrair questões específicas por área de conhecimento.

---

## 🚀 Fluxo de Trabalho Completo (Pipeline)
Agora você tem uma esteira de automação completa na sua pasta:

### Passo 1: Converter e Limpar
```bash
pip install pdfplumber
python pdf_to_md_cleaner.py
```
> **Saída:** Gera arquivos como `auditor_fiscal_da_receita_estadual_limpo.md` prontos e limpos.

### Passo 2: Extrair e Categorizar
```bash
python extrator_questoes.py
```
> **Saída:** Lê os arquivos `_limpo.md` e popula os arquivos `questoes_direito_tributario.md`, `questoes_contabilidade.md`, etc.

### Passo 3: Analisar Temas com Granularidade Fina
```bash
python analisador_temas_fiscal.py
```
> **Saída:** Gera relatórios detalhados com TOP temas por disciplina e tópicos específicos (CSV, MD, JSON)

---

## 🧠 Lógica de Extração (Camada 2)

O sistema `extrator_questoes.py` opera com as seguintes regras determinísticas:

1. **Descoberta de Fontes:** O sistema varre o diretório `CONTABILIDADE` buscando todos os arquivos `.md` (provas digitalizadas).
2. **Mapeamento de Áreas:** Define-se um catálogo de áreas de conhecimento (ex: Direito Tributário, Constitucional, Administrativo, Civil, Penal, Empresarial, Financeiro, etc.).
3. **Extração Inteligente (Duas Camadas):**
   - **Camada 1 (Estrutural):** Busca por cabeçalhos de seção explícitos na prova (ex: `## DIREITO TRIBUTÁRIO`, `### Legislação do Amazonas`).
   - **Camada 2 (Semântica/Keywords):** Se não há cabeçalho ou para validar o conteúdo, o sistema analisa cada bloco de questão em busca de palavras-chave específicas da área (ex: "ICMS" para Tributário, "Improbidade" para Administrativo, "Falência" para Empresarial).
4. **Normalização e Limpeza:** Remove ruídos como "Espaço livre", numeração de página, rodapés e instruções gerais.
5. **Persistência:** Salva cada área em um arquivo dedicado (`questoes_{area}.md`) com metadados da prova de origem.

---

## 📈 Lógica de Análise de Temas (Camada 3)

O `analisador_temas_fiscal.py` opera com classificação automática por:

1. **Banco de Patterns:** +300 expressões regulares mapeadas para tópicos específicos
2. **20 Disciplinas:** Direito Tributário, Contabilidade (Geral/Avançada/Custos), Auditoria, Direito Constitucional, Administrativo, Civil, Penal, Empresarial, TI/Análise de Dados, Matemática Financeira, Estatística, Raciocínio Lógico, AFO, Economia, Gerenciamento de Projetos, etc.
3. **Granularidade Fina:** Exemplo: dentro de "Direito Tributário" identifica "ICMS - Fato Gerador", "Simples Nacional/MEI", "Lançamento Tributário", etc.
4. **Múltiplos Formatos:** Gera relatórios em Markdown (legível), CSV (Excel) e JSON (programático)
5. **TOP Temas:** Ranking automático dos 20 temas mais cobrados em todas as provas

---
*🤖 Automação desenvolvida para otimizar estudos, revisões e criação de bancos de questões por disciplina.*
