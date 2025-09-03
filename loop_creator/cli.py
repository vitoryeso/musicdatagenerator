from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .generator import LoopParams, generate_loop


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Gerar loop circular com mola/inércia")
	parser.add_argument("--duration", type=float, default=2.0, help="Duração em segundos")
	parser.add_argument("--fps", type=int, default=60, help="Frames por segundo")
	parser.add_argument("--radius", type=float, default=100.0, help="Raio do caminho circular")
	parser.add_argument("--center-x", type=float, default=0.0)
	parser.add_argument("--center-y", type=float, default=0.0)
	parser.add_argument("--phase0", type=float, default=0.0, help="Fase inicial (rad)")
	parser.add_argument("--elasticidade", type=float, default=0.5)
	parser.add_argument("--fluidez", type=float, default=0.5)
	parser.add_argument("--inercia", type=float, default=0.5)
	parser.add_argument("--amolecimento", type=float, default=0.2)
	parser.add_argument("--loops", type=int, default=1)
	parser.add_argument("--pre-roll-loops", type=int, default=3)
	parser.add_argument("--out", type=str, default="-", help="Arquivo de saída ou '-' para stdout")
	return parser


def main(argv: list[str] | None = None) -> int:
	parser = build_parser()
	args = parser.parse_args(argv)
	params = LoopParams(
		duration_seconds=args.duration,
		fps=args.fps,
		radius=args.radius,
		center_x=args.center_x,
		center_y=args.center_y,
		phase0_rad=args.phase0,
		elasticidade=args.elasticidade,
		fluidez=args.fluidez,
		inercia=args.inercia,
		amolecimento=args.amolecimento,
		loops=args.loops,
		pre_roll_loops=args.pre_roll_loops,
	)
	frames = generate_loop(params)
	data = {
		"params": params.__dict__,
		"frames": [asdict(f) for f in frames],
	}
	text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
	if args.out == "-":
		print(text)
	else:
		with open(args.out, "w", encoding="utf-8") as f:
			f.write(text)
	return 0


if __name__ == "__main__":
	exit(main())

