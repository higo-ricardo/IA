import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict


# ==========================================
# CONFIGURAÇÃO DAS ÁREAS E PALAVRAS-CHAVE
# ==========================================
AREAS = {
    "direito_tributario": {
        "titulo": "Direito Tributário",
        "headers": ["DIREITO TRIBUTÁRIO", "TRIBUTÁRIO", "SISTEMA TRIBUTÁRIO NACIONAL"],
        "keywords": ["icms", "iptu", "iss", "ipva", "ctn", "código tributário", "lançamento tributário", "fato gerador", "isenção tributária", "imunidade tributária", "sonegação", "dívida ativa", "contribuinte", "base de cálculo", "alíquota"]
    },
    "legislacao_tributaria_estadual": {
        "titulo": "Legislação Tributária Estadual",
        "headers": ["LEGISLAÇÃO TRIBUTÁRIA", "LEGISLAÇÃO ESPECÍFICA", "REGULAMENTO DO ICMS"],
        "keywords": ["código tributário do estado", "lei do icms do", "regulamento do icms", "dever contumaz", "dief", "processo administrativo fiscal estadual"]
    },
    "direito_constitucional": {
        "titulo": "Direito Constitucional",
        "headers": ["DIREITO CONSTITUCIONAL", "CONSTITUCIONAL"],
        "keywords": ["constituição federal", "cf/88", "controle de constitucionalidade", "adi", "poderes da união", "direitos fundamentais", "competência legislativa", "cláusula pétrea"]
    },
    "direito_administrativo": {
        "titulo": "Direito Administrativo",
        "headers": ["DIREITO ADMINISTRATIVO", "ADMINISTRATIVO"],
        "keywords": ["ato administrativo", "licitação", "contrato administrativo", "servidor público", "improbidade administrativa", "poder de polícia", "responsabilidade civil do estado", "concurso público", "processo administrativo disciplinar"]
    },
    "direito_civil": {
        "titulo": "Direito Civil",
        "headers": ["DIREITO CIVIL", "CIVIL"],
        "keywords": ["código civil", "contratos civis", "obrigações", "sucessões", "família", "bens", "posse", "propriedade", "evicção", "vício redibitório", "prescrição", "decadência"]
    },
    "direito_penal": {
        "titulo": "Direito Penal",
        "headers": ["DIREITO PENAL", "PENAL"],
        "keywords": ["código penal", "crime contra", "pena", "tipicidade", "dolo", "culpa", "prescrição penal", "concurso de crimes", "lei de drogas", "lei de armas", "homicídio", "furto", "roubo"]
    },
    "direito_empresarial": {
        "titulo": "Direito Empresarial",
        "headers": ["DIREITO EMPRESARIAL", "EMPRESARIAL", "DIREITO COMERCIAL"],
        "keywords": ["sociedade empresária", "falência", "recuperação judicial", "título de crédito", "estabelecimento empresarial", "nome empresarial", "lei de falências", "duplicata", "cheque"]
    },
    "direito_financeiro": {
        "titulo": "Direito Financeiro e AFO",
        "headers": ["DIREITO FINANCEIRO", "ADMINISTRAÇÃO FINANCEIRA", "ORÇAMENTO"],
        "keywords": ["orçamento público", "lrf", "lei de responsabilidade fiscal", "ppa", "ldo", "loa", "crédito adicional", "receita pública", "despesa pública", "restos a pagar", "empenho", "dívida pública", "siafi"]
    },
    "economia": {
        "titulo": "Economia",
        "headers": ["ECONOMIA", "MICROECONOMIA", "MACROECONOMIA"],
        "keywords": ["microeconomia", "macroeconomia", "curva de demanda", "curva de oferta", "monopólio", "oligopólio", "inflação", "pib", "política monetária", "sistema financeiro nacional"]
    },
    "contabilidade": {
        "titulo": "Contabilidade",
        "headers": ["CONTABILIDADE", "CONTABILIDADE GERAL", "CONTABILIDADE AVANÇADA"],
        "keywords": ["balanço patrimonial", "dre", "ativo", "passivo", "lançamento contábil", "depreciação", "cpc", "ifrs", "auditoria contábil"]
    }
}


# ==========================================
# MODELOS
# ==========================================
@dataclass
class Questao:
    numero: str
    texto: str
    prova_origem: str


# ==========================================
# INTERFACES ABC
# ==========================================
class DocumentCleaner(ABC):
    """Base para limpadores/normalizadores de documentos jurídicos."""

    @abstractmethod
    def clean(self, content: str) -> str:
        ...

    @abstractmethod
    def get_output_extension(self) -> str:
        ...


class QuestionProcessor(ABC):
    """Base para processadores de questões."""

    @abstractmethod
    def extract(self, filepath: str) -> List[str]:
        ...

    @abstractmethod
    def classify(self, questions: List[str]) -> Dict[str, List[Questao]]:
        ...


# ==========================================
# IMPLEMENTAÇÕES - CLEANERS
# ==========================================
class SumulaVinculanteCleaner(DocumentCleaner):
    """Limpa arquivos de súmulas vinculantes, extraindo número + enunciado."""

    PATTERN = re.compile(
        r"SÚMULA VINCULANTE (\d+)\s*\n(.*?)(?=SÚMULA VINCULANTE \d+|$)",
        re.DOTALL
    )

    def clean(self, content: str) -> str:
        matches = self.PATTERN.findall(content)
        lines = []
        for num, enunciado in matches:
            enunciado = re.sub(r'\s+', ' ', enunciado).strip()
            enunciado = re.sub(r'\s+\d+\s*$', '', enunciado).strip()
            lines.append(f"SÚMULA VINCULANTE {num} {enunciado}")
        return "\n\n".join(lines)

    def get_output_extension(self) -> str:
        return "_limpo.md"

    def count_items(self, content: str) -> int:
        return len(self.PATTERN.findall(content))


