"""Visualización interactiva de la simulación con SolaraViz.

Para abrirla en el navegador, ejecuta desde esta carpeta:
    solara run app.py
"""

from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

from agents import CleaningRobot
from model import CleaningModel


def agent_portrayal(agent):
    """Define cómo se dibuja cada agente.

    Los robots son círculos azules; la suciedad, cuadros cafés.
    """
    if isinstance(agent, CleaningRobot):
        return AgentPortrayalStyle(color="tab:blue", marker="o", size=40,
                                   zorder=2)
    return AgentPortrayalStyle(color="saddlebrown", marker="s", size=30,
                               zorder=1)


def post_process(ax):
    """Ajusta los ejes de la cuadrícula."""
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


model_params = {
    "rng": {
        "type": "InputText",
        "value": 42,
        "label": "Semilla aleatoria",
    },
    "width": {
        "type": "SliderInt",
        "value": 20,
        "label": "Ancho (M)",
        "min": 5,
        "max": 50,
        "step": 1,
    },
    "height": {
        "type": "SliderInt",
        "value": 20,
        "label": "Alto (N)",
        "min": 5,
        "max": 50,
        "step": 1,
    },
    "num_agents": {
        "type": "SliderInt",
        "value": 4,
        "label": "Número de agentes",
        "min": 1,
        "max": 64,
        "step": 1,
    },
    "dirty_fraction": {
        "type": "SliderFloat",
        "value": 0.5,
        "label": "Celdas inicialmente sucias",
        "min": 0,
        "max": 1,
        "step": 0.05,
    },
    "max_steps": {
        "type": "SliderInt",
        "value": 1000,
        "label": "Tiempo máximo (pasos)",
        "min": 10,
        "max": 10000,
        "step": 10,
    },
}

model1 = CleaningModel()

renderer = SpaceRenderer(model1, backend="matplotlib").setup_agents(
    agent_portrayal
)
renderer.render()
renderer.post_process = post_process

clean_plot = make_plot_component("CleanPercentage")
moves_plot = make_plot_component("Moves")

page = SolaraViz(
    model1,
    renderer,
    components=[clean_plot, moves_plot],
    model_params=model_params,
    name="Robot de limpieza reactivo",
)
page  # noqa
