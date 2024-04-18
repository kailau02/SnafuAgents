import numpy as np
from abc import ABC, abstractmethod
from player import Player
from game_state import GameState
from enums import Direction
import random

class AbstractAgent(ABC):
    # static variable
    last_key_press = 'd'

    @classmethod
    def calc_next_pos(cls, player:Player, dir:Direction) -> np.ndarray:
        next_pos = np.copy(player.position)
        if dir == Direction.UP:
            next_pos[0] -= 1
        elif dir == Direction.RIGHT:
            next_pos[1] += 1
        elif dir == Direction.DOWN:
            next_pos[0] += 1
        elif dir == Direction.LEFT:
            next_pos[1] -= 1
        return next_pos
    
    @abstractmethod
    def get_next_direction(cls, player:Player, game_state:GameState) -> Direction:
        pass



class KeyboardAgent(AbstractAgent):

    @classmethod
    def get_next_direction(cls, player:Player, game_state:GameState) -> Direction:
        key = AbstractAgent.last_key_press
        if key == 'w':
            return Direction.UP
        elif key == 'd':
            return Direction.RIGHT
        elif key == 's':
            return Direction.DOWN
        elif key == 'a':
            return Direction.LEFT
        else:
            raise Exception("Invalid state in get_next_direction in KeyboardAgent")



class DefaultAgent(AbstractAgent):

    @classmethod
    def get_next_direction(cls, player:Player, game_state: GameState) -> Direction:
        curr_dir = player.dir
        next_pos = AbstractAgent.calc_next_pos(player, curr_dir)

        if not game_state.is_death_cell(next_pos[0], next_pos[1]):
            return curr_dir
        
        dirs = random.sample([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT], 4)
        for dir in dirs:
            next_pos = AbstractAgent.calc_next_pos(player, dir)
            if not game_state.is_death_cell(next_pos[0], next_pos[1]):
                return dir
            
        return curr_dir