"""
============================================================
ANALISADOR DE TEMAS - PROVAS DE AUDITOR FISCAL
Granularidade Fina por Disciplina e Tópico Específico
============================================================

Este script analisa provas de concurso para Auditor Fiscal,
extraindo temas com granularidade fina (tópicos específicos
dentro de cada disciplina).

Uso: python analise_temas_fiscal.py
"""

import os
import re
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import json


# ============================================================
# CONFIGURAÇÃO
# ============================================================

PASTA_PROVAS = r"c:\Users\hig0\Downloads\PIPELINE DE DADOS\NORMALIZACAO"

ARQUIVOS_PROVAS = [
    "auditor_fiscal_da_receita_estadual_auditoria_e_fiscalizacao_tarde.md",
    "auditor_fiscal_da_receita_estadual.md",
    "auditor_fiscal_de_tributos_estaduais_manhacns001_tipo_1.md",
    "auditor_fiscal_de_tributos_estaduais_tarde.md",
    "auditor_fiscal_tributario_da_receita_municipal_gestao_tributaria_manha.md",
    "auditor_fiscal.md",
    "cespe-cebraspe-2025-sefaz-se-auditor-fiscal-tributario-geral-prova.md",
    "esaf-2005-set-rn-auditor-fiscal-do-tesouro-estadual-prova-1-prova.md",
    "prova_auditor_fiscal_conhec_espec.md",
    "prova_auditor_fiscal_conhec_gerais.md",
    "sefaz-es-auditor-fiscal-da-receita-estadual-p1-af01-tipo-1.md",
]

# ============================================================
# BANCO DE DADOS DE TÓPICOS - Mapeamento de palavras-chave
# para classificação automática por disciplina e tópico
# ============================================================

