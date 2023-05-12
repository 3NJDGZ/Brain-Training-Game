import mysql.connector
import pygame_gui
import pygame
import sys

pygame.init()

# Initialise Variables for Pygame
WIDTH = 1280
TILE = 100
HEIGHT = 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
cols = WIDTH // TILE
rows = HEIGHT // TILE
pygame.display.set_caption("User Customisation")
CLOCK = pygame.time.Clock()
screen_colour = (191, 191, 191)

# Pygame_GUI
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'Theme/theme.json')

# Connect to host root server on computer 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="MainDB"
)
# Setup cursor to execute SQL commands on DB
mycursor = db.cursor()

def show_text(text):
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        WIN.fill(screen_colour)
        new_text = pygame.font.SysFont("bahnschrift", 50).render(f"You have successfully registered {text}!", True, "black")
        new_text_rect = new_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        WIN.blit(new_text, new_text_rect)

        CLOCK.tick(60)

        pygame.display.update()

# Used to register and log the new player on the database
def register(username, password):
    if len(username) > 0 and len(password) > 0:
        mycursor.execute(f"""
        INSERT INTO Player (Username, Password)
        VALUES ('{username}', '{password}');
        """)

        mycursor.execute("""
        SELECT *
        FROM Player;
        """)
        for x in mycursor:
            print(x)

        show_text(username)

def register_screen():
    # Base Variables
    running = True
    UI_REFRESH_RATE = CLOCK.tick(60)/20000
    username = ""
    password = ""

    # UI
    USERNAME_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)-70)), (400, 50)), manager = MANAGER, object_id="#username_text_entry")
    PASSWORD_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)+30)), (400, 50)), manager = MANAGER, object_id="#password_text_entry")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            # Checks if the User has changed the fields within the corresponding boxes
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
                username = event.text
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
                password = event.text
            
            # Checks if the user has pressed 'ENTER' and then stores their input username and password
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                print(f"Username: {username}, Password: {password}")
                register(username, password)
            
            
            MANAGER.process_events(event)

        WIN.fill(screen_colour)
        MANAGER.update(UI_REFRESH_RATE)
        MANAGER.draw_ui(WIN)
        pygame.display.update()

def intro_screen():
    running = True

    # UI
    UI_REFRESH_RATE = CLOCK.tick(60)
    LOGIN_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, HEIGHT/2+50), (200, 75)), manager=MANAGER, object_id="#login_button", text="LOGIN")
    REGISTER_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((690, HEIGHT/2+50), (200, 75)), manager=MANAGER, object_id="#register_button", text="REGISTER")
    TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((390, HEIGHT/2-100), (500, 75)), manager=MANAGER, object_id="#title_label", text="BRAIN TRAINING GAME")

    while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#login_button":
                    print("Login button pressed")
                    running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#register_button":
                    print("Register button pressed")
                    running = False          

                MANAGER.process_events(event)

            MANAGER.update(UI_REFRESH_RATE)

            WIN.fill(screen_colour)
            MANAGER.draw_ui(WIN)
            pygame.display.update()

intro_screen()
