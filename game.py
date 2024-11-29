import pygame
import input
from player import Player
from sprite import sprites, Sprite
from map import Tile, Map
from entity import Entity, active_objects
from physics import Body
from agent import Agent

"""
Ethan Axl Burayag
Ezra Jeonadab Del Rosario
Elisha Jeremy Ong

References:
Assets obtained from: https://github.com/thiagodnf/wumpus-world-simulator
Note: Only sprites were obtained from the github link.
"""

pygame.init()

pygame.display.set_caption("Adventure World")
screen = pygame.display.set_mode((800, 600))

clear_color = (0,0,0)
running = True

# Constants
R, C = 3,4 # Player start position
N = 5 # Map size

player = Entity(Player(), Sprite("images/player_facing_to_down.png"), Body(0, 0, 32, 32), x=C*64, y=R*64)

tile_kinds = [
    Tile("hidden", "images/floor_1.png", False), # 0
    Tile("safe", "images/floor.png", False), # 1
    Tile("gold", "images/floor_gold.png", False), # 2
    Tile("pit", "images/hole.png", False), # 3
    Tile("wall", "images/wall_1.png", True), # 4
    Tile("home", "images/home.png", False) # 5
]

map = Map("maps/test2.txt", tile_kinds, 64)
agent = Agent(map, (R,C), N)

positions = [None]
game_over = None
screen.fill(clear_color)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
            player_pos = player.get(Player).get_tile_position()

            # Check if player quits
            if event.key == pygame.K_ESCAPE:
                game_over = agent.check_win(player_pos, True)
        elif event.type == pygame.KEYUP:
            input.keys_down.remove(event.key)
    
    if not game_over:
        # Update Code
        for a in active_objects:
            a.update()

        # draw
        player_pos = player.get(Player).get_tile_position()
        R, C = player_pos

        if positions[-1] != (R, C): # If player moves
            positions.append((R, C))

            map.reveal_tile(R, C)
            print(map.get_tile_type(R, C))
            agent.query_move(player_pos)
            game_over = agent.check_win(player_pos, False)
            
            # Gold Counter
            font = pygame.font.SysFont("Comic Sans", 24) 
            text_surface = font.render(f"Gold Counter: {agent.get_gold_count()}", True, (255, 215, 0))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2 + 250, 64*(N+2) // 2))
            pygame.draw.rect(screen, clear_color, text_rect)
            screen.blit(text_surface, text_rect)

            print("explored", map.explored_safe, "unexplored", map.unexplored_safe, "unknown", map.unknown)
    
    else:
        map.reveal_all_tiles()

    
    map.draw(screen)

    for sprite in sprites:
        sprite.draw(screen)

    if game_over:
        font = pygame.font.SysFont("Comic Sans", 40) 
        if game_over == "lose":
            text_surface = font.render("You Lose", True, (255, 0, 0))
        else:
            text_surface = font.render("You Win", True, (0, 255, 0))

        text_rect = text_surface.get_rect(center=(64*(N+2) // 2, 64*(N+2) // 2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    pygame.time.delay(17)
pygame.quit()
print(positions)