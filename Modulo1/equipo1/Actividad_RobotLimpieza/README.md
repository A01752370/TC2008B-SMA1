# Robot de limpieza reactivo

Simulación multiagente (Python + [Mesa](https://mesa.readthedocs.io)) de robots
reactivos que limpian una habitación de M×N celdas. Sigue la misma estructura
que el ejemplo del Juego de la Vida visto en clase (`agents.py`, `model.py`,
`app.py`).

**Reporte:** [`Informe_Robot_Limpieza.pdf`](Informe_Robot_Limpieza.pdf)

## Reglas de la simulación

- Se ensucia al azar un porcentaje de las celdas.
- Todos los agentes empiezan en la celda [1,1] (coordenada `(0, 0)`).
- En cada paso, cada agente (en orden aleatorio):
  - si su celda está sucia, aspira;
  - si está limpia, elige una de sus 8 celdas vecinas al azar y se mueve;
    si la celda está fuera de la habitación, se queda donde está.
- La simulación termina cuando todo está limpio o se llega al tiempo máximo.

Se reporta: tiempo hasta limpiar todo (o tiempo máximo), porcentaje de celdas
limpias al final y número total de movimientos de todos los agentes.

## Archivos

| Archivo                       | Contenido                                                  |
|-------------------------------|------------------------------------------------------------|
| `agents.py`                   | Agentes `CleaningRobot` (reactivo) y `Dirt` (suciedad)     |
| `model.py`                    | `CleaningModel`: habitación, reglas y estadísticas         |
| `app.py`                      | Visualización interactiva con SolaraViz                    |
| `run.py`                      | Una simulación con parámetros por línea de comandos        |
| `experiments.py`              | Barrido de número de agentes, CSV y gráficas del informe   |
| `resultados/`                 | CSV y gráficas generadas por `experiments.py`              |


## Uso

```bash
pip install -r requirements.txt

# Visualización en el navegador
solara run app.py

# Una simulación desde la terminal
python run.py --width 20 --height 20 --agents 4 --dirty 0.5 --max-steps 2000 --seed 7

# Experimentos del informe (7 cantidades de agentes × 30 repeticiones)
python experiments.py
```

| Parámetro     | Descripción                              | Valor por defecto |
|---------------|------------------------------------------|-------------------|
| `--width`     | Columnas de la habitación (M)            | 20                |
| `--height`    | Filas de la habitación (N)               | 20                |
| `--agents`    | Número de robots                         | 1                 |
| `--dirty`     | Fracción de celdas sucias (0 a 1)        | 0.5               |
| `--max-steps` | Tiempo máximo de ejecución (pasos)       | 1000              |
| `--seed`      | Semilla aleatoria para reproducibilidad  | ninguna           |

## Estilo de código

PEP 8 (verificado con `pycodestyle`), docstrings en todas las clases y
funciones, y la misma organización de archivos del ejemplo de clase.

## Autores

Erika Pacheco Martinez
Braulio Barbosa Maruri 
— equipo1
