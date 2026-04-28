#!/usr/bin/env python3
"""
Markdown Cleaner — Pipeline integrado de limpeza, encoding e extração jurídica.

Consolida funcionalidades de:
  - corrigir_encoding.py  (EncodingDetector, MarkdownValidator)
  - limpar-md-integrado.py (GenericCleaner, QuestionProcessor, PipelineOrchestrator)

Novas funcionalidades:
  - Remoção de espaços duplos/triplos com preservação de blocos de código
  - Normalização de espaço antes de pontuação (., ; ,)
  - Remoção de BOM e caracteres de controle inválidos
  - Normalização de headers Markdown (# sem espaço → # com espaço)
  - Limpeza de negrito/itálico com espaços internos (** texto ** → **texto**)
  - Detecção de links Markdown vazios [texto]()
  - Relatório JSON de limpeza por arquivo
  - Modo dry-run (preview sem salvar)
"""

import os
import re
import sys
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# ENCODING DETECTOR
# ─────────────────────────────────────────────────────────────────────────────
class EncodingDetector:
    """Detecta e corrige encoding de arquivos de texto em pt-BR."""

    # Caracteres cp1252 mal interpretados
    REPLACEMENTS = {
        "\x82": ",",   "\x84": '"',  "\x85": "...", "\x88": "^",
        "\x91": "'",   "\x92": "'",  "\x93": '"',   "\x94": '"',
        "\x95": "•",   "\x96": "-",  "\x97": "—",
        "\xa0": " ",   "\xa7": "§",  "\xa9": "©",   "\xaa": "ª",
        "\xab": "«",   "\xac": "¬",  "\xad": "",    "\xae": "®",
        "\xb0": "°",   "\xb1": "±",  "\xb2": "²",   "\xb3": "³",
        "\xb6": "¶",   "\xba": "º",  "\xbb": "»",
        "\xc0": "À",   "\xc1": "Á",  "\xc2": "Â",   "\xc3": "Ã",
        "\xc4": "Ä",   "\xc7": "Ç",  "\xc9": "É",   "\xca": "Ê",
        "\xd3": "Ó",   "\xd4": "Ô",  "\xd5": "Õ",   "\xda": "Ú",
        "\xe0": "à",   "\xe1": "á",  "\xe2": "â",   "\xe3": "ã",
        "\xe4": "ä",   "\xe7": "ç",  "\xe9": "é",   "\xea": "ê",
        "\xed": "í",   "\xf3": "ó",  "\xf4": "ô",   "\xf5": "õ",
        "\xfa": "ú",   "\xfc": "ü",
    }

    # UTF-8 mal decodificado como latin-1 (sequências duplas comuns)
    PT_BR_CORRECT = {
        "Ã¡": "á",  "Ã©": "é",  "Ã­": "í",  "Ã³": "ó",  "Ãº": "ú",
        "Ã£": "ã",  "Ãµ": "õ",  "Ã¢": "â",  "Ãª": "ê",  "Ã´": "ô",
        "Ã§": "ç",  "Ã‡": "Ç",  "Ã…": "à",  "Ã‰": "É",  "Ãš": "Ú",
        "â\x80\x99": "'",  "â\x80\x9c": '"',  "â\x80\x9d": '"',
        "â\x80\x94": "—",  "â\x80\x93": "–",
    }

    ENCODINGS_TO_TRY = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]

    @classmethod
    def detect_and_correct(cls, filepath: str) -> Tuple[str, str]:
        """Lê arquivo com detecção automática e corrige caracteres problemáticos."""
        content, used_encoding = None, None
        for enc in cls.ENCODINGS_TO_TRY:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    content = f.read()
                used_encoding = enc
                break
            except (UnicodeDecodeError, UnicodeError):
                continue

        if content is None:
            with open(filepath, "rb") as f:
                content = f.read().decode("utf-8", errors="replace")
            used_encoding = "utf-8 (com substituição)"

        content = cls.correct_characters(content)
        return used_encoding, content

    @classmethod
    def correct_characters(cls, content: str) -> str:
        """Aplica todas as correções de caracteres em sequência."""
        for wrong, right in cls.REPLACEMENTS.items():
            content = content.replace(wrong, right)
        for wrong, right in cls.PT_BR_CORRECT.items():
            content = content.replace(wrong, right)
        # Remove caracteres de controle inválidos (preserva \t \n \r)
        content = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", content)
        return content


