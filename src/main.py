# import necessary modules
import sys
from exercises import *
from screens import *

# bypasses recursion limit stated by python; required for the recursive DFS when generating more complex and larger mazes https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-and-how-to-increase-it
sys.setrecursionlimit(10**6)

pygame.init()

class Game:
    def __init__(self):
        # Base attributes (used for boilerplate-ish code)
        self.__CLOCK = pygame.time.Clock()
        self.__UI_REFRESH_RATE = 0.06

        # Screens
        self.__intro_screen = Intro_Screen("Intro!")
        self.__register_screen = Register_Screen("REGISTER MENU", "INVALID INPUTS, TRY AGAIN")
        self.__login_screen = Login_Screen("LOGIN MENU", "INVALID DETAILS, TRY AGAIN.")
        self.__registration_confirmation_screen = Registration_Confirmation_Screen("REGISTRATION SUCCESSFUL", "PRESS 'SPACE' TO CONTINUE.")
        self.__login_confirmation_screen = Login_Confirmation_Screen("LOGIN SUCCESSFUL", "PRESS 'SPACE' TO CONTINUE.")
        self.__skill_selection_screen = Skill_Selection_Screen("SKILL SLIDER SELECTION")
        self.__main_menu_screen = Main_Menu_Screen("MAIN MENU")
        self.__maze_screen = None
        self.__settings_screen = Settings_Screen("Settings")
        self.__stats_and_performance_screen = Stats_and_Performance_Screen("Stats and Performance")
        self.__leaderboard_screen = Leaderboard_Screen("LEADERBOARD")

        self.__create_maze_screen = False

        # Array of screens which will be used to specify the current screen to the user as the current index positioning.
        self.screens = [self.__intro_screen, #0
                        self.__register_screen, #1
                        self.__login_screen, #2
                        self.__registration_confirmation_screen, #3
                        self.__login_confirmation_screen, #4
                        self.__skill_selection_screen, #5
                        self.__main_menu_screen, #6
                        self.__maze_screen, #7
                        self.__settings_screen, #8
                        self.__stats_and_performance_screen, #9
                        self.__leaderboard_screen #10
                        ]
        self.__current_pos = 0 # acts as the index positioning for the screens; also can be seen as the current 'state' that the entire 'system' (application) is in
        self.__current_screen = self.screens[self.__current_pos] # sets state to that of the first screen

        self.__disable_player_movement_for_question_exercise = False

    def get_state(self):
        return self.__current_pos

    def play(self):
        running = True
        while running: 
                     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if isinstance(self.__current_screen, Maze_Screen):
                    # Player Input for all the exercises
                    if not self.__disable_player_movement_for_question_exercise:
                        self.__current_screen.player_input(event)
                    if isinstance(self.__current_screen.check_type_of_exercise_cell(), ChalkboardChallenge):
                        self.__current_screen.check_type_of_exercise_cell().user_input(event)
                    elif isinstance(self.__current_screen.check_type_of_exercise_cell(), MemoryMatrix):
                        self.__current_screen.check_type_of_exercise_cell().user_input(event)
                    elif isinstance(self.__current_screen.check_type_of_exercise_cell(), SchulteTable):
                        self.__current_screen.check_type_of_exercise_cell().user_input(event)
                    elif isinstance(self.__current_screen.check_type_of_exercise_cell(), Aiming):
                        self.__current_screen.check_type_of_exercise_cell().user_input(event)
                    elif isinstance(self.__current_screen.check_type_of_exercise_cell(), QuestionAnswerExercise):
                        self.__current_screen.check_type_of_exercise_cell().user_input(event)

                        # Disables player input for the game so that they can type their answers within the text entry box
                        if not self.__current_screen.check_type_of_exercise_cell().get_completely_finished():
                            self.__disable_player_movement_for_question_exercise = True
                        else:
                            self.__disable_player_movement_for_question_exercise = False
                
                self.__current_screen._get_MANAGER().process_events(event)
            
            # print(f"Current State: {self.get_state()}")
                    
            self.__current_screen = self.screens[self.__current_pos]
            self.__current_screen.show_UI_elements()
            self.__current_screen._fill_with_colour()
            
            # Checking what type of screen should be displayed
            # USER ON-BOARDING Screens
            self.check_if_screen_is_intro()
            self.check_if_screen_is_register()
            self.check_if_screen_is_login()
            self.check_if_screen_is_skill_screens()
            self.check_if_screen_is_registration_confirmation()
            self.check_if_screen_is_login_confirmation()
            # GAMEPLAY Screens
            self.check_if_screen_is_main_menu()
            self.check_if_screen_is_maze_screen()
            self.check_if_screen_is_settings_screen()
            self.check_if_screen_is_stats_and_performance_screen()
            self.check_if_screen_is_leaderboard()

            # Draw UI of corresponding screen
            self.draw_UI(self.__current_screen)
            self.update_UI_screen(self.__current_screen)
            self.update_screen()
            self.__CLOCK.tick(60)

    # These methods can be seen as 'state transition functions' changing the state of the system when needed to show the correct screen to the user
    def check_if_screen_is_registration_confirmation(self):
        if not isinstance(self.__current_screen, Registration_Confirmation_Screen):
            self.__registration_confirmation_screen.remove_UI_elements()
        else:
            self.__current_screen.show_UI_elements()
            if self.__current_screen.check_for_user_interaction_with_UI():
                self.__current_pos -= 1

    def check_if_screen_is_login_confirmation(self):
        if not isinstance(self.__current_screen, Login_Confirmation_Screen):
            self.__login_confirmation_screen.remove_UI_elements()
        else:
            self.__current_screen.show_UI_elements()
            if self.__current_screen.check_for_user_interaction_with_UI():
                self.__current_pos += 2

    def check_if_screen_is_register(self):
        if not isinstance(self.__current_screen, Register_Screen):
            # Set visibility of register_screen UI as false (current screen will not be register_screen)
            self.__register_screen.remove_UI_elements()
        else:
            # Current Screen will now be register_screen so we can now set its UI elements' visibility to True
            self.__current_screen.show_UI_elements()
            # Check what type of UI was interacted by the player 
            ui_interacted = self.__current_screen.check_for_user_interaction_with_UI()
            if ui_interacted == "BUTTON":
                # if pressed, remove UI elements of register (current) screen and set state back to intro_screen
                self.__current_screen.remove_UI_elements()
                self.__current_pos -= 1
            elif ui_interacted == "TEXT_ENTRY":
                # if the player has finished and entered their username and password to be registered, move current screen to login screen
                self.__current_screen.remove_UI_elements()
                self.__current_pos += 4

    def check_if_screen_is_login(self):
        if not isinstance(self.__current_screen, Login_Screen):
            # Set visibility of login_screen UI as false as the current_screen will not be the login_screen
            self.__login_screen.remove_UI_elements()
        else:
            # Current screen will now be login_screen so reveal UI elements
            ui_finished = self.__current_screen.check_for_user_interaction_with_UI()
            if ui_finished == "TEXT_ENTRY":
                self.__current_screen.remove_UI_elements()
                self.__current_pos += 2
            elif ui_finished == "BUTTON":
                self.__current_screen.remove_UI_elements()
                self.__current_pos -= 2

    def check_if_screen_is_intro(self):
        if isinstance(self.__current_screen, Intro_Screen):
            # Check which button is pressed by user
            button_pressed = self.__current_screen.check_for_user_interaction_with_UI()
            # Functionality not yet implemented for the login button
            if button_pressed == "Login":
                self.__current_screen.remove_UI_elements()
                self.__current_pos += 2
            # if register button pressed remove the UI elements of the intro (current) screen and set state to register_screen
            elif button_pressed == "Register":
                self.__current_screen.remove_UI_elements()
                self.__current_pos += 1

    def check_if_screen_is_skill_screens(self):
        if not isinstance(self.__current_screen, Skill_Selection_Screen):
            self.__skill_selection_screen.remove_UI_elements()
        else:
            self.__current_screen.show_UI_elements()
            confirmed = self.__current_screen.check_for_user_interaction_with_UI()
            if confirmed:
                self.__current_pos -= 2
    
    def check_if_screen_is_main_menu(self):
        if not isinstance(self.__current_screen, Main_Menu_Screen):
            self.__main_menu_screen.remove_UI_elements()
        else:
            self.__current_screen.show_UI_elements()
            button_pressed = self.__current_screen.check_for_user_interaction_with_UI()
            if button_pressed == "PLAY":
                self.__current_screen.remove_UI_elements()
                self.__current_pos += 1
                player_id = PDM.get_player_id()
                if player_id is not None:
                    if not self.__create_maze_screen:
                        self.screens[7] =  Maze_Screen("MAZE SCREEN TEST", 100, (132, 87, 255)) # The common factors of 1600 and 900 are: 1, 2, 4, 5, 10, 20, 25, 50, 100
                        self.__create_maze_screen = True
            elif button_pressed == "SETTINGS":
                self.__current_screen.remove_UI_elements()
                self.__current_pos += 2
            elif button_pressed == "STATS":
                self.__current_pos += 3
            elif button_pressed == "LEADERBOARD":
                self.__current_pos += 4
    
    def check_if_screen_is_maze_screen(self):
        if not isinstance(self.__current_screen, Maze_Screen) and self.__maze_screen is not None:
            self.__maze_screen.remove_UI_elements()
        else:
            if isinstance(self.__current_screen, Maze_Screen):
                self.__create_maze_screen = False
                self.__current_screen.setup_maze_level_with_player()
                if self.__current_screen.get_return_to_main_menu():
                    self.__current_pos -= 1
    
    def check_if_screen_is_settings_screen(self):
        if not isinstance(self.__current_screen, Settings_Screen):
            self.__settings_screen.remove_UI_elements() 
        else:
            self.__current_screen.show_UI_elements()
            button_pressed = self.__current_screen.check_for_user_interaction_with_UI()
            if button_pressed == "BUTTON":
                self.__current_screen.remove_UI_elements()
                self.__current_pos -= 2
    
    def check_if_screen_is_stats_and_performance_screen(self):
        if not isinstance(self.__current_screen, Stats_and_Performance_Screen):
            self.__stats_and_performance_screen.remove_UI_elements()
        else:
            self.__current_screen.show_UI_elements()
            button_pressed = self.__current_screen.check_for_user_interaction_with_UI()
            if button_pressed == "BUTTON":
                self.__current_pos -= 3
    
    def check_if_screen_is_leaderboard(self):
        if not isinstance(self.__current_screen, Leaderboard_Screen):
            self.__leaderboard_screen.remove_UI_elements()
        else:
            self.__current_screen.show_UI_elements()
            button_pressed = self.__current_screen.check_for_user_interaction_with_UI()
            if button_pressed == "BUTTON":
                self.__current_pos -= 4

    def check_screen_state(self): # Used for checking the 'state' of the system 
        return self.__current_pos

    def update_screen(self):
        pygame.display.update()

    def update_UI_screen(self, screen: Screen):
        screen._get_MANAGER().update(self.__UI_REFRESH_RATE)
    
    def draw_UI(self, screen: Screen):
        screen._get_MANAGER().draw_ui(screen._get_WIN())
    
brain_training_game = Game()
brain_training_game.play()
