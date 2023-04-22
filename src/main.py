import pygame
import sys
from screens import Intro_Screen, Register_Screen, Screen
from screens import MANAGER, CLOCK

pygame.init()

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