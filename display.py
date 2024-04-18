import pygame
from pygame import Rect
from game_state import GameState, GridCell

UNIT_SIZE = 20

BORDER_THICK = 40
BORDER_THIN = 20
SCORES_HEIGHT = 40

FONT_SIZE = 55

BORDER_COLOR = (0, 176, 0)
RED = (232, 0, 0)
YELLOW = (252, 224, 24)
GREEN = (192, 208, 116)
BLUE = (0, 0, 220)

CELL_STATE_TO_COLOR = {
    GridCell.RED: RED,
    GridCell.YELLOW: YELLOW,
    GridCell.GREEN: GREEN,
    GridCell.BLUE: BLUE
}

class PyGameDisplay:
    def __init__(self, game_units_w:int, game_units_h:int) -> None:
        # store screen dimensions
        self.game_units_w = game_units_w
        self.game_units_h = game_units_h

        self.screen_w = (BORDER_THICK * 2) + (self.game_units_w * UNIT_SIZE)
        self.screen_h = (BORDER_THIN * 2) + BORDER_THICK + SCORES_HEIGHT + (self.game_units_h * UNIT_SIZE)

        self.game_x_offset = BORDER_THICK
        self.game_y_offset = BORDER_THIN

        # init pygame
        pygame.init()
        pygame.display.set_caption('Snafu AI')
        self.screen = pygame.display.set_mode([self.screen_w, self.screen_h])
        self.font = pygame.font.Font('Pixel Intv.otf', FONT_SIZE)

        self.running = True

    def draw_static_ui(self) -> None:
        self.screen.fill((168, 168, 168))

        # draw borders
        pygame.draw.rect(self.screen, BORDER_COLOR, Rect(0, 0, BORDER_THICK, self.screen_h)) # LEFT
        pygame.draw.rect(self.screen, BORDER_COLOR, Rect(0, 0, self.screen_w, BORDER_THIN)) # TOP
        pygame.draw.rect(self.screen, BORDER_COLOR, Rect(self.screen_w-BORDER_THICK, 0, BORDER_THICK, self.screen_h)) # RIGHT
        pygame.draw.rect(self.screen, BORDER_COLOR, Rect(0, self.screen_h-BORDER_THIN, self.screen_w, BORDER_THIN)) # BOTTOM

        pygame.draw.rect(self.screen, BORDER_COLOR, Rect(0, self.screen_h-BORDER_THIN-SCORES_HEIGHT-BORDER_THICK, self.screen_w, BORDER_THICK)) # DIVIDER

    def draw_dynamic_ui(self, game_state:GameState) -> None:
        # draw player colors
        grid = game_state.grid_as_enum()
        for row in range(self.game_units_h):
            for col in range(self.game_units_w):
                cell_state = grid[row][col]
                if cell_state != GridCell.EMPTY:
                    x_pos = self.game_x_offset + (col * UNIT_SIZE)
                    y_pos = self.game_y_offset + (row * UNIT_SIZE)
                    pygame.draw.rect(self.screen, CELL_STATE_TO_COLOR[cell_state], Rect(x_pos, y_pos, UNIT_SIZE, UNIT_SIZE))
        
        # draw scoreboard
        scores_left = BORDER_THICK
        scores_top = BORDER_THIN+BORDER_THICK + (self.game_units_h*UNIT_SIZE)
        scores_width = self.game_units_w * UNIT_SIZE

        games_text = [self.font.render(str(game_state.get_games_completed()), True, (255, 255, 255))]
        score_texts = [self.font.render(str(p.n_wins), True, CELL_STATE_TO_COLOR[p.cell_color]) for p in game_state.players]
        all_texts = games_text + score_texts
        sum_text_widths = sum([text.get_width() for text in all_texts])
        n_texts = len(all_texts)
        x_spacing = (scores_width - sum_text_widths) // (n_texts + 1)

        x_pos = scores_left
        for text in all_texts:
            x_pos += x_spacing
            self.screen.blit(text, (x_pos, scores_top-15))
            x_pos += text.get_width()


    def render(self, game_state:GameState) -> bool:
        if not self.running:
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return False

        self.draw_static_ui()
        self.draw_dynamic_ui(game_state)

        # render everything to the screen
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
