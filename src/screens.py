import pygame
import pygame_gui
import mysql.connector
from abc import ABC, abstractmethod

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

# Reset auto increment of PlayerID in Player Entity
def reset_auto_increment(x: int):
    mycursor.execute(f"""
    ALTER TABLE Player 
    AUTO_INCREMENT = {x};
    """)
    db.commit()
    db.close()

# reset_auto_increment(5)

class Screen(ABC):
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
    
    @abstractmethod
    def show_UI_elements(self):
        pass

    @abstractmethod
    def remove_UI_elements(self):
        pass


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
        super(Register_Screen, self).__init__(Title)
        # UI
        self.__USERNAME_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)-70)), (400, 50)), manager = MANAGER, object_id="#username_text_entry")
        self.__PASSWORD_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)+30)), (400, 50)), manager = MANAGER, object_id="#password_text_entry")
        self.__GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=MANAGER, object_id="#go_back_button", text="GO BACK")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((465, 150), (350, 75)), manager=MANAGER, object_id="#title_label", text="REGISTER MENU")

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
        ui_finished = ""
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
                self.set_username(event.text)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
                self.set_password(event.text)
            
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                self.register(self.get_username(), self.get_password())
                ui_finished = "TEXT_ENTRY"
                return ui_finished
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
                return ui_finished

            MANAGER.process_events(event)
    
    def register(self, username, password):
        successful_registration = False
        if len(username) > 0 and len(password) > 0:
            mycursor.execute(f"""
            INSERT INTO Player (Username, Password)
            VALUES ('{username}', '{password}');
            """)

            # Fetch PlayerID of the newly registered Player from the Player Entity
            mycursor.execute(f"""
            SELECT PlayerID
            FROM Player
            WHERE Player.Username = '{username}'
            AND Player.Password = '{password}'
            """)
            for x in mycursor:
                current_player_id = x[0]

            # Set up default information in Weights Entity 
            mycursor.execute(f"""
            INSERT INTO WEIGHTS (PlayerID, CognitiveAreaID, WeightValue)
            VALUES ({current_player_id}, 1, 0.25),
            ({current_player_id}, 2, 0.25),
            ({current_player_id}, 3, 0.25),
            ({current_player_id}, 4, 0.25);
            """)

            # Set up default information in Performance Entity
            mycursor.execute(f"""
            INSERT INTO Performance (PlayerID, CognitiveAreaID, Score)
            VALUES ({current_player_id}, 1, 0),
            ({current_player_id}, 2, 0),
            ({current_player_id}, 3, 0),
            ({current_player_id}, 4, 0)
            """)

            # Commit Changes to DB
            # db.commit()
            # db.close()

            successful_registration = True
        return successful_registration
    
    def remove_UI_elements(self):
        self.__USERNAME_INPUT.hide()
        self.__PASSWORD_INPUT.hide()
        self.__GO_BACK_BUTTON.hide()
        self.__TITLE_LABEL.hide()
    
    def show_UI_elements(self):
        self.__USERNAME_INPUT.visible = True
        self.__PASSWORD_INPUT.visible = True
        self.__GO_BACK_BUTTON.visible = True
        self.__TITLE_LABEL.visible = True

class Registration_Confirmation_Screen(Screen):
    def __init__(self, Title: str):
        super(Registration_Confirmation_Screen, self).__init__(Title)
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((380, 250), (520, 75)), manager=MANAGER, object_id="#title_label", text="REGISTRATION COMPLETE")
        self.__SUBTITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((440, 350), (400, 75)), manager=MANAGER, object_id="#subtitle_label", text="PRESS 'SPACE' TO CONTINUE")

    def check_if_user_presses_space(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return True
        return False 

    def show_UI_elements(self):
        self.__TITLE_LABEL.visible = True
        self.__SUBTITLE_LABEL.visible = True
    
    def remove_UI_elements(self):
        self.__TITLE_LABEL.hide()
        self.__SUBTITLE_LABEL.hide()

class Login_Screen(Screen):
    def __init__(self, Title: str):
        super(Login_Screen, self).__init__(Title)

        # UI
        self.__USERNAME_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)-70)), (400, 50)), manager = MANAGER, object_id="#username_text_entry")
        self.__PASSWORD_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)+30)), (400, 50)), manager = MANAGER, object_id="#password_text_entry")
        self.__GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=MANAGER, object_id="#go_back_button", text="GO BACK")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((490, 150), (300, 75)), manager=MANAGER, object_id="#title_label", text="LOGIN MENU")

        # Other
        self.__login_username = ""
        self.__login_password = ""

    def get_login_username(self):
        return self.__login_username
    
    def get_login_password(self):
        return self.__login_password
    
    def check_for_user_interaction_with_ui(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
                pass

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
                pass
            
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                pass
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                return True

            MANAGER.process_events(event)

    def show_UI_elements(self):
        self.__USERNAME_INPUT.visible = True
        self.__PASSWORD_INPUT.visible = True
        self.__GO_BACK_BUTTON.visible = True
        self.__TITLE_LABEL.visible = True
    
    def remove_UI_elements(self):
        self.__USERNAME_INPUT.hide()
        self.__PASSWORD_INPUT.hide()
        self.__GO_BACK_BUTTON.hide()
        self.__TITLE_LABEL.hide()




