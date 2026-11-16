"""Ejecuta una sola simulación con parámetros dados por línea de comandos.

Ejemplo:
    python run.py --width 20 --height 20 --agents 4 --dirty 0.5 \
        --max-steps 2000 --seed 7
"""

import argparse

from model import CleaningModel


def parse_args():
    """Define y lee los parámetros de la simulación."""
    parser = argparse.ArgumentParser(
        description="Simulación de robots de limpieza reactivos."
    )
    parser.add_argument("--width", type=int, default=20,
                        help="M columnas")
    parser.add_argument("--height", type=int, default=20,
                        help="N filas")
    parser.add_argument("--agents", type=int, default=1,
                        help="número de robots")
    parser.add_argument("--dirty", type=float, default=0.5,
                        help="fracción de celdas sucias (0 a 1)")
    parser.add_argument("--max-steps", type=int, default=1000,
                        help="tiempo máximo de ejecución (pasos)")
    parser.add_argument("--seed", type=int, default=None,
                        help="semilla aleatoria")
    return parser.parse_args()


def main():
    """Corre la simulación e imprime sus estadísticas."""
    args = parse_args()
    model = CleaningModel(
        width=args.width,
        height=args.height,
        num_agents=args.agents,
        dirty_fraction=args.dirty,
        max_steps=args.max_steps,
        rng=args.seed,
    )
    result = model.run()

    if result["all_clean"]:
        status = f"todo limpio en {result['steps']} pasos"
    else:
        status = f"se alcanzó el tiempo máximo ({result['steps']} pasos)"
    print(f"Habitación {args.width}x{args.height}, "
          f"{result['agents']} agente(s): {status}")
    print(f"Celdas limpias al final: {result['clean_percentage']:.2f} %")
    print(f"Movimientos totales: {result['moves']}")


if __name__ == "__main__":
    main()
