class PhysicsEngine {
    constructor() {
        // Propriedades do objeto
        this.position = { x: 0, y: 0 };
        this.velocity = { x: 0, y: 0 };
        this.acceleration = { x: 0, y: 0 };
        this.force = { x: 0, y: 0 };
        
        // Parâmetros físicos
        this.mass = 1.0;
        this.radius = 150;
        this.angle = 0;
        this.angularVelocity = 2.0;
        this.angularAcceleration = 0;
        
        // Propriedades elásticas e de amortecimento
        this.elasticity = 0.8;
        this.inertia = 0.5;
        this.fluidity = 0.5;
        this.softness = 0.3;
        this.damping = 0.98;
        
        // Estado da simulação
        this.centerX = 300;
        this.centerY = 300;
        this.time = 0;
        this.deltaTime = 0.016; // 60 FPS
        
        // Deformação do objeto
        this.deformation = { x: 1, y: 1 };
        this.deformationVelocity = { x: 0, y: 0 };
        
        // Perturbações
        this.perturbation = { x: 0, y: 0 };
        this.perturbationDecay = 0.95;
        
        // Trail para efeito visual
        this.trail = [];
        this.maxTrailLength = 30;
    }
    
    updateParameters(params) {
        if (params.radius !== undefined) this.radius = params.radius;
        if (params.speed !== undefined) this.angularVelocity = params.speed;
        if (params.elasticity !== undefined) this.elasticity = params.elasticity;
        if (params.inertia !== undefined) this.inertia = params.inertia;
        if (params.fluidity !== undefined) this.fluidity = params.fluidity;
        if (params.softness !== undefined) this.softness = params.softness;
        if (params.mass !== undefined) this.mass = params.mass;
        if (params.damping !== undefined) this.damping = params.damping;
    }
    
    update() {
        // Calcular momento de inércia
        const I = this.inertia * this.mass * this.radius * this.radius;
        
        // Força centrípeta
        const centripetalForce = this.mass * this.angularVelocity * this.angularVelocity * this.radius;
        
        // Aplicar perturbação
        this.perturbation.x *= this.perturbationDecay;
        this.perturbation.y *= this.perturbationDecay;
        
        // Calcular posição ideal no movimento circular
        const idealX = this.centerX + (this.radius + this.perturbation.x) * Math.cos(this.angle);
        const idealY = this.centerY + (this.radius + this.perturbation.y) * Math.sin(this.angle);
        
        // Calcular força elástica (Lei de Hooke)
        const dx = idealX - this.position.x;
        const dy = idealY - this.position.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Força elástica proporcional à distância
        const springConstant = this.elasticity * 10;
        this.force.x = springConstant * dx;
        this.force.y = springConstant * dy;
        
        // Aplicar amortecimento viscoso
        this.force.x -= this.velocity.x * (1 - this.damping) * 10;
        this.force.y -= this.velocity.y * (1 - this.damping) * 10;
        
        // Segunda Lei de Newton: F = ma
        this.acceleration.x = this.force.x / this.mass;
        this.acceleration.y = this.force.y / this.mass;
        
        // Integração de Verlet para maior estabilidade
        const newVelocityX = this.velocity.x + this.acceleration.x * this.deltaTime;
        const newVelocityY = this.velocity.y + this.acceleration.y * this.deltaTime;
        
        // Aplicar fluidez ao movimento
        this.velocity.x = this.velocity.x * (1 - this.fluidity) + newVelocityX * this.fluidity;
        this.velocity.y = this.velocity.y * (1 - this.fluidity) + newVelocityY * this.fluidity;
        
        // Atualizar posição
        this.position.x += this.velocity.x * this.deltaTime;
        this.position.y += this.velocity.y * this.deltaTime;
        
        // Inicializar posição se necessário
        if (this.position.x === 0 && this.position.y === 0) {
            this.position.x = idealX;
            this.position.y = idealY;
        }
        
        // Calcular deformação baseada na velocidade e softness
        const speed = Math.sqrt(this.velocity.x * this.velocity.x + this.velocity.y * this.velocity.y);
        const targetDeformationX = 1 + (this.velocity.x / 100) * this.softness;
        const targetDeformationY = 1 - (this.velocity.y / 100) * this.softness;
        
        // Aplicar suavização à deformação
        this.deformationVelocity.x = (targetDeformationX - this.deformation.x) * 0.1;
        this.deformationVelocity.y = (targetDeformationY - this.deformation.y) * 0.1;
        
        this.deformation.x += this.deformationVelocity.x;
        this.deformation.y += this.deformationVelocity.y;
        
        // Limitar deformação
        this.deformation.x = Math.max(0.7, Math.min(1.3, this.deformation.x));
        this.deformation.y = Math.max(0.7, Math.min(1.3, this.deformation.y));
        
        // Atualizar ângulo considerando o momento de inércia
        const angularDamping = Math.pow(this.damping, I);
        this.angularVelocity *= angularDamping;
        this.angle += this.angularVelocity * this.deltaTime;
        
        // Atualizar tempo
        this.time += this.deltaTime;
        
        // Adicionar à trilha
        this.trail.push({
            x: this.position.x,
            y: this.position.y,
            time: this.time
        });
        
        // Limitar tamanho da trilha
        if (this.trail.length > this.maxTrailLength) {
            this.trail.shift();
        }
    }
    
    addPerturbation() {
        // Adicionar perturbação aleatória
        const angle = Math.random() * Math.PI * 2;
        const magnitude = 30 + Math.random() * 50;
        this.perturbation.x = Math.cos(angle) * magnitude;
        this.perturbation.y = Math.sin(angle) * magnitude;
        
        // Adicionar impulso à velocidade
        this.velocity.x += Math.cos(angle) * magnitude * 2;
        this.velocity.y += Math.sin(angle) * magnitude * 2;
    }
    
    reset() {
        this.angle = 0;
        this.position = { x: this.centerX + this.radius, y: this.centerY };
        this.velocity = { x: 0, y: 0 };
        this.acceleration = { x: 0, y: 0 };
        this.perturbation = { x: 0, y: 0 };
        this.deformation = { x: 1, y: 1 };
        this.trail = [];
        this.time = 0;
    }
    
    getKineticEnergy() {
        const speed = Math.sqrt(this.velocity.x * this.velocity.x + this.velocity.y * this.velocity.y);
        return 0.5 * this.mass * speed * speed;
    }
    
    getAngularMomentum() {
        const I = this.inertia * this.mass * this.radius * this.radius;
        return I * this.angularVelocity;
    }
}