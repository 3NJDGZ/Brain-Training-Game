import unittest
from screens import *

class TestRegisterScreen(unittest.TestCase):
    def test_remove_UI_elements(self):
        register_screen = Register_Screen("Test_Register")

        # Test removing UI elements
        register_screen.remove_UI_elements()

        # Assert that UI elements are hidden
        self.assertFalse(register_screen._Register_Screen__USERNAME_INPUT.visible)
        self.assertFalse(register_screen._Register_Screen__PASSWORD_INPUT.visible)
        self.assertFalse(register_screen._Register_Screen__GO_BACK_BUTTON.visible)
        self.assertFalse(register_screen._Register_Screen__TITLE_LABEL.visible)
        

    def test_show_UI_elements(self):
        register_screen = Register_Screen("Test_Register")

        # Hide elements first 
        register_screen.remove_UI_elements()

        # Test showing UI elements
        register_screen.show_UI_elements()

        # Assert that UI elements are visible
        self.assertTrue(register_screen._Register_Screen__USERNAME_INPUT.visible)
        self.assertTrue(register_screen._Register_Screen__PASSWORD_INPUT.visible)
        self.assertTrue(register_screen._Register_Screen__GO_BACK_BUTTON.visible)
        self.assertTrue(register_screen._Register_Screen__TITLE_LABEL.visible)
    
    def test_register_user(self):
        register_screen = Register_Screen("Test_Register")

        # Set Found = False
        Found_LOGIN_Details = False

        # Set Username and Password
        register_screen.set_username("TestUsername")
        register_screen.set_password("TestPassword")
        test_username = register_screen.get_username()
        test_password = register_screen.get_password()

        # Check if registration was successful for the the test inputs
        self.assertTrue(register_screen.register(test_username, test_password))
    
if __name__ == "__main__":
    unittest.main()
