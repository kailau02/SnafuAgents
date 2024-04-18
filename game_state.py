import numpy as np
from player import Player
from enums import GridCell


class GameState:
    def __init__(self, game_units_w:int, game_units_h:int, players:list[Player]) -> None:
        self.grid = np.zeros((game_units_h, game_units_w))
        self.players = players

    def get_games_completed(self):
        n_games = 0
        for player in self.players:
            n_games += player.n_wins
        return n_games

    def clear_grid(self) -> None:
        self.grid = np.zeros(self.grid.shape)

    def set_grid_cell(self, row, col, val_enum:GridCell=None, val_int:int=None) -> None:
        if val_enum:
            self.grid[row][col] = val_enum.value
        elif val_int:
            self.grid[row][col] = val_int
        else:
            raise Exception("Error: No grid value provided in `set_grid_cell` method call.")

    def grid_as_enum(self) -> np.ndarray:
        mapping = {
            0: GridCell.EMPTY,
            1: GridCell.RED,
            2: GridCell.YELLOW,
            3: GridCell.GREEN,
            4: GridCell.BLUE
        }

        enum_grid = np.vectorize(mapping.get)(self.grid)
        return enum_grid

    def start_game(self) -> None:
        self.clear_grid()
        for player in self.players:
            player.spawn()

    def is_death_cell(self, row:int, col:int) -> bool:
        # out of bounds
        if col < 0 or row < 0 or col >= self.grid.shape[1] or row >= self.grid.shape[0]:
            return True
            
        # collision with existing color
        elif self.grid[row, col] != GridCell.EMPTY.value:
            return True

    def update(self) -> None:
        # update player positions
        for player in self.players:
            player.on_update(self)
        
        # check for player collisions
        player_death_indexes = []
        for i in range(0, len(self.players)):
            if not self.players[i].is_alive:
                continue
            p_row, p_col = self.players[i].position

            # location out of bounds or hitting a color
            if self.is_death_cell(row=p_row, col=p_col):
                player_death_indexes.append(i)

            # head-on collision with enemy
            for j in range(i+1, len(self.players)):
                if i == j:
                    continue
                if (self.players[i].position == self.players[j].position).all():
                    if i not in player_death_indexes:
                        player_death_indexes.append(i)
                    if j not in player_death_indexes:
                        player_death_indexes.append(j)
            

        # show/remove players colors from game:
        for i, player in enumerate(self.players):
            if i in player_death_indexes: # execute player death
                player.is_alive = False
                self.grid = np.where(self.grid == player.cell_color.value, 0, self.grid)
            
            elif player.is_alive: # draw new player position
                self.grid[player.position[0], player.position[1]] = player.cell_color.value
        
        # check for end of game
        sum_alive = sum([p.is_alive for p in self.players])
        if sum_alive == 1:
            for player in self.players:
                if player.is_alive:
                    player.n_wins += 1
                    break
        if sum_alive <= 1:
            self.start_game()
