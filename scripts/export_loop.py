#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

# Garante que o diretório raiz do workspace esteja no sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from loop_creator import LoopParams, generate_loop


def main() -> int:
	params = LoopParams(duration_seconds=2.0, fps=60, radius=120.0, elasticidade=0.65, fluidez=0.55, inercia=0.4, amolecimento=0.25, loops=1, pre_roll_loops=3)
	frames = generate_loop(params)
	data = {"params": params.__dict__, "frames": [asdict(f) for f in frames]}
	out = Path(__file__).parent / "loop.json"
	out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
	print(f"Exportado: {out}")
	return 0


if __name__ == "__main__":
	exit(main())