# ==========================================
# IMPLEMENTAÇÕES - QUESTION PROCESSOR
# ==========================================
class DefaultQuestionProcessor(QuestionProcessor):
    """Extrai e classifica questões de provas."""

    QUESTION_PATTERN = re.compile(
        r'(?:QUESTÃO|Questão|Item|item|^\s*\d+[\.\)-])\s*(\d+)',
        re.MULTILINE
    )

    def __init__(self, areas: Dict[str, dict]):
        self.areas = areas

    def extract(self, filepath: str) -> List[str]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return []

        questions = []
        matches = list(self.QUESTION_PATTERN.finditer(content))

        for i, match in enumerate(matches):
            start_idx = match.start()
            end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            q_text = content[start_idx:end_idx].strip()
            q_text = re.sub(r'\n\s*\n', '\n\n', q_text)
            if len(q_text) > 50:
                questions.append(q_text)

        return questions

    def classify(self, questions: List[str]) -> Dict[str, List[Questao]]:
        collected: Dict[str, List[Questao]] = {key: [] for key in self.areas}

        for q_text in questions:
            q_lower = q_text.lower()
            best_score = 0
            best_area = None

            for area_key, config in self.areas.items():
                score = 0
                for kw in config['keywords']:
                    if kw.lower() in q_lower:
                        score += 2
                for header in config['headers']:
                    if header.lower() in q_lower:
                        score += 10
                if score > best_score:
                    best_score = score
                    best_area = area_key

            if best_area and best_score > 2:
                q_number_match = self.QUESTION_PATTERN.search(q_text)
                num = q_number_match.group(1) if q_number_match else "?"
                collected[best_area].append(Questao(numero=num, texto=q_text, prova_origem=""))

        return collected


# ==========================================
# ORQUESTRADOR
# ==========================================
class PipelineOrchestrator:
    """Orquestra cleaners e question processors no diretório."""

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.cleaners: List[DocumentCleaner] = []
        self.question_processor: QuestionProcessor | None = None

    def register_cleaner(self, cleaner: DocumentCleaner):
        self.cleaners.append(cleaner)

    def set_question_processor(self, processor: QuestionProcessor):
        self.question_processor = processor

    def run_cleaners(self):
        for cleaner in self.cleaners:
            md_files = [
                f for f in os.listdir(self.base_dir)
                if f.endswith('.md') and not f.endswith(cleaner.get_output_extension())
            ]
            for filename in md_files:
                filepath = os.path.join(self.base_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                cleaned = cleaner.clean(content)
                count = cleaner.count_items(content) if hasattr(cleaner, 'count_items') else '?'

                if cleaned.strip():
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(self.base_dir, f"{name}{cleaner.get_output_extension()}{ext}")
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned)
                    print(f"  ✅ {count} itens extraídos → {os.path.basename(output_path)}")

    def run_question_extraction(self, output_dir: str | None = None):
        if not self.question_processor:
            print("⚠️ Nenhum question processor registrado.")
            return

        target_dir = output_dir or self.base_dir

        # Limpar arquivos anteriores
        for f in os.listdir(target_dir):
            if f.startswith('questoes_') and f.endswith('.md'):
                os.remove(os.path.join(target_dir, f))

        md_files = [
            f for f in os.listdir(target_dir)
            if f.endswith('.md') and not f.startswith('questoes_')
        ]

        print(f"🔍 Encontrados {len(md_files)} arquivos para processar.")

        areas = AREAS
        global_stats = {key: 0 for key in areas}

        for filename in md_files:
            filepath = os.path.join(target_dir, filename)
            print(f"📄 Processando: {filename}...")

            questions = self.question_processor.extract(filepath)
            if not questions:
                print(f"   ⚠️ Nenhuma questão identificada.")
                continue

            collected = self.question_processor.classify(questions)

            for area_key, questoes in collected.items():
                if not questoes:
                    continue
                area_config = areas[area_key]
                output_path = os.path.join(target_dir, f"questoes_{area_key}.md")
                mode = 'a' if os.path.exists(output_path) else 'w'

                with open(output_path, mode, encoding='utf-8') as f:
                    if mode == 'w':
                        f.write(f"# Questões de {area_config['titulo']}\n\n")
                        f.write(f"> Extraídas automaticamente das provas do diretório.\n\n")
                        f.write("---\n\n")

                    f.write(f"## Proveniente de: {filename}\n\n")
                    for q in questoes:
                        f.write(f"### Questão {q.numero}\n\n")
                        f.write(f"{q.texto}\n\n")
                        f.write("---\n\n")

                global_stats[area_key] += len(questoes)

            print(f"   ✅ Extraídas {len(questions)} questões.")

        print("\n📊 Relatório Final de Extração:")
        print("-" * 50)
        for area_key, total in global_stats.items():
            titulo = areas[area_key]['titulo']
            print(f"  {titulo:40} | {total:3} questões")
        print("-" * 50)
        print("✅ Processo finalizado. Verifique os arquivos 'questoes_*.md' na pasta.")


# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================
def run_extraction():
    base_dir = r'c:\Users\hig0\Downloads\PIPELINE DE DADOS\NORMALIZACAO'

    orchestrator = PipelineOrchestrator(base_dir)

    # Registrar cleaners
    orchestrator.register_cleaner(SumulaVinculanteCleaner())

    # Registrar question processor
    orchestrator.set_question_processor(DefaultQuestionProcessor(AREAS))

    # Executar pipeline
    print("🧹 Executando cleaners...")
    orchestrator.run_cleaners()

    print("\n📝 Extraindo questões...")
    orchestrator.run_question_extraction()


if __name__ == "__main__":
    run_extraction()