# ─────────────────────────────────────────────────────────────────────────────
# RESULTADO DE LIMPEZA
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class CleaningResult:
    arquivo: str
    encoding_original: str = "utf-8"
    limpezas: List[str] = field(default_factory=list)
    linhas_antes: int = 0
    linhas_depois: int = 0
    chars_antes: int = 0
    chars_depois: int = 0
    erro: Optional[str] = None
    salvo: bool = False


# ─────────────────────────────────────────────────────────────────────────────
# MARKDOWN CLEANER — LIMPEZAS INTEGRADAS
# ─────────────────────────────────────────────────────────────────────────────
class MarkdownCleaner:
    """
    Aplica uma cadeia de limpezas a conteúdo Markdown.

    Transformações (em ordem):
      1.  BOM (byte order mark) → removido
      2.  CRLF → LF
      3.  Espaços duplos/triplos → único (fora de blocos de código)
      4.  Espaços no final de linha (trailing whitespace)
      5.  Linhas em branco excessivas → máx. 2 consecutivas
      6.  Espaço antes de pontuação: " ," " ." " ;" " :" → sem espaço
      7.  Headers sem espaço: ##Titulo → ## Titulo
      8.  Negrito/itálico com espaços internos: ** texto ** → **texto**
      9.  Links Markdown vazios: [texto]() → sinalizado no log
      10. Uma única \n no final do arquivo
    """

    def clean(self, content: str) -> Tuple[str, List[str]]:
        """Retorna (conteúdo limpo, lista de limpezas aplicadas)."""
        limpezas = []
        original = content

        # 1. BOM
        if content.startswith("\ufeff"):
            content = content[1:]
            limpezas.append("BOM removido")

        # 2. CRLF → LF
        if "\r\n" in content:
            content = content.replace("\r\n", "\n")
            limpezas.append("CRLF → LF")

        # 3. Espaços duplos/triplos fora de blocos de código
        content, n = self._fix_multiple_spaces(content)
        if n:
            limpezas.append(f"Espaços múltiplos removidos ({n} ocorrências)")

        # 4. Trailing whitespace
        lines = content.split("\n")
        stripped = [line.rstrip() for line in lines]
        if stripped != lines:
            limpezas.append("Trailing whitespace removido")
        lines = stripped

        # 5. Linhas em branco excessivas (máx. 2)
        lines, n = self._fix_blank_lines(lines)
        if n:
            limpezas.append(f"Linhas em branco excessivas reduzidas ({n}x)")

        content = "\n".join(lines)

        # 6. Espaço antes de pontuação
        content, n = self._fix_space_before_punctuation(content)
        if n:
            limpezas.append(f"Espaço antes de pontuação corrigido ({n}x)")

        # 7. Headers sem espaço
        content, n = self._fix_headers(content)
        if n:
            limpezas.append(f"Headers normalizados ({n}x)")

        # 8. Negrito/itálico com espaços internos
        content, n = self._fix_bold_italic_spaces(content)
        if n:
            limpezas.append(f"Espaços em negrito/itálico removidos ({n}x)")

        # 9. Links vazios (apenas detecta, não altera)
        empty_links = re.findall(r"\[([^\]]+)\]\(\s*\)", content)
        if empty_links:
            limpezas.append(f"Links vazios detectados: {len(empty_links)} ([texto]())")

        # 10. Garante única \n no final
        content = content.rstrip("\n") + "\n"

        return content, limpezas

    # ── helpers ──────────────────────────────────────────────────────────────

    def _fix_multiple_spaces(self, content: str) -> Tuple[str, int]:
        """Remove espaços duplos/triplos, preservando blocos de código."""
        parts = re.split(r"(```[\s\S]*?```|`[^`]+`)", content)
        total = 0
        result = []
        for i, part in enumerate(parts):
            if i % 2 == 0:  # fora de código
                novo, n = re.subn(r" {2,}", " ", part)
                result.append(novo)
                total += n
            else:
                result.append(part)
        return "".join(result), total

    def _fix_blank_lines(self, lines: List[str]) -> Tuple[List[str], int]:
        """Reduz sequências de mais de 2 linhas em branco para exatamente 2."""
        result, consecutive, reductions = [], 0, 0
        for line in lines:
            if line.strip() == "":
                consecutive += 1
                if consecutive <= 2:
                    result.append(line)
                else:
                    reductions += 1
            else:
                consecutive = 0
                result.append(line)
        return result, reductions

    def _fix_space_before_punctuation(self, content: str) -> Tuple[str, int]:
        """Remove espaço indevido antes de ., , ; : em texto corrido."""
        content, n1 = re.subn(r" +([,;:])", r"\1", content)
        # Para ponto final: apenas quando seguido de espaço ou fim de linha
        content, n2 = re.subn(r" +(\.(?=\s|$))", r"\1", content)
        return content, n1 + n2

    def _fix_headers(self, content: str) -> Tuple[str, int]:
        """Garante espaço entre # e o título: ##Titulo → ## Titulo."""
        return re.subn(r"^(#{1,6})([^#\s])", r"\1 \2", content, flags=re.MULTILINE)

    def _fix_bold_italic_spaces(self, content: str) -> Tuple[str, int]:
        """Remove espaços internos em **texto** e *texto*."""
        content, n1 = re.subn(r"\*\*\s+(.+?)\s+\*\*", r"**\1**", content)
        content, n2 = re.subn(r"\*\s+(.+?)\s+\*", r"*\1*", content)
        return content, n1 + n2


