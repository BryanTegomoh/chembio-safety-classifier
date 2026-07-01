#!/usr/bin/env python3
"""Validate safe example labels against the reference classifier."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from chembio_classifier import classify_text  # noqa: E402


EXAMPLES = ROOT / "examples" / "safe_eval_examples.jsonl"


def main() -> int:
    failures: list[str] = []
    for line_no, line in enumerate(EXAMPLES.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        expected = item["expected"]["risk_level"]
        if "prompt" not in item:
            continue
        result = classify_text(item["prompt"], request_id=item["id"])
        if result.risk_level.value != expected:
            failures.append(
                f"line {line_no}: expected {expected}, got {result.risk_level.value}"
            )

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"validated {EXAMPLES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

