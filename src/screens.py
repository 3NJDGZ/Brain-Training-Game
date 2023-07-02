# pygame modules
import pygame_gui
from pygame_gui.core import ObjectID
import pygame

# custom modules (player + maze)
from player import Player
from maze_generation import Maze

# data handling
from mysqlmodel import MySQLDatabaseConnection, PlayerDataManager

# miscellaneous 
from abc import ABC, abstractmethod

pygame.init()

pygame.display.set_caption("Brain Training Game")

PDM = PlayerDataManager(MySQLDatabaseConnection())

class Screen(ABC):
    """
    An abstract base class to represent a Screen in a Pygame GUI.

    ...

    Attributes
    ----------
    Title : str
        The title of the screen.
    _WIDTH : int
        The width of the screen.
    _HEIGHT : int
        The height of the screen.
    _MANAGER : pygame_gui.UIManager
        The Pygame GUI manager for the screen.
    _WIN : pygame.Surface
        The Pygame surface for the screen.
    _screen_colour : tuple of int
        The RGB color of the screen.

    Methods
    -------
    _get_WIN():
        Returns the Pygame surface for the screen.
    _get_MANAGER():
        Returns the Pygame GUI manager for the screen.
    _fill_with_colour():
        Fills the screen with its color.
    show_UI_elements():
        Abstract method to show UI elements on the screen.
    remove_UI_elements():
        Abstract method to remove UI elements from the screen.
    check_for_user_interaction_with_UI():
        Abstract method to check for user interaction with UI elements on the screen.
    """
    
    def __init__(self, Title: str):
        """Initializes a Screen object with a title and sets up protected attributes."""
        # setup protected attributes which will be used by inherited classes
        self.Title = Title
        self._WIDTH = 1600
        self._HEIGHT = 900
        self._MANAGER = pygame_gui.UIManager((self._WIDTH, self._HEIGHT), 'Theme/theme.json')
        self._WIN = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        # self._UI_REFRESH_RATE = CLOCK.tick(60)
        self._screen_colour = (191, 191, 191)
    
    def _get_WIN(self):
        """Returns the Pygame surface for the screen."""
        return self._WIN

    def _get_MANAGER(self):
        """Returns the Pygame GUI manager for the screen."""
        # refactored code to try and avoid the use of global variables such as the MANAGER for the pygame_gui 
        return self._MANAGER 

    def _fill_with_colour(self):
        """Fills the screen with its color."""
        self._WIN.fill((self._screen_colour))
    
    # Abstract methods that are required for every sub-class of 'Screen'
    
    @abstractmethod
    def show_UI_elements(self):
        """Abstract method to show UI elements on the screen."""
        pass

    @abstractmethod
    def remove_UI_elements(self):
        """Abstract method to remove UI elements from the screen."""
        pass

    @abstractmethod
    def check_for_user_interaction_with_UI(self):
        """Abstract method to check for user interaction with UI elements on the screen."""
        pass

class Intro_Screen(Screen):
    """
    A class to represent the Intro Screen in a Pygame GUI.

    Inherits from the Screen abstract base class.

    ...

    Attributes
    ----------
    __LOGIN_BUTTON : pygame_gui.elements.UIButton
        The login button on the intro screen.
    __REGISTER_BUTTON : pygame_gui.elements.UIButton
        The register button on the intro screen.
    __TITLE_LABEL : pygame_gui.elements.UILabel
        The title label on the intro screen.

    Methods
    -------
    check_for_user_interaction_with_UI():
        Checks for user interaction with UI elements on the intro screen.
    remove_UI_elements():
        Removes UI elements from the intro screen.
    show_UI_elements():
        Shows UI elements on the intro screen.
    """
    
    def __init__(self, Title: str):
        """Initializes an Intro_Screen object with a title and sets up UI elements."""
        super(Intro_Screen, self).__init__(Title)

        # UI
        self.__LOGIN_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#login_button"), text="LOGIN")
        self.__REGISTER_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#register_button"), text="REGISTER")
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 350), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="BRAIN TRAINING GAME")

    def check_for_user_interaction_with_UI(self):
        """
        Checks for user interaction with UI elements on the intro screen.

        Returns
        -------
        str or None
            Returns "Login" if the login button is pressed,
            "Register" if the register button is pressed,
            or None if no interaction is detected.
        """
        
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#login_button":
                return "Login"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#register_button":
                return "Register"

            self._MANAGER.process_events(event)
        return None

    def remove_UI_elements(self):
        """Removes UI elements from the intro screen."""
        self.__LOGIN_BUTTON.hide()
        self.__REGISTER_BUTTON.hide()
        self.__TITLE_LABEL.hide()
    
    def show_UI_elements(self):
        """Shows UI elements on the intro screen."""
        self.__LOGIN_BUTTON.show()
        self.__REGISTER_BUTTON.show()
        self.__TITLE_LABEL.show()

