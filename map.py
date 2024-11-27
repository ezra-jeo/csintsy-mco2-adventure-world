import pygame
import math

map = None

class Tile:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        global map
        self.tile_kinds = tile_kinds
        self.tile_size = tile_size
        self.breeze_pos = set()
        self.glitter_pos = set()
        self.unexplored_safe = set()
        self.explored_safe = set()
        self.unknown = set()


        self.font = pygame.font.SysFont("Arial", 14)

        map = self

        with open(map_file, "r") as file:
            data = file.read()

        self.tiles = []
        self.hidden_layer = []  # Hidden layer to track visibility

        data = data.split("\n")

        for r, line in enumerate(data):
            row = []
            hidden_row = []
            for c, tile_number in enumerate(line.strip()):
                n = len(data)
                row.append(int(tile_number))

                if int(tile_number) != 4:
                    hidden_row.append(True)  # Initially, all tiles are hidden except walls
                else:
                    hidden_row.append(False)

                # Check if pit or gold to add markers
                if int(tile_number) == 2:
                    #self.add_glitter(r, c, n)
                    self.glitter_pos.add((r, c))
                elif int(tile_number) == 3:
                    self.add_breeze(r, c, n)

            self.tiles.append(row)
            self.hidden_layer.append(hidden_row)


    def add_breeze(self, row, col, n):
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for DR, DC in neighbors:
            if 1 <= row + DR < n-1 and 1 <= col + DC < n-1:
                self.breeze_pos.add((row + DR, col + DC))

        
    # def add_glitter(self, row, col, n):
    #     neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    #     for DR, DC in neighbors:
    #         if 1 <= row + DR < n-1 and 1 <= col + DC < n-1:
    #             self.glitter_pos.add((row + DR, col + DC))


    # Collision
    def is_point_solid(self, x, y):
        x_tile = int(x / self.tile_size)
        y_tile = int(y / self.tile_size)

        if x_tile < 0 or y_tile < 0 or \
           y_tile >= len(self.tiles) or \
           x_tile >= len(self.tiles[y_tile]):
            return False
        tile = self.tiles[y_tile][x_tile]

        return self.tile_kinds[tile].is_solid

    def is_rect_solid(self, x, y, width, height):
        x_checks = int(math.ceil(width / self.tile_size))
        y_checks = int(math.ceil(height / self.tile_size))

        for yi in range(y_checks):
            for xi in range(x_checks):
                x = xi * self.tile_size + x
                y = yi * self.tile_size + y
                if self.is_point_solid(x, y):
                    return True
        return False

    # Hidden tiles
    def reveal_tile(self, tile_row, tile_col):
        if 0 <= tile_row < len(self.hidden_layer) and 0 <= tile_col < len(self.hidden_layer[0]):
            self.hidden_layer[tile_row][tile_col] = False
    
    def reveal_all_tiles(self):
        for y, row in enumerate(self.hidden_layer):
            for x, _ in enumerate(row):
                self.hidden_layer[y][x] = False

    def is_tile_hidden(self, tile_row, tile_col):
        if 0 <= tile_row < len(self.hidden_layer) and 0 <= tile_col < len(self.hidden_layer[0]):
            return self.hidden_layer[tile_row][tile_col]
        return False

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size, y * self.tile_size)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)

                # Draw "S" for explored safe
                if (y, x) in self.explored_safe:
                    text = "S"
                    text_surface = self.font.render(text, True, (0, 255, 0)) 
                    text_rect = text_surface.get_rect(center=(location[0] + self.tile_size // 2, (location[1] + self.tile_size // 2)))
                    screen.blit(text_surface, text_rect)
                
                # Draw "Breeze" if applicable
                if (y, x) in self.breeze_pos:
                    text = "Breeze"
                    text_surface = self.font.render(text, True, (135, 206, 235)) 
                    text_rect = text_surface.get_rect(center=(location[0] + self.tile_size // 2, (location[1] + self.tile_size // 2)-20))
                    screen.blit(text_surface, text_rect)

                # Draw "Glitter" if applicable
                if (y, x) in self.glitter_pos:
                    text = "Glitter"
                    text_surface = self.font.render(text, True, (255, 215, 0)) 
                    text_rect = text_surface.get_rect(center=(location[0] + self.tile_size // 2, (location[1] + self.tile_size // 2)+20))
                    screen.blit(text_surface, text_rect)

                base_y = location[1] + self.tile_size // 2
                # Draw overlay if tile is hidden
                if self.is_tile_hidden(y, x): # If hidden 
                    overlay = self.tile_kinds[0].image
                    screen.blit(overlay, location)
                    
                    # Draw "US" for unexplored safe 
                    if (y, x) in self.unexplored_safe:
                        text = "US"
                        text_surface = self.font.render(text, True, (255, 255, 255)) 
                        text_rect = text_surface.get_rect(center=(location[0] + self.tile_size // 2, base_y))
                        screen.blit(text_surface, text_rect)
                    # Draw "US" for unexplored safe 
                    elif (y, x) in self.unknown:
                        text = "?"
                        text_surface = self.font.render(text, True, (255, 0, 0)) 
                        text_rect = text_surface.get_rect(center=(location[0] + self.tile_size // 2, base_y))
                        screen.blit(text_surface, text_rect)




    def get_tile_type(self, player_row, player_col):
        return self.tile_kinds[self.tiles[player_row][player_col]].name

