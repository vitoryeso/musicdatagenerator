import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import tkinter as tk
from tkinter import ttk
import math

class CircularMotionSimulator:
    """
    Simulador de movimento circular com propriedades físicas realistas:
    - Elasticidade
    - Momento de inércia
    - Fluidez
    - Amolecimento
    """
    
    def __init__(self):
        # Parâmetros físicos do objeto
        self.mass = 1.0  # kg
        self.radius = 0.1  # m
        self.moment_of_inertia = 0.5 * self.mass * self.radius**2  # kg⋅m²
        
        # Parâmetros de movimento
        self.angular_velocity = 2.0  # rad/s
        self.angular_acceleration = 0.0  # rad/s²
        self.angle = 0.0  # rad
        
        # Parâmetros de elasticidade
        self.elasticity = 0.8  # coeficiente de restituição (0-1)
        self.spring_constant = 100.0  # N/m
        
        # Parâmetros de fluidez e amolecimento
        self.fluidity = 0.1  # coeficiente de fluidez (0-1)
        self.softening = 0.05  # coeficiente de amolecimento (0-1)
        self.damping = 0.02  # amortecimento
        
        # Posição e velocidade
        self.center_x = 0.0
        self.center_y = 0.0
        self.orbit_radius = 2.0  # raio da órbita circular
        
        # Controle de loops
        self.loop_count = 0
        self.max_loops = 10
        self.loop_duration = 2 * np.pi / self.angular_velocity
        
        # Histórico para visualização
        self.trajectory_x = []
        self.trajectory_y = []
        self.time_history = []
        self.energy_history = []
        
        # Tempo
        self.dt = 0.01  # passo de tempo
        self.time = 0.0
        
    def calculate_moment_of_inertia(self):
        """Calcula o momento de inércia baseado na geometria do objeto"""
        # Para um cilindro sólido: I = 0.5 * m * r²
        return 0.5 * self.mass * self.radius**2
    
    def apply_elastic_force(self, displacement):
        """Aplica força elástica baseada no deslocamento"""
        return -self.spring_constant * displacement
    
    def apply_fluid_damping(self, velocity):
        """Aplica amortecimento fluido"""
        return -self.fluidity * velocity
    
    def apply_softening_effect(self, force):
        """Aplica efeito de amolecimento à força"""
        return force * (1 - self.softening)
    
    def update_physics(self):
        """Atualiza a física do sistema"""
        # Calcular posição atual na órbita
        x = self.center_x + self.orbit_radius * np.cos(self.angle)
        y = self.center_y + self.orbit_radius * np.sin(self.angle)
        
        # Calcular deslocamento do centro (para elasticidade)
        displacement = np.sqrt(x**2 + y**2) - self.orbit_radius
        
        # Aplicar forças
        elastic_force = self.apply_elastic_force(displacement)
        fluid_damping = self.apply_fluid_damping(self.angular_velocity)
        softened_force = self.apply_softening_effect(elastic_force)
        
        # Calcular aceleração angular
        total_torque = softened_force * self.orbit_radius + fluid_damping
        self.angular_acceleration = total_torque / self.moment_of_inertia
        
        # Atualizar velocidade e posição angular
        self.angular_velocity += self.angular_acceleration * self.dt
        self.angular_velocity *= (1 - self.damping)  # amortecimento geral
        
        self.angle += self.angular_velocity * self.dt
        
        # Verificar se completou um loop
        if self.angle >= 2 * np.pi:
            self.angle -= 2 * np.pi
            self.loop_count += 1
        
        # Atualizar tempo
        self.time += self.dt
        
        # Armazenar histórico
        self.trajectory_x.append(x)
        self.trajectory_y.append(y)
        self.time_history.append(self.time)
        
        # Calcular energia total
        kinetic_energy = 0.5 * self.moment_of_inertia * self.angular_velocity**2
        potential_energy = 0.5 * self.spring_constant * displacement**2
        total_energy = kinetic_energy + potential_energy
        self.energy_history.append(total_energy)
        
        # Limitar histórico para performance
        if len(self.trajectory_x) > 1000:
            self.trajectory_x = self.trajectory_x[-500:]
            self.trajectory_y = self.trajectory_y[-500:]
            self.time_history = self.time_history[-500:]
            self.energy_history = self.energy_history[-500:]
    
    def get_current_position(self):
        """Retorna a posição atual do objeto"""
        x = self.center_x + self.orbit_radius * np.cos(self.angle)
        y = self.center_y + self.orbit_radius * np.sin(self.angle)
        return x, y
    
    def reset_simulation(self):
        """Reinicia a simulação"""
        self.angle = 0.0
        self.angular_velocity = 2.0
        self.angular_acceleration = 0.0
        self.loop_count = 0
        self.time = 0.0
        self.trajectory_x = []
        self.trajectory_y = []
        self.time_history = []
        self.energy_history = []
    
    def set_parameters(self, mass=None, radius=None, elasticity=None, 
                      fluidity=None, softening=None, damping=None,
                      angular_velocity=None, orbit_radius=None):
        """Define parâmetros da simulação"""
        if mass is not None:
            self.mass = mass
            self.moment_of_inertia = self.calculate_moment_of_inertia()
        if radius is not None:
            self.radius = radius
            self.moment_of_inertia = self.calculate_moment_of_inertia()
        if elasticity is not None:
            self.elasticity = max(0, min(1, elasticity))
        if fluidity is not None:
            self.fluidity = max(0, min(1, fluidity))
        if softening is not None:
            self.softening = max(0, min(1, softening))
        if damping is not None:
            self.damping = max(0, min(1, damping))
        if angular_velocity is not None:
            self.angular_velocity = angular_velocity
        if orbit_radius is not None:
            self.orbit_radius = orbit_radius


