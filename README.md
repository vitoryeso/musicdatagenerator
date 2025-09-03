# Simulador de Movimento Circular com Loops

Um simulador interativo de movimento circular que incorpora leis físicas de elasticidade, momento de inércia, fluidez e amortecimento para criar padrões de movimento complexos e loops naturais.

## Características Principais

### Física Implementada
- **Elasticidade**: Força de restauração que tenta manter o objeto no raio base
- **Momento de Inércia**: Afeta a conservação do momento angular durante mudanças de raio
- **Amortecimento**: Reduz gradualmente a energia do sistema
- **Fluidez**: Controla a suavidade das transições de movimento

### Funcionalidades
- Visualização em tempo real da trajetória do objeto
- Vetores de velocidade e aceleração visíveis
- Controles interativos via sliders para todos os parâmetros
- Informações físicas em tempo real (raio, velocidade, energia cinética)
- Criação natural de loops e padrões complexos

## Como Usar

### Instalação
```bash
pip install -r requirements.txt
```

### Execução
```bash
python circular_motion_simulator.py
```

### Controles Interativos

#### Sliders Disponíveis:
- **Elasticidade (0.1-1.0)**: Controla a força que tenta manter o raio base
- **Amortecimento (0.0-0.1)**: Reduz a energia do sistema ao longo do tempo
- **Fluidez (0.1-1.0)**: Suaviza as transições de movimento
- **Momento de Inércia (0.1-2.0)**: Afeta como o objeto responde a mudanças de raio
- **Velocidade Inicial (1.0-10.0)**: Velocidade inicial do movimento
- **Raio Base (0.5-4.0)**: Raio de referência do movimento circular

#### Botões:
- **Reset**: Reinicia a simulação com os parâmetros atuais
- **Limpar**: Remove o rastro da trajetória

## Física por Trás do Simulador

### Forças Implementadas

1. **Força Centrípeta**: `F_c = m * ω² * r`
2. **Força Elástica**: `F_e = -k * (r - r_0)` onde k é o coeficiente de elasticidade
3. **Força de Amortecimento**: `F_d = -c * v_r` onde c é o coeficiente de amortecimento

### Conservação do Momento Angular
O momento angular `L = I * ω` é modificado pelo momento de inércia ajustável, permitindo diferentes comportamentos quando o raio muda.

### Criação de Loops
Os loops surgem naturalmente da interação entre:
- A força centrípeta tentando manter o movimento circular
- A força elástica tentando restaurar o raio original
- O amortecimento reduzindo a energia
- A fluidez suavizando as transições

## Exemplos de Uso

### Movimento Circular Simples
- Elasticidade: 0.8
- Amortecimento: 0.01
- Fluidez: 0.8
- Momento de Inércia: 0.5

### Loops Complexos
- Elasticidade: 0.3
- Amortecimento: 0.05
- Fluidez: 0.2
- Momento de Inércia: 1.5

### Espiral Amortecida
- Elasticidade: 0.6
- Amortecimento: 0.08
- Fluidez: 0.9
- Momento de Inércia: 0.3

## Visualização

O simulador mostra:
- **Linha azul**: Trajetória do objeto (rastro)
- **Ponto vermelho**: Posição atual do objeto
- **Linha verde**: Vetor velocidade
- **Linha vermelha**: Vetor aceleração
- **Painel informativo**: Parâmetros físicos em tempo real

## Requisitos do Sistema

- Python 3.7+
- NumPy 1.21.0+
- Matplotlib 3.5.0+

## Autor

Desenvolvido como uma demonstração interativa de física aplicada em movimento circular com parâmetros ajustáveis.