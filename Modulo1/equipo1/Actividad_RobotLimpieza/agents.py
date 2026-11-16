"""Agentes de la simulación del robot de limpieza reactivo.

Contiene dos tipos de agentes:

* ``Dirt``: suciedad fija en una celda; desaparece cuando la aspiran.
* ``CleaningRobot``: robot reactivo que aspira si su celda está sucia y,
  si no, intenta moverse a una de sus 8 celdas vecinas al azar.
"""

from mesa.discrete_space import CellAgent, FixedAgent

# Desplazamientos hacia las 8 celdas vecinas (vecindad de Moore).
DIRECTIONS = (
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1),
)


class Dirt(FixedAgent):
    """Representa una celda sucia de la habitación."""

    def __init__(self, model, cell):
        """Crea la suciedad en la celda indicada.

        Args:
            model: Modelo al que pertenece el agente.
            cell: Celda de la cuadrícula donde se coloca la suciedad.
        """
        super().__init__(model)
        self.cell = cell


class CleaningRobot(CellAgent):
    """Robot reactivo: solo percibe si su celda actual está sucia.

    Atributos:
        moves: Número de veces que el robot cambió de celda.
        failed_moves: Intentos de moverse fuera de la habitación.
        cleaned: Número de celdas que el robot aspiró.
    """

    def __init__(self, model, cell):
        """Crea el robot en la celda indicada con sus contadores en cero.

        Args:
            model: Modelo al que pertenece el agente.
            cell: Celda inicial del robot.
        """
        super().__init__(model)
        self.cell = cell
        self.moves = 0
        self.failed_moves = 0
        self.cleaned = 0

    @property
    def dirt_here(self):
        """Suciedad presente en la celda actual, o ``None`` si está limpia."""
        for agent in self.cell.agents:
            if isinstance(agent, Dirt):
                return agent
        return None

    def step(self):
        """Ejecuta una acción: aspirar o intentar moverse."""
        dirt = self.dirt_here
        if dirt is not None:
            self.vacuum(dirt)
        else:
            self.move_randomly()

    def vacuum(self, dirt):
        """Aspira la suciedad de la celda actual.

        Args:
            dirt: Agente ``Dirt`` que se elimina de la simulación.
        """
        dirt.remove()
        self.cleaned += 1

    def move_randomly(self):
        """Elige una de las 8 direcciones y se mueve si es posible.

        Si la celda destino queda fuera de la habitación, el robot
        permanece en la misma celda.
        """
        x, y = self.cell.coordinate
        dx, dy = self.random.choice(DIRECTIONS)
        target = (x + dx, y + dy)
        if not self.model.in_bounds(target):
            self.failed_moves += 1
            return
        self.cell = self.model.grid[target]
        self.moves += 1
