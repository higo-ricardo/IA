#!/usr/bin/env python3
"""
Markdown Validator — Validação de consistência de numerais em documentos Markdown.

Verifica se súmulas, artigos, parágrafos, incisos e capítulos
listados no sumário/texto estão devidamente presentes nas seções.

Extraído e aprimorado de corrigir_encoding.py.
"""

import argparse
import re
import sys
import json
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

# Importa EncodingDetector do cleaner (mesmo pacote)
try:
    from md_cleaner import EncodingDetector
except ImportError:
    # Fallback standalone
    class EncodingDetector:
        ENCODINGS_TO_TRY = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

        @classmethod
        def detect_and_correct(cls, filepath: str) -> Tuple[str, str]:
            for enc in cls.ENCODINGS_TO_TRY:
                try:
                    with open(filepath, "r", encoding=enc) as f:
                        return enc, f.read()
                except (UnicodeDecodeError, UnicodeError):
                    continue
            with open(filepath, "rb") as f:
                return "utf-8 (substituição)", f.read().decode("utf-8", errors="replace")


logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DE PADRÕES
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class PatternConfig:
    label: str
    pattern: str
    section_level: int = 2
    enabled: bool = True
    case_sensitive: bool = False


DEFAULT_PATTERNS: Dict[str, PatternConfig] = {
    "sumulas": PatternConfig(
        label="Súmulas",
        pattern=r"S[úu]mula\s+(\d+)",
        section_level=2,
    ),
    "artigos": PatternConfig(
        label="Artigos",
        pattern=r"Art\.?\s*(\d+)",
        section_level=2,
    ),
    "paragrafos": PatternConfig(
        label="Parágrafos",
        pattern=r"(?:§\s*|Par[áa]grafo\s+)(?:[úu]nico|[\dºª]+)",
        section_level=2,
    ),
    "incisos": PatternConfig(
        label="Incisos",
        pattern=r"Inciso\s+([IVXLCM]+)",
        section_level=3,
    ),
    "capitulos": PatternConfig(
        label="Capítulos",
        pattern=r"CAP[IÍ]TULO\s+([IVXLCM\d]+)",
        section_level=1,
        case_sensitive=True,
    ),
    "normas": PatternConfig(
        label="Normas",
        pattern=r"(?:Lei|Decreto|Portaria|Instrução Normativa)\s+(?:n\.?\s*)?(\d+(?:\.\d{3})*(?:\/\d{4})?)",
        section_level=2,
    ),
    "questoes": PatternConfig(
        label="Questões",
        pattern=r"Quest[ãa]o\s+(\d+)",
        section_level=2,
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# VALIDADOR
# ─────────────────────────────────────────────────────────────────────────────
class MarkdownValidator:
    """Valida consistência de numerais em documentos Markdown."""

    def __init__(self, patterns: Dict[str, PatternConfig] = None):
        self.patterns = patterns or DEFAULT_PATTERNS

    def validate_file(
        self,
        filepath: str,
        pattern_key: Optional[str] = None,
        fix_encoding: bool = True,
    ) -> Dict:
        """Valida um arquivo e retorna dicionário com resultado."""
        if fix_encoding:
            encoding, content = EncodingDetector.detect_and_correct(filepath)
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            encoding = "utf-8"

        patterns_to_check = (
            [(pattern_key, self.patterns[pattern_key])]
            if pattern_key and pattern_key in self.patterns
            else [(k, v) for k, v in self.patterns.items() if v.enabled]
        )

        results = {}
        all_ok = True

        for key, cfg in patterns_to_check:
            flags = 0 if cfg.case_sensitive else re.IGNORECASE
            all_matches = re.findall(cfg.pattern, content, flags)

            if not all_matches:
                continue  # padrão não encontrado no arquivo, pula

            section_marker = "#" * cfg.section_level
            sections = re.split(
                rf"(?m)^\s*{re.escape(section_marker)}\s+.*$", content
            )
            section_matches = []
            for sec in sections:
                if sec.strip():
                    section_matches.extend(re.findall(cfg.pattern, sec, flags))

            ok = len(all_matches) == len(section_matches)
            all_ok = all_ok and ok

            results[key] = {
                "label": cfg.label,
                "total": len(all_matches),
                "em_secoes": len(section_matches),
                "status": "OK" if ok else "INCONSISTENTE",
                "amostra": list(all_matches[:5]),
            }

            if not ok:
                logger.warning(
                    f"{filepath}: {cfg.label} — {len(all_matches)} no total, "
                    f"{len(section_matches)} em seções"
                )

        return {
            "arquivo": filepath,
            "encoding": encoding,
            "timestamp": datetime.now().isoformat(),
            "status": "OK" if all_ok else "INCONSISTENTE",
            "padroes": results,
        }

    def auto_discover(self, directory: str = ".", recursive: bool = False) -> List[str]:
        path = Path(directory)
        files = list(path.rglob("*.md")) if recursive else list(path.glob("*.md"))
        return [str(f) for f in files if not f.name.startswith(".")]

    def generate_report(self, results: List[Dict], fmt: str = "text") -> str:
        if fmt == "json":
            return json.dumps(results, indent=2, ensure_ascii=False)

        lines = [
            "=" * 65,
            "RELATÓRIO DE VALIDAÇÃO — DOCUMENTOS MARKDOWN",
            f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 65,
        ]

        ok_count = sum(1 for r in results if r.get("status") == "OK")

        for r in results:
            lines.append(f"\n[ARQUIVO] {r['arquivo']}")
            lines.append(f"   Encoding  : {r['encoding']}")
            lines.append(f"   Status    : {r['status']}")

            for key, pat in r.get("padroes", {}).items():
                icon = "[OK]" if pat["status"] == "OK" else "[!!]"
                lines.append(
                    f"   {icon} {pat['label']:<20} "
                    f"total={pat['total']}  em_seções={pat['em_secoes']}"
                )
                if pat["amostra"]:
                    lines.append(f"       Amostra: {', '.join(str(x) for x in pat['amostra'])}")

        lines.extend([
            "\n" + "=" * 65,
            f"RESUMO: {ok_count}/{len(results)} arquivo(s) consistente(s)",
            "=" * 65,
        ])
        return "\n".join(lines)

    def fix_file(self, filepath: str) -> bool:
        """Reescreve arquivo com encoding corrigido."""
        try:
            _, content = EncodingDetector.detect_and_correct(filepath)
            Path(filepath).write_text(content, encoding="utf-8")
            logger.info(f"Corrigido: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Erro ao corrigir {filepath}: {e}")
            return False


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="md_validator.py",
        description="Valida consistência de numerais em documentos Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python md_validator.py --auto
  python md_validator.py --auto --recursive
  python md_validator.py --pattern sumulas arquivo.md
  python md_validator.py --auto --format json -o relatorio.json
  python md_validator.py --fix arquivo.md
  python md_validator.py --listar-padroes
        """,
    )

    parser.add_argument("files", nargs="*", help="Arquivo(s) Markdown para validar")
    parser.add_argument("-a", "--auto", action="store_true", help="Auto-detectar .md no diretório")
    parser.add_argument("-r", "--recursive", action="store_true", help="Busca recursiva (requer --auto)")
    parser.add_argument(
        "-p", "--pattern",
        choices=list(DEFAULT_PATTERNS.keys()),
        help="Padrão específico para verificar",
    )
    parser.add_argument("-f", "--fix", action="store_true", help="Corrige encoding dos arquivos")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("-o", "--output", metavar="ARQUIVO", help="Salva relatório em arquivo")
    parser.add_argument("--listar-padroes", action="store_true", help="Lista padrões disponíveis")
    parser.add_argument("--section-level", type=int, choices=[1, 2, 3, 4], help="Nível de seção")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.listar_padroes:
        print("\nPadrões disponíveis:")
        for key, cfg in DEFAULT_PATTERNS.items():
            print(f"  {key:<20} {cfg.label}")
        return 0

    if not args.auto and not args.files:
        parser.error("Especifique arquivos ou use --auto")

    validator = MarkdownValidator()

    # Substitui section_level se solicitado
    if args.section_level and args.pattern:
        validator.patterns[args.pattern].section_level = args.section_level

    files = []
    if args.auto:
        files.extend(validator.auto_discover(".", args.recursive))
    files.extend(args.files)
    files = list(dict.fromkeys(files))

    if not files:
        logger.error("Nenhum arquivo encontrado.")
        return 1

    logger.info(f"Validando {len(files)} arquivo(s)...")

    results = []
    for filepath in files:
        if not Path(filepath).exists():
            logger.warning(f"Não encontrado: {filepath}")
            continue
        try:
            result = validator.validate_file(
                filepath,
                pattern_key=args.pattern,
                fix_encoding=args.fix,
            )
            results.append(result)
        except Exception as e:
            logger.error(f"Erro em {filepath}: {e}")

    if args.fix:
        for filepath in files:
            if Path(filepath).exists():
                validator.fix_file(filepath)

    report = validator.generate_report(results, args.format)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        logger.info(f"Relatório salvo: {args.output}")
    else:
        print(report)

    return 0 if all(r.get("status") == "OK" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