TOPICOS_POR_DISCIPLINA = {
    "Direito Tributário": {
        "ICMS - Fato Gerador e Incidência": [
            r"ICMS.*incide", r"incidência.*ICMS", r"ICMS.*fato gerador",
            r"fato gerador.*ICMS", r"operação.*ICMS", r"ICMS.*operação",
            r"ICMS.*interestadual", r"circulação.*mercadoria",
            r"prestação.*serviço.*transporte", r"ICMS.*combustível",
            r"ICMS.*energia elétrica", r"energia.*elétrica.*ICMS",
            r"ICMS.*importação", r"importação.*ICMS",
            r"ICMS.*exportação", r"não incidência.*ICMS",
            r"ICMS.*não incide", r"alíquota.*ICMS",
            r"ICMS.*alíquota", r"DIFAL", r"diferencial.*alíquota",
            r"EC.*87", r"consumidor.*final.*ICMS",
        ],
        "ICMS - Base de Cálculo": [
            r"base.*cálculo.*ICMS", r"ICMS.*base.*cálculo",
            r"integrar.*base.*cálculo", r"valor.*ICMS.*base",
            r"ICMS.*por dentro", r"pauta.*fiscal.*ICMS",
        ],
        "ICMS - Benefícios Fiscais / Convênio CONFAZ": [
            r"convênio.*CONFAZ", r"CONFAZ.*ICMS", r"isenção.*ICMS",
            r"ICMS.*isenção", r"benefício.*fiscal.*ICMS",
            r"redução.*base.*cálculo.*ICMS", r"incentivo.*fiscal.*ICMS",
            r"LC.*160", r"remissão.*ICMS",
            r"regularização.*benefício", r"antecipação.*tributária.*ICMS",
        ],
        "Simples Nacional / MEI": [
            r"Simples Nacional", r"Simples.*Nacional", r"MEI",
            r"Microempreendedor Individual", r"microempresa",
            r"empresa.*pequeno porte", r"EPP", r"extrapolação.*receita",
            r"receita.*bruta.*Simples", r"DAS.*Simples",
            r"LC.*123", r"regime.*especial.*unificado",
        ],
        "Lançamento Tributário": [
            r"lançamento.*tributário", r"lançamento.*ofício",
            r"decadência.*tributária", r"prazo.*decadencial",
            r"prescrição.*tributária", r"lançamento.*homologação",
            r"homologação.*lançamento", r"lançamento.*por.*declaração",
        ],
        "Obrigação e Crédito Tributário": [
            r"obrigação.*tributária", r"obrigação.*principal",
            r"obrigação.*acessória", r"crédito.*tributário",
            r"suspensão.*exigibilidade", r"extinção.*crédito",
            r"denúncia.*espontânea", r"moratória.*tributária",
            r"parcelamento.*tributário", r"transação.*tributária",
            r"medida.*liminar.*tributário", r"depósito.*prévio",
        ],
        "Responsabilidade Tributária": [
            r"responsabilidade.*tributária", r"responsável.*tributário",
            r"sucessão.*tributária", r"terceiro.*responsável",
            r"responsabilidade.*solidária.*tributo",
        ],
        "Repartição de Receitas": [
            r"repartição.*receita", r"participação.*arrecadação",
            r"receita.*pertence", r"produto.*arrecadação.*ICMS",
            r"produto.*arrecadação.*IPVA", r"produto.*arrecadação.*ITR",
            r"repartição.*IR", r"percentual.*município",
        ],
        "Taxas": [
            r"taxa.*poder.*polícia", r"poder.*polícia.*taxa",
            r"serviço.*público.*específico.*divisível",
            r"utilização.*efetiva.*potencial", r"taxa.*fato gerador",
        ],
        "Contribuições": [
            r"contribuição.*melhoria", r"contribuição.*social",
            r"contribuição.*intervenção.*domínio.*econômico",
            r"contribuição.*iluminação.*pública",
            r"CIDE.*combustíveis", r"contribuição.*previdenciária",
            r"custeio.*seguridade",
        ],
        "Impostos em Espécie (não ICMS)": [
            r"ITCMD.*incide", r"ITCMD.*fato gerador",
            r"ITCMD.*base.*cálculo", r"ITCMD.*doação",
            r"ITCMD.*causa.*mortis", r"ITCMD.*isenção",
            r"IPVA.*incide", r"IPVA.*alíquota", r"IPVA.*fato gerador",
            r"IPVA.*isenção", r"IPVA.*lançamento",
            r"IPTU.*incide", r"IPTU.*fato gerador",
            r"IPTU.*isenção", r"IRPF.*IRPJ",
            r"Imposto.*Renda.*IR", r"imposto.*extraordinário",
            r"imposto.*residual", r"ITBI.*incide",
            r"ITBI.*fato gerador", r"ITBI.*isenção",
            r"ITR.*incide",
        ],
        "Administração Tributária / Fiscalização": [
            r"administração.*tributária", r"fiscalização.*tributária",
            r"domicílio.*tributário", r"sigilo.*fiscal",
            r"certidão.*negativa", r"certidão.*quitação",
            r"dívida.*ativa", r"CDA", r"protesto.*CDA",
            r"arbitramento.*ICMS", r"auto.*infração",
            r"processo.*administrativo.*fiscal", r"impugnação.*fiscal",
            r"recurso.*fiscal", r"CERF", r"devedor.*contumaz",
            r"rep*etição.*indébito", r"restituição.*tributo",
            r"compensação.*tributária",
            r"capacidade.*tributária.*ativa",
            r"delegação.*arrecadação",
        ],
        "Limitações ao Poder de Tributar": [
            r"imunidade.*tributária", r"imunidade.*recíproca",
            r"imunidade.*templo", r"imunidade.*livro",
            r"irretroatividade.*tributária",
            r"anterioridade.*tributária",
            r"princípio.*irretroatividade",
            r"vedação.*tributo",
        ],
        "Legislação Tributária / CTN": [
            r"legislação.*tributária", r"CTN",
            r"integração.*legislação", r"analogia.*tributária",
            r"princípios.*direito.*tributário",
        ],
        "IBS / Reforma Tributária": [
            r"IBS", r"imposto.*bens.*serviços",
            r"EC.*132", r"reforma.*tributária",
            r"IVA.*dual",
        ],
        "Direito Tributário - Geral": [
            r"competência.*tributária", r"tributo.*conceito",
            r"classificação.*tributo", r"espécie.*tributária",
            r"natureza.*jurídica.*tributo",
            r"lei.*complementar.*tributária",
            r"reserva.*lei.*tributária",
            r"senado.*federal.*tributo",
            r"tributário",
        ],
    },

    "Contabilidade Geral": {
        "Balanço Patrimonial": [
            r"balanço.*patrimonial", r"ativo.*circulante",
            r"ativo.*não circulante", r"passivo.*circulante",
            r"passivo.*não circulante", r"patrimônio.*líquido",
            r"BP.*apresentação", r"estrutura.*balanço",
            r"saldos.*devedores.*credores",
            r"classificação.*contas", r"grupos.*subgrupos.*ativo",
            r"capital.*circulante.*líquido", r"CCL",
            r"impostos.*diferidos.*balanço",
            r"equação.*patrimonial", r"Ativo.*Passivo.*PL",
            r"fato.*contábil.*permutativo",
            r"fato.*contábil.*modificativo",
        ],
        "DRE e Apuração de Lucro": [
            r"DRE", r"demonstração.*resultado",
            r"apuração.*lucro", r"lucro.*líquido",
            r"lucro.*antes.*imposto", r"LAIR",
            r"receita.*líquida.*venda", r"custo.*mercadoria.*vendida",
            r"CMV", r"resultado.*bruto",
            r"despesa.*operacional", r"receita.*operacional",
            r"composição.*resultado", r"prejuízo.*fiscal",
            r"compensação.*prejuízo",
        ],
        "Estoques": [
            r"estoque", r"PEPS", r"primeiro.*entra.*primeiro.*sai",
            r"média.*ponderada", r"custo.*aquisição.*mercadoria",
            r"estoque.*final", r"estoque.*inicial",
            r"inventário.*periódico", r"inventário.*permanente",
            r"NBC.*TG.*16", r"CPC.*16", r"estoques",
            r"avaliação.*estoque",
        ],
        "Depreciação": [
            r"depreciação", r"vida.*útil", r"valor.*residual",
            r"método.*linear", r"método.*soma.*dígitos",
            r"depreciação.*acumulada", r"encargo.*depreciação",
            r"despesa.*depreciação",
        ],
        "Patrimônio Líquido e Destinação de Lucro": [
            r"reserva.*legal", r"reserva.*estatutária",
            r"reserva.*lucros", r"dividendo",
            r"participações.*lucro", r"DLPA",
            r"demonstração.*mutações.*patrimônio",
            r"DMPL", r"destinação.*lucro",
            r"lucro.*acumulado", r"reserva.*capital",
            r"ajustes.*avaliação.*patrimonial",
            r"partes.*beneficiárias", r"bônus.*subscrição",
            r"participações.*estatutárias",
        ],
        "Demonstração dos Fluxos de Caixa": [
            r"fluxo.*caixa", r"CPC.*03", r"DFC",
            r"atividade.*operacional", r"atividade.*investimento",
            r"atividade.*financiamento", r"método.*direto",
            r"método.*indireto.*fluxo.*caixa",
        ],
        "Ativo Imobilizado": [
            r"imobilizado", r"CPC.*27", r"NBC.*TG.*27",
            r"terreno.*valorização", r"propriedade.*investimento",
            r"alienação.*imobilizado", r"baixa.*imobilizado",
            r"CPC.*28", r"propriedade.*para.*investimento",
        ],
        "Ativo Intangível e Impairment": [
            r"intangível", r"CPC.*04", r"NBC.*TG.*04",
            r"goodwill", r"ágio", r"impairment",
            r"test.*recuperabilidade", r"CPC.*01", r"NBC.*TG.*01",
            r"perda.*valor", r"valor.*em.*uso",
            r"diferido", r"ativo.*diferido",
        ],
        "Escrituração e Balancete": [
            r"escrituração", r"balancete.*verificação",
            r"lançamento.*contábil", r"débito.*crédito",
            r"partidas.*dobradas", r"livro.*diário",
            r"elementos.*essenciais.*escrituração",
        ],
        "Equivalência Patrimonial": [
            r"equivalência.*patrimonial", r"controlada",
            r"coligada", r"investimento.*controlada",
            r"lucro.*controlada.*equivalência",
        ],
        "Índices Financeiros": [
            r"liquidez", r"ROA", r"giro.*ativo",
            r"endividamento", r"índice.*financeiro",
            r"indicador.*financeiro", r"análise.*vertical",
            r"análise.*horizontal", r"margem.*lucro",
            r"rentabilidade",
        ],
        "Valor Presente / Ajuste a Valor Presente": [
            r"valor.*presente", r"AVP", r"CPC.*12",
            r"ajuste.*valor.*presente", r"taxa.*desconto",
        ],
        "Provisões": [
            r"provisão.*contingência", r"provisão.*trabalhista",
            r"provisão.*fiscal", r"provisão.*cível",
            r"CPC.*25", r"NBC.*TG.*25",
            r"passivo.*contingente", r"probabilidade.*provável",
        ],
        "Ações em Tesouraria": [
            r"ações.*tesouraria", r"compra.*ações.*próprias",
            r"alienação.*ações.*próprias",
        ],
        "Combinação de Negócios / Goodwill": [
            r"combinação.*negócio", r"CPC.*15",
            r"goodwill.*aquisição", r"valor.*justo.*aquisição",
        ],
        "Consolidação": [
            r"consolidação", r"demonstração.*consolidada",
            r"consolidado", r"não.*controlador",
        ],
        "DVA": [
            r"DVA", r"demonstração.*valor.*adicionado",
            r"riqueza.*gerada", r"riqueza.*distribuída",
        ],
        "Ativos Biológicos": [
            r"ativo.*biológico", r"CPC.*29", r"NBC.*TG.*29",
            r"produto.*agrícola",
        ],
        "Debêntures / Instrumentos Financeiros": [
            r"debênture", r"instrumento.*financeiro",
            r"custo.*transação.*debênture",
            r"avaliação.*instrumento.*financeiro",
            r"valor.*justo.*financeiro",
        ],
        "ICMS na Contabilidade": [
            r"ICMS.*recuperável", r"ICMS.*lançamento.*contábil",
            r"crédito.*ICMS", r"débito.*ICMS.*contábil",
            r"estorno.*ICMS",
        ],
        "Contabilidade - Geral/Outros": [
            r"princípio.*contábil", r"princípio.*competência",
            r"princípio.*prudência", r"regime.*competência",
            r"regime.*caixa", r"não.*compensação",
            r"CPC.*00", r"estrutura.*conceitual",
            r"relatório.*financeiro.*fins.*gerais",
            r"representação.*fidedigna",
            r"contraprestação.*não monetária",
            r"CPC.*47", r"receita.*contrato.*cliente",
            r"CPC.*20", r"custo.*empréstimo",
            r"ativo.*qualificável",
            r"contábil",
        ],
    },

    "Contabilidade Avançada": {
        "Equivalência Patrimonial Avançada": [
            r"equivalência.*patrimonial.*lucro",
            r"equivalência.*patrimonial.*dividendo",
            r"equivalência.*patrimonial.*prejuízo",
            r"lucro.*controlada.*não realizado",
            r"venda.*controlada.*investidora",
            r"transação.*partes.*relacionadas.*lucro",
        ],
        "Combinação de Negócios e Goodwill": [
            r"goodwill.*combinação", r"combinação.*negócio.*valor.*justo",
            r"ágio.*expectativa.*rentabilidade",
            r"acionamento.*não.*controlador.*valor.*justo",
        ],
        "Mudança de Política Contábil e Estimativa": [
            r"mudança.*política.*contábil",
            r"mudança.*estimativa.*contábil",
            r"CPC.*23", r"NBC.*TG.*23",
            r"retificação.*erro", r"ajuste.*exercício.*anterior",
        ],
        "Arrendamento Mercantil": [
            r"arrendamento", r"CPC.*06", r"NBC.*TG.*06",
            r"leasing", r"arrendatário", r"arrendador",
            r"direito.*uso.*arrendamento",
            r"passivo.*arrendamento",
        ],
        "Instrumentos Financeiros / Valor Justo": [
            r"mensuração.*valor.*justo", r"CPC.*46", r"NBC.*TG.*46",
            r"mercado.*principal", r"mercado.*mais.*vantajoso",
            r"hierarquia.*valor.*justo",
            r"aplicações.*financeiras.*valor.*justo",
        ],
        "Variação Cambial / Moeda Funcional": [
            r"variação.*cambial", r"moeda.*funcional",
            r"CPC.*02", r"NBC.*TG.*02",
            r"subsidiária.*exterior", r"conversão.*demonstração",
            r"investida.*exterior",
        ],
        "Subvenção Governamental": [
            r"subvenção.*governamental", r"CPC.*07", r"NBC.*TG.*07",
            r"subvenção.*investimento", r"subvenção.*custeio",
        ],
        "Ajuste a Valor Presente Avançado": [
            r"ajuste.*valor.*presente.*taxa",
            r"AVP.*ativo.*longo.*prazo",
            r"AVP.*passivo.*longo.*prazo",
        ],
        "Reorganização Societária": [
            r"incorporação", r"fusão.*sociedade",
            r"cisão.*sociedade", r"transformação.*sociedade",
            r"reorganização.*societária",
        ],
        "Depleção / Recursos Naturais": [
            r"depleção", r"exaustão.*mina",
            r"recurso.*natural.*contabilidade",
        ],
        "Ativo Não Circulante Mantido para Venda": [
            r"mantido.*venda", r"CPC.*27.*não circulante.*venda",
            r"descontinuação.*operação",
        ],
        "Contabilidade Avançada - Outros": [
            r"contabilidade.*avançada",
        ],
    },

    "Contabilidade de Custos": {
        "Classificação de Custos": [
            r"custo.*fixo", r"custo.*variável",
            r"custo.*direto", r"custo.*indireto",
            r"custo.*primário", r"custo.*transformação",
            r"custo.*conversão",
            r"custo.*produção", r"classificação.*custo",
            r"custo.*fabricação",
        ],
        "Custeio por Absorção vs Variável": [
            r"custeio.*absorção", r"custeio.*variável",
            r"custeio.*pleno", r"custeio.*direto",
        ],
        "Ponto de Equilíbrio": [
            r"ponto.*equilíbrio", r"break-even",
            r"ponto.*equilíbrio.*contábil",
            r"ponto.*equilíbrio.*financeiro",
            r"ponto.*equilíbrio.*econômico",
        ],
        "Margem de Contribuição e Segurança": [
            r"margem.*contribuição", r"margem.*segurança",
            r"relação.*custo.*volume.*lucro",
        ],
        "Grau de Alavancagem Operacional": [
            r"alavancagem.*operacional", r"grau.*alavancagem",
            r"GAO", r"grau.*alavanca",
        ],
        "Rateio de Custos Indiretos": [
            r"rateio.*custo.*indireto", r"rateio.*CIF",
            r"base.*rateio", r"horas.*máquina",
            r"mão.*obra.*direta.*rateio",
            r"departamentalização.*custo",
        ],
        "Custeio por Produção Contínua vs Ordem": [
            r"produção.*contínua", r"produção.*ordem",
            r"produção.*batelada", r"custeio.*ordem.*produção",
        ],
        "Taxa de Aplicação de Custos Indiretos": [
            r"taxa.*aplicação.*custo.*indireto",
            r"CIP.*custo.*indireto.*produção",
            r"variação.*CIP", r"custo.*indireto.*taxa",
        ],
        "Custo Padrão vs Estimado": [
            r"custo.*padrão", r"custo.*corrente",
            r"custo.*estimado", r"custo.*meta",
            r"variação.*custo.*padrão",
        ],
        "Custos Controláveis vs Não Controláveis": [
            r"custo.*controlável", r"custo.*não controlável",
            r"custo.*responsabilidade", r"custeio.*responsabilidade",
        ],
        "Coprodutos e Subprodutos": [
            r"coproduto", r"subproduto",
            r"custo.*conjunto", r"ponto.*separação",
        ],
        "ABC - Activity Based Costing": [
            r"ABC", r"custeio.*baseado.*atividade",
            r"Activity Based", r"direcionador.*custo",
            r"driver.*custo",
        ],
        "Decisão Gerencial de Custos": [
            r"decisão.*eliminar.*produto",
            r"manter.*produto.*margem",
            r"custo.*oportunidade.*decisão",
            r"decisão.*gerencial.*custo",
        ],
        "Custos - Classificação de Gastos": [
            r"custo.*despesa.*perda.*investimento",
            r"classificação.*gasto", r"gasto.*classificação",
        ],
    },

    "Auditoria": {
        "NBC TA 500 - Evidência de Auditoria": [
            r"evidência.*auditoria", r"NBC.*TA.*500",
            r"evidência.*apropriada.*suficiente",
            r"evidência.*suficiente.*apropriada",
            r"procedimento.*auditoria",
            r"indagação.*auditoria",
            r"investigação.*auditoria",
            r"confirmação.*externa",
        ],
        "NBC TA 530 - Amostragem": [
            r"amostragem.*auditoria", r"NBC.*TA.*530",
            r"risco.*amostragem", r"tamanho.*amostra",
            r"taxa.*tolerável.*desvio",
            r"taxa.*esperada.*desvio",
            r"unidade.*amostragem",
        ],
        "NBC TA 705 - Modificações no Relatório": [
            r"modificação.*opinião", r"NBC.*TA.*705",
            r"opinião.*com.*ressalva", r"opinião.*adversa",
            r"abstenção.*opinião", r"opinião.*sem.*ressalva",
            r"limitação.*alcance.*auditoria",
            r"distorção.*relevante.*generalizada",
            r"impossibilidade.*evidência",
        ],
        "Testes de Observância e Substantivos": [
            r"teste.*observância", r"teste.*substantivo",
            r"teste.*controle", r"teste.*detalhe",
            r"teste.*conformidade",
        ],
        "Risco de Auditoria": [
            r"risco.*auditoria", r"risco.*inerente",
            r"risco.*controle", r"risco.*detecção",
            r"risco.*fraude", r"risco.*erro",
            r"aceitação.*incorreta", r"rejeição.*incorreta",
        ],
        "Procedimentos Analíticos": [
            r"procedimento.*analítico", r"NBC.*TA.*520",
            r"revisão.*analítica", r"análise.*tendência",
            r"razão.*análise", r"teste.*razão",
            r"flutuação.*significativa",
        ],
        "Planejamento de Auditoria": [
            r"planejamento.*auditoria", r"NBC.*TA.*300",
            r"plano.*auditoria", r"estratégia.*auditoria",
            r"materialidade", r"importância.*relativa",
        ],
        "Fraude e Erro": [
            r"fraude.*auditoria", r"erro.*auditoria",
            r"responsabilidade.*fraude",
            r"indicador.*fraude",
        ],
        "Comunicação e Representação": [
            r"comunicação.*governança", r"comunicação.*administração",
            r"carta.*representação", r"representação.*formal",
            r"NBC.*TA.*580",
        ],
        "Eventos Subsequentes": [
            r"evento.*subsequente", r"NBC.*TA.*560",
            r"fato.*posterior.*auditoria",
        ],
        "Auditoria do Ativo": [
            r"auditoria.*cliente", r"auditoria.*estoque",
            r"auditoria.*imobilizado", r"circularização",
            r"contagem.*física.*estoque",
        ],
        "Auditoria do Passivo e PL": [
            r"auditoria.*passivo", r"auditoria.*patrimônio.*líquido",
            r"auditoria.*provisão",
        ],
        "Relatório / Parecer de Auditoria": [
            r"relatório.*auditor.*independente",
            r"parecer.*auditoria",
            r"parágrafo.*ênfase", r"outros.*assuntos.*auditoria",
            r"DVA.*relatório.*auditor",
        ],
        "Controles Internos": [
            r"controle.*interno", r"efetividade.*controle",
            r"avaliação.*controle.*interno",
        ],
        "Auditoria Interna": [
            r"auditoria.*interna", r"NBC.*TI.*01",
        ],
        "Saldos Iniciais": [
            r"saldos.*iniciais", r"saldos.*abertura.*auditoria",
        ],
        "Auditoria de Grupo/Consolidado": [
            r"auditoria.*grupo", r"auditoria.*consolidado",
            r"consolidação.*distorção",
            r"não.*consolidação.*controlada",
        ],
        "Contabilidade Criativa / Fraude": [
            r"contabilidade.*criativa", r"fraude.*contábil",
        ],
        "Sigilo Bancário / LC 105": [
            r"sigilo.*bancário", r"LC.*105",
            r"operação.*financeira.*sigilo",
        ],
        "Estatísticas de Finanças Públicas": [
            r"estatística.*finança.*pública",
            r"EFP.*demonstração.*contábil",
        ],
        "Auditoria - Outros": [
            r"auditoria",
        ],
    },

    "Direito Constitucional": {
        "Normas Constitucionais (Eficácia)": [
            r"norma.*constitucional.*eficácia",
            r"eficácia.*plena", r"eficácia.*contida",
            r"eficácia.*limitada", r"norma.*programática",
            r"força.*normativa.*constituição",
        ],
        "Direitos e Garantias Fundamentais": [
            r"direito.*fundamental", r"garantia.*fundamental",
            r"direito.*individual", r"artigo.*5º",
            r"art.*5.*CRFB", r"cláusula.*abertura.*direito",
            r"dimensão.*direito.*fundamental",
        ],
        "Organização Político-Administrativa": [
            r"organização.*político.*administrativa",
            r"federação.*brasileira", r"estado.*membro",
            r"autonomia.*estadual", r"auto.*organização",
            r"competência.*estado", r"competência.*município",
            r"federalismo.*cooperativo",
            r"formação.*novo.*estado", r"desmembramento",
        ],
        "Organização dos Poderes": [
            r"Poder.*Legislativo", r"Poder.*Executivo",
            r"Poder.*Judiciário", r"organização.*poderes",
            r"CPI", r"comissão.*parlamentar.*inquérito",
            r"TCU.*competência", r"Tribunal.*Contas",
            r"autonomia.*financeira.*Judiciário",
            r"impeachment", r"juízo.*admissibilidade",
            r"extinção.*órgão.*decreto",
        ],
        "Remédios Constitucionais": [
            r"mandado.*segurança", r"habeas.*data",
            r"mandado.*injunção", r"ação.*popular",
            r"habeas.*corpus", r"remédio.*constitucional",
        ],
        "Processo Legislativo": [
            r"processo.*legislativo", r"iniciativa.*lei",
            r"veto.*presidencial", r"promulgação.*lei",
            r"lei.*complementar.*iniciativa",
        ],
        "Competência Legislativa": [
            r"competência.*legislativa",
            r"competência.*privativa.*União",
            r"competência.*concorrente",
            r"competência.*comum",
        ],
        "Foro por Prerrogativa de Função": [
            r"foro.*prerrogativa.*função", r"foro.*privilegiado",
            r"competência.*originária.*tribunal",
        ],
        "Elegibilidade e Condições": [
            r"elegibilidade", r"condição.*elegibilidade",
            r"filiação.*partidária", r"inelegibilidade",
            r"estrangeiro.*elegível",
            r"equivalência.*português",
        ],
        "Partidos Políticos": [
            r"partido.*político", r"personalidade.*jurídica.*partido",
            r"fundo.*partidário", r"fundo.*eleitoral",
        ],
        "Teto Remuneratório": [
            r"teto.*remuneratório", r"acumulação.*provento",
            r"pensão.*morte.*remuneração", r"subsídio",
        ],
        "Regime Previdenciário": [
            r"regime.*próprio.*previdência", r"RPPS",
            r"regime.*geral.*previdência", r"RGPS",
            r"cargo.*comissão.*previdência",
            r"trabalho.*temporário.*previdência",
        ],
        "Controle de Constitucionalidade": [
            r"controle.*constitucionalidade",
            r"ADI", r"ADC", r"ADPF",
            r"declaração.*inconstitucionalidade",
        ],
        "Direito Constitucional - Outros": [
            r"constitucional",
        ],
    },

    "Direito Administrativo": {
        "Responsabilidade Civil do Estado": [
            r"responsabilidade.*civil.*Estado",
            r"responsabilidade.*objetiva.*Estado",
            r"responsabilidade.*subjetiva.*Estado",
            r"risco.*administrativo",
            r"ação.*regressiva.*Estado",
            r"dano.*causado.*servidor",
            r"excludente.*responsabilidade",
            r"culpa.*vítima.*Estado",
            r"má.*conservação.*rodovia",
        ],
        "Licitações": [
            r"licitação", r"dispensa.*licitação",
            r"inexigibilidade.*licitação", r"pregão",
            r"RDC", r"regime.*diferenciado.*contratação",
            r"Lei.*14\.133", r"Lei.*8\.666",
            r"fornecedor.*exclusivo.*licitação",
            r"indicação.*marca.*licitação",
            r"registro.*preço",
        ],
        "Contratos Administrativos": [
            r"contrato.*administrativo",
            r"supressão.*contrato", r"rescisão.*contrato",
            r"responsabilidade.*subsidiária.*encargo.*trabalhista",
            r"responsabilidade.*contratual.*Estado",
            r"alteração.*contratual",
        ],
        "Improbidade Administrativa": [
            r"improbidade.*administrativa",
            r"Lei.*8\.429", r"Lei.*14\.230",
            r"ato.*improbidade", r"sanção.*improbidade",
        ],
        "Administração Direta e Indireta": [
            r"autarquia", r"empresa.*pública",
            r"sociedade.*economia.*mista", r"fundação.*pública",
            r"administração.*direta", r"administração.*indireta",
            r"entidade.*paraestatal",
            r"delegação.*poder.*polícia",
        ],
        "Poder de Polícia": [
            r"poder.*polícia", r"polícia.*administrativa",
            r"exercício.*regular.*poder.*polícia",
        ],
        "Processo Administrativo Disciplinar": [
            r"processo.*administrativo.*disciplinar",
            r"agente.*fato", r"agente.*putativo",
            r"ato.*administrativo.*vício",
        ],
        "Intervenção na Propriedade": [
            r"desapropriação", r"servidão.*administrativa",
            r"requisição.*administrativa",
            r"ocupação.*temporária",
            r"tombamento.*bem",
        ],
        "Delegação e Competência": [
            r"delegação.*competência", r"avocação.*competência",
            r"competência.*administrativa",
        ],
        "Bens Públicos": [
            r"bem.*público", r"bem.*dominical",
            r"bem.*uso.*comum", r"bem.*uso.*especial",
            r"alienação.*bem.*público",
        ],
        "LAIA / Transparência": [
            r"Lei.*Acesso.*Informação", r"LAI",
            r"transparência.*administração",
        ],
        "Servidor Público": [
            r"servidor.*público", r"reversão.*servidor",
            r"regime.*jurídico.*servidor",
            r"cargo.*efetivo", r"cargo.*comissão",
            r"estabilidade.*servidor",
        ],
        "LRF e Sanções": [
            r"LRF", r"Lei.*Responsabilidade.*Fiscal",
            r"sanção.*LRF", r"excesso.*gasto.*pessoal",
        ],
        "Direito Administrativo - Outros": [
            r"administrativo",
        ],
    },

    "Direito Civil": {
        "Obrigações": [
            r"obrigação", r"pagamento.*obrigação",
            r"inadimplemento", r"inexecução.*obrigação",
            r"obrigação.*indivisível",
            r"obrigação.*solidária",
            r"caso.*fortuito.*força.*maior",
        ],
        "Responsabilidade Civil": [
            r"responsabilidade.*civil",
            r"ato.*ilícito", r"indenização",
            r"responsabilidade.*empregador",
            r"responsabilidade.*objetiva.*civil",
            r"dever.*indenizar",
        ],
        "Sucessão": [
            r"sucessão", r"herança", r"partilha",
            r"herdeiro", r"legado", r"legatário",
            r"sucessão.*legítima", r"ordem.*vocação.*hereditária",
            r"inventário", r"monte",
        ],
        "Negócio Jurídico": [
            r"negócio.*jurídico", r"capacidade.*civil",
            r"nulidade.*negócio", r"anulabilidade",
            r"vício.*consentimento", r"vício.*social",
        ],
        "Prescrição e Decadência": [
            r"prescrição", r"decadência",
            r"prazo.*prescricional", r"prazo.*decadencial",
            r"renúncia.*prescrição",
        ],
        "Desconsideração da Personalidade Jurídica": [
            r"desconsideração.*personalidade.*jurídica",
            r"Art.*50.*CC", r"desvio.*finalidade",
            r"confusão.*patrimonial",
        ],
        "Propriedade e Posse": [
            r"propriedade", r"posse",
            r"transferência.*propriedade",
            r"fruto.*coisa", r"vizinhança",
            r"usucapião", r"servidão.*passagem",
            r"propriedade.*fidelidade",
        ],
        "Contratos em Espécie": [
            r"mútuo", r"depósito", r"compra.*venda",
            r"evicção", r"vício.*redibitório",
            r"mandato", r"pagamento.*terceiro",
            r"credor.*putativo",
        ],
        "LINDB": [
            r"LINDB", r"vigência.*lei", r"vacatio.*legis",
            r"interpretação.*lei.*LINDB",
        ],
        "Regime de Bens": [
            r"regime.*bem", r"comunhão.*parcial",
            r"comunhão.*universal", r"separação.*bem",
            r"pacto.*antenupcial",
        ],
        "CDC": [
            r"CDC", r"consumidor", r"consumidor.*equiparação",
            r"defesa.*consumidor",
        ],
        "Direito Civil - Outros": [
            r"civil",
        ],
    },

    "Direito Empresarial": {
        "Sociedades Empresárias": [
            r"sociedade.*empresária", r"sociedade.*limitada",
            r"sociedade.*simples", r"sociedade.*anônima",
            r"constituição.*sociedade",
            r"registro.*junta.*comercial",
            r"responsabilidade.*sócio",
            r"sociedade.*não.*registrada",
        ],
        "Sociedade Limitada": [
            r"sociedade.*limitada.*dissolução",
            r"cláusula.*dissolução.*limitada",
            r"sociedade.*limitada.*regência",
            r"quórum.*limitada",
        ],
        "Falência e Recuperação Judicial": [
            r"falência", r"recuperação.*judicial",
            r"Lei.*Falência", r"Lei.*11\.101",
            r"crédito.*extraconcursal",
            r"empresário.*falido",
        ],
        "Estabelecimento Empresarial": [
            r"estabelecimento.*empresarial",
            r"alienação.*estabelecimento",
            r"ponto.*comercial", r"fundo.*comércio",
            r"responsabilidade.*adquirente.*estabelecimento",
        ],
        "Reorganização Societária": [
            r"fusão", r"cisão", r"incorporação.*sociedade",
            r"transformação.*sociedade",
        ],
        "Títulos de Crédito": [
            r"duplicata", r"nota.*promissória",
            r"cheque", r"prescrição.*título",
            r"regresso.*coobrigado",
            r"desconto.*comercial",
        ],
        "Acionista e S/A": [
            r"acionista.*controlador", r"companhia.*aberta",
            r"consórcio.*sociedade", r"Conselho.*Administração",
        ],
        "EIRELI / EI": [
            r"EIRELI", r"empresário.*individual",
            r"empresário.*individual.*unipessoal",
        ],
        "Direito Empresarial - Outros": [
            r"empresarial",
        ],
    },

    "Direito Penal": {
        "Crimes contra Ordem Tributária": [
            r"crime.*ordem.*tributária", r"sonegação.*fiscal",
            r"declaração.*falsa.*tributo",
            r"omissão.*informação.*tributo",
            r"Lei.*8\.137", r"Lei.*4\.729",
        ],
        "Crimes Funcionais contra Ordem Tributária": [
            r"crime.*funcional.*tributário",
            r"corrupção.*passiva.*fiscal",
            r"extravio.*mercadoria.*tributada",
            r"advocacia.*administrativa.*fiscal",
        ],
        "Crimes contra Finanças Públicas": [
            r"crime.*finança.*pública",
            r"operação.*crédito.*ilegal",
            r"resto.*pagar", r"despesa.*não.*empenhada",
            r"assunção.*obrigação.*último.*ano.*mandato",
            r"garantia.*graciosa",
            r"aumento.*despesa.*pessoal",
            r"LC.*101.*crime",
        ],
        "Princípio da Insignificância": [
            r"insignificância", r"bagatela",
            r"princípio.*bagatela",
            r"patamar.*mínimo.*sonegação",
        ],
        "Lei Penal no Tempo": [
            r"lei.*penal.*tempo", r"retroatividade.*lei.*penal",
            r"lei.*penal.*mais.*grave",
            r"ultratividade.*lei.*penal",
        ],
        "Crime-Meio vs Crime-Fim": [
            r"crime.*meio", r"crime.*fim",
            r"falsificação.*documento.*estelionato",
            r"princípio.*consunção",
        ],
        "Crimes Funcionais": [
            r"concussão", r"peculato",
            r"corrupção.*passiva", r"corrupção.*ativa",
            r"condescendência.*criminosa",
            r"prevaricação",
        ],
        "Descaminho e Contrabando": [
            r"descaminho", r"contrabando",
        ],
        "Falsidade Ideológica": [
            r"falsidade.*ideológica",
            r"crime.*fé.*pública", r"selo.*falsificado",
        ],
        "Inserção de Dados Falsos": [
            r"inserção.*dados.*falsos.*sistema",
            r"art.*313.*A.*CP",
        ],
        "Sonegação Previdenciária": [
            r"sonegação.*contribuição.*previdenciária",
            r"art.*168.*A.*CP",
            r"omitir.*receita.*previdência",
        ],
        "Denúncia e Lançamento Definitivo": [
            r"lançamento.*definitivo.*denúncia",
            r"condição.*procedibilidade.*tributário",
        ],
        "Crimes contra Relações de Consumo": [
            r"crime.*relação.*consumo", r"venda.*especificação",
            r"mistura.*gênero",
        ],
        "Elemento Subjetivo": [
            r"elemento.*subjetivo.*crime.*tributário",
            r"dolo.*crime.*tributário",
            r"dolo.*eventual.*tributário",
        ],
        "Direito Penal - Outros": [
            r"penal",
        ],
    },

    "Língua Portuguesa": {
        "Interpretação de Texto": [
            r"interpretação.*texto", r"ideia.*central",
            r"compreensão.*texto", r"paráfrase",
            r"inferência.*texto",
            r"significação.*texto",
        ],
        "Estrutura Argumentativa": [
            r"tese", r"argumento", r"contra.*argumentação",
            r"estrutura.*argumentativa",
            r"opinião.*enunciador",
        ],
        "Gramática (Concordância, Regência, Pontuação)": [
            r"concordância.*verbal", r"concordância.*nominal",
            r"regência.*verbal", r"regência.*nominal",
            r"pontuação", r"vírgula",
        ],
        "Linguagem Figurada / Metáfora": [
            r"metáfora", r"linguagem.*figurada",
            r"sentido.*figurado", r"figura.*linguagem",
        ],
        "Discurso Direto e Indireto": [
            r"discurso.*direto", r"discurso.*indireto",
            r"discurso.*indireto.*livre",
        ],
        "Coesão e Coerência": [
            r"coesão.*textual", r"coerência.*textual",
            r"conectivo", r"referência.*anafora",
            r"referência.*catafora", r"pronom.*relativo",
        ],
        "Fraseologia / Expressões Idiomáticas": [
            r"fraseologia", r"expressão.*idiomática",
            r"frase.*feita",
        ],
        "Reescrita de Frases": [
            r"reescrita", r"reescritura",
            r"proposta.*reescrita",
        ],
        "Classes Gramaticais / Morfologia": [
            r"classe.*gramatical", r"morfologia",
            r"particípio", r"gerúndio",
        ],
    },

    "Matemática Financeira": {
        "Taxas de Juros (Nominal, Real, Fisher)": [
            r"taxa.*nominal", r"taxa.*real.*juros",
            r"taxa.*aparente", r"equação.*Fisher",
            r"inflação.*taxa.*juros",
        ],
        "Sistema de Amortização (SAC, Price)": [
            r"SAC", r"Sistema.*Amortização.*Constante",
            r"Price", r"Sistema.*Francês",
            r"amortização.*constante",
            r"parcela.*amortização", r"saldo.*devedor",
            r"SACRE", r"subperíodo.*amortização",
        ],
        "Desconto (Comercial, Racional, Simples, Composto)": [
            r"desconto.*comercial", r"desconto.*racional",
            r"desconto.*simples", r"desconto.*composto",
            r"desconto.*bancário", r"valor.*nominal.*desconto",
            r"desconto.*razional.*composto",
        ],
        "Juros Simples e Compostos": [
            r"juro.*simples", r"juro.*composto",
            r"montante.*juros", r"capital.*aplicado",
            r"taxa.*juros.*mês",
        ],
        "Valor Presente e Futuro": [
            r"valor.*presente", r"valor.*atual",
            r"valor.*futuro", r"fator.*acumulação.*capital",
            r"fator.*valor.*atual",
        ],
        "VPL / TIR": [
            r"VPL", r"valor.*presente.*líquido",
            r"TIR", r"taxa.*interna.*retorno",
            r"taxa.*mínima.*atratividade", r"TMA",
        ],
        "Equivalência de Capitais": [
            r"equivalência.*capital",
            r"substituição.*parcela",
            r"pagamento.*equivalente",
        ],
        "Matemática Financeira - Outros": [
            r"matemática.*financeira",
        ],
    },

    "Estatística": {
        "Distribuição Normal / Z": [
            r"distribuição.*normal", r"normal.*padrão",
            r"padronização.*Z", r"tabela.*Z",
            r"curva.*normal",
        ],
        "Teste de Hipóteses": [
            r"teste.*hipótese", r"hipótese.*nula",
            r"hipótese.*alternativa", r"nível.*significância",
            r"teste.*Z", r"teste.*t.*Student",
            r"teste.*qui.*quadrado", r"teste.*F.*Snedecor",
            r"regra.*decisão.*teste",
        ],
        "Estatística Descritiva (Média, Mediana, Moda, Variância)": [
            r"média.*amostral", r"mediana", r"moda",
            r"variância.*amostral", r"desvio.*padrão",
            r"medida.*tendência.*central",
            r"medida.*dispersão",
            r"outlier", r"descarte.*atípico",
        ],
        "Intervalo de Confiança": [
            r"intervalo.*confiança", r"IC.*proporção",
            r"IC.*média", r"confiança.*95%",
            r"confiança.*99%",
        ],
        "Distribuição Binomial": [
            r"distribuição.*binomial", r"Bernoulli",
            r"probabilidade.*sucesso.*binomial",
            r"probabilidade.*exatamente.*sucesso",
        ],
        "Distribuição de Poisson": [
            r"distribuição.*Poisson", r"taxa.*Poisson",
            r"probabilidade.*Poisson",
        ],
        "Dimensionamento de Amostra": [
            r"tamanho.*amostra", r"dimensionamento.*amostra",
            r"erro.*amostral", r"margem.*erro",
            r"confiança.*amostra",
        ],
        "Distribuição de Frequências": [
            r"distribuição.*frequência", r"tabela.*frequência",
            r"ponto.*médio.*classe",
            r"classe.*frequência",
        ],
        "Regressão e Correlação": [
            r"regressão.*linear", r"mínimos.*quadrados",
            r"correlação.*Pearson", r"coeficiente.*correlação",
            r"covariância",
        ],
        "Teste de Independência / Tabela de Contingência": [
            r"teste.*independência",
            r"tabela.*contingência",
            r"qui.*quadrado.*independência",
            r"grau.*liberdade.*contingência",
        ],
        "Estatística - Outros": [
            r"probabilidade.*conjunta",
            r"variável.*aleatória",
        ],
    },

    "Tecnologia da Informação / Análise de Dados": {
        "Banco de Dados Relacional": [
            r"banco.*dados.*relacional", r"SGBD",
            r"chave.*primária", r"chave.*estrangeira",
            r"foreign.*key", r"primary.*key",
            r"tabela.*banco.*dados", r"tupla.*atributo",
            r"integridade.*referencial",
            r"view.*banco.*dados",
            r"índice.*clusterizado", r"índice.*não.*clusterizado",
            r"índice.*composto", r"índice.*bitmap",
            r"árvore.*B", r"B.*tree",
            r"metadados.*banco.*dados",
        ],
        "SQL": [
            r"SQL", r"CREATE TABLE", r"SELECT.*FROM",
            r"LEFT JOIN", r"RIGHT JOIN", r"INNER JOIN",
            r"INSERT.*INTO", r"UPDATE.*SET",
            r"DELETE.*FROM", r"WHERE.*AND.*OR",
            r"BETWEEN.*SQL", r"NOT.*SQL",
            r"DDL.*SQL", r"DML.*SQL",
        ],
        "Power BI": [
            r"Power BI", r"Power BI.*Service",
            r"Power BI.*Desktop", r"Power BI.*Report Builder",
            r"mapa.*coroplético", r"relatório.*paginado",
        ],
        "Data Warehouse / OLAP": [
            r"data.*warehouse", r"OLAP",
            r"drill.*down", r"roll.*up",
            r"slice.*dice", r"drill.*across",
            r"processamento.*OLAP",
            r"consulta.*analítica",
            r"modelo.*dimensional",
            r"tabela.*fato", r"tabela.*dimensão",
        ],
        "CRISP-DM": [
            r"CRISP.*DM", r"ciclo.*vida.*ciência.*dados",
            r"entendimento.*negócio",
            r"preparação.*dados.*CRISP",
        ],
        "Machine Learning": [
            r"aprendizado.*máquina", r"machine.*learning",
            r"aprendizado.*supervisionado",
            r"aprendizado.*não.*supervisionado",
            r"aprendizado.*reforço",
            r"K.*Means", r"k.*means",
            r"centroide.*cluster", r"agrupamento.*dados",
            r"clusterização",
        ],
        "Mineração de Dados": [
            r"mineração.*dados", r"data.*mining",
            r"árvore.*decisão", r"decision.*tree",
            r"Apriori", r"regra.*associação",
            r"suporte.*regra", r"confiança.*regra",
            r"discretização", r"histograma.*discretização",
            r"entropia.*discretização", r"enfaixamento",
            r"binning",
            r"sobreajuste", r"overfitting",
            r"falso.*negativo", r"falso.*positivo",
            r"detecção.*anomalia",
        ],
        "Dados Abertos": [
            r"dado.*aberto", r"open.*data",
            r"reuso.*redistribuição.*dado",
            r"participação.*universal.*dado",
        ],
        "Big Data": [
            r"big.*data", r"5.*Vs",
            r"volume.*variedade.*velocidade",
            r"veracidade.*valor",
        ],
        "Integração de Dados / ETL": [
            r"integração.*dados", r"ETL",
            r"extract.*transform.*load", r"ELT",
            r"governança.*dados",
            r"dicionário.*dados",
            r"modelo.*unificado.*dados",
            r"conflito.*semântico",
        ],
        "Segurança da Informação / Criptografia": [
            r"criptografia", r"criptografia.*simétrica",
            r"criptografia.*assimétrica",
            r"chave.*pública.*privada",
            r"certificado.*digital", r"ICP.*Brasil",
            r"certificado.*A1", r"certificado.*A3",
            r"autenticidade.*integridade.*não.*repúdio",
            r"confidencialidade.*segurança",
            r"X\.509",
        ],
        "EFD ICMS/IPI / NF-e / SPED": [
            r"EFD", r"escrituração.*fiscal.*digital",
            r"NF.*e", r"nota.*fiscal.*eletrônica",
            r"XML.*NF.*e", r"DANFE",
            r"protocolo.*ICMS",
            r"bloco.*EFD", r"registro.*EFD",
            r"sped.*fiscal", r"layout.*EFD",
            r"tag.*det", r"cEAN",
            r"validação.*NF.*e",
            r"credenciamento.*NF.*e",
        ],
        "LGPD": [
            r"LGPD", r"Lei.*Geral.*Proteção.*Dados",
            r"dado.*pessoal.*sensível",
            r"proteção.*dados.*pessoais",
        ],
        "Balanced Scorecard": [
            r"Balanced.*Scorecard", r"BSC",
            r"perspectiva.*financeira.*cliente",
            r"processo.*interno.*aprendizado.*crescimento",
        ],
        "Malware / Segurança": [
            r"malware", r"worm", r"vírus.*computador",
            r"propagação.*malware",
        ],
        "Hardware": [
            r"DDR4", r"memória.*RAM", r"hardware",
        ],
        "TI - Outros": [
            r"tecnologia.*informação", r"informática",
        ],
    },

    "Raciocínio Lógico": {
        "Lógica Proposicional": [
            r"lógica.*proposicional", r"proposição.*composta",
            r"equivalência.*lógica", r"silogismo",
            r"diagrama.*lógico", r"condicional.*equivalência",
            r"bicondicional", r"disjunção.*exclusiva",
        ],
        "Negação de Proposições": [
            r"negação.*proposição", r"De.*Morgan",
            r"negação.*condicional", r"negação.*conjunção",
            r"negação.*disjunção",
        ],
        "Validade de Argumentos": [
            r"validade.*argumento", r"argumento.*válido",
            r"premissa.*conclusão",
        ],
        "Combinatória e Contagem": [
            r"combinatória", r"arranjo", r"combinação",
            r"permutação", r"princípio.*fundamental.*contagem",
            r"fila.*ordem.*crescente",
        ],
        "Teoria dos Números": [
            r"congruência.*modular", r"divisibilidade",
            r"MMC", r"MDC", r"resto.*divisão",
            r"número.*primo",
        ],
        "Sequências e Progressões": [
            r"sequência.*numérica", r"progressão.*aritmética",
            r"progressão.*geométrica", r"sequência.*recursiva",
        ],
        "Problemas de Tempo e Horas": [
            r"problema.*hora", r"cálculo.*horário",
            r"atraso.*chegada", r"tempo.*espera",
        ],
        "Desigualdades e Intervalos": [
            r"desigualdade", r"intervalo.*valor",
            r"inequação",
        ],
        "Operações Definidas por Fórmula": [
            r"operação.*definida", r"símbolo.*definição",
        ],
        "Raciocínio Lógico - Outros": [
            r"raciocínio.*lógico",
        ],
    },

    "Administração Financeira e Orçamentária": {
        "Orçamento Público": [
            r"orçamento.*público", r"LOA", r"PPA",
            r"LDO", r"princípio.*orçamentário",
            r"universalidade.*orçamento",
            r"orçamento.*programa",
            r"ciclo.*orçamentário",
            r"função.*estabilizadora.*orçamento",
            r"função.*distributiva.*orçamento",
        ],
        "Execução Orçamentária": [
            r"execução.*orçamentária", r"execução.*financeira",
            r"SIAFI", r"descentralização.*orçamentária",
            r"provisão.*destaque", r"TED.*transferência",
            r"empenho.*liquidação.*pagamento",
        ],
        "Receita Pública": [
            r"receita.*pública", r"receita.*corrente",
            r"receita.*capital", r"lançamento.*receita",
            r"dívida.*ativa.*receita",
            r"fonte.*financiamento.*receita",
        ],
        "LRF": [
            r"LRF.*despesa", r"despesa.*obrigatória.*continuada",
            r"limite.*pessoal.*LRF", r"receita.*corrente.*líquida",
            r"transparência.*fiscal.*LRF",
            r"relatório.*resumo.*execução.*orçamentária",
            r"relatório.*gestão.*fiscal",
            r"dívida.*fundada", r"operação.*crédito.*antecipação",
        ],
        "AFO - Outros": [
            r"administração.*financeira.*orçamentária",
            r"AFO",
        ],
    },

    "Economia / Finanças": {
        "Demanda por Moeda / Taxa de Juros": [
            r"demanda.*moeda", r"oferta.*moeda",
            r"taxa.*juros.*real.*demanda",
        ],
        "Operações de Mercado Aberto": [
            r"operação.*mercado.*aberto", r"open.*market",
            r"preço.*título.*juros",
        ],
        "Política Monetária (SELIC / Compulsório)": [
            r"SELIC", r"recolhimento.*compulsório",
            r"política.*monetária.*contracionista",
            r"liquidez.*inflação.*SELIC",
        ],
        "Equilíbrio de Mercado": [
            r"equilíbrio.*mercado", r"concorrência.*perfeita",
            r"função.*demanda", r"função.*oferta",
            r"custo.*marginal.*maximização",
        ],
    },

    "Gerenciamento de Projetos / BPM": {
        "PMBOK": [
            r"PMBOK", r"gerente.*projeto",
            r"backlog.*projeto", r"estimativa.*custo.*projeto",
            r"determinar.*orçamento.*projeto",
            r"gerenciamento.*requisito.*ágil",
            r"gestão.*pessoas.*PMBOK",
            r"gerenciamento.*financeiro.*projeto",
            r"representação.*relação.*lógica.*PMBOK",
            r"Termo.*Abertura.*Projeto",
        ],
        "BPM - Modelagem de Processos": [
            r"BPM", r"modelagem.*processo",
            r"visão.*processo.*funcional",
            r"representação.*processo.*negócio",
        ],
    },

    "Conhecimentos Regionais": {
        "Geografia / Cultura do Estado": [
            r"região.*geoeconômica", r"zona.*mata.*cana",
            r"agreste", r"sertão", r"litoral.*estado",
            r"indígena.*ocupação.*territorial",
            r"toré", r"cultura.*povo.*indígena",
            r"conhecimento.*estado",
        ],
    },
}


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class QuestaoInfo:
    """Representa uma questão extraída da prova."""
    numero: int
    disciplina: str
    topico: str
    texto_questao: str = ""


