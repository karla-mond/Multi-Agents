from mesa import Agent

class Cell(Agent):

    """Represents a single ALIVE or DEAD cell in the simulation."""
    DEAD = 0
    ALIVE = 1

    def __init__(self, pos, model, init_state=DEAD):
        # Create a cell in the given state at a given position
        super().__init__(pos, model)
        self.x, self.y = pos
        self.state = init_state
        self._nextState = None
    
    def isAlive(self):
        return self.state == self.ALIVE

    def neighbors(self):
        # returns an iterator of all neighbors 
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def step(self):
        upNeighbors = []
        
        for neighbor in self.neighbors():
            #if(self.y)
            if ((self.y+1)%50==neighbor.y and neighbor.isAlive()): 
                upNeighbors.append(1)
            elif((self.y+1)%50==neighbor.y and not neighbor.isAlive()): 
                upNeighbors.append(0)

        self._nextState = self.state
        
        # Assume nextState is unchanged, unless changed below.
        if upNeighbors == [0,0,0]:
            self._nextState = self.DEAD
        elif upNeighbors == [0,0,1]:
            self._nextState = self.ALIVE
        elif upNeighbors == [0,1,0]:
            self._nextState = self.DEAD
        elif upNeighbors == [0,1,1]:
            self._nextState = self.ALIVE
        elif upNeighbors == [1,0,0]:
            self._nextState = self.ALIVE
        elif upNeighbors == [1,0,1]:
            self._nextState = self.DEAD
        elif upNeighbors == [1,1,0]:
            self._nextState = self.ALIVE
        elif upNeighbors == [1,1,1]:
            self._nextState = self.DEAD

    def advance(self):
        """
        Set the state to the new computed state -- computed in step().
        """
        self.state = self._nextState
        
