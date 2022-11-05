from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import Automata

def portrayalCell(cell):
    assert cell is not None
    return {
        "Shape": "rect",
        "w": 0.8,
        "h": 0.8,
        "Filled": "true",
        "Layer": 0,
        "x": cell.x,
        "y": cell.y,
        "Color": "pink" if cell.isAlive() else "white",
    }

# Canvas that is 50x50 on a 250x250 display
canvas_element = CanvasGrid(portrayalCell, 50, 50, 500, 500)

server = ModularServer(Automata, [canvas_element], "Automata Celular 1", {"height": 50, "width": 50, "density": UserSettableParameter("slider", "Cell density", 0.1, 0.01, 0.5, 0.01)})

server.launch()
