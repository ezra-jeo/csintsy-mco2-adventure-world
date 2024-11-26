import pygame
import input

pygame.init()

pygame.display.set_caption("Adventure World")
screen = pygame.display.set_mode((800, 600))

clear_color = (0,0,0)
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            input.keys_down.add(event.key)
        elif event.type == pygame.KEYUP:
            input.keys_down.remove(event.key)

            
    # Draw
    screen.fill(clear_color)

    pygame.display.flip()
pygame.quit()