import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Leaderboard")

font = pygame.font.Font(None, 36)
scores = [("Player1", 100), ("Player2", 75), ("Player3", 50)]  # Example scores

def display_scores():
    screen.fill((0, 0, 0))
    for idx, (name, score) in enumerate(scores):
        text = font.render(f"{idx+1}. {name}: {score}", True, (255, 255, 255))
        screen.blit(text, (50, 50 + idx * 50))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_scores()
    pygame.display.flip()
    pygame.time.delay(100)  # Add a small delay to control frame rate

pygame.quit()
