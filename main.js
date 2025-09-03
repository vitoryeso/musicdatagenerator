class CircularMotionSimulation {
    constructor() {
        this.canvas = document.getElementById('canvas');
        this.physics = new PhysicsEngine();
        this.renderer = new Renderer(this.canvas, this.physics);
        
        this.isRunning = true;
        this.animationId = null;
        
        this.setupControls();
        this.bindEvents();
        this.start();
    }
    
    setupControls() {
        // Configurar todos os controles deslizantes
        const controls = [
            { id: 'radius', property: 'radius', suffix: 'px' },
            { id: 'speed', property: 'speed', suffix: '' },
            { id: 'elasticity', property: 'elasticity', suffix: '' },
            { id: 'inertia', property: 'inertia', suffix: '' },
            { id: 'fluidity', property: 'fluidity', suffix: '' },
            { id: 'softness', property: 'softness', suffix: '' },
            { id: 'mass', property: 'mass', suffix: 'kg' },
            { id: 'damping', property: 'damping', suffix: '' }
        ];
        
        controls.forEach(control => {
            const slider = document.getElementById(control.id);
            const valueDisplay = document.getElementById(`${control.id}-value`);
            
            slider.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                valueDisplay.textContent = value.toFixed(control.property === 'damping' ? 2 : 1) + control.suffix;
                
                const params = {};
                params[control.property] = value;
                this.physics.updateParameters(params);
            });
        });
    }
    
    bindEvents() {
        // Redimensionar canvas quando a janela mudar
        window.addEventListener('resize', () => this.resizeCanvas());
        
        // Adicionar interação com o mouse
        this.canvas.addEventListener('click', (e) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calcular direção da perturbação
            const dx = x - this.physics.position.x;
            const dy = y - this.physics.position.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance > 0) {
                this.physics.perturbation.x = (dx / distance) * 50;
                this.physics.perturbation.y = (dy / distance) * 50;
                
                // Adicionar impulso
                this.physics.velocity.x += (dx / distance) * 100;
                this.physics.velocity.y += (dy / distance) * 100;
            }
        });
        
        // Arrastar para criar perturbação contínua
        let isDragging = false;
        
        this.canvas.addEventListener('mousedown', () => {
            isDragging = true;
        });
        
        this.canvas.addEventListener('mousemove', (e) => {
            if (isDragging) {
                const rect = this.canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const dx = x - this.physics.centerX;
                const dy = y - this.physics.centerY;
                const angle = Math.atan2(dy, dx);
                
                this.physics.angle = angle;
            }
        });
        
        this.canvas.addEventListener('mouseup', () => {
            isDragging = false;
        });
        
        // Teclas de atalho
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case ' ':
                    e.preventDefault();
                    this.togglePause();
                    break;
                case 'r':
                    this.reset();
                    break;
                case 'p':
                    this.addPerturbation();
                    break;
            }
        });
    }
    
    resizeCanvas() {
        // Manter proporção quadrada
        const size = Math.min(window.innerWidth - 40, 600);
        this.canvas.width = size;
        this.canvas.height = size;
        
        // Atualizar centro
        this.physics.centerX = size / 2;
        this.physics.centerY = size / 2;
        
        // Reconfigurar renderizador
        this.renderer.setupCanvas();
    }
    
    start() {
        this.animate();
    }
    
    animate() {
        if (this.isRunning) {
            // Atualizar física
            this.physics.update();
            
            // Renderizar
            this.renderer.render();
            
            // Atualizar informações
            this.updateInfo();
        }
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }
    
    updateInfo() {
        const pos = this.physics.position;
        const vel = this.physics.velocity;
        const speed = Math.sqrt(vel.x * vel.x + vel.y * vel.y);
        const energy = this.physics.getKineticEnergy();
        const angleDegrees = (this.physics.angle * 180 / Math.PI) % 360;
        
        document.getElementById('position-info').textContent = 
            `(${pos.x.toFixed(1)}, ${pos.y.toFixed(1)})`;
        document.getElementById('velocity-info').textContent = 
            `${speed.toFixed(1)} px/s`;
        document.getElementById('energy-info').textContent = 
            `${energy.toFixed(2)} J`;
        document.getElementById('angle-info').textContent = 
            `${angleDegrees.toFixed(1)}°`;
    }
    
    togglePause() {
        this.isRunning = !this.isRunning;
    }
    
    reset() {
        this.physics.reset();
    }
    
    addPerturbation() {
        this.physics.addPerturbation();
    }
    
    stop() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

// Inicializar simulação quando a página carregar
let simulation;

document.addEventListener('DOMContentLoaded', () => {
    simulation = new CircularMotionSimulation();
    
    // Mostrar instruções iniciais
    console.log('🎮 Controles:');
    console.log('- Clique no canvas para adicionar perturbação');
    console.log('- Arraste para controlar a posição');
    console.log('- Tecla Espaço: Pausar/Continuar');
    console.log('- Tecla R: Reiniciar');
    console.log('- Tecla P: Adicionar perturbação aleatória');
});