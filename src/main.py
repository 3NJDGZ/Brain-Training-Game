import mysql.connector
import pygame_gui
import pygame
import sys


pygame.init()

# Initialise Variables for Pygame
WIDTH = 1280
TILE = 100
HEIGHT = 720
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Brain Training Game")

# Pygame_GUI
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'src/Theme/theme.json')

# Connect to host root server on computer 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="MainDB"
)
# Setup cursor to execute SQL commands on DB
mycursor = db.cursor()

class Screen:
    def __init__(self, Title: str):
        self.Title = Title
        self._WIDTH = 1280
        self._HEIGHT = 720
        self._WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self._UI_REFRESH_RATE = CLOCK.tick(60)
        self._screen_colour = (191, 191, 191)
    
    def _get_WIN(self):
        return self._WIN

    def _fill_with_colour(self):
        self._WIN.fill((self._screen_colour))

class Intro_Screen(Screen):
    def __init__(self, Title: str):
        super(Intro_Screen, self).__init__(Title)
        # UI
        self.__LOGIN_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, HEIGHT/2+50), (200, 75)), manager=MANAGER, object_id="#login_button", text="LOGIN")
        self.__REGISTER_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((690, HEIGHT/2+50), (200, 75)), manager=MANAGER, object_id="#register_button", text="REGISTER")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((390, HEIGHT/2-100), (500, 75)), manager=MANAGER, object_id="#title_label", text="BRAIN TRAINING GAME")

    def check_for_button_pressed(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#login_button":
                return "Login"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#register_button":
                return "Register"

            MANAGER.process_events(event)
        return None

    def remove_UI_elements(self):
        self.__LOGIN_BUTTON.hide()
        self.__REGISTER_BUTTON.hide()
        self.__TITLE_LABEL.hide()
    
    def show_UI_elements(self):
        self.__LOGIN_BUTTON.visible = True
        self.__REGISTER_BUTTON.visible = True
        self.__TITLE_LABEL.visible = True

class Register_Screen(Screen):
    def __init__(self, Title: str):
        super().__init__(Title)
        # UI
        self.__USERNAME_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)-70)), (400, 50)), manager = MANAGER, object_id="#username_text_entry")
        self.__PASSWORD_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)+30)), (400, 50)), manager = MANAGER, object_id="#password_text_entry")
        self.__GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=MANAGER, object_id="#go_back_button", text="GO BACK")

        # Other
        self.__username = ""
        self.__password = ""
    
    def set_username(self, username):
        self.__username = username
    
    def set_password(self, password):
        self.__password = password
    
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password

    def check_for_user_interaction_with_ui(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
                self.set_username(event.text)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
                self.set_password(event.text)
            
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                self.register(self.get_username(), self.get_password())
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                return True

            MANAGER.process_events(event)
    
    def register(self, username, password):
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
    
    def remove_UI_elements(self):
        self.__USERNAME_INPUT.hide()
        self.__PASSWORD_INPUT.hide()
        self.__GO_BACK_BUTTON.hide()
    
    def show_UI_elements(self):
        self.__USERNAME_INPUT.visible = True
        self.__PASSWORD_INPUT.visible = True
        self.__GO_BACK_BUTTON.visible = True

class Game:
    def __init__(self):
        self.__UI_REFRESH_RATE = CLOCK.tick(60)/10000

        # Screens
        self.__intro_screen = Intro_Screen("Intro!")
        self.__register_screen = Register_Screen("Register!")
        self.screens = [self.__intro_screen, self.__register_screen]
        self.__current_pos = 0
        self.__current_screen = self.screens[self.__current_pos]

    def get(self):
        return self.__current_pos

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                
                MANAGER.process_events(event)
        
            self.__current_screen = self.screens[self.__current_pos]
            self.__current_screen.show_UI_elements()
            
            self.update_UI_screen()
            self.__current_screen._fill_with_colour()

            # Check if current screen is the Intro Screen
            if isinstance(self.__current_screen, Intro_Screen):

                # Check which button is pressed by user
                button_pressed = self.__current_screen.check_for_button_pressed()

                # Functionality not yet implemented for the login button
                if button_pressed == "Login":
                    print("Login")
                
                # if register button pressed remove the UI elements of the intro (current) screen and set state to register_screen
                elif button_pressed == "Register":
                    self.__current_screen.remove_UI_elements()
                    self.__current_pos += 1
            
            # Check if current screen is the Register Screen
            if not isinstance(self.__current_screen, Register_Screen):

                # Set visibility of register_screen UI as false (current screen will not be register_screen)
                self.__register_screen.remove_UI_elements()

            else:

                # Current Screen will now be register_screen so we can now set its UI elements' visibility to True
                self.__current_screen.show_UI_elements()

                # Check if the go_back button is pressed
                if self.__current_screen.check_for_user_interaction_with_ui():

                    # if pressed, remove UI elements of register (current) screen and set state back to intro_screen
                    self.__current_screen.remove_UI_elements()
                    self.__current_pos -= 1
        
                    

            self.draw_UI(self.__current_screen)
            self.update_screen()
    
    def update_screen(self):
        pygame.display.update()

    def update_UI_screen(self):
        MANAGER.update(self.__UI_REFRESH_RATE)
    
    def draw_UI(self, screen: Screen):
        MANAGER.draw_ui(screen._get_WIN())
    
brain_training_game = Game()
brain_training_game.play()