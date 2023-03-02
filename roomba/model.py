""" 
Ana Paula Katsuda Zalce, A01025303
Karla Valeria Mondragón Rosas, A01025108"""

# Importar
from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import RoombaAgent, ObstacleAgent, GarbageAgent

# Definir modelo
class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, N, width, height, garbageDensity, maxtime):
        self.num_agents = N
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 
        self.time = maxtime
        self.num_roombas = 0

        # obtener datos
        self.datacollector = DataCollector( 
            agent_reporters= {
                "Steps": lambda a: a.steps_taken if isinstance(a, RoombaAgent) else 0
            }, 
            model_reporters= {
                "Trash Cleaned": lambda m: m.countTrash(),
                "Clean Cells": lambda m: m.cleanCells()
            }) 
            
        # Crear borde en el grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]
        # celdas para agregar basura posteriormente
        cells = [(x,y) for y in range(height) for x in range(width)]

        # Agregar obstáculos al borde
        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.grid.place_agent(obs, pos)

        # Agregar agente a la posición (1,1)
        for i in range(self.num_agents):
            roomba = RoombaAgent(i+2000, self)
            self.schedule.add(roomba)
            self.grid.place_agent(roomba, (1,1))
        
        # Agregar basura random en celdas
        i = 0
        for position in cells: 
            trash = GarbageAgent(i+1000, self) 
            if(self.random.random() < garbageDensity and self.grid.is_cell_empty(position)):
                self.grid.place_agent(trash, position)
            i+=1
 
        self.datacollector.collect(self)

    # Función para contar basura
    def countTrash(self):
        counterTrash = 0
        for coord in self.grid.coord_iter():
            for element in coord[0]:
                if(isinstance(element, GarbageAgent)):
                    counterTrash+=1

        return counterTrash 
    
    # Funcion para contar celdas limpias
    def cleanCells(self):
        new_height = self.grid.height - 1
        new_width = self.grid.width - 1 
        return(new_height * new_width - self.countTrash())

    def step(self):
        '''Advance the model by one step.'''
        self.time -= 1
        # Condición de finalización de simulación
        if(self.time==0 or self.countTrash()==0):
            self.running = False 

        self.schedule.step()
        self.datacollector.collect(self)