@dataclass
class ResultadoAnalise:
    """Resultado da análise de um arquivo."""
    arquivo: str
    nome_prova: str
    total_questoes: int
    contagem_disciplina_topico: Dict[str, Dict[str, int]] = field(default_factory=dict)
    questoes: List[QuestaoInfo] = field(default_factory=list)


# ============================================================
# FUNÇÕES DE CLASSIFICAÇÃO
# ============================================================

def classificar_topico(texto: str) -> Tuple[str, str]:
    """
    Classifica um texto de questão em (disciplina, topico_especifico).
    Retorna ('Não Classificado', 'Não Classificado') se não encontrar match.
    """
    texto_lower = texto.lower()

    melhor_match = None
    melhor_score = 0
    melhor_disciplina = "Não Classificado"
    melhor_topico = "Não Classificado"

    for disciplina, topicos in TOPICOS_POR_DISCIPLINA.items():
        for topico, patterns in topicos.items():
            for pattern in patterns:
                if re.search(pattern, texto_lower, re.IGNORECASE):
                    # Conta o número de palavras do pattern que dão match
                    score = len(pattern)
                    if score > melhor_score:
                        melhor_score = score
                        melhor_disciplina = disciplina
                        melhor_topico = topico

    return melhor_disciplina, melhor_topico


