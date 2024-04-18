import pygame
from enums import GridCell
from display import PyGameDisplay
from game_state import GameState
from player import Player
from agents import *
import time
import sys

GAME_UNITS_W = 37
GAME_UNITS_H = 21
FRAME_DELAY = 0.2

def detect_key_press():
    global running
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                AbstractAgent.last_key_press = 'w'
            if event.key == pygame.K_a:
                AbstractAgent.last_key_press = 'a'
            if event.key == pygame.K_s:
                AbstractAgent.last_key_press = 's'
            if event.key == pygame.K_d:
                AbstractAgent.last_key_press = 'd'

def main():
    # setup game objects
    players = [
        Player(6, 10, GridCell.RED, KeyboardAgent()), # left
        Player(18, 6, GridCell.GREEN, DefaultAgent()), # top
        Player(31, 10, GridCell.BLUE, DefaultAgent()), # right
        Player(18, 15, GridCell.YELLOW, DefaultAgent()) # bottom
    ]

    game_state = GameState(GAME_UNITS_W, GAME_UNITS_H, players)
    display = PyGameDisplay(GAME_UNITS_W, GAME_UNITS_H)

    game_state.start_game()

    # main game loop
    time_old = 0
    while display.running:
        time_now = time.time()
        time_elapsed = time_now - time_old
        detect_key_press()
        if time_elapsed > FRAME_DELAY:
            game_state.update()
            display.render(game_state)
            time_old = time_now

    display.quit()

if __name__ == "__main__":
    main()