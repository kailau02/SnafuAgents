import random
import numpy as np
from enums import Direction, GridCell


class Player:
    def __init__(self, x_spawn:int, y_spawn:int, cell_color:GridCell, agent) -> None:
        self.n_wins = 0
        self.is_alive = False
        self.cell_color = cell_color
        self.x_spawn = x_spawn
        self.y_spawn = y_spawn
        self.position = np.array([y_spawn, x_spawn])
        self.dir = Direction.UP
        self.agent = agent
    
    def spawn(self) -> None:
        self.position = np.array([self.y_spawn, self.x_spawn])
        self.is_alive = True
        self.dir = random.choice([Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT])

    def get_next_direction(self, game_state) -> Direction:
        return self.agent.get_next_direction(self, game_state)

    def on_update(self, game_state) -> None:
        if not self.is_alive:
            return
        
        # get input for next direction
        next_dir = self.get_next_direction(game_state)
        if (self.dir == Direction.UP and next_dir == Direction.DOWN) or \
           (self.dir == Direction.RIGHT and next_dir == Direction.LEFT) or \
           (self.dir == Direction.DOWN and next_dir == Direction.UP) or \
           (self.dir == Direction.LEFT and next_dir == Direction.RIGHT):
            print("WARNING: player switched directions a full 180 degrees")
        
        self.dir = next_dir

        # move player based on their direction
        if self.dir == Direction.UP:
            self.position[0] -= 1
        elif self.dir == Direction.RIGHT:
            self.position[1] += 1
        elif self.dir == Direction.DOWN:
            self.position[0] += 1
        elif self.dir == Direction.LEFT:
            self.position[1] -= 1
        else:
            raise Exception("Invalid Direction found in on_update method")