# ─────────────────────────────────────────────────────────────────────────────
# ÁREAS JURÍDICAS
# ─────────────────────────────────────────────────────────────────────────────
AREAS = {
    "direito_tributario": {
        "titulo": "Direito Tributário",
        "headers": ["DIREITO TRIBUTARIO", "TRIBUTARIO", "DIREITO TRIBUTÁRIO"],
        "keywords": ["icms", "iptu", "iss", "ipva", "ipi", "ir", "cofins", "pis",
                     "csll", "ctn", "tributario", "tributário", "imposto", "tributo",
                     "fisco", "contribuinte", "lançamento", "obrigação tributária"],
    },
    "direito_administrativo": {
        "titulo": "Direito Administrativo",
        "headers": ["DIREITO ADMINISTRATIVO", "ADMINISTRATIVO"],
        "keywords": ["licitacao", "licitação", "servidor publico", "servidor público",
                     "improbidade", "concurso", "autarquia", "fundação pública",
                     "ato administrativo", "poder de polícia", "administração pública",
                     "lei 8112", "lei 8666", "lei 14133"],
    },
    "direito_civil": {
        "titulo": "Direito Civil",
        "headers": ["DIREITO CIVIL", "CIVIL"],
        "keywords": ["codigo civil", "código civil", "contratos", "obrigacoes",
                     "obrigações", "familia", "família", "propriedade", "posse",
                     "usucapião", "sucessões", "responsabilidade civil", "dano moral"],
    },
    "direito_penal": {
        "titulo": "Direito Penal",
        "headers": ["DIREITO PENAL", "PENAL"],
        "keywords": ["codigo penal", "código penal", "crime", "pena", "homicidio",
                     "homicídio", "furto", "roubo", "estelionato", "peculato",
                     "corrupção", "lavagem de dinheiro", "tráfico", "reclusão"],
    },
    "processual": {
        "titulo": "Direito Processual",
        "headers": ["PROCESSO", "PROCESSUAL", "CPC", "CPP"],
        "keywords": ["recurso", "apelacao", "apelação", "embargos", "sentenca",
                     "sentença", "liminar", "tutela", "mandado de segurança",
                     "habeas corpus", "agravo", "cpc", "cpp", "prazo processual"],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# PROCESSADOR DE QUESTÕES
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Questao:
    numero: str
    texto: str
    area: str = ""


class QuestionProcessor:
    """Extrai e classifica questões jurídicas de arquivos Markdown."""

    QUESTION_PATTERN = re.compile(
        r"(?:QUESTAO|Quest[^\d]+|QUESTÃO|Item|item|^\s*\d+[\.\)\-])\s*(\d+)",
        re.MULTILINE | re.IGNORECASE,
    )

    def __init__(self, areas: Dict[str, dict] = None):
        self.areas = areas or AREAS

    def extract(self, content: str) -> List[str]:
        """Extrai blocos de texto de cada questão."""
        content = re.sub(r"\r\n", "\n", content)
        content = re.sub(r"\n{3,}", "\n\n", content)
        questions = []
        matches = list(self.QUESTION_PATTERN.finditer(content))
        for i, match in enumerate(matches):
            start_idx = max(0, match.start() - 30)
            end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            q_text = content[start_idx:end_idx].strip()
            q_text = self._clean_header(q_text)
            if 50 < len(q_text) < 10000:
                questions.append(q_text)
        return questions

    def classify(self, questions: List[str]) -> Dict[str, List[Questao]]:
        """Classifica questões por área jurídica usando score de keywords."""
        collected: Dict[str, List[Questao]] = {k: [] for k in self.areas}
        for q_text in questions:
            q_lower = q_text.lower()
            best_score, best_area = 0, None
            for area_key, config in self.areas.items():
                score = sum(2 for kw in config["keywords"] if kw.lower() in q_lower)
                score += sum(10 for h in config["headers"] if h.lower() in q_lower)
                if score > best_score:
                    best_score, best_area = score, area_key
            if best_area and best_score >= 3:
                m = self.QUESTION_PATTERN.search(q_text)
                num = m.group(1) if m else "?"
                collected[best_area].append(Questao(num, q_text, best_area))
        return collected

    def _clean_header(self, text: str) -> str:
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if re.search(r"^##\s*Quest", line, re.IGNORECASE):
                return "\n".join(lines[i:]).strip()
        return text.strip()


# ─────────────────────────────────────────────────────────────────────────────
# ORQUESTRADOR DO PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
class PipelineOrchestrator:
    """Orquestra o pipeline completo: encoding → limpeza → extração → relatório."""

    def __init__(self, base_dir: str, dry_run: bool = False, sufixo: str = "_limpo"):
        self.base_dir = Path(base_dir)
        self.dry_run = dry_run
        self.sufixo = sufixo
        self.cleaner = MarkdownCleaner()
        self.question_processor = QuestionProcessor()
        self.results: List[CleaningResult] = []

    def run(self, extrair_questoes: bool = True) -> List[CleaningResult]:
        """Executa pipeline completo."""
        print(f"\n{'='*60}")
        print(f"  MARKDOWN CLEANER PIPELINE")
        print(f"  Diretório: {self.base_dir}")
        print(f"  Modo: {'DRY-RUN (sem salvar)' if self.dry_run else 'PRODUÇÃO'}")
        print(f"{'='*60}\n")

        md_files = self._coletar_arquivos()
        if not md_files:
            print("  [AVISO] Nenhum arquivo .md encontrado.")
            return []

        print(f"  [INFO] {len(md_files)} arquivo(s) encontrado(s)\n")

        for filepath in md_files:
            result = self._processar_arquivo(filepath)
            self.results.append(result)

        if extrair_questoes:
            self._extrair_questoes(md_files)

        self._exibir_relatorio()
        return self.results

    def salvar_relatorio_json(self, output_path: str):
        """Salva relatório de limpeza em JSON."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "diretorio": str(self.base_dir),
            "dry_run": self.dry_run,
            "arquivos": [asdict(r) for r in self.results],
        }
        Path(output_path).write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"\n  [OK] Relatório JSON salvo em: {output_path}")

    # ── privados ─────────────────────────────────────────────────────────────

    def _coletar_arquivos(self) -> List[Path]:
        """Coleta .md excluindo arquivos gerados pelo próprio pipeline."""
        return [
            f for f in self.base_dir.glob("*.md")
            if not f.name.startswith("questoes_")
            and not f.name.startswith("relatorio")
            and not f.name.endswith(f"{self.sufixo}.md")
        ]

    def _processar_arquivo(self, filepath: Path) -> CleaningResult:
        result = CleaningResult(arquivo=filepath.name)
        print(f"  [ARQ] {filepath.name}")

        try:
            encoding, content = EncodingDetector.detect_and_correct(str(filepath))
            result.encoding_original = encoding
            result.chars_antes = len(content)
            result.linhas_antes = content.count("\n")

            if encoding not in ("utf-8", "utf-8-sig"):
                result.limpezas.append(f"Encoding corrigido: {encoding} → utf-8")
                print(f"        [ENC] {encoding} → utf-8")

            cleaned, limpezas = self.cleaner.clean(content)
            result.limpezas.extend(limpezas)
            result.chars_depois = len(cleaned)
            result.linhas_depois = cleaned.count("\n")

            for l in limpezas:
                print(f"        [FIX] {l}")

            if not self.dry_run and cleaned.strip():
                output_path = filepath.parent / f"{filepath.stem}{self.sufixo}.md"
                output_path.write_text(cleaned, encoding="utf-8")
                result.salvo = True
                print(f"        [OK] → {output_path.name}")
            elif self.dry_run:
                print(f"        [DRY] Não salvo (dry-run)")

        except Exception as e:
            result.erro = str(e)
            print(f"        [ERRO] {e}")

        return result

    def _extrair_questoes(self, md_files: List[Path]):
        print(f"\n{'='*60}")
        print(f"  FASE 2: EXTRAÇÃO DE QUESTÕES JURÍDICAS")
        print(f"{'='*60}\n")

        # Limpa arquivos de questões anteriores
        if not self.dry_run:
            for f in self.base_dir.glob("questoes_*.md"):
                f.unlink()

        global_stats: Dict[str, int] = {k: 0 for k in AREAS}

        for filepath in md_files:
            print(f"  [ARQ] {filepath.name}")
            try:
                _, content = EncodingDetector.detect_and_correct(str(filepath))
            except Exception as e:
                print(f"        [ERRO] {e}")
                continue

            questions = self.question_processor.extract(content)
            if not questions:
                print(f"        [INFO] Nenhuma questão encontrada")
                continue

            print(f"        [QTD] {len(questions)} questão(ões)")
            classified = self.question_processor.classify(questions)

            for area_key, questoes in classified.items():
                if not questoes:
                    continue
                output_path = self.base_dir / f"questoes_{area_key}.md"
                mode = "a" if output_path.exists() else "w"
                if not self.dry_run:
                    with open(output_path, mode, encoding="utf-8") as f:
                        if mode == "w":
                            f.write(f"# {AREAS[area_key]['titulo']}\n\n")
                            f.write("> Extraídas automaticamente pelo Markdown Cleaner\n\n---\n\n")
                        f.write(f"## {filepath.name}\n\n")
                        for q in questoes:
                            f.write(f"### Questão {q.numero}\n\n{q.texto}\n\n---\n\n")
                global_stats[area_key] += len(questoes)
                print(f"        [SALVO] {len(questoes)}x em questoes_{area_key}.md")

        print(f"\n  Distribuição por área:")
        for area_key, total in global_stats.items():
            if total > 0:
                print(f"    {AREAS[area_key]['titulo']:<35} {total:>4} questão(ões)")

    def _exibir_relatorio(self):
        print(f"\n{'='*60}")
        print(f"  RELATÓRIO FINAL")
        print(f"{'='*60}")
        total = len(self.results)
        com_erro = sum(1 for r in self.results if r.erro)
        salvos = sum(1 for r in self.results if r.salvo)
        total_limpezas = sum(len(r.limpezas) for r in self.results)
        chars_economizados = sum(r.chars_antes - r.chars_depois for r in self.results if not r.erro)

        print(f"  Arquivos processados : {total}")
        print(f"  Arquivos salvos      : {salvos}")
        print(f"  Erros                : {com_erro}")
        print(f"  Total de limpezas    : {total_limpezas}")
        print(f"  Chars removidos      : {chars_economizados:,}")
        print(f"{'='*60}\n")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="md_cleaner.py",
        description="Pipeline de limpeza, encoding e extração jurídica para arquivos Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Limpar todos os .md de uma pasta
  python md_cleaner.py /minha/pasta

  # Limpar sem salvar (preview)
  python md_cleaner.py /minha/pasta --dry-run

  # Limpar sem extrair questões
  python md_cleaner.py /minha/pasta --sem-questoes

  # Gerar relatório JSON
  python md_cleaner.py /minha/pasta --relatorio saida.json

  # Sufixo personalizado para arquivos limpos
  python md_cleaner.py /minha/pasta --sufixo _normalizado
        """,
    )
    parser.add_argument("diretorio", nargs="?", default=".", help="Diretório com arquivos .md")
    parser.add_argument("--dry-run", action="store_true", help="Preview sem salvar arquivos")
    parser.add_argument("--sem-questoes", action="store_true", help="Pula extração de questões jurídicas")
    parser.add_argument("--relatorio", metavar="ARQUIVO", help="Salva relatório JSON em arquivo")
    parser.add_argument("--sufixo", default="_limpo", help="Sufixo dos arquivos de saída (padrão: _limpo)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Saída detalhada")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    base_dir = Path(args.diretorio).resolve()
    if not base_dir.exists():
        print(f"[ERRO] Diretório não encontrado: {base_dir}")
        sys.exit(1)

    orchestrator = PipelineOrchestrator(base_dir, dry_run=args.dry_run, sufixo=args.sufixo)
    orchestrator.run(extrair_questoes=not args.sem_questoes)

    if args.relatorio:
        orchestrator.salvar_relatorio_json(args.relatorio)


if __name__ == "__main__":
    main()
