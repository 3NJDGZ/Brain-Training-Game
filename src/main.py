import pygame
import sys
from screens import *

pygame.init()

class Game:
    def __init__(self):
        self.__UI_REFRESH_RATE = CLOCK.tick(60)/10000

        # Screens
        self.__intro_screen = Intro_Screen("Intro!")
        self.__register_screen = Register_Screen("REGISTER MENU")
        self.__login_screen = Login_Screen("LOGIN MENU")
        self.__registration_confirmation_screen = Registration_Confirmation_Screen("REGISTRATION SUCCESSFUL", "PRESS 'SPACE' TO CONTINUE.")
        self.__login_confirmation_screen = Login_Confirmation_Screen("LOGIN SUCCESSFUL", "PRESS 'SPACE' TO CONTINUE.")
        self.screens = [self.__intro_screen, self.__register_screen, self.__login_screen, self.__registration_confirmation_screen, self.__login_confirmation_screen]
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

            # print(f"Current State: {self.check_screen_state()}")

            self.__current_screen.show_UI_elements()
            
            self.update_UI_screen()
            self.__current_screen._fill_with_colour()

            self.check_if_screen_is_intro()
            self.check_if_screen_is_register()
            self.check_if_screen_is_login()

            self.check_if_screen_is_registration_confirmation()
            self.check_if_screen_is_login_confirmation()

            self.draw_UI(self.__current_screen)
            self.update_screen()

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
                print("sewey")

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
                self.__current_pos += 2

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

    def check_screen_state(self):
        return self.__current_pos

    def update_screen(self):
        pygame.display.update()

    def update_UI_screen(self):
        MANAGER.update(self.__UI_REFRESH_RATE)
    
    def draw_UI(self, screen: Screen):
        MANAGER.draw_ui(screen._get_WIN())
    
brain_training_game = Game()
brain_training_game.play()