def classificar_questao(texto_questao: str, num_questao: int) -> QuestaoInfo:
    """Classifica uma única questão."""
    disciplina, topico = classificar_topico(texto_questao)
    return QuestaoInfo(
        numero=num_questao,
        disciplina=disciplina,
        topico=topico,
        texto_questao=texto_questao[:200]  # Preview
    )


# ============================================================
# FUNÇÕES DE EXTRAÇÃO DE QUESTÕES DO ARQUIVO
# ============================================================

def extrair_questoes_do_arquivo(caminho: str) -> List[QuestaoInfo]:
    """
    Extrai questões de um arquivo .md, classificando cada uma.
    Versão otimizada com regex mais eficiente.
    """
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    questoes = []
    
    # Estratégia otimizada: dividir por números de questão seguidos de texto
    # Padrão mais eficiente
    padrao = re.compile(r'(?:^|\n)(?:QUESTÃO\s*|Questão\s*|questão\s*)?(\d{1,3})(?:\s*\n|\s*\.)')
    
    matches = list(padrao.finditer(conteudo))
    
    for i, match in enumerate(matches):
        num = int(match.group(1))
        inicio = match.end()
        fim = matches[i + 1].start() if i + 1 < len(matches) else len(conteudo)
        
        texto = conteudo[inicio:fim].strip()
        
        # Filtra blocos muito pequenos (instruções, cabeçalhos)
        if len(texto) > 50:
            questao_info = classificar_questao(texto, num)
            questoes.append(questao_info)

    return questoes


