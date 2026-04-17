import pdfplumber
import os
import re
from collections import Counter
from typing import List, Tuple

# ==========================================
# CONFIGURAÇÃO
# ==========================================
BASE_DIR = r'c:\Users\hig0\Downloads\PIPELINE DE DADOS\NORMALIZACAO'
OUTPUT_SUFFIX = "_limpo.md"

# Padrões para identificar o início real da prova (cortar instruções iniciais)
START_MARKERS = [
    r'LÍNGUA PORTUGUESA', r'CONHECIMENTOS GERAIS', r'CONHECIMENTOS ESPECÍFICOS',
    r'QUESTÃO\s*1', r'QUESTÃO\s*01', r'TEXTO 1A1-I', r'PROVA OBJETIVA'
]

# Padrões de lixo comum para remoção via Regex
JUNK_PATTERNS = [
    r'Espaço livre', r'RASCUNHO', r'ESPACO LIVRE',
    r'www\.fgv\.br', r'www\.cebraspe\.org\.br', r'www\.esaf\.fazenda\.gov\.br',
    r'Página\s+\d+', r'\d+\s*/\s*\d+', r'Tipo\s*\d+\s*–\s*\w+',
    r'Secretaria\s+de\s+Fazenda', r'Governos?\s+do\s+Estado',
    r'Boa\s+(sorte|prova)!', r'NÃO\s+SERÁ\s+PERMITIDO', r'INFORMAÇÕES\s+GERAIS'
]

# ==========================================
# CLASSE DE LIMPEZA
# ==========================================
class PDFProcessor:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.splitext(os.path.basename(filepath))[0]
        self.pages_text = []

    def extract_raw_text(self) -> bool:
        """Extrai texto bruto usando pdfplumber."""
        print(f"📖 Extraindo texto de {self.filename}...")
        try:
            with pdfplumber.open(self.filepath) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        self.pages_text.append(text)
            return len(self.pages_text) > 0
        except Exception as e:
            print(f"❌ Erro ao extrair PDF: {e}")
            return False

    def identify_headers_footers(self, threshold: float = 0.5) -> set:
        """Identifica linhas repetitivas que aparecem em >threshold% das páginas."""
        if not self.pages_text:
            return set()

        all_lines = []
        for page in self.pages_text:
            lines = page.split('\n')
            # Pega apenas as 3 primeiras e 3 últimas linhas (cabeçalho/rodapé prováveis)
            if len(lines) > 6:
                all_lines.extend([l.strip() for l in lines[:3] + lines[-3:]])
            else:
                all_lines.extend([l.strip() for l in lines])

        # Conta frequências
        counts = Counter(all_lines)
        num_pages = len(self.pages_text)
        limit = num_pages * threshold
        
        # Retorna linhas que aparecem frequentemente
        return {text for text, count in counts.items() if count >= limit and len(text) > 0}

    def clean_text(self, headers_footers: set) -> str:
        """Aplica limpezas, remoção de headers e normalização."""
        full_text = '\n'.join(self.pages_text)
        
        # 1. Remover Headers/Footers identificados
        if headers_footers:
            for hf in headers_footers:
                # Regex para remover a linha exata e possíveis espaços ao redor
                pattern = r'^\s*' + re.escape(hf) + r'\s*$'
                full_text = re.sub(pattern, '', full_text, flags=re.MULTILINE)

        # 2. Remover padrões de lixo (Marcas d'água, links, etc)
        for pattern in JUNK_PATTERNS:
            full_text = re.sub(pattern, '', full_text, flags=re.IGNORECASE | re.MULTILINE)

        # 3. Cortar Instruções Iniciais
        # Procura o primeiro marcador de início de prova
        start_match = None
        for marker in START_MARKERS:
            match = re.search(marker, full_text, re.IGNORECASE)
            if match and (start_match is None or match.start() < start_match.start()):
                start_match = match

        if start_match:
            # Mantém tudo a partir do início da prova, mas garante que o cabeçalho da matéria seja preservado
            full_text = full_text[start_match.start():]

        # 4. Normalização final
        # Remove linhas vazias excessivas
        full_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', full_text)
        # Remove espaços em branco no início/fim de linhas
        full_text = '\n'.join([line.strip() for line in full_text.splitlines()])
        
        return full_text

    def save_markdown(self, clean_text: str):
        """Salva o arquivo Markdown."""
        output_filename = f"{self.filename}{OUTPUT_SUFFIX}"
        output_path = os.path.join(BASE_DIR, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {self.filename} (Processado)\n\n")
            f.write(clean_text)
        
        print(f"✅ Salvo em: {output_filename}")

# ==========================================
# EXECUÇÃO
# ==========================================

def run_pdf_processor():
    print("🚀 Iniciando processamento de PDFs para Markdown limpo...")
    
    pdf_files = [f for f in os.listdir(BASE_DIR) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("⚠️ Nenhum arquivo PDF encontrado na pasta.")
        return

    for pdf_file in pdf_files:
        filepath = os.path.join(BASE_DIR, pdf_file)
        
        # 1. Instanciar e Extrair
        processor = PDFProcessor(filepath)
        if processor.extract_raw_text():
            # 2. Identificar ruídos repetitivos
            noise = processor.identify_headers_footers(threshold=0.4) # 40% das páginas
            
            # 3. Limpar
            clean_text = processor.clean_text(noise)
            
            # 4. Salvar
            processor.save_markdown(clean_text)
        else:
            print(f"⏩ Pulando {pdf_file} (não foi possível extrair texto ou está protegido).")

    print("\n🎉 Processo finalizado! Agora execute o script de extração de questões.")

if __name__ == "__main__":
    # Requer: pip install pdfplumber
    run_pdf_processor()
