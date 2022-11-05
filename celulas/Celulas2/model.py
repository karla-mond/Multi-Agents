from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import Grid

from agent import Cell

class Automata(Model):
    """ 
    Automata Celular
    """
    def __init__(self, height=50, width=50, density=0.5):
        
        self.schedule = SimultaneousActivation(self)
        self.grid = Grid(height, width, torus=True)

        for(contents, x, y) in self.grid.coord_iter():
            new_cell = Cell((x, y), self)
            if self.random.random() < density:
                new_cell.state = new_cell.ALIVE
            self.grid.place_agent(new_cell, (x,y))
            self.schedule.add(new_cell)
        
        self.running = True
    
    def step(self):
        self.schedule.step()