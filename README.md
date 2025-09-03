# I)
# loop_creator

Gera loops de movimento circular com elasticidade (mola), amortecimento (fluidez), inércia de orientação e amolecimento (squash & stretch).

## Uso rápido

Executar via módulo:

```bash
python3 -m loop_creator --duration 2.0 --fps 60 --radius 100 \
  --elasticidade 0.6 --fluidez 0.5 --inercia 0.4 --amolecimento 0.25 \
  --loops 1 --pre-roll-loops 3 --out -
```

Salvar em arquivo JSON:

```bash
python3 -m loop_creator --out loop.json
```

Ou usar o script de exemplo:

```bash
python3 scripts/export_loop.py
```

## Parâmetros

- `duration` (s): duração do loop a ser emitido
- `fps`: frames por segundo
- `radius`: raio do caminho circular
- `center-x`, `center-y`: centro do círculo
- `phase0` (rad): fase inicial do movimento
- `elasticidade` [0..1]: quão responsivo e “saltitante” é o movimento
- `fluidez` [0..1+]: amortecimento (0 pouco, 1 alto)
- `inercia` [0..1]: momento de inércia da orientação (0 segue rápido, 1 mais pesado)
- `amolecimento` [0..1]: intensidade do squash & stretch conforme velocidade tangencial
- `loops`: quantos giros dentro da duração
- `pre-roll-loops`: giros de pré-aquecimento para estabilizar o sistema

## Estrutura de saída

```json
{
  "params": { ... },
  "frames": [
    {
      "index": 0,
      "time": 0.0,
      "x": 100.0,
      "y": 0.0,
      "travel_angle": 0.05,
      "orientation": 1.62,
      "scale_tangent": 1.03,
      "scale_normal": 0.97
    }
  ]
}
```
# II)
# Simulador de Movimento Circular com Física Avançada

Um simulador interativo que demonstra movimento circular com física realista, incluindo elasticidade, momento de inércia, fluidez e amolecimento.

## 🎯 Características

- **Física Realista**: Implementa leis de elasticidade (Lei de Hooke) e momento de inércia
- **Parâmetros Ajustáveis**: Controle total sobre todos os aspectos físicos do movimento
- **Efeitos Visuais**: Trilha de movimento, deformação do objeto, partículas de fluidez
- **Interação em Tempo Real**: Clique e arraste para perturbar o movimento
- **Interface Moderna**: Design responsivo com controles intuitivos

## 🚀 Como Usar

1. Abra o arquivo `index.html` em um navegador web moderno
2. Use os controles deslizantes para ajustar os parâmetros:
   - **Raio da Órbita**: Distância do centro de rotação
   - **Velocidade Angular**: Velocidade de rotação
   - **Elasticidade**: Rigidez da "mola" que mantém o objeto na órbita
   - **Momento de Inércia**: Resistência a mudanças no movimento rotacional
   - **Fluidez**: Suavidade do movimento e transições
   - **Amolecimento**: Deformação do objeto baseada na velocidade
   - **Massa**: Massa do objeto (afeta inércia e força)
   - **Amortecimento**: Perda gradual de energia

## 🎮 Controles

### Mouse
- **Clique**: Adiciona perturbação na direção do clique
- **Arrastar**: Controla diretamente a posição do objeto

### Teclado
- **Espaço**: Pausar/Continuar simulação
- **R**: Reiniciar simulação
- **P**: Adicionar perturbação aleatória

## 🔧 Física Implementada

### Lei de Hooke
```
F = -k * x
```
Onde k é a constante elástica e x é o deslocamento.

### Momento de Inércia
```
I = m * r²
```
Afeta a resistência do objeto a mudanças na velocidade angular.

### Amortecimento Viscoso
```
F_damping = -b * v
```
Simula perda de energia por atrito.

## 📊 Visualizações

- **Objeto Principal**: Círculo verde que se deforma com base na velocidade
- **Trilha**: Mostra o caminho percorrido
- **Vetores**: Visualização de forças e velocidades (amarelo = velocidade, vermelho = força)
- **Partículas de Fluidez**: Indicam o nível de fluidez do movimento
- **Efeito Glow**: Intensidade baseada na velocidade

## 🛠️ Estrutura do Código

- `index.html`: Interface e estrutura
- `physics.js`: Motor de física com todas as leis implementadas
- `renderer.js`: Sistema de renderização e efeitos visuais
- `main.js`: Lógica principal e controles

## 📈 Exemplos de Uso

1. **Movimento Elástico**: Aumente a elasticidade para ver o objeto "quicar" de volta à órbita
2. **Alta Inércia**: Aumente o momento de inércia para movimento mais estável
3. **Objeto Fluido**: Maximize fluidez e amolecimento para movimento orgânico
4. **Baixo Amortecimento**: Reduza para ver oscilações persistentes

## 🔍 Observações Físicas

- A energia cinética é calculada e exibida em tempo real
- O ângulo mostra a posição angular atual
- A deformação visual representa as forças atuando no objeto
- O sistema conserva momento angular (com amortecimento)
