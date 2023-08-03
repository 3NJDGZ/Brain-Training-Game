import pygame
import sys

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("One-Time Key Press")

clock = pygame.time.Clock()

def handle_events():
    global key_pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not key_pressed:
                print("Space key pressed!")
                # Add your desired action here
                key_pressed = True

key_pressed = False

while True:
    screen.fill((255, 255, 255))

    handle_events()

    pygame.display.update()

    clock.tick(60)
