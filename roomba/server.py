"""
Tiempo necesario hasta que todas las celdas estén limpias (o se haya llegado al tiempo máximo).
Porcentaje de celdas limpias después del termino de la simulación.
Número de movimientos realizados por todos los agentes.

Ana Paula Katsuda Zalce, A01025303
Karla Valeria Mondragón Rosas, A01025108
"""

# Importar librerías
from model import RandomModel, ObstacleAgent, GarbageAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter # set params

# Visualización del agente
def agent_portrayal(agent):
    if agent is None: return
    # Manera de mostrar al agente --> Roomba
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "green",
                 "r": 0.5}
    # Para los obstáculos, definir cómo mostrarlos
    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3
    # Para la basura, definir cómo mostrarla
    if (isinstance(agent, GarbageAgent)):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3

    return portrayal

# Pedir al usuario el ancho y alto del grid (en la terminal)
widthParam = int(input("Elige el ancho: "))
heightParam = int(input("Elige el alto: "))

# Definir parámetros del modelo
model_params = {"N":UserSettableParameter("number", "Number of Roombas", value = 5), "width":widthParam, "height":heightParam, "garbageDensity": UserSettableParameter("slider", "Garbage density", 0.1, 0.01, 1.0, 0.01), "maxtime": UserSettableParameter("number", "Maximum Time", value=5000)}

# Definir grid
grid = CanvasGrid(agent_portrayal, widthParam, heightParam, 500, 500)

# Gráfico de barras para pasos por cada roomba
bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"green"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

# Gráfico de pastel para radio entre celdas limpias y sucias
pie_chart = PieChartModule(
    [{"Label":"Trash Cleaned", "Color":"#AA0000"}, {"Label":"Clean Cells", "Color":"blue"}])

# Definir servidor
server = ModularServer(RandomModel, [grid, bar_chart, pie_chart], "Random Agents", model_params)
                       
server.port = 8521 # Default
server.launch() 