def extrair_por_secao(caminho: str) -> List[QuestaoInfo]:
    """
    Extrai questões identificando as seções/disciplinas do arquivo.
    Esta abordagem usa os títulos de seção como disciplina.
    """
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    questoes = []

    # Identifica títulos de seção (linhas sem numeração que parecem ser títulos de disciplina)
    padrao_secao = re.compile(
        r'\n([A-ZÁÉÍÓÚÂÃÔÇÀ\s]+(?:e\s[A-ZÁÉÍÓÚÂÃÔÇÀ\s]+)*)\n',
        re.MULTILINE
    )

    # Divide por seções
    secoes = padrao_secao.split(conteudo)

    disciplina_atual = "Geral"
    num_questao = 1

    for i in range(0, len(secoes), 2):
        if i + 1 < len(secoes):
            titulo_secao = secoes[i].strip()
            conteudo_secao = secoes[i + 1]

            # Tenta mapear o título para uma disciplina conhecida
            disciplina_mapeada = mapear_disciplina_titulo(titulo_secao)
            if disciplina_mapeada:
                disciplina_atual = disciplina_mapeada

            # Extrai questões do conteúdo da seção
            questoes_secao = extrair_questoes_texto(conteudo_secao, num_questao)
            for q in questoes_secao:
                q.disciplina = disciplina_atual
                questoes.append(q)

            num_questao += len(questoes_secao)

    return questoes


