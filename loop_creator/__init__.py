"""loop_creator

Pequena biblioteca para gerar loops de movimento circular com elasticidade,
amortecimento (fluidez), inércia rotacional e amolecimento (squash & stretch).
"""

from .generator import LoopParams, LoopFrame, generate_loop

__all__ = [
	"LoopParams",
	"LoopFrame",
	"generate_loop",
]

__version__ = "0.1.0"

