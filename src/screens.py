import pygame
import random
import mysql.connector
import pygame_gui
from pygame_gui.core import ObjectID
from abc import ABC, abstractmethod
from player import Player
from maze_generation import Maze

pygame.init()

pygame.display.set_caption("Brain Training Game")

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

class Screen(ABC):
    def __init__(self, Title: str):
        # setup protected attributes which will be used by inherited classes
        self.Title = Title
        self._WIDTH = 1600
        self._HEIGHT = 900
        self._MANAGER = pygame_gui.UIManager((self._WIDTH, self._HEIGHT), 'src/Theme/theme.json')
        self._WIN = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        # self._UI_REFRESH_RATE = CLOCK.tick(60)
        self._screen_colour = (191, 191, 191)
    
    def _get_WIN(self):
        return self._WIN

    def _get_MANAGER(self):
        return self._MANAGER # refactored code to try and avoid the use of global variables such as the MANAGER for the pygame_gui 

    def _fill_with_colour(self):
        self._WIN.fill((self._screen_colour))
    
    # Create connection to the MySQL DB
    def _create_connection(self):
        # Connect to host root server on computer 
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="MainDB"
        )
        return db
    
    # Abstract methods that are required for every sub-class of 'Screen'
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
        self.__LOGIN_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#login_button"), text="LOGIN")
        self.__REGISTER_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#register_button"), text="REGISTER")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 350), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="BRAIN TRAINING GAME")

    def check_for_user_interaction_with_UI(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#login_button":
                return "Login"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#register_button":
                return "Register"

            self._MANAGER.process_events(event)
        return None

    def remove_UI_elements(self):
        self.__LOGIN_BUTTON.hide()
        self.__REGISTER_BUTTON.hide()
        self.__TITLE_LABEL.hide()
    
    def show_UI_elements(self):
        self.__LOGIN_BUTTON.show()
        self.__REGISTER_BUTTON.show()
        self.__TITLE_LABEL.show()

# A type of 'Screen' which is mainly used to get essential info from the player, such as username, and password (e.g., being used in register/login screens)
# basically was made to avoid repeating bits of code here and there
class Get_User_Info_Screen(Screen):
    def __init__(self, Title: str):
        super(Get_User_Info_Screen, self).__init__(Title)

        # UI
        self._USERNAME_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, ((self._HEIGHT/2)-70)), (400, 50)), manager = self._MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#username_text_entry"))
        self._PASSWORD_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, ((self._HEIGHT/2)+30)), (400, 50)), manager = self._MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#password_text_entry"))
        self._GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#go_back_button"), text="GO BACK")
        self._TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((625, 250), (350, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text=Title)

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
        self._USERNAME_INPUT.hide()
        self._PASSWORD_INPUT.hide()
        self._GO_BACK_BUTTON.hide()
        self._TITLE_LABEL.hide()
    
    def show_UI_elements(self):
        self._USERNAME_INPUT.show()
        self._PASSWORD_INPUT.show()
        self._GO_BACK_BUTTON.show()
        self._TITLE_LABEL.show()

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

            self._MANAGER.process_events(event)
        
    def generate_random_salt(self):
        '''
        Generates random salt
        Arguments: None
        Returns: salt ()
        '''
        random_length = random.randint(5, 20)
        salt = ""

        for loop in range(random_length):
            salt += chr(random.randint(0, 127))
        
        return salt

    def register(self, username, password):

        # Create connection + create cursor
        db = self._create_connection()
        mycursor = db.cursor()

        successful_registration = False
        if len(username) > 0 and len(password) > 0:
            salt = self.generate_random_salt()
            mycursor.execute(f"""
            INSERT INTO Player (Username, Password, Salt)
            VALUES ('{username}', aes_encrypt(concat('{password}', md5('{salt}')), 'encryptionkey1234'), md5('{salt}'));
            """)

            # Fetch PlayerID of the newly registered Player from the Player Entity
            mycursor.execute(f"""
            SELECT *
            FROM Player
            ORDER BY PlayerID DESC
            """)

            records = mycursor.fetchall()
            for record in records:
                current_player_id = record[0]
                break

            print(current_player_id)

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
            db.commit()
            db.close()

            successful_registration = True
            mycursor.reset()
            mycursor.close()
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
            
            self._MANAGER.process_events(event)
        return ui_finished
    
    def login(self, username: str, password: str):

        # Create connection + create cursor
        db = self._create_connection()
        mycursor = db.cursor()

        valid_details = False
        # check if username and password is valid (replace + decrypt salted passwords)
        mycursor.execute(f"""
        SELECT Username, replace(cast(aes_decrypt(Password, 'encryptionkey1234') as char(100)), Salt, '') 
        FROM Player;
        """)

        for combination in mycursor:
            if combination[0] == username and combination[1] == password:
                valid_details = True
                break
            else:
                valid_details = False
        
        mycursor.reset()
        mycursor.close()

        return valid_details

# same concept as the 'Get_User_Info_Screen'; may change later as it is kind of redundant but cba
class Confirmation_Screen(Screen):
    def __init__(self, Title: str, subtitle: str):
        super(Confirmation_Screen, self).__init__(Title)
        self.__subtitle = subtitle
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((540, 350), (520, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text=Title)
        self.__SUBTITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((600, 450), (400, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#subtitle_label"), text=self.__subtitle)

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
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 150), (900, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels", object_id="#title_label"), text=Title)
        
        # Labels for each Slider
        self.__MEMORY_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1160, 253), (130, 40)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#memory_subtitle_label"), text="MEMORY")
        self.__ATTENTION_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1160, 353), (150, 40)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#attention_subtitle_label"), text="ATTENTION")
        self.__SPEED_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1160, 453), (100, 40)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#speed_subtitle_label"), text="SPEED")
        self.__PROBLEM_SOLVING_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((1160, 553), (250, 40)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#problem_solving_subtitle_label"), text="PROBLEM SOLVING")

        # Sliders for each Category
        self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((450, 250), (700, 50)), manager=self._MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider1_memory"))
        self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((450, 350), (700, 50)), manager=self._MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider2_attention"))
        self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((450, 450), (700, 50)), manager=self._MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider3_speed"))
        self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((450, 550), (700, 50)), manager=self._MANAGER, start_value=0, value_range=(0, 100), click_increment=1, object_id=ObjectID(class_id="@horizontal_sliders", object_id="#slider4_problem_solving"))
        self.__CONFIRM_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 650), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#confirm_button"), text="CONFIRM")

    # Get values from each Horiztonal Slider
    def get_value_from_slider(self):
        memory_value = self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY.get_current_value()
        attention_value = self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION.get_current_value()
        speed_value = self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED.get_current_value()
        problem_solving_value = self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING.get_current_value()
        array_of_values = [memory_value, attention_value, speed_value, problem_solving_value] # in order of the cognitive areas entity within the database
        return array_of_values

    def check_for_user_interaction_with_UI(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#confirm_button":
                values = self.get_value_from_slider()
                weight_values = self.calculate_weighted_values_for_player(values[0], values[1], values[2], values[3])
                self.register_weights_onto_DB(weight_values)
                return True

            self._MANAGER.process_events(event)
    
    # simple algorithm used to calculate weight values for the player 
    def calculate_weighted_values_for_player(self, memory_value: int, attention_value: int, speed_value: int, problem_solving_value: int):
        total_value = speed_value + attention_value + memory_value + problem_solving_value
        
        weight_speed_value = speed_value / total_value
        weight_attention_value = attention_value / total_value
        weight_memory_value = memory_value / total_value
        weight_problem_solving_value = problem_solving_value / total_value

        return (weight_memory_value, weight_attention_value, weight_speed_value, weight_problem_solving_value)

    def register_weights_onto_DB(self, weights):

        # Create connection + create cursor
        db = self._create_connection()
        mycursor = db.cursor()
        
        # Get Player_ID
        mycursor.execute("""
        SELECT * 
        FROM Player
        ORDER BY PlayerID DESC
        """)

        records = mycursor.fetchall()
        for record in records:
            player_id = record[0]
            break
            
        print(player_id)

        # Cogntiive Area ID 1 (Memory)
        mycursor.execute(f"""
        UPDATE Weights
        SET WeightValue = {weights[0]}
        WHERE CognitiveAreaID = 1
        AND PlayerID = {player_id};
        """)

        # Cognitive Area ID 2 (Attention)
        mycursor.execute(f"""
        UPDATE Weights
        SET WeightValue = {weights[1]}
        WHERE CognitiveAreaID = 2
        AND PlayerID = {player_id};
        """)

        # Cognitive Area ID 3 (Speed)
        mycursor.execute(f"""
        UPDATE Weights
        SET WeightValue = {weights[2]}
        WHERE CognitiveAreaID = 3
        AND PlayerID = {player_id};
        """)

        # Cognitive Area ID 4 (Problem Solving)
        mycursor.execute(f"""
        UPDATE Weights
        SET WeightValue = {weights[3]}
        WHERE CognitiveAreaID = 4
        AND PlayerID = {player_id};
        """)
    
        # Printing if the values have been recorded 
        mycursor.execute("""
        SELECT *
        FROM Weights;
        """)
        print("\n")
        for x in mycursor:
            print(x)
        
        # Commit Changes to DB
        db.commit()
        db.close()

        mycursor.reset()
        mycursor.close()
    
    def remove_UI_elements(self):
        self.__TITLE_LABEL.hide()
        self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY.hide()
        self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION.hide()
        self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED.hide()
        self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING.hide()
        self.__CONFIRM_BUTTON.hide()
        self.__SPEED_LABEL.hide()
        self.__ATTENTION_LABEL.hide()
        self.__MEMORY_LABEL.hide()
        self.__PROBLEM_SOLVING_LABEL.hide()
    
    def show_UI_elements(self):
        self.__TITLE_LABEL.show()
        self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY.show()
        self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION.show()
        self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED.show()
        self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING.show()
        self.__CONFIRM_BUTTON.show()
        self.__SPEED_LABEL.show()
        self.__ATTENTION_LABEL.show()
        self.__MEMORY_LABEL.show()
        self.__PROBLEM_SOLVING_LABEL.show()
    
class Main_Menu_Screen(Screen):
    def __init__(self, Title: str):
        super(Main_Menu_Screen, self).__init__(Title)

        # UI
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 175), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="MAIN MENU")
        self.__PLAY_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 300), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#play_button"), text="PLAY")
        self.__SETTINGS_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 400), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#settings_button"), text="SETTINGS")
        self.__TUTORIAL_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 500), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#tutorial_button"), text="TUTORIAL")
        self.__STATS_AND_PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 600), (450, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#stats_and_performance_button"), text="STATS & PERFORMANCE")
    
    def show_UI_elements(self):
        self.__TITLE_LABEL.show()
        self.__PLAY_BUTTON.show()
        self.__SETTINGS_BUTTON.show()
        self.__TUTORIAL_BUTTON.show()
        self.__STATS_AND_PERFORMANCE_BUTTON.show()
    
    def remove_UI_elements(self):
        self.__TITLE_LABEL.hide()
        self.__PLAY_BUTTON.hide()
        self.__SETTINGS_BUTTON.hide()
        self.__TUTORIAL_BUTTON.hide()
        self.__STATS_AND_PERFORMANCE_BUTTON.hide()

    def check_for_user_interaction_with_UI(self):
        ui_finished = ""
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#play_button":
                ui_finished = "PLAY"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#settings_button":
                ui_finished = "SETTINGS"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#tutorial_button":
                ui_finished = "TUTORIAL"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#stats_and_performance_button":
                ui_finished = "STATS"
            
            self._MANAGER.process_events(event)
        return ui_finished

class Gameplay_Selection_Screen(Screen):
    def __init__(self, Title: str):
        super(Gameplay_Selection_Screen, self).__init__(Title)

        # UI
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 350), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="SELECT AN OPTION")
        self.__LINEAR_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#linear_button"), text="LINEAR")
        self.__ENDLESS_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#endless_button"), text="ENDLESS")
    
    def show_UI_elements(self):
        self.__TITLE_LABEL.show()
        self.__LINEAR_BUTTON.show()
        self.__ENDLESS_BUTTON.show()
    
    def remove_UI_elements(self):
        self.__TITLE_LABEL.hide()
        self.__LINEAR_BUTTON.hide()
        self.__ENDLESS_BUTTON.hide()
    
    def check_for_user_interaction_with_UI(self):
        ui_finished = ""
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#linear_button":
                ui_finished = "LINEAR"
                print(ui_finished)
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#endless_button":
                ui_finished = "ENDLESS"
                print(ui_finished)
            self._MANAGER.process_events(event)
        return ui_finished    

class Maze_Screen(Screen):
    def __init__(self, Title: str, STARTING_TILE_SIZE: int, LINE_COLOUR: tuple):
        super(Maze_Screen, self).__init__(Title)

        self.__STARTING_TILE_SIZE = STARTING_TILE_SIZE

        # The common factors of 1600 and 900 are: 1, 2, 4, 5, 10, 20, 25, 50, 100; lower the value, the more complex and larger the maze will be
        self.__maze = Maze(STARTING_TILE_SIZE, LINE_COLOUR, self._WIDTH, self._HEIGHT, self._WIN)
        self.__player = Player()

    def setup_maze_level_with_player(self):
        self.__maze.setup_maze()
        self._WIN.blit(self.__player.get_player_image(), self.__player.get_rect())
        self.__player.player_input(self.__maze.get_grid_of_cells())
    
    # UI will need to be added; this UI will actually be separate 
    def show_UI_elements(self):
        return super().show_UI_elements()

    def remove_UI_elements(self):
        return super().remove_UI_elements()
    
    def check_for_user_interaction_with_UI(self):
        return super().check_for_user_interaction_with_UI()  