def mapear_disciplina_titulo(titulo: str) -> Optional[str]:
    """Mapeia um título de seção para uma disciplina conhecida."""
    titulo_lower = titulo.lower()

    mapeamentos = {
        "direito tributário": "Direito Tributário",
        "tributário": "Direito Tributário",
        "contabilidade geral": "Contabilidade Geral",
        "contabilidade avançada": "Contabilidade Avançada",
        "contabilidade de custos": "Contabilidade de Custos",
        "custos": "Contabilidade de Custos",
        "auditoria": "Auditoria",
        "auditoria contábil": "Auditoria",
        "auditoria fiscal": "Auditoria",
        "direito constitucional": "Direito Constitucional",
        "constitucional": "Direito Constitucional",
        "direito administrativo": "Direito Administrativo",
        "administrativo": "Direito Administrativo",
        "direito civil": "Direito Civil",
        "civil": "Direito Civil",
        "direito penal": "Direito Penal",
        "penal": "Direito Penal",
        "direito empresarial": "Direito Empresarial",
        "empresarial": "Direito Empresarial",
        "comercial": "Direito Empresarial",
        "língua portuguesa": "Língua Portuguesa",
        "português": "Língua Portuguesa",
        "portuguesa": "Língua Portuguesa",
        "matemática financeira": "Matemática Financeira",
        "financeira": "Matemática Financeira",
        "financeiro": "Matemática Financeira",
        "estatística": "Estatística",
        "tecnologia": "Tecnologia da Informação / Análise de Dados",
        "informática": "Tecnologia da Informação / Análise de Dados",
        "análise de dados": "Tecnologia da Informação / Análise de Dados",
        "dados": "Tecnologia da Informação / Análise de Dados",
        "raciocínio lógico": "Raciocínio Lógico",
        "lógico": "Raciocínio Lógico",
        "lógica": "Raciocínio Lógico",
        "administração financeira": "Administração Financeira e Orçamentária",
        "orçamentária": "Administração Financeira e Orçamentária",
        "orçamento": "Administração Financeira e Orçamentária",
        "economia": "Economia / Finanças",
        "gerenciamento": "Gerenciamento de Projetos / BPM",
        "projetos": "Gerenciamento de Projetos / BPM",
        "legislação": "Legislação Tributária Estadual",
        "regional": "Conhecimentos Regionais",
        "segurança": "Tecnologia da Informação / Análise de Dados",
        "legislação tributária": "Legislação Tributária Estadual",
    }

    for chave, disciplina in mapeamentos.items():
        if chave in titulo_lower:
            return disciplina

    return None


