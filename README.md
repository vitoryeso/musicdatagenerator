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

## Licença
MIT
