"""Modelo de la habitación de MxN celdas con robots de limpieza."""

from mesa import DataCollector, Model
from mesa.discrete_space import OrthogonalMooreGrid

from agents import CleaningRobot, Dirt

START_POSITION = (0, 0)  # Celda [1,1] del enunciado (índices desde 0).


class CleaningModel(Model):
    """Habitación con celdas sucias y robots de limpieza reactivos.

    Atributos:
        width: Número de columnas (M).
        height: Número de filas (N).
        max_steps: Tiempo máximo de ejecución (pasos).
        steps_to_clean: Paso en el que todo quedó limpio, o ``None``.
    """

    def __init__(self, width=20, height=20, num_agents=1,
                 dirty_fraction=0.5, max_steps=1000, rng=None):
        """Crea la habitación, la suciedad y los robots.

        Args:
            width: Número de columnas de la habitación (M).
            height: Número de filas de la habitación (N).
            num_agents: Cantidad de robots.
            dirty_fraction: Fracción de celdas sucias al inicio (0 a 1).
            max_steps: Número máximo de pasos a ejecutar.
            rng: Semilla para reproducir los resultados.
        """
        super().__init__(rng=rng)
        if not 0 <= dirty_fraction <= 1:
            raise ValueError("dirty_fraction debe estar entre 0 y 1")
        if num_agents < 1:
            raise ValueError("num_agents debe ser al menos 1")

        self.width = width
        self.height = height
        self.max_steps = max_steps
        self.total_cells = width * height
        self.steps_to_clean = None
        # Sin bordes que den la vuelta y sin límite de robots por celda.
        self.grid = OrthogonalMooreGrid(
            (width, height), capacity=None, random=self.random, torus=False
        )

        num_dirty = round(dirty_fraction * self.total_cells)
        for cell in self.random.sample(list(self.grid.all_cells), num_dirty):
            Dirt(self, cell)

        start = self.grid[START_POSITION]
        for _ in range(num_agents):
            CleaningRobot(self, start)

        self.datacollector = DataCollector(
            model_reporters={
                "CleanPercentage": lambda m: m.clean_percentage(),
                "Moves": lambda m: m.total_moves(),
            }
        )
        self.running = True
        self.datacollector.collect(self)

    @property
    def robots(self):
        """Conjunto de robots de la simulación."""
        return self.agents_by_type[CleaningRobot]

    def in_bounds(self, coordinate):
        """Indica si ``coordinate`` está dentro de la habitación."""
        x, y = coordinate
        return 0 <= x < self.width and 0 <= y < self.height

    def dirty_cells(self):
        """Número de celdas que siguen sucias."""
        return len(self.agents_by_type.get(Dirt, []))

    def clean_percentage(self):
        """Porcentaje de celdas limpias de la habitación (0 a 100)."""
        clean = self.total_cells - self.dirty_cells()
        return 100 * clean / self.total_cells

    def total_moves(self):
        """Suma de los movimientos realizados por todos los robots."""
        return sum(robot.moves for robot in self.robots)

    def step(self):
        """Avanza un paso: cada robot actúa una vez en orden aleatorio."""
        self.robots.shuffle_do("step")
        self.datacollector.collect(self)

        if self.dirty_cells() == 0:
            self.steps_to_clean = self.steps
            self.running = False
        elif self.steps >= self.max_steps:
            self.running = False

    def run(self):
        """Corre la simulación hasta limpiar todo o llegar al límite.

        Returns:
            Diccionario con las estadísticas finales de la corrida.
        """
        while self.running:
            self.step()
        return self.results()

    def results(self):
        """Estadísticas solicitadas por la actividad."""
        return {
            "agents": len(self.robots),
            "steps": self.steps,
            "all_clean": self.steps_to_clean is not None,
            "clean_percentage": self.clean_percentage(),
            "moves": self.total_moves(),
            "failed_moves": sum(r.failed_moves for r in self.robots),
        }
