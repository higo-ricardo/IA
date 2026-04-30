import re
import sys

def classificar_sentenca(texto):
    texto_lower = texto.lower()
    
    classes = {
        'Direito Penal': ['crime', 'penal', 'tráfico', 'drogas', 'estupro', 'roubo', 'furto', 'homicídio', 'violência', 'arma', 'letal', 'pena', 'prisão', 'condenação', 'ação penal', 'processo penal', 'extradição', 'extraditando', 'infração', 'delito', 'típico', 'consumação', 'tentativa', 'dolo', 'culpa', 'medida de segurança'],
        'Direito Civil': ['civil', 'contrato', 'compra e venda', 'locação', 'imóvel', 'propriedade', 'posse', 'usucapião', 'sucessão', 'herança', 'testamento', 'casamento', 'divórcio', 'separação', 'união estável', 'alimentos', 'doação', 'parentesco', 'adoção', 'código civil'],
        'Direito Tributário': ['tributário', 'tributario', 'imposto', 'icms', 'iptu', 'iss', 'cofins', 'ipi', 'ir', 'imposto de renda', 'tributo', 'fazenda', 'receita federal', 'tributação', 'compensação', 'restituição', 'isenção', 'ctn', 'contribuição'],
        'Direito Administrativo': ['administrativo', 'administração', 'servidor', 'concurso', 'licitação', 'contrato administrativo', 'ato administrativo', 'processo administrativo', 'disciplinar', 'improbidade', 'concessão', 'permissão', 'autorização', 'sanção', 'pública', 'autarquia', 'fundação', 'empresa pública'],
        'Direito do Consumidor': ['consumidor', 'consumo', 'cdc', 'código de defesa do consumidor', 'procon', 'vício', 'defeito', 'garantia', 'produto', 'serviço', 'cláusula abusiva'],
        'Direito Previdenciário': ['previdenciário', 'inss', 'aposentadoria', 'benefício', 'pensão', 'auxílio', 'salário-maternidade', 'seguro social', 'rgps', 'contribuição previdenciária', 'dependente', 'segurado', 'carência'],
        'Direito Processual Civil': ['processo civil', 'cpc', 'ação', 'execução', 'embargos', 'recurso', 'apelação', 'agravo', 'mandado de segurança', 'tutela', 'sentença', 'acórdão', 'competência', 'jurisdição', 'foro', 'código de processo civil'],
        'Direito Processual Penal': ['processo penal', 'cpp', 'ação penal', 'inquérito', 'prisão', 'fiança', 'habeas corpus', 'extradição', 'prisão preventiva', 'medidas cautelares', 'execução penal', 'pena', 'condenação', 'absolvição', 'código de processo penal'],
        'Direito do Trabalho': ['trabalhista', 'trabalho', 'clt', 'empregado', 'empregador', 'salário', 'férias', 'fgts', 'seguro desemprego', 'acidente do trabalho', 'justiça do trabalho', 'sindicato', 'greve'],
        'Direito Ambiental': ['ambiental', 'meio ambiente', 'poluição', 'ecológico', 'fauna', 'flora', 'reserva', 'licenciamento', 'desapropriação', 'crimes ambientais'],
        'Direito Constitucional': ['constitucional', 'constituição', 'federal', 'lei complementar', 'lei ordinária', 'emenda constitucional', 'congresso', 'senado', 'câmara', 'presidente', 'federação', 'poder']
    }
    
    for materia, palavras in classes.items():
        if any(palavra in texto_lower for palavra in palavras):
            return materia
    return 'Outras Súmulas'

def processar_arquivo(caminho, titulo):
    with open(caminho, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    header = lines[0]
    entries = []
    current = None
    
    for line in lines:
        if line.startswith('Súmula ') or line.startswith('Súmula '):
            if current:
                entries.append(current)
            current = {'texto': line}
        elif current and line.strip() == '':
            continue
        elif current:
            current['texto'] += '\n' + line
    
    if current:
        entries.append(current)
    
    # Remover duplicatas vazias
    entries = [e for e in entries if e['texto'].strip()]
    
    # Classificar
    classificados = {}
    for e in entries:
        texto_limpo = e['texto'].split('\n')[0]  # primeira linha
        materia = classificar_sentenca(texto_limpo)
        if materia not in classificados:
            classificados[materia] = []
        classificados[materia].append(e)
    
    # Ordem das matérias
    materias_ordem = [
        'Direito Penal', 'Direito Civil', 'Direito Tributário',
        'Direito Administrativo', 'Direito do Consumidor',
        'Direito Previdenciário', 'Direito Processual Civil',
        'Direito Processual Penal', 'Direito do Trabalho',
        'Direito Ambiental', 'Direito Constitucional',
        'Outras Súmulas'
    ]
    
    novo_content = header + '\n\n'
    for materia in materias_ordem:
        if materia in classificados and classificados[materia]:
            novo_content += f'## {materia}\n\n'
            for e in classificados[materia]:
                novo_content += e['texto'] + '\n\n'
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(novo_content)
    
    print(f'{titulo}: {len(entries)} súmulas classificadas em {len(classificados)} matérias.')

# Processar ambos
processar_arquivo('VerbetesSTJ.md', 'VerbetesSTJ.md')
processar_arquivo('VerbetesSTF.md', 'VerbetesSTF.md')
print('Concluído.')
