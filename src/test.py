# # Reset auto increment of PlayerID in Player Entity
# def reset_auto_increment(x: int):
#     # Connect to host root server on computer 
#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         passwd="password",
#         database="MainDB"
#     )
#     # Setup cursor to execute SQL commands on DB
#     mycursor = db.cursor()

#     mycursor.execute(f"""
#     ALTER TABLE Player 
#     AUTO_INCREMENT = {x};
#     """)
#     db.commit()
#     db.close()

# reset_auto_increment(3)

import pygame
pygame.init()
# Create a surface with width 400 and height 300
sample_surface = pygame.display.set_mode((400, 300))
# Fill the surface with white color
sample_surface.fill((255, 255, 255))
# Create a subsurface inside the parent surface with width 100 and height 100
sub_surface = sample_surface.subsurface(pygame.Rect(50, 50, 100, 100))
# Fill the subsurface with red color
sub_surface.fill((255, 0, 0))
# Update the display
pygame.display.flip()

# Wait for the user to close the window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()

