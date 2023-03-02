'''
Ana Paula Katsuda Zalce, A01025303
Karla Valeria Mondragón Rosas, A01025108

Agent file for Roomba Simulation 
'''
from mesa import Agent

"""
Creates a new random agent.
Args:
    unique_id: The agent's ID
    model: Model reference for the agent
"""
# Definir agente
class RoombaAgent(Agent):
    def __init__(self, unique_id, model, type="roomba"):
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        self.type = type

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        # CHecar pasos posibles
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True) 

        # Checks which grid cells are empty
        freeSpaces =list(map(self.model.grid.is_cell_empty, possible_steps)) 
        next_moves1 = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
        # Lista de agentes vecinos
        neighList = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)

        
        if(len(next_moves1) > 0):
            next_move = self.random.choice(next_moves1)
        else:
            next_move = self.pos
        # 
        for neighbor in neighList:
            if(isinstance(neighbor, GarbageAgent) and neighbor.pos == self.pos):
                self.clean(neighbor)
            elif(isinstance(neighbor, GarbageAgent) and neighbor.pos != self.pos):
                next_move = neighbor.pos
        
        # Now move:
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken+=1
    
    def clean(self, agent):
        self.model.grid.remove_agent(agent)
    
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        self.move()

"""
Creates a new garbage agent.
"""
class GarbageAgent(Agent):
    def __init__(self, model, unique_id, type="trash"):
        super().__init__(unique_id, model)
        self.type = type
    
    def step(self):
        pass

"""
Obstacle agent. Just to add obstacles to the grid.
"""
class ObstacleAgent(Agent):
    def __init__(self, unique_id, model, type="obstacle"):
        super().__init__(unique_id, model)
        self.type = type

    def step(self):
        pass  