class CircularMotionVisualizer:
    """Interface visual para o simulador de movimento circular"""
    
    def __init__(self):
        self.simulator = CircularMotionSimulator()
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 10))
        self.fig.suptitle('Simulador de Movimento Circular com Propriedades Físicas', fontsize=16)
        
        # Configurar subplots
        self.ax_trajectory = self.axes[0, 0]
        self.ax_energy = self.axes[0, 1]
        self.ax_velocity = self.axes[1, 0]
        self.ax_parameters = self.axes[1, 1]
        
        # Configurar plot de trajetória
        self.ax_trajectory.set_xlim(-3, 3)
        self.ax_trajectory.set_ylim(-3, 3)
        self.ax_trajectory.set_aspect('equal')
        self.ax_trajectory.set_title('Trajetória do Movimento')
        self.ax_trajectory.grid(True, alpha=0.3)
        
        # Configurar plot de energia
        self.ax_energy.set_title('Energia Total vs Tempo')
        self.ax_energy.set_xlabel('Tempo (s)')
        self.ax_energy.set_ylabel('Energia (J)')
        self.ax_energy.grid(True, alpha=0.3)
        
        # Configurar plot de velocidade
        self.ax_velocity.set_title('Velocidade Angular vs Tempo')
        self.ax_velocity.set_xlabel('Tempo (s)')
        self.ax_velocity.set_ylabel('Velocidade Angular (rad/s)')
        self.ax_velocity.grid(True, alpha=0.3)
        
        # Configurar plot de parâmetros
        self.ax_parameters.set_title('Parâmetros do Sistema')
        self.ax_parameters.axis('off')
        
        # Elementos visuais
        self.circle = Circle((0, 0), self.simulator.radius, color='red', alpha=0.7)
        self.orbit_circle = Circle((0, 0), self.simulator.orbit_radius, 
                                 fill=False, color='blue', linestyle='--', alpha=0.5)
        self.trajectory_line, = self.ax_trajectory.plot([], [], 'g-', alpha=0.6, linewidth=1)
        self.energy_line, = self.ax_energy.plot([], [], 'b-', linewidth=2)
        self.velocity_line, = self.ax_velocity.plot([], [], 'r-', linewidth=2)
        
        self.ax_trajectory.add_patch(self.orbit_circle)
        self.ax_trajectory.add_patch(self.circle)
        
        # Texto de informações
        self.info_text = self.ax_parameters.text(0.1, 0.9, '', transform=self.ax_parameters.transAxes,
                                                fontsize=10, verticalalignment='top',
                                                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        # Animação
        self.animation = None
        self.is_running = False
        
    def update_visualization(self, frame):
        """Atualiza a visualização"""
        if not self.is_running:
            return
        
        # Atualizar física
        self.simulator.update_physics()
        
        # Obter posição atual
        x, y = self.simulator.get_current_position()
        
        # Atualizar círculo
        self.circle.center = (x, y)
        
        # Atualizar trajetória
        if len(self.simulator.trajectory_x) > 1:
            self.trajectory_line.set_data(self.simulator.trajectory_x, 
                                        self.simulator.trajectory_y)
        
        # Atualizar gráfico de energia
        if len(self.simulator.energy_history) > 1:
            self.energy_line.set_data(self.simulator.time_history, 
                                    self.simulator.energy_history)
            self.ax_energy.relim()
            self.ax_energy.autoscale_view()
        
        # Atualizar gráfico de velocidade
        if len(self.simulator.time_history) > 1:
            velocity_data = [self.simulator.angular_velocity] * len(self.simulator.time_history)
            self.velocity_line.set_data(self.simulator.time_history, velocity_data)
            self.ax_velocity.relim()
            self.ax_velocity.autoscale_view()
        
        # Atualizar informações
        info = f"""Parâmetros Atuais:
Massa: {self.simulator.mass:.2f} kg
Raio: {self.simulator.radius:.2f} m
Elasticidade: {self.simulator.elasticity:.2f}
Fluidez: {self.simulator.fluidity:.2f}
Amolecimento: {self.simulator.softening:.2f}
Amortecimento: {self.simulator.damping:.2f}

Estado Atual:
Ângulo: {self.simulator.angle:.2f} rad
Velocidade Angular: {self.simulator.angular_velocity:.2f} rad/s
Loops Completados: {self.simulator.loop_count}
Tempo: {self.simulator.time:.2f} s"""
        
        self.info_text.set_text(info)
        
        return [self.circle, self.trajectory_line, self.energy_line, 
                self.velocity_line, self.info_text]
    
    def start_animation(self):
        """Inicia a animação"""
        if not self.is_running:
            self.is_running = True
            self.animation = animation.FuncAnimation(
                self.fig, self.update_visualization, interval=50, blit=False)
            plt.show()
    
    def stop_animation(self):
        """Para a animação"""
        self.is_running = False
        if self.animation:
            self.animation.event_source.stop()
    
    def reset_simulation(self):
        """Reinicia a simulação"""
        self.stop_animation()
        self.simulator.reset_simulation()
        self.trajectory_line.set_data([], [])
        self.energy_line.set_data([], [])
        self.velocity_line.set_data([], [])
        self.circle.center = (0, 0)
        plt.draw()


def create_control_panel():
    """Cria painel de controle para ajustar parâmetros"""
    root = tk.Tk()
    root.title("Controle do Simulador de Movimento Circular")
    root.geometry("400x600")
    
    # Criar visualizador
    visualizer = CircularMotionVisualizer()
    
    # Frame principal
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Controles de massa e raio
    ttk.Label(main_frame, text="Propriedades do Objeto").grid(row=0, column=0, columnspan=2, pady=5)
    
    ttk.Label(main_frame, text="Massa (kg):").grid(row=1, column=0, sticky=tk.W)
    mass_var = tk.DoubleVar(value=visualizer.simulator.mass)
    mass_scale = ttk.Scale(main_frame, from_=0.1, to=5.0, variable=mass_var, orient=tk.HORIZONTAL)
    mass_scale.grid(row=1, column=1, sticky=(tk.W, tk.E))
    
    ttk.Label(main_frame, text="Raio (m):").grid(row=2, column=0, sticky=tk.W)
    radius_var = tk.DoubleVar(value=visualizer.simulator.radius)
    radius_scale = ttk.Scale(main_frame, from_=0.05, to=0.5, variable=radius_var, orient=tk.HORIZONTAL)
    radius_scale.grid(row=2, column=1, sticky=(tk.W, tk.E))
    
    # Controles de propriedades físicas
    ttk.Label(main_frame, text="Propriedades Físicas").grid(row=3, column=0, columnspan=2, pady=(20,5))
    
    ttk.Label(main_frame, text="Elasticidade:").grid(row=4, column=0, sticky=tk.W)
    elasticity_var = tk.DoubleVar(value=visualizer.simulator.elasticity)
    elasticity_scale = ttk.Scale(main_frame, from_=0.0, to=1.0, variable=elasticity_var, orient=tk.HORIZONTAL)
    elasticity_scale.grid(row=4, column=1, sticky=(tk.W, tk.E))
    
    ttk.Label(main_frame, text="Fluidez:").grid(row=5, column=0, sticky=tk.W)
    fluidity_var = tk.DoubleVar(value=visualizer.simulator.fluidity)
    fluidity_scale = ttk.Scale(main_frame, from_=0.0, to=1.0, variable=fluidity_var, orient=tk.HORIZONTAL)
    fluidity_scale.grid(row=5, column=1, sticky=(tk.W, tk.E))
    
    ttk.Label(main_frame, text="Amolecimento:").grid(row=6, column=0, sticky=tk.W)
    softening_var = tk.DoubleVar(value=visualizer.simulator.softening)
    softening_scale = ttk.Scale(main_frame, from_=0.0, to=1.0, variable=softening_var, orient=tk.HORIZONTAL)
    softening_scale.grid(row=6, column=1, sticky=(tk.W, tk.E))
    
    ttk.Label(main_frame, text="Amortecimento:").grid(row=7, column=0, sticky=tk.W)
    damping_var = tk.DoubleVar(value=visualizer.simulator.damping)
    damping_scale = ttk.Scale(main_frame, from_=0.0, to=0.1, variable=damping_var, orient=tk.HORIZONTAL)
    damping_scale.grid(row=7, column=1, sticky=(tk.W, tk.E))
    
    # Controles de movimento
    ttk.Label(main_frame, text="Parâmetros de Movimento").grid(row=8, column=0, columnspan=2, pady=(20,5))
    
    ttk.Label(main_frame, text="Velocidade Angular:").grid(row=9, column=0, sticky=tk.W)
    velocity_var = tk.DoubleVar(value=visualizer.simulator.angular_velocity)
    velocity_scale = ttk.Scale(main_frame, from_=0.1, to=10.0, variable=velocity_var, orient=tk.HORIZONTAL)
    velocity_scale.grid(row=9, column=1, sticky=(tk.W, tk.E))
    
    ttk.Label(main_frame, text="Raio da Órbita:").grid(row=10, column=0, sticky=tk.W)
    orbit_var = tk.DoubleVar(value=visualizer.simulator.orbit_radius)
    orbit_scale = ttk.Scale(main_frame, from_=1.0, to=5.0, variable=orbit_var, orient=tk.HORIZONTAL)
    orbit_scale.grid(row=10, column=1, sticky=(tk.W, tk.E))
    
    # Botões de controle
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=11, column=0, columnspan=2, pady=20)
    
    def update_parameters():
        visualizer.simulator.set_parameters(
            mass=mass_var.get(),
            radius=radius_var.get(),
            elasticity=elasticity_var.get(),
            fluidity=fluidity_var.get(),
            softening=softening_var.get(),
            damping=damping_var.get(),
            angular_velocity=velocity_var.get(),
            orbit_radius=orbit_var.get()
        )
        visualizer.orbit_circle.radius = orbit_var.get()
        visualizer.ax_trajectory.set_xlim(-orbit_var.get()-1, orbit_var.get()+1)
        visualizer.ax_trajectory.set_ylim(-orbit_var.get()-1, orbit_var.get()+1)
    
    def start_simulation():
        update_parameters()
        visualizer.start_animation()
    
    def stop_simulation():
        visualizer.stop_animation()
    
    def reset_simulation():
        visualizer.reset_simulation()
    
    ttk.Button(button_frame, text="Iniciar", command=start_simulation).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Parar", command=stop_simulation).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="Reiniciar", command=reset_simulation).grid(row=0, column=2, padx=5)
    
    # Configurar redimensionamento
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    
    return root, visualizer


if __name__ == "__main__":
    # Criar e executar o simulador
    root, visualizer = create_control_panel()
    
    print("Simulador de Movimento Circular Iniciado!")
    print("Use o painel de controle para ajustar os parâmetros e iniciar a simulação.")
    print("\nParâmetros disponíveis:")
    print("- Massa: Controla a inércia do objeto")
    print("- Raio: Afeta o momento de inércia")
    print("- Elasticidade: Força de restauração elástica")
    print("- Fluidez: Amortecimento fluido")
    print("- Amolecimento: Reduz a intensidade das forças")
    print("- Amortecimento: Perda geral de energia")
    print("- Velocidade Angular: Velocidade inicial de rotação")
    print("- Raio da Órbita: Tamanho da trajetória circular")
    
    root.mainloop()