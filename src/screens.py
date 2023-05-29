import pygame
import pygame_gui
from pygame_gui import *
from pygame_gui.core import ObjectID
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

    @abstractmethod
    def check_for_user_interaction_with_UI(self):
        pass

class Intro_Screen(Screen):
    def __init__(self, Title: str):
        super(Intro_Screen, self).__init__(Title)
        # UI
        self.__LOGIN_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((390, HEIGHT/2+50), (200, 75)), manager=MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#login_button"), text="LOGIN")
        self.__REGISTER_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((690, HEIGHT/2+50), (200, 75)), manager=MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#register_button"), text="REGISTER")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((390, HEIGHT/2-100), (500, 75)), manager=MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="BRAIN TRAINING GAME")

    def check_for_user_interaction_with_UI(self):
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
        self.__LOGIN_BUTTON.show()
        self.__REGISTER_BUTTON.show()
        self.__TITLE_LABEL.show()

class Get_User_Info_Screen(Screen):
    def __init__(self, Title: str):
        super(Get_User_Info_Screen, self).__init__(Title)
        # UI
        self.__USERNAME_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)-70)), (400, 50)), manager = MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#username_text_entry"))
        self.__PASSWORD_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((440, ((HEIGHT/2)+30)), (400, 50)), manager = MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#password_text_entry"))
        self.__GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#go_back_button"), text="GO BACK")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((465, 150), (350, 75)), manager=MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text=Title)

        # Other
        self._username = ""
        self._password = ""

    # Getters + Setters for Protected Attributes
    def set_username(self, username):
        self._username = username
    
    def set_password(self, password):
        self._password = password
    
    def get_username(self):
        return self._username
    
    def get_password(self):
        return self._password

    def remove_UI_elements(self):
        self.__USERNAME_INPUT.hide()
        self.__PASSWORD_INPUT.hide()
        self.__GO_BACK_BUTTON.hide()
        self.__TITLE_LABEL.hide()
    
    def show_UI_elements(self):
        self.__USERNAME_INPUT.show()
        self.__PASSWORD_INPUT.show()
        self.__GO_BACK_BUTTON.show()
        self.__TITLE_LABEL.show()

class Register_Screen(Get_User_Info_Screen):
    def __init__(self, Title: str):
        super(Register_Screen, self).__init__(Title)

    def check_for_user_interaction_with_UI(self):
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

            mycursor.execute("""
            SELECT * 
            FROM Player;
            """)

            for record in mycursor:
                print(record)

            # Commit Changes to DB
            # db.commit()
            # db.close()

            successful_registration = True
            mycursor.reset()
        return successful_registration

class Login_Screen(Get_User_Info_Screen):
    def __init__(self, Title: str):
        super(Login_Screen, self).__init__(Title)

    def check_for_user_interaction_with_UI(self):
        ui_finished = ""
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
                print(event.text)
                self.set_username(event.text)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
                print(event.text)
                self.set_password(event.text)
            
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if self.login(self.get_username(), self.get_password()):
                    ui_finished = "TEXT_ENTRY"
                else:
                    print("Invalid Details")
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"

            MANAGER.process_events(event)
        return ui_finished
    
    def login(self, username: str, password: str):

        valid_details = False
        # check if username and password is valid 
        mycursor.execute(f"""
        SELECT Username, Password
        FROM Player;
        """)

        for combination in mycursor:
            if combination[0] == username and combination[1] == password:
                valid_details = True
                break
            else:
                valid_details = False
        
        mycursor.reset()

        return valid_details

