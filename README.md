# Simulador de Movimento Circular com Propriedades Físicas

Este projeto implementa um simulador avançado de movimento circular que incorpora leis físicas realistas, incluindo elasticidade, momento de inércia, fluidez e amolecimento.

## Características

### Propriedades Físicas Implementadas

1. **Momento de Inércia**: Calculado baseado na geometria do objeto (cilindro sólido)
2. **Elasticidade**: Força de restauração elástica com coeficiente configurável
3. **Fluidez**: Amortecimento fluido que simula resistência do meio
4. **Amolecimento**: Efeito que reduz a intensidade das forças aplicadas
5. **Amortecimento**: Perda geral de energia do sistema

### Funcionalidades

- **Simulação em Tempo Real**: Animação fluida do movimento circular
- **Controles Interativos**: Painel de controle para ajustar todos os parâmetros
- **Visualizações Múltiplas**: 
  - Trajetória do movimento
  - Gráfico de energia total vs tempo
  - Gráfico de velocidade angular vs tempo
  - Informações dos parâmetros em tempo real
- **Sistema de Loops**: Contagem automática de ciclos completados
- **Histórico de Dados**: Armazenamento e visualização do histórico de movimento

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o simulador:
```bash
python circular_motion_simulator.py
```

## Como Usar

1. **Ajuste os Parâmetros**: Use os controles deslizantes no painel de controle para modificar:
   - Massa do objeto (0.1 - 5.0 kg)
   - Raio do objeto (0.05 - 0.5 m)
   - Elasticidade (0.0 - 1.0)
   - Fluidez (0.0 - 1.0)
   - Amolecimento (0.0 - 1.0)
   - Amortecimento (0.0 - 0.1)
   - Velocidade angular inicial (0.1 - 10.0 rad/s)
   - Raio da órbita (1.0 - 5.0 m)

2. **Inicie a Simulação**: Clique em "Iniciar" para começar a animação

3. **Monitore os Resultados**: Observe os gráficos que mostram:
   - A trajetória do objeto em movimento
   - A variação da energia total do sistema
   - A velocidade angular ao longo do tempo
   - Informações atualizadas dos parâmetros

4. **Controle a Simulação**: Use os botões para parar ou reiniciar a simulação

## Física Implementada

### Momento de Inércia
Para um cilindro sólido: `I = 0.5 * m * r²`

### Força Elástica
`F = -k * x` onde k é a constante elástica e x é o deslocamento

### Amortecimento Fluido
`F_damping = -c * v` onde c é o coeficiente de fluidez e v é a velocidade

### Efeito de Amolecimento
`F_softened = F * (1 - softening_factor)`

### Equação de Movimento
O sistema resolve numericamente as equações diferenciais do movimento circular com as forças aplicadas.

## Estrutura do Código

- `CircularMotionSimulator`: Classe principal que implementa a física
- `CircularMotionVisualizer`: Classe responsável pela visualização e animação
- `create_control_panel()`: Função que cria a interface de controle

## Exemplos de Uso

### Simulação Básica
```python
simulator = CircularMotionSimulator()
simulator.set_parameters(mass=1.0, elasticity=0.8, fluidity=0.1)
```

### Simulação com Alto Amortecimento
```python
simulator.set_parameters(damping=0.05, fluidity=0.3)
```

### Simulação Elástica
```python
simulator.set_parameters(elasticity=0.95, softening=0.02)
```

## Contribuições

Este simulador pode ser estendido para incluir:
- Diferentes geometrias de objetos
- Campos de força externos
- Colisões entre múltiplos objetos
- Análise de estabilidade
- Exportação de dados

## Licença

Este projeto é de código aberto e pode ser usado para fins educacionais e de pesquisa.