import pygame

from constants import SCREEN_RESOLUTION, FPS, LIGHT_BLACK
from assets import World

def end_game() -> None:
    pygame.quit()
    quit()


#Init

pygame.init()
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
clock = pygame.time.Clock()

grid = World()

# Timer event

time_delay = 200
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, time_delay)

def game_loop_scene() -> None:
    #Game Loop
    while True:

        clock.tick(FPS)
        screen.fill(LIGHT_BLACK)

        #Events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    end_game()
                if event.key == pygame.K_LEFT:
                    grid.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    grid.move(1, 0)
                if event.key == pygame.K_SPACE:
                    grid.rotate()
            elif event.type == timer_event:
                grid.move(0, 1)

        #Draw
        grid.draw(screen)
        pygame.display.update()


game_loop_scene()