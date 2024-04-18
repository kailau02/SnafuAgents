from enum import Enum

class GridCell(Enum):
    EMPTY = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