# A type of 'Screen' which is mainly used to get essential info from the player, such as username, and password (e.g., being used in register/login screens)
# basically was made to avoid repeating bits of code here and there
class Get_User_Info_Screen(Screen):
    """
    A class to represent the Get User Info Screen in a Pygame GUI.

    Inherits from the Screen abstract base class.

    ...

    Attributes
    ----------
    _USERNAME_INPUT : pygame_gui.elements.UITextEntryLine
        The username input field on the get user info screen.
    _PASSWORD_INPUT : pygame_gui.elements.UITextEntryLine
        The password input field on the get user info screen.
    _GO_BACK_BUTTON : pygame_gui.elements.UIButton
        The go back button on the get user info screen.
    _TITLE_LABEL : pygame_gui.elements.UILabel
        The title label on the get user info screen.
    _ERROR_LABEL : pygame_gui.elements.UILabel
        The error label on the get user info screen.
    _username : str
        The entered username.
    _password : str
        The entered password.

    Methods
    -------
    set_username(username):
        Sets the entered username.
    set_password(password):
        Sets the entered password.
    get_username():
        Returns the entered username.
    get_password():
        Returns the entered password.
    remove_UI_elements():
        Removes UI elements from the get user info screen.
    show_UI_elements():
        Shows UI elements on the get user info screen.
    show_error():
        Shows the error label on the get user info screen.
    """
    
    def __init__(self, Title: str, error_msg):
        """Initializes a Get_User_Info_Screen object with a title and sets up UI elements."""
        super(Get_User_Info_Screen, self).__init__(Title)

        # UI
        self._USERNAME_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, ((self._HEIGHT/2)-70)), (400, 50)), manager = self._MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#username_text_entry"))
        self._PASSWORD_INPUT = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((600, ((self._HEIGHT/2)+30)), (400, 50)), manager = self._MANAGER, object_id=ObjectID(class_id="@text_entry_lines",object_id="#password_text_entry"))
        self._GO_BACK_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((15, 15), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#go_back_button"), text="GO BACK")
        self._TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((625, 250), (350, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text=Title)
        self._ERROR_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 600), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#error_label"), text=error_msg)

        # Other
        self._username = ""
        self._password = ""

    # Getters + Setters for Protected Attributes
    
    def set_username(self, username):
        """Sets the entered username."""
        self._username = username
    
    def set_password(self, password):
        """Sets the entered password."""
        self._password = password

    def get_username(self):
        """Returns the entered username."""
        return self._username
    
    def get_password(self):
        """Returns the entered password."""
        return self._password

    def remove_UI_elements(self):
        """Removes UI elements from the get user info screen."""
        self._USERNAME_INPUT.hide()
        self._PASSWORD_INPUT.hide()
        self._GO_BACK_BUTTON.hide()
        self._TITLE_LABEL.hide()
        self._ERROR_LABEL.hide()
    
    def show_UI_elements(self):
        """Shows UI elements on the get user info screen."""
        self._USERNAME_INPUT.show()
        self._PASSWORD_INPUT.show()
        self._GO_BACK_BUTTON.show()
        self._TITLE_LABEL.show()
    
    def show_error(self):
        """Shows the error label on the get user info screen."""
        self._ERROR_LABEL.show()

class Register_Screen(Get_User_Info_Screen):
    """
    A class to represent the Register Screen in a Pygame GUI.

    Inherits from the Get_User_Info_Screen class.

    ...

    Attributes
    ----------
    __PW_ERROR_LABEL : pygame_gui.elements.UILabel
        The password error label on the register screen.

    Methods
    -------
    show_PW_error():
        Shows the password error label on the register screen.
    remove_UI_elements():
        Removes UI elements from the register screen.
    check_for_user_interaction_with_UI():
        Checks for user interaction with UI elements on the register screen.
    register(username, password):
        Registers a new user with a username and password.
    """
    
    def __init__(self, Title: str, error_msg):
        """Initializes a Register_Screen object with a title and sets up UI elements."""
        super().__init__(Title, error_msg)

        self.__PW_ERROR_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 600), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels",object_id="#error_label"), text="PASSWORD IS TOO SHORT (>=5 CHAR)")
    
    def show_PW_error(self):
        """ Shows the password error label on the register screen."""
        self.__PW_ERROR_LABEL.show()

    def remove_UI_elements(self):
        """Removes UI elements from the register screen."""
        self._USERNAME_INPUT.hide()
        self._PASSWORD_INPUT.hide()
        self._GO_BACK_BUTTON.hide()
        self._TITLE_LABEL.hide()
        self._ERROR_LABEL.hide()
        self.__PW_ERROR_LABEL.hide()
    

    def check_for_user_interaction_with_UI(self):
        """
        Checks for user interaction with UI elements on the register screen.

        Returns
        -------
        str or None
            Returns "TEXT_ENTRY" if text entry is finished,
            "BUTTON" if the go back button is pressed,
            or None if no interaction is detected.
        """
         
        ui_finished = ""
         
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
                self.set_username(event.text)

            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
                self.set_password(event.text)
                
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if len(self.get_username()) > 0:
                    if len(self.get_password()) >= 5:
                        self.register(self.get_username(), self.get_password())
                        ui_finished = "TEXT_ENTRY"
                        return ui_finished
                    else:
                        self.show_PW_error()
                else:
                    self.show_error()
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
                return ui_finished

            self._MANAGER.process_events(event)

    def register(self, username, password):
        """Registers a new user with a username and password."""
        PDM.register_new_player_data(username, password)

