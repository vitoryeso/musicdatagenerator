from __future__ import annotations

from dataclasses import dataclass
from typing import List
import math


@dataclass
class LoopParams:
	duration_seconds: float = 2.0
	fps: int = 60
	radius: float = 100.0
	center_x: float = 0.0
	center_y: float = 0.0
	phase0_rad: float = 0.0
	elasticidade: float = 0.5
	fluidez: float = 0.5
	inercia: float = 0.5
	amolecimento: float = 0.2
	loops: int = 1
	pre_roll_loops: int = 3


@dataclass
class LoopFrame:
	index: int
	time: float
	x: float
	y: float
	travel_angle: float
	orientation: float
	scale_tangent: float
	scale_normal: float


def generate_loop(params: LoopParams) -> List[LoopFrame]:
	"""Gera uma lista de frames descrevendo um loop de movimento circular.

	O movimento ao longo do ângulo é modelado como um sistema de 2ª ordem
	que rastreia um alvo (ângulo linear no tempo), com parâmetros de
	elasticidade (rigidez efetiva) e fluidez (amortecimento). A orientação
	do objeto (heading) persegue a tangente com momento de inércia
	(segunda ordem também). O amolecimento aplica squash & stretch baseado
	na velocidade tangencial.
	"""

	def clamp(value: float, lo: float, hi: float) -> float:
		return lo if value < lo else hi if value > hi else value

	# Parâmetros derivados básicos
	loops = max(1, int(params.loops))
	fps = max(1, int(params.fps))
	N = max(1, int(round(params.duration_seconds * fps)))
	dt = 1.0 / fps
	T = N * dt

	# Alvo: ângulo avança linearmente em função do tempo
	omega_target = (2.0 * math.pi * loops) / T

	# Mapeamentos de parâmetros intuitivos -> parâmetros do sistema de 2ª ordem
	# Fluidez controla o amortecimento (zeta). 0 = sem amortecimento; 1 = super amortecido
	zeta_pos = clamp(0.05 + 1.95 * params.fluidez, 0.05, 2.5)
	# Elasticidade controla quão "nervoso"/responsivo é o sistema (frequência natural)
	omega_n_pos = omega_target * (0.5 + 3.0 * clamp(params.elasticidade, 0.0, 1.0))

	# Orientação com inércia: frequência natural menor quando inércia é maior
	zeta_orient = clamp(0.05 + 1.95 * params.fluidez, 0.05, 2.5)
	omega_n_orient = omega_target * (2.0 - 1.8 * clamp(params.inercia, 0.0, 1.0))
	omega_n_orient = clamp(omega_n_orient, omega_target * 0.15, omega_target * 4.0)

	# Pré-roll para atingir regime permanente e garantir loop suave
	pre_loops = max(0, int(params.pre_roll_loops))
	pre_duration = (pre_loops / float(loops)) * T
	pre_steps = int(round(pre_duration / dt))

	# Estados: ângulo e derivadas (posição, velocidade), orientação idem
	theta = params.phase0_rad
	theta_d = omega_target
	psi = theta + math.pi * 0.5  # orientação visada: tangente adiantada de 90°
	psi_d = theta_d

	def step_once(t: float) -> None:
		nonlocal theta, theta_d, psi, psi_d
		# Alvos instantâneos
		theta_target = params.phase0_rad + omega_target * t
		theta_target_d = omega_target

		# Dinâmica de 2ª ordem (rastreador) para o ângulo na circunferência
		# theta_dd = ω_n^2 (θ* - θ) + 2 ζ ω_n (θ'* - θ')
		theta_dd = (omega_n_pos * omega_n_pos) * (theta_target - theta) \
			+ 2.0 * zeta_pos * omega_n_pos * (theta_target_d - theta_d)
		theta_d += theta_dd * dt
		theta += theta_d * dt

		# Orientação persegue a tangente (ψ* = θ + π/2) com inércia
		psi_target = theta + math.pi * 0.5
		psi_target_d = theta_d
		psi_dd = (omega_n_orient * omega_n_orient) * (psi_target - psi) \
			+ 2.0 * zeta_orient * omega_n_orient * (psi_target_d - psi_d)
		psi_d += psi_dd * dt
		psi += psi_d * dt

	# Pré-aquecimento
	if pre_steps > 0:
		# Simula de t = -pre_duration até 0 (não grava frames)
		t = -pre_duration
		for _ in range(pre_steps):
			step_once(t)
			t += dt

	frames: List[LoopFrame] = []
	# Simulação principal para 1 período (N frames, sem repetir o último)
	t = 0.0
	for i in range(N):
		# Avança estado antes de amostrar posição, para evitar fase em t=0 com pré-roll
		step_once(t)
		# Posição na circunferência
		x = params.center_x + params.radius * math.cos(theta)
		y = params.center_y + params.radius * math.sin(theta)

		# Squash & stretch baseado na velocidade tangencial relativa
		v = abs(params.radius * theta_d)
		v_mean = abs(params.radius * omega_target) + 1e-8
		norm_speed = clamp((v - v_mean) / v_mean, -1.0, 1.0)
		stretch_gain = 0.6 * clamp(params.amolecimento, 0.0, 1.0)
		stretch = clamp(stretch_gain * norm_speed, -0.9, 1.5)
		scale_tangent = clamp(1.0 + stretch, 0.4, 2.5)
		scale_normal = clamp(1.0 / scale_tangent, 0.4, 2.5)

		frames.append(
			LoopFrame(
				index=i,
				time=t,
				x=x,
				y=y,
				travel_angle=theta,
				orientation=psi,
				scale_tangent=scale_tangent,
				scale_normal=scale_normal,
			)
		)
		t += dt

	return frames

