#!/usr/bin/env python3
"""
Simulador de Movimento Circular com Loops
Incorpora leis de elasticidade, momento de inércia, fluidez e amortecimento
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button
import math

class CircularMotionSimulator:
    def __init__(self):
        # Parâmetros físicos
        self.mass = 1.0  # massa do objeto
        self.radius = 2.0  # raio base do movimento
        self.initial_velocity = 5.0  # velocidade inicial
        
        # Parâmetros ajustáveis
        self.elasticity = 0.8  # coeficiente de elasticidade (0-1)
        self.damping = 0.02  # coeficiente de amortecimento
        self.fluidity = 0.5  # fluidez do movimento (0-1)
        self.moment_of_inertia = 0.5  # momento de inércia
        
        # Estado do sistema
        self.angle = 0.0
        self.angular_velocity = self.initial_velocity / self.radius
        self.angular_acceleration = 0.0
        self.current_radius = self.radius
        self.radial_velocity = 0.0
        
        # Histórico de posições para criar loops
        self.history_x = []
        self.history_y = []
        self.max_history = 1000
        
        # Configuração da visualização
        self.setup_plot()
        
    def setup_plot(self):
        """Configura a interface gráfica"""
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        plt.subplots_adjust(bottom=0.35)
        
        # Configuração do plot principal
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title('Simulador de Movimento Circular com Loops', fontsize=14, fontweight='bold')
        
        # Elementos visuais
        self.trail_line, = self.ax.plot([], [], 'b-', alpha=0.6, linewidth=1, label='Trajetória')
        self.object_point, = self.ax.plot([], [], 'ro', markersize=8, label='Objeto')
        self.velocity_vector, = self.ax.plot([], [], 'g-', linewidth=2, alpha=0.7, label='Velocidade')
        self.acceleration_vector, = self.ax.plot([], [], 'r-', linewidth=2, alpha=0.7, label='Aceleração')
        
        self.ax.legend(loc='upper right')
        
        # Sliders para controle dos parâmetros
        self.create_sliders()
        
        # Botões de controle
        self.create_buttons()
        
        # Texto para mostrar informações
        self.info_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                     verticalalignment='top', fontsize=10,
                                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
    def create_sliders(self):
        """Cria os sliders para controle dos parâmetros"""
        # Posições dos sliders
        slider_height = 0.03
        slider_spacing = 0.04
        slider_left = 0.1
        slider_width = 0.35
        
        # Elasticidade
        ax_elasticity = plt.axes([slider_left, 0.25, slider_width, slider_height])
        self.slider_elasticity = Slider(ax_elasticity, 'Elasticidade', 0.1, 1.0, 
                                       valinit=self.elasticity, valfmt='%.2f')
        
        # Amortecimento
        ax_damping = plt.axes([slider_left, 0.25 - slider_spacing, slider_width, slider_height])
        self.slider_damping = Slider(ax_damping, 'Amortecimento', 0.0, 0.1, 
                                    valinit=self.damping, valfmt='%.3f')
        
        # Fluidez
        ax_fluidity = plt.axes([slider_left, 0.25 - 2*slider_spacing, slider_width, slider_height])
        self.slider_fluidity = Slider(ax_fluidity, 'Fluidez', 0.1, 1.0, 
                                     valinit=self.fluidity, valfmt='%.2f')
        
        # Momento de Inércia
        ax_inertia = plt.axes([slider_left, 0.25 - 3*slider_spacing, slider_width, slider_height])
        self.slider_inertia = Slider(ax_inertia, 'Momento Inércia', 0.1, 2.0, 
                                    valinit=self.moment_of_inertia, valfmt='%.2f')
        
        # Velocidade Inicial
        ax_velocity = plt.axes([slider_left + slider_width + 0.1, 0.25, slider_width, slider_height])
        self.slider_velocity = Slider(ax_velocity, 'Velocidade', 1.0, 10.0, 
                                     valinit=self.initial_velocity, valfmt='%.1f')
        
        # Raio Base
        ax_radius = plt.axes([slider_left + slider_width + 0.1, 0.25 - slider_spacing, slider_width, slider_height])
        self.slider_radius = Slider(ax_radius, 'Raio Base', 0.5, 4.0, 
                                   valinit=self.radius, valfmt='%.1f')
        
        # Conectar eventos dos sliders
        self.slider_elasticity.on_changed(self.update_parameters)
        self.slider_damping.on_changed(self.update_parameters)
        self.slider_fluidity.on_changed(self.update_parameters)
        self.slider_inertia.on_changed(self.update_parameters)
        self.slider_velocity.on_changed(self.update_parameters)
        self.slider_radius.on_changed(self.update_parameters)
        
    def create_buttons(self):
        """Cria botões de controle"""
        # Reset
        ax_reset = plt.axes([0.7, 0.05, 0.1, 0.04])
        self.button_reset = Button(ax_reset, 'Reset')
        self.button_reset.on_clicked(self.reset_simulation)
        
        # Clear Trail
        ax_clear = plt.axes([0.82, 0.05, 0.1, 0.04])
        self.button_clear = Button(ax_clear, 'Limpar')
        self.button_clear.on_clicked(self.clear_trail)
        
    def update_parameters(self, val):
        """Atualiza os parâmetros baseado nos sliders"""
        self.elasticity = self.slider_elasticity.val
        self.damping = self.slider_damping.val
        self.fluidity = self.slider_fluidity.val
        self.moment_of_inertia = self.slider_inertia.val
        self.initial_velocity = self.slider_velocity.val
        self.radius = self.slider_radius.val
        
    def reset_simulation(self, event):
        """Reseta a simulação"""
        self.angle = 0.0
        self.angular_velocity = self.initial_velocity / self.radius
        self.angular_acceleration = 0.0
        self.current_radius = self.radius
        self.radial_velocity = 0.0
        self.history_x.clear()
        self.history_y.clear()
        
    def clear_trail(self, event):
        """Limpa o rastro da trajetória"""
        self.history_x.clear()
        self.history_y.clear()
        
    def calculate_physics(self, dt):
        """Calcula a física do movimento circular com elasticidade e amortecimento"""
        # Força centrípeta baseada na velocidade angular atual
        centripetal_force = self.mass * self.angular_velocity**2 * self.current_radius
        
        # Força elástica - tenta manter o raio base
        elastic_force = -self.elasticity * (self.current_radius - self.radius) * 10
        
        # Força de amortecimento radial
        damping_force = -self.damping * self.radial_velocity * 50
        
        # Força total radial
        total_radial_force = elastic_force + damping_force
        
        # Aceleração radial
        radial_acceleration = total_radial_force / self.mass
        
        # Atualiza velocidade e posição radial
        self.radial_velocity += radial_acceleration * dt
        self.current_radius += self.radial_velocity * dt
        
        # Limita o raio para evitar valores negativos ou muito grandes
        self.current_radius = max(0.1, min(self.current_radius, 8.0))
        
        # Amortecimento angular baseado na fluidez
        angular_damping = (1.0 - self.fluidity) * 0.1
        angular_friction = -angular_damping * self.angular_velocity
        
        # Conservação do momento angular modificada pelo momento de inércia
        # L = I * ω (momento angular)
        # Quando o raio muda, a velocidade angular se ajusta para conservar energia
        base_inertia = self.mass * self.radius**2
        current_inertia = self.mass * self.current_radius**2 * self.moment_of_inertia
        
        # Ajuste da velocidade angular baseado na mudança do momento de inércia
        if current_inertia > 0:
            conservation_factor = base_inertia / current_inertia
            target_angular_velocity = self.initial_velocity / self.radius * conservation_factor * 0.5
            
            # Suaviza a transição da velocidade angular
            velocity_diff = target_angular_velocity - self.angular_velocity
            self.angular_velocity += velocity_diff * self.fluidity * dt * 2
        
        # Aplica amortecimento angular
        self.angular_velocity += angular_friction * dt
        
        # Atualiza o ângulo
        self.angle += self.angular_velocity * dt
        
        # Mantém o ângulo entre 0 e 2π para evitar overflow
        self.angle = self.angle % (2 * math.pi)
        
    def get_position(self):
        """Calcula a posição atual do objeto"""
        x = self.current_radius * math.cos(self.angle)
        y = self.current_radius * math.sin(self.angle)
        return x, y
        
    def get_velocity_vector(self):
        """Calcula o vetor velocidade para visualização"""
        x, y = self.get_position()
        
        # Componente tangencial da velocidade
        vx_tangential = -self.angular_velocity * self.current_radius * math.sin(self.angle)
        vy_tangential = self.angular_velocity * self.current_radius * math.cos(self.angle)
        
        # Componente radial da velocidade
        vx_radial = self.radial_velocity * math.cos(self.angle)
        vy_radial = self.radial_velocity * math.sin(self.angle)
        
        # Velocidade total
        vx_total = vx_tangential + vx_radial
        vy_total = vy_tangential + vy_radial
        
        # Escala o vetor para visualização
        scale = 0.3
        return [x, x + vx_total * scale], [y, y + vy_total * scale]
        
    def get_acceleration_vector(self):
        """Calcula o vetor aceleração para visualização"""
        x, y = self.get_position()
        
        # Aceleração centrípeta
        ax_centripetal = -self.angular_velocity**2 * self.current_radius * math.cos(self.angle)
        ay_centripetal = -self.angular_velocity**2 * self.current_radius * math.sin(self.angle)
        
        # Aceleração radial (elástica + amortecimento)
        elastic_acc = -self.elasticity * (self.current_radius - self.radius) * 10 / self.mass
        damping_acc = -self.damping * self.radial_velocity * 50 / self.mass
        radial_acc = elastic_acc + damping_acc
        
        ax_radial = radial_acc * math.cos(self.angle)
        ay_radial = radial_acc * math.sin(self.angle)
        
        # Aceleração total
        ax_total = ax_centripetal + ax_radial
        ay_total = ay_centripetal + ay_radial
        
        # Escala o vetor para visualização
        scale = 0.1
        return [x, x + ax_total * scale], [y, y + ay_total * scale]
        
    def update_info_text(self):
        """Atualiza o texto informativo"""
        info = f"""Parâmetros Atuais:
