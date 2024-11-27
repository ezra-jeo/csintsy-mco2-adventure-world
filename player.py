import pygame
from sprite import Sprite
from input import is_key_pressed
from physics import Body
from entity import active_objects

GRID_SIZE = 64

class Player(): # extends Sprite
    def __init__(self):
        active_objects.append(self)
        self.moving = False

    def update(self):
        previous_x = self.entity.x
        previous_y = self.entity.y

        sprite = self.entity.get(Sprite)
        body = self.entity.get(Body)

        if self.moving:
            if not (is_key_pressed(pygame.K_w) or 
                    is_key_pressed(pygame.K_a) or 
                    is_key_pressed(pygame.K_s) or 
                    is_key_pressed(pygame.K_d)):
                self.moving = False
            return None

        # Process movement if not already moving
        if is_key_pressed(pygame.K_w):
            self.entity.y -= GRID_SIZE
            self.moving = True
        elif is_key_pressed(pygame.K_a):
            self.entity.x -= GRID_SIZE
            self.moving = True
        elif is_key_pressed(pygame.K_s):
            self.entity.y += GRID_SIZE
            self.moving = True
        elif is_key_pressed(pygame.K_d):
            self.entity.x += GRID_SIZE
            self.moving = True

        # Collision validation
        if not body.is_position_valid():
            self.entity.x = previous_x
            self.entity.y = previous_y
        else:
            # Snap to the grid
            self.entity.x = round(self.entity.x / GRID_SIZE) * GRID_SIZE
            self.entity.y = round(self.entity.y / GRID_SIZE) * GRID_SIZE

    def get_tile_position(self):
        tile_col= self.entity.x // GRID_SIZE
        tile_row = self.entity.y // GRID_SIZE 
        
        return tile_row, tile_col