def extrair_questoes_texto(texto: str, num_inicial: int) -> List[QuestaoInfo]:
    """Extrai questões de um bloco de texto e classifica cada uma."""
    questoes = []

    # Divide o texto em blocos de questões
    # Busca por alternativas (A), (B), (C), (D), (E) ou A) B) C) etc.
    blocos = re.split(r'\n(?=\d{1,3}\s*[.\)]\s*\n)', texto)

    for idx, bloco in enumerate(blocos):
        if len(bloco.strip()) > 20:
            questao_info = classificar_questao(bloco, num_inicial + idx)
            questoes.append(questao_info)

    return questoes


# ============================================================
# FUNÇÃO PRINCIPAL DE ANÁLISE
# ============================================================

def analisar_todas_provas(pasta: str, arquivos: List[str]) -> List[ResultadoAnalise]:
    """
    Analisa todas as provas e retorna resultados consolidados.
    """
    resultados = []

    for nome_arquivo in arquivos:
        caminho = os.path.join(pasta, nome_arquivo)
        if not os.path.exists(caminho):
            print(f"⚠️ Arquivo não encontrado: {caminho}")
            continue

        print(f"📄 Analisando: {nome_arquivo}")

        # Aborda extração por classificação automática de conteúdo
        questoes = extrair_questoes_do_arquivo(caminho)

        # Conta por disciplina e tópico
        contagem = defaultdict(lambda: defaultdict(int))
        for q in questoes:
            contagem[q.disciplina][q.topico] += 1

        resultado = ResultadoAnalise(
            arquivo=nome_arquivo,
            nome_prova=nome_arquivo.replace('.md', '').replace('_', ' ').title(),
            total_questoes=len(questoes),
            contagem_disciplina_topico=dict(contagem),
            questoes=questoes
        )

        resultados.append(resultado)
        print(f"   ✅ {len(questoes)} questões classificadas")

    return resultados