class Confirmation_Screen(Screen):
    def __init__(self, Title: str, subtitle: str):
        super(Confirmation_Screen, self).__init__(Title)
        self.__subtitle = subtitle
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((380, 250), (520, 75)), manager=MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text=Title)
        self.__SUBTITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((440, 350), (400, 75)), manager=MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#subtitle_label"), text=self.__subtitle)

    def check_for_user_interaction_with_UI(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return True
        return False 

    def show_UI_elements(self):
        self.__TITLE_LABEL.show()
        self.__SUBTITLE_LABEL.show()
    
    def remove_UI_elements(self):
        self.__TITLE_LABEL.hide()
        self.__SUBTITLE_LABEL.hide()

class Registration_Confirmation_Screen(Confirmation_Screen):
    def __init__(self, Title: str, subtitle: str):
        super(Registration_Confirmation_Screen, self).__init__(Title, subtitle)

class Login_Confirmation_Screen(Confirmation_Screen):
    def __init__(self, Title: str, subtitle: str):
        super(Login_Confirmation_Screen, self).__init__(Title, subtitle)

class Skill_Selection_Screen(Screen):
    def __init__(self, Title: str):
        super(Skill_Selection_Screen, self).__init__(Title)

        # UI
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((190, 100), (900, 75)), manager=MANAGER, object_id=ObjectID(class_id="@title_labels", object_id="#title_label"), text=Title)
        
        # Labels for each Slider
        self.__SPEED_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1000, 203), (100, 40)), manager=MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#speed_subtitle_label"), text="SPEED")
        self.__ATTENTION_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1000, 303), (150, 40)), manager=MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#attention_subtitle_label"), text="ATTENTION")
        self.__MEMORY_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1000, 403), (130, 40)), manager=MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#memory_subtitle_label"), text="MEMORY")
        self.__PROBLEM_SOLVING_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1000, 503), (250, 40)), manager=MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#problem_solving_subtitle_label"), text="PROBLEM SOLVING")

        # Sliders for each Category
        self.__HORIZONTAL_SLIDER_OPTION_ONE = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((290, 200), (700, 50)), manager=MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider1"))
        self.__HORIZONTAL_SLIDER_OPTION_TWO = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((290, 300), (700, 50)), manager=MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider2"))
        self.__HORIZONTAL_SLIDER_OPTION_THREE = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((290, 400), (700, 50)), manager=MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider3"))
        self.__HORIZONTAL_SLIDER_OPTION_FOUR = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((290, 500), (700, 50)), manager=MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider4"))
        self.__CONFIRM_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((540, 600), (200, 75)), manager=MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#confirm_button"), text="CONFIRM")

    # Get values from each Horiztonal Slider
    def get_value_from_slider(self):
        speed_value = self.__HORIZONTAL_SLIDER_OPTION_ONE.get_current_value()
        attention_value = self.__HORIZONTAL_SLIDER_OPTION_TWO.get_current_value()
        memory_value = self.__HORIZONTAL_SLIDER_OPTION_THREE.get_current_value()
        problem_solving_value = self.__HORIZONTAL_SLIDER_OPTION_FOUR.get_current_value()
        array_of_values = [speed_value, attention_value, memory_value, problem_solving_value]
        return array_of_values

    def check_for_user_interaction_with_UI(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#confirm_button":
                values = self.get_value_from_slider()
                weight_values = self.calculate_weighted_values_for_player(values[0], values[1], values[2], values[3])
                self.register_weights_onto_DB(weight_values)


            MANAGER.process_events(event)
    
    def calculate_weighted_values_for_player(self, speed_value: int, attention_value: int, memory_value: int, problem_solving_value: int):
        total_value = speed_value + attention_value + memory_value + problem_solving_value
        
        weight_speed_value = speed_value / total_value
        weight_attention_value = attention_value / total_value
        weight_memory_value = memory_value / total_value
        weight_problem_solving_value = problem_solving_value / total_value

        return (weight_speed_value, weight_attention_value, weight_memory_value, weight_problem_solving_value)

    def register_weights_onto_DB(self, *weights):

        # Retrieve most recently added record
        mycursor.execute("""
        SELECT * 
        FROM Player
        ORDER BY PlayerID DESC;
        """)

        for record in mycursor: # store in the variable record
            print(record)
            break
        player_id = record[0]
        print(player_id)

    
    def remove_UI_elements(self):
        self.__TITLE_LABEL.hide()
        self.__HORIZONTAL_SLIDER_OPTION_ONE.hide()
        self.__HORIZONTAL_SLIDER_OPTION_TWO.hide()
        self.__HORIZONTAL_SLIDER_OPTION_THREE.hide()
        self.__HORIZONTAL_SLIDER_OPTION_FOUR.hide()
        self.__CONFIRM_BUTTON.hide()
        self.__SPEED_LABEL.hide()
        self.__ATTENTION_LABEL.hide()
        self.__MEMORY_LABEL.hide()
        self.__PROBLEM_SOLVING_LABEL.hide()
    
    def show_UI_elements(self):
        self.__TITLE_LABEL.show()
        self.__HORIZONTAL_SLIDER_OPTION_ONE.show()
        self.__HORIZONTAL_SLIDER_OPTION_TWO.show()
        self.__HORIZONTAL_SLIDER_OPTION_THREE.show()
        self.__HORIZONTAL_SLIDER_OPTION_FOUR.show()
        self.__CONFIRM_BUTTON.show()
        self.__SPEED_LABEL.show()
        self.__ATTENTION_LABEL.show()
        self.__MEMORY_LABEL.show()
        self.__PROBLEM_SOLVING_LABEL.show()
    

