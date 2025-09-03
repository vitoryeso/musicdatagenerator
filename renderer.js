class Renderer {
    constructor(canvas, physics) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.physics = physics;
        
        // Configurações visuais
        this.objectSize = 20;
        this.trailOpacity = 0.3;
        this.glowIntensity = 0.8;
        
        // Cores
        this.colors = {
            object: '#4CAF50',
            trail: '#81C784',
            orbit: '#424242',
            center: '#616161',
            glow: '#69F0AE'
        };
        
        // Configurar canvas
        this.setupCanvas();
    }
    
    setupCanvas() {
        // Configurar qualidade de renderização
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';
    }
    
    clear() {
        // Criar efeito de fade para trilha
        this.ctx.fillStyle = 'rgba(10, 10, 10, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    render() {
        // Limpar canvas com efeito de trilha
        this.clear();
        
        // Desenhar grade de fundo
        this.drawGrid();
        
        // Desenhar órbita
        this.drawOrbit();
        
        // Desenhar centro
        this.drawCenter();
        
        // Desenhar trilha
        this.drawTrail();
        
        // Desenhar objeto com efeitos
        this.drawObject();
        
        // Desenhar informações de debug
        this.drawForceVectors();
    }
    
    drawGrid() {
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        this.ctx.lineWidth = 1;
        
        const gridSize = 50;
        for (let x = 0; x < this.canvas.width; x += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y < this.canvas.height; y += gridSize) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
    }
    
    drawOrbit() {
        this.ctx.strokeStyle = this.colors.orbit;
        this.ctx.lineWidth = 2;
        this.ctx.setLineDash([5, 5]);
        
        this.ctx.beginPath();
        this.ctx.arc(
            this.physics.centerX,
            this.physics.centerY,
            this.physics.radius,
            0,
            Math.PI * 2
        );
        this.ctx.stroke();
        
        this.ctx.setLineDash([]);
    }
    
    drawCenter() {
        // Desenhar ponto central
        this.ctx.fillStyle = this.colors.center;
        this.ctx.beginPath();
        this.ctx.arc(
            this.physics.centerX,
            this.physics.centerY,
            5,
            0,
            Math.PI * 2
        );
        this.ctx.fill();
        
        // Adicionar brilho ao centro
        const gradient = this.ctx.createRadialGradient(
            this.physics.centerX,
            this.physics.centerY,
            0,
            this.physics.centerX,
            this.physics.centerY,
            20
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.3)');
        gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(
            this.physics.centerX,
            this.physics.centerY,
            20,
            0,
            Math.PI * 2
        );
        this.ctx.fill();
    }
    
    drawTrail() {
        if (this.physics.trail.length < 2) return;
        
        // Desenhar trilha com gradiente de opacidade
        for (let i = 1; i < this.physics.trail.length; i++) {
            const prev = this.physics.trail[i - 1];
            const curr = this.physics.trail[i];
            
            const opacity = (i / this.physics.trail.length) * this.trailOpacity;
            this.ctx.strokeStyle = `rgba(129, 199, 132, ${opacity})`;
            this.ctx.lineWidth = 2 + (i / this.physics.trail.length) * 2;
            
            this.ctx.beginPath();
            this.ctx.moveTo(prev.x, prev.y);
            this.ctx.lineTo(curr.x, curr.y);
            this.ctx.stroke();
        }
    }
    
    drawObject() {
        const { x, y } = this.physics.position;
        const { x: dx, y: dy } = this.physics.deformation;
        
        // Salvar contexto para transformações
        this.ctx.save();
        
        // Aplicar transformações para deformação
        this.ctx.translate(x, y);
        this.ctx.scale(dx, dy);
        
        // Desenhar brilho/glow
        this.drawGlow(0, 0);
        
        // Desenhar objeto principal
        this.ctx.fillStyle = this.colors.object;
        this.ctx.beginPath();
        this.ctx.arc(0, 0, this.objectSize, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Adicionar efeito de luz interna
        const innerGradient = this.ctx.createRadialGradient(
            -this.objectSize * 0.3,
            -this.objectSize * 0.3,
            0,
            0,
            0,
            this.objectSize
        );
        innerGradient.addColorStop(0, 'rgba(255, 255, 255, 0.4)');
        innerGradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
        
        this.ctx.fillStyle = innerGradient;
        this.ctx.beginPath();
        this.ctx.arc(0, 0, this.objectSize, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Restaurar contexto
        this.ctx.restore();
        
        // Desenhar partículas ao redor (efeito de fluidez)
        this.drawFluidityParticles(x, y);
    }
    
    drawGlow(x, y) {
        const glowSize = this.objectSize * 2;
        const speed = Math.sqrt(
            this.physics.velocity.x * this.physics.velocity.x +
            this.physics.velocity.y * this.physics.velocity.y
        );
        const intensity = Math.min(1, speed / 100) * this.glowIntensity;
        
        const gradient = this.ctx.createRadialGradient(
            x, y, this.objectSize,
            x, y, glowSize
        );
        gradient.addColorStop(0, `rgba(105, 240, 174, ${intensity * 0.5})`);
        gradient.addColorStop(0.5, `rgba(105, 240, 174, ${intensity * 0.2})`);
        gradient.addColorStop(1, 'rgba(105, 240, 174, 0)');
        
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(x, y, glowSize, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    drawFluidityParticles(x, y) {
        const particleCount = Math.floor(this.physics.fluidity * 10);
        const speed = Math.sqrt(
            this.physics.velocity.x * this.physics.velocity.x +
            this.physics.velocity.y * this.physics.velocity.y
        );
        
        for (let i = 0; i < particleCount; i++) {
            const angle = (i / particleCount) * Math.PI * 2 + this.physics.time * 2;
            const distance = this.objectSize + 10 + Math.sin(this.physics.time * 3 + i) * 5;
            
            const px = x + Math.cos(angle) * distance;
            const py = y + Math.sin(angle) * distance;
            
            const opacity = this.physics.fluidity * 0.3;
            this.ctx.fillStyle = `rgba(129, 199, 132, ${opacity})`;
            
            this.ctx.beginPath();
            this.ctx.arc(px, py, 2, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }
    
    drawForceVectors() {
        const { x, y } = this.physics.position;
        const scale = 0.1;
        
        // Desenhar vetor de velocidade
        this.ctx.strokeStyle = 'rgba(255, 255, 0, 0.6)';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(
            x + this.physics.velocity.x * scale,
            y + this.physics.velocity.y * scale
        );
        this.ctx.stroke();
        
        // Desenhar vetor de força
        this.ctx.strokeStyle = 'rgba(255, 0, 0, 0.6)';
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(
            x + this.physics.force.x * scale * 0.1,
            y + this.physics.force.y * scale * 0.1
        );
        this.ctx.stroke();
    }
}