# ============================================================
# FUNÇÕES DE RELATÓRIO
# ============================================================

def gerar_tabela_consolidada(resultados: List[ResultadoAnalise]) -> Dict[str, Dict[str, int]]:
    """Gera tabela consolidada de todas as provas."""
    consolidado = defaultdict(lambda: defaultdict(int))

    for resultado in resultados:
        for disciplina, topicos in resultado.contagem_disciplina_topico.items():
            for topico, count in topicos.items():
                consolidado[disciplina][topico] += count

    return dict(consolidado)


def gerar_relatorio_markdown(resultados: List[ResultadoAnalise], caminho_saida: str):
    """Gera relatório em formato Markdown."""
    consolidado = gerar_tabela_consolidada(resultados)

    linhas = []
    linhas.append("# TEMAS COBRADOS NAS PROVAS DE AUDITOR FISCAL - GRANULARIDADE FINA\n")
    linhas.append("## Análise Automática por Classificação de Conteúdo\n")
    linhas.append(f"**Total de provas analisadas:** {len(resultados)}\n")
    linhas.append(f"**Data da análise:** 13/04/2026\n")

    # Tabela consolidada geral
    linhas.append("\n---\n")
    linhas.append("\n## TABELA CONSOLIDADA GERAL (Todas as Provas)\n")
    linhas.append("\n| DISCIPLINA | TEMA ESPECÍFICO | OCORRÊNCIAS |\n")
    linhas.append("|-----------|----------------|:-----------:|\n")

    # Ordena por total decrescente
    totais = {}
    for disc, topicos in consolidado.items():
        total_disc = sum(topicos.values())
        totais[disc] = total_disc

    discipl_ord = sorted(totais.keys(), key=lambda d: totais[d], reverse=True)

    for disciplina in discipl_ord:
        topicos = consolidado[disciplina]
        total_disc = sum(topicos.values())

        # Ordena tópicos dentro da disciplina
        top_ord = sorted(topicos.items(), key=lambda x: x[1], reverse=True)

        for idx, (topico, count) in enumerate(top_ord):
            if idx == 0:
                linhas.append(f"| **{disciplina}** | {topico} | **{count}** |")
            else:
                linhas.append(f"| {disciplina} | {topico} | {count} |")

        linhas.append(f"| **{disciplina}** | **TOTAL** | **{total_disc}** |")
        linhas.append("")

    # TOP 20 temas
    linhas.append("\n---\n")
    linhas.append("\n## 🏆 TOP 20 TEMAS MAIS COBRADOS\n")
    linhas.append("\n| RANK | TEMA ESPECÍFICO | OCORRÊNCIAS |\n")
    linhas.append("|:----:|----------------|:-----------:|\n")

    todos_temas = []
    for disc, topicos in consolidado.items():
        for topico, count in topicos.items():
            todos_temas.append((disc, topico, count))

    todos_temas.sort(key=lambda x: x[2], reverse=True)

    for rank, (disc, topico, count) in enumerate(todos_temas[:20], 1):
        linhas.append(f"| {rank}° | {topico} ({disc}) | {count} |")

    # Relatório por arquivo
    linhas.append("\n---\n")
    linhas.append("\n## DETALHAMENTO POR ARQUIVO\n")

    for resultado in resultados:
        linhas.append(f"\n### {resultado.nome_prova}\n")
        linhas.append(f"**Total de questões classificadas:** {resultado.total_questoes}\n")

        if resultado.contagem_disciplina_topico:
            linhas.append("\n| DISCIPLINA | TEMA ESPECÍFICO | QTD |\n")
            linhas.append("|-----------|----------------|:---:|\n")

            disc_ord = sorted(
                resultado.contagem_disciplina_topico.items(),
                key=lambda x: sum(x[1].values()),
                reverse=True
            )

            for disc, topicos in disc_ord:
                total_disc = sum(topicos.values())
                top_ord = sorted(topicos.items(), key=lambda x: x[1], reverse=True)

                for idx, (topico, count) in enumerate(top_ord):
                    if idx == 0:
                        linhas.append(f"| **{disc}** | {topico} | {count} |")
                    else:
                        linhas.append(f"| {disc} | {topico} | {count} |")

                linhas.append(f"| **{disc}** | **TOTAL** | **{total_disc}** |")

            linhas.append("")

    # Salva o arquivo
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas))

    print(f"\n📝 Relatório salvo em: {caminho_saida}")


def gerar_relatorio_csv(resultados: List[ResultadoAnalise], caminho_saida: str):
    """Gera relatório em formato CSV para análise no Excel."""
    import csv

    with open(caminho_saida, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['DISCIPLINA', 'TEMA_ESPECIFICO', 'OCORRENCIAS'])

        consolidado = gerar_tabela_consolidada(resultados)

        rows = []
        for disc, topicos in consolidado.items():
            for topico, count in topicos.items():
                rows.append((disc, topico, count))

        rows.sort(key=lambda x: x[2], reverse=True)

        for disc, topico, count in rows:
            writer.writerow([disc, topico, count])

    print(f"📊 CSV salvo em: {caminho_saida}")


def gerar_relatorio_json(resultados: List[ResultadoAnalise], caminho_saida: str):
    """Gera relatório em formato JSON."""
    consolidado = gerar_tabela_consolidada(resultados)

    dados = {
        "metadata": {
            "total_provas": len(resultados),
            "data_analise": "2026-04-13",
        },
        "consolidado": {
            disc: dict(topicos)
            for disc, topicos in consolidado.items()
        },
        "por_arquivo": {
            r.arquivo: {
                "total_questoes": r.total_questoes,
                "disciplinas": {
                    disc: dict(topicos)
                    for disc, topicos in r.contagem_disciplina_topico.items()
                }
            }
            for r in resultados
        }
    }

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"📋 JSON salvo em: {caminho_saida}")


# ============================================================
# MAIN
# ============================================================

def main():
    """Função principal."""
    print("=" * 60)
    print("📊 ANALISADOR DE TEMAS - PROVAS DE AUDITOR FISCAL")
    print("=" * 60)
    print()

    # Executa análise
    resultados = analisar_todas_provas(PASTA_PROVAS, ARQUIVOS_PROVAS)

    if not resultados:
        print("❌ Nenhum arquivo encontrado. Verifique os caminhos.")
        return

    # Gera relatórios
    pasta_saida = os.path.join(PASTA_PROVAS, "PIPELINE DE DADOS")
    os.makedirs(pasta_saida, exist_ok=True)

    gerar_relatorio_markdown(
        resultados,
        os.path.join(pasta_saida, "analise_granularidade_fina_auto.md")
    )

    gerar_relatorio_csv(
        resultados,
        os.path.join(pasta_saida, "analise_granularidade_fina_auto.csv")
    )

    gerar_relatorio_json(
        resultados,
        os.path.join(pasta_saida, "analise_granularidade_fina_auto.json")
    )

    # Resumo final
    consolidado = gerar_tabela_consolidada(resultados)
    total_geral = sum(
        sum(topicos.values())
        for topicos in consolidado.values()
    )

    print()
    print("=" * 60)
    print("📊 RESUMO FINAL")
    print("=" * 60)
    print(f"Total de provas analisadas: {len(resultados)}")
    print(f"Total de questões classificadas: {total_geral}")
    print(f"Total de disciplinas identificadas: {len(consolidado)}")
    print()

    # TOP 5 disciplinas
    print("🏆 TOP 5 Disciplinas:")
    totais_disc = {d: sum(t.values()) for d, t in consolidado.items()}
    for i, (disc, total) in enumerate(
        sorted(totais_disc.items(), key=lambda x: x[1], reverse=True)[:5], 1
    ):
        print(f"  {i}° {disc}: {total} ocorrências")

    print()
    print("✅ Análise concluída com sucesso!")
    print(f"📁 Arquivos gerados em: {pasta_saida}")


if __name__ == "__main__":
    main()