Raio: {self.current_radius:.2f}m
Velocidade Angular: {self.angular_velocity:.2f} rad/s
Velocidade Radial: {self.radial_velocity:.2f} m/s
Energia Cinética: {0.5 * self.mass * (self.angular_velocity * self.current_radius)**2:.2f}J
Ângulo: {math.degrees(self.angle):.1f}°"""
        self.info_text.set_text(info)
        
    def animate(self, frame):
        """Função de animação"""
        dt = 0.02  # intervalo de tempo
        
        # Calcula a física
        self.calculate_physics(dt)
        
        # Obtém a posição atual
        x, y = self.get_position()
        
        # Adiciona ao histórico
        self.history_x.append(x)
        self.history_y.append(y)
        
        # Limita o tamanho do histórico
        if len(self.history_x) > self.max_history:
            self.history_x.pop(0)
            self.history_y.pop(0)
        
        # Atualiza os elementos visuais
        self.trail_line.set_data(self.history_x, self.history_y)
        self.object_point.set_data([x], [y])
        
        # Vetores de velocidade e aceleração
        vel_x, vel_y = self.get_velocity_vector()
        self.velocity_vector.set_data(vel_x, vel_y)
        
        acc_x, acc_y = self.get_acceleration_vector()
        self.acceleration_vector.set_data(acc_x, acc_y)
        
        # Atualiza informações
        self.update_info_text()
        
        return self.trail_line, self.object_point, self.velocity_vector, self.acceleration_vector, self.info_text
        
    def run(self):
        """Executa a simulação"""
        # Cria a animação
        self.animation = animation.FuncAnimation(
            self.fig, self.animate, interval=20, blit=False, cache_frame_data=False
        )
        
        plt.show()

def main():
    """Função principal"""
    print("Iniciando Simulador de Movimento Circular com Loops")
    print("=" * 50)
    print("Controles:")
    print("- Use os sliders para ajustar os parâmetros em tempo real")
    print("- Elasticidade: controla a força de restauração do raio")
    print("- Amortecimento: reduz a energia do sistema")
    print("- Fluidez: suaviza as transições de movimento")
    print("- Momento de Inércia: afeta a conservação do momento angular")
    print("- Botão Reset: reinicia a simulação")
    print("- Botão Limpar: limpa o rastro da trajetória")
    print("=" * 50)
    
    simulator = CircularMotionSimulator()
    simulator.run()

if __name__ == "__main__":
    main()