class Login_Screen(Get_User_Info_Screen):
    """
    A class to represent the Login Screen in a Pygame GUI.

    Inherits from the Get_User_Info_Screen class.

    ...

    Methods
    -------
    check_for_user_interaction_with_UI():
        Checks for user interaction with UI elements on the login screen.
    login(username, password):
        Logs in a user with a username and password.
    """
    
    def __init__(self, Title: str, error_msg):
        """Initializes a Login_Screen object with a title."""
        super().__init__(Title, error_msg)

    def check_for_user_interaction_with_UI(self):
        """
        Checks for user interaction with UI elements on the login screen.

        Returns
        -------
        str or None
            Returns "TEXT_ENTRY" if text entry is finished,
            "BUTTON" if the go back button is pressed,
            or None if no interaction is detected.
        """
         
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
                    self.show_error()
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#go_back_button":
                ui_finished = "BUTTON"
            
            self._MANAGER.process_events(event)
        return ui_finished
    
    def login(self, username: str, password: str):
        """Logs in a user with a username and password."""
        return PDM.check_user_login(username, password)

# same concept as the 'Get_User_Info_Screen'; may change later as it is kind of redundant but cba
class Confirmation_Screen(Screen):
    """
    A class to represent a Confirmation Screen in a Pygame GUI.

    Inherits from the Screen abstract base class.

    ...

    Attributes
    ----------
    __subtitle : str
        The subtitle on the confirmation screen.
    __TITLE_LABEL : pygame_gui.elements.UILabel
        The title label on the confirmation screen.
    __SUBTITLE_LABEL : pygame_gui.elements.UILabel
        The subtitle label on the confirmation screen.

    Methods
    -------
    check_for_user_interaction_with_UI():
        Checks for user interaction with UI elements on the confirmation screen.
    show_UI_elements():
        Shows UI elements on the confirmation screen.
    remove_UI_elements():
        Removes UI elements from the confirmation screen.
    """
    
    def __init__(self, Title: str, subtitle: str):
        """Initializes a Confirmation_Screen object with a title and sets up UI elements."""
        super(Confirmation_Screen, self).__init__(Title)
        
        self.__subtitle = subtitle
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((540, 350), (520, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text=Title)
        self.__SUBTITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((600, 450), (400, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#subtitle_label"), text=self.__subtitle)

    def check_for_user_interaction_with_UI(self):
         """
         Checks for user interaction with UI elements on the confirmation screen.

         Returns
         -------
         bool
             True if space key is pressed, False otherwise.
         """
         
         keys = pygame.key.get_pressed()
         
         if keys[pygame.K_SPACE]:
            return True
         return False 

    def show_UI_elements(self):
         """Shows UI elements on the confirmation screen."""
         self.__TITLE_LABEL.show()
         self.__SUBTITLE_LABEL.show()
    
    def remove_UI_elements(self):
         """Removes UI elements from the confirmation screen."""
         self.__TITLE_LABEL.hide()
         self.__SUBTITLE_LABEL.hide()

class Registration_Confirmation_Screen(Confirmation_Screen):
    """A class to represent a Registration Confirmation Screen in a Pygame GUI."""
    def __init__(self, Title: str, subtitle: str):        
        super(Registration_Confirmation_Screen, self).__init__(Title, subtitle)

class Login_Confirmation_Screen(Confirmation_Screen):
    """A class to represent a Login Confirmation Screen in a Pygame GUI."""
    def __init__(self, Title: str, subtitle: str):        
        super(Login_Confirmation_Screen, self).__init__(Title, subtitle)

class Skill_Selection_Screen(Screen):
    """
    A class to represent a Skill Selection Screen in a Pygame GUI.

    Inherits from the Screen abstract base class.

    ...

    Attributes
    ----------
    __TITLE_LABEL : pygame_gui.elements.UILabel
        The title label on the skill selection screen.
    __MEMORY_LABEL : pygame_gui.elements.UILabel
        The memory label on the skill selection screen.
    __ATTENTION_LABEL : pygame_gui.elements.UILabel
        The attention label on the skill selection screen.
    __SPEED_LABEL : pygame_gui.elements.UILabel
        The speed label on the skill selection screen.
    __PROBLEM_SOLVING_LABEL : pygame_gui.elements.UILabel
        The problem solving label on the skill selection screen.
    __HORIZONTAL_SLIDER_OPTION_ONE_MEMORY : pygame_gui.elements.UIHorizontalSlider
        The memory slider on the skill selection screen.
    __HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION : pygame_gui.elements.UIHorizontalSlider
        The attention slider on the skill selection screen.
    __HORIZONTAL_SLIDER_OPTION_THREE_SPEED : pygame_gui.elements.UIHorizontalSlider
        The speed slider on the skill selection screen.
    __HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING : pygame_gui.elements.UIHorizontalSlider
        The problem solving slider on the skill selection screen.
    __CONFIRM_BUTTON : pygame_gui.elements.UIButton
        The confirm button on the skill selection screen.
    __ERROR_LABEL : pygame_gui.elements.UILabel
        The error label on the skill selection screen.

    Methods
    -------
    get_value_from_slider():
        Returns an array of values from each slider on the skill selection screen.
    check_for_user_interaction_with_UI():
        Checks for user interaction with UI elements on the skill selection screen.
    calculate_weighted_values_for_player(memory_value, attention_value, speed_value, problem_solving_value):
        Calculates weighted values for a player based on their slider values.
    register_weights_onto_DB(weights):
        Registers weighted values onto the database.
    remove_UI_elements():
        Removes UI elements from the skill selection screen.
    show_error_msg():
        Shows an error message on the skill selection screen.
    show_UI_elements():
        Shows UI elements on the skill selection screen.
    """
    
    def __init__(self, Title: str):
        """Initializes a Skill_Selection_Screen object with a title and sets up UI elements."""
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

        # Error Message
        self.__ERROR_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 775), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@subtitle_labels", object_id="#error_label"), text="EACH SLIDER MUST BE > 0")

    # Get values from each Horiztonal Slider
    
    def get_value_from_slider(self):
        """
        Returns an array of values from each slider on the skill selection screen.

        Returns
        -------
        list of float
            An array of values from each slider on the skill selection screen.
        """
         
        memory_value = self.__HORIZONTAL_SLIDER_OPTION_ONE_MEMORY.get_current_value()
        attention_value = self.__HORIZONTAL_SLIDER_OPTION_TWO_ATTENTION.get_current_value()
        speed_value = self.__HORIZONTAL_SLIDER_OPTION_THREE_SPEED.get_current_value()
        problem_solving_value = self.__HORIZONTAL_SLIDER_OPTION_FOUR_PROBLEM_SOLVING.get_current_value()
        array_of_values = [memory_value, attention_value, speed_value, problem_solving_value] # in order of the cognitive areas entity within the database
        return array_of_values



    def check_for_user_interaction_with_UI(self):
        """
        Checks for user interaction with UI elements on the skill selection screen.

        Returns
        -------
        bool or None
            Returns True if confirm button is pressed and weighted values are calculated,
            or None if no interaction is detected.
        """
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#confirm_button":
                values = self.get_value_from_slider()
                weight_values = self.calculate_weighted_values_for_player(values[0], values[1], values[2], values[3])
                if weight_values is None:
                    self.show_error_msg()
                else:
                    self.register_weights_onto_DB(weight_values)
                    return True

            self._MANAGER.process_events(event)
    
    # simple algorithm used to calculate weight values for the player 
    def calculate_weighted_values_for_player(self, memory_value: int, attention_value: int, speed_value: int, problem_solving_value: int):
         
        """
        Calculates weighted values for a player based on their slider values.

        Parameters
        ----------
        memory_value : int
            The value of the memory slider.
        attention_value : int
            The value of the attention slider.
        speed_value : int
            The value of the speed slider.
        problem_solving_value : int
            The value of the problem solving slider.

        Returns
        -------
        tuple of float or None
            A tuple of weighted values for each cognitive area,
            or None if any slider value is 0.
        """
        if memory_value == 0 or attention_value == 0 or speed_value == 0 or problem_solving_value == 0:
            return None
        else:
            total_value = speed_value + attention_value + memory_value + problem_solving_value
            
            weight_speed_value = speed_value / total_value
            weight_attention_value = attention_value / total_value
            weight_memory_value = memory_value / total_value
            weight_problem_solving_value = problem_solving_value / total_value

            return (weight_memory_value, weight_attention_value, weight_speed_value, weight_problem_solving_value)

    def register_weights_onto_DB(self, weights):
        """Registers weighted values onto the database."""
        PDM.register_weights_onto_DB(weights)
    
    def remove_UI_elements(self):
        """Removes UI elements from the skill selection screen."""
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
        self.__ERROR_LABEL.hide()
    
    def show_error_msg(self):
        """Shows an error message on the skill selection screen."""
        self.__ERROR_LABEL.show()
    
    def show_UI_elements(self):
        """Shows UI elements on the skill selection screen."""
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
    """
    A class to represent a Main Menu Screen in a Pygame GUI.

    Inherits from the Screen abstract base class.

    ...

    Attributes
    ----------
    __TITLE_LABEL : pygame_gui.elements.UILabel
        The title label on the main menu screen.
    __PLAY_BUTTON : pygame_gui.elements.UIButton
        The play button on the main menu screen.
    __SETTINGS_BUTTON : pygame_gui.elements.UIButton
        The settings button on the main menu screen.
    __TUTORIAL_BUTTON : pygame_gui.elements.UIButton
        The tutorial button on the main menu screen.
    __STATS_AND_PERFORMANCE_BUTTON : pygame_gui.elements.UIButton
        The stats and performance button on the main menu screen.

    Methods
    -------
    show_UI_elements():
        Shows UI elements on the main menu screen.
    remove_UI_elements():
        Removes UI elements from the main menu screen.
    check_for_user_interaction_with_UI():
        Checks for user interaction with UI elements on the main menu screen.
    """
    def __init__(self, Title: str):
        """Initializes a Main_Menu_Screen object with a title and sets up UI elements."""
        super(Main_Menu_Screen, self).__init__(Title)

        # UI
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 175), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="MAIN MENU")
        self.__PLAY_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 300), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#play_button"), text="PLAY")
        self.__SETTINGS_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 400), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#settings_button"), text="SETTINGS")
        self.__TUTORIAL_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 500), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#tutorial_button"), text="TUTORIAL")
        self.__STATS_AND_PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 600), (450, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#stats_and_performance_button"), text="STATS & PERFORMANCE")
    
    def show_UI_elements(self):
        """Shows UI elements on the main menu screen."""
        self.__TITLE_LABEL.show()
        self.__PLAY_BUTTON.show()
        self.__SETTINGS_BUTTON.show()
        self.__TUTORIAL_BUTTON.show()
        self.__STATS_AND_PERFORMANCE_BUTTON.show()
    
    def remove_UI_elements(self):
        """Removes UI elements from the main menu screen."""
        self.__TITLE_LABEL.hide()
        self.__PLAY_BUTTON.hide()
        self.__SETTINGS_BUTTON.hide()
        self.__TUTORIAL_BUTTON.hide()
        self.__STATS_AND_PERFORMANCE_BUTTON.hide()

    def check_for_user_interaction_with_UI(self):
        """
        Checks for user interaction with UI elements on the main menu screen.

        Returns
        -------
        str or None
            Returns a string indicating which button was pressed,
            or None if no interaction is detected.
        """
        
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
    """
    A class to represent a Gameplay Selection Screen in a Pygame GUI.

    Inherits from the Screen abstract base class.

    ...

    Attributes
    ----------
    __TITLE_LABEL : pygame_gui.elements.UILabel
        The title label on the gameplay selection screen.
    __LINEAR_BUTTON : pygame_gui.elements.UIButton
        The linear button on the gameplay selection screen.
    __ENDLESS_BUTTON : pygame_gui.elements.UIButton
        The endless button on the gameplay selection screen.

    Methods
    -------
    show_UI_elements():
        Shows UI elements on the gameplay selection screen.
    remove_UI_elements():
        Removes UI elements from the gameplay selection screen.
    check_for_user_interaction_with_UI():
        Checks for user interaction with UI elements on the gameplay selection screen.
    """
    def __init__(self, Title: str):
        """Initializes a Gameplay_Selection_Screen object with a title and sets up UI elements."""
        super(Gameplay_Selection_Screen, self).__init__(Title)

        # UI
        self.__TITLE_LABEL = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((550, 350), (500, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@title_labels",object_id="#title_label"), text="SELECT AN OPTION")
        self.__LINEAR_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#linear_button"), text="LINEAR")
        self.__ENDLESS_BUTTON = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((825, 475), (200, 75)), manager=self._MANAGER, object_id=ObjectID(class_id="@buttons",object_id="#endless_button"), text="ENDLESS")
    
    def show_UI_elements(self):
        """Shows UI elements on the gameplay selection screen."""
        self.__TITLE_LABEL.show()
        self.__LINEAR_BUTTON.show()
        self.__ENDLESS_BUTTON.show()
    
    def remove_UI_elements(self):
        """Removes UI elements from the gameplay selection screen."""
        self.__TITLE_LABEL.hide()
        self.__LINEAR_BUTTON.hide()
        self.__ENDLESS_BUTTON.hide()

    def check_for_user_interaction_with_UI(self):
        """
        Checks for user interaction with UI elements on the gameplay selection screen.

        Returns
        -------
        str or None
            Returns a string indicating which button was pressed,
            or None if no interaction is detected.
        """
        
        ui_finished = ""
        
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#linear_button":
                ui_finished = "LINEAR"
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_object_id == "#endless_button":
                ui_finished = "ENDLESS"
            
            self._MANAGER.process_events(event)
        return ui_finished

class Maze_Screen(Screen):
    """
    A class to represent a Maze Screen in a Pygame GUI.

    Inherits from the Screen abstract base class.

    ...

    Attributes
    ----------
    __maze : Maze
        The maze object on the maze screen.
    __player : Player
        The player object on the maze screen.

    Methods
    -------
    setup_maze_level_with_player():
        Sets up the maze level with the player.
    player_input(event):
        Processes player input on the maze screen.
    show_UI_elements():
        Shows UI elements on the maze screen.
    remove_UI_elements():
        Removes UI elements from the maze screen.
    check_for_user_interaction_with_UI():
        Checks for user interaction with UI elements on the maze screen.
    """
    def __init__(self, Title: str, STARTING_TILE_SIZE: int, LINE_COLOUR: tuple):
        """Initializes a Maze_Screen object with a title and sets up a maze and player."""
        super(Maze_Screen, self).__init__(Title)

        # The common factors of 1600 and 900 are: 1, 2, 4, 5, 10, 20, 25, 50, 100; lower the value, the more complex and larger the maze will be
        self.__maze = Maze(STARTING_TILE_SIZE, LINE_COLOUR, self._WIDTH, self._HEIGHT, self._WIN)
        self.__player = Player()

    def setup_maze_level_with_player(self):
        """Sets up the maze level with the player."""
        self.__maze.setup_maze()
        self._WIN.blit(self.__player.get_player_image(), self.__player.get_rect())
    
    def check_player_cell_is_exit(self):
        self.__player.check_if_current_cell_is_exit(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells())
    
    def check_player_cell_is_exercise(self):
        self.__player.check_if_current_cell_is_exercise(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells(), self._WIN)
    
    def player_input(self, event):
        """Processes player input on the maze screen"""
        self.__player.player_input(self.__maze.get_rects(), self.__maze.get_cols(), self.__maze.get_grid_of_cells(), event)
    
    # UI will need to be added; this UI will actually be separate 
    def show_UI_elements(self):
        """Shows UI elements on the screen"""
        return super().show_UI_elements()

    def remove_UI_elements(self):
        """Removes UI elements on the screen"""
        return super().remove_UI_elements()
    
    def check_for_user_interaction_with_UI(self):
        """Checks for user interaction with the screen"""
        return super().check_for_user_interaction_with_UI()  