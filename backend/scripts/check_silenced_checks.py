from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CHECKS = [
    (re.compile(r"\|\|\s*true\b"), "comando silenciado con '|| true'"),
    (
        re.compile(r"continue-on-error\s*:\s*true\b", re.IGNORECASE),
        "step de GitHub Actions permitido a fallar",
    ),
    (re.compile(r"pytest\.mark\.skip(?:if)?\b"), "test de pytest marcado como skip"),
    (re.compile(r"pytest\.skip\s*\("), "test de pytest saltado en ejecución"),
    (
        re.compile(r"unittest\.skip(?:If|Unless)?\b"),
        "test de unittest marcado como skip",
    ),
    (re.compile(r"@skip(?:If|Unless)?\b"), "decorador de test saltado"),
]

TARGETS = [
    ROOT / ".github",
    ROOT / "backend" / "tests",
]


def iter_files(path: Path):
    if not path.exists():
        return
    if path.is_file():
        yield path
        return
    for candidate in path.rglob("*"):
        if candidate.is_file() and candidate.suffix in {".yml", ".yaml", ".py"}:
            yield candidate


def main() -> int:
    violations: list[tuple[Path, int, str, str]] = []
    for target in TARGETS:
        for file in iter_files(target):
            try:
                lines = file.read_text(encoding="utf-8").splitlines()
            except UnicodeDecodeError:
                continue
            for number, line in enumerate(lines, 1):
                for pattern, reason in CHECKS:
                    if pattern.search(line):
                        violations.append(
                            (file.relative_to(ROOT), number, reason, line.strip())
                        )

    if violations:
        print("Se encontraron checks silenciados:")
        for file, number, reason, line in violations:
            print(f"  {file}:{number}: {reason}")
            print(f"    {line}")
        return 1

    print("OK: no se encontraron checks silenciados en .github ni backend/tests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
