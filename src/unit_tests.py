import unittest
from screens import *

class TestRegisterScreen(unittest.TestCase):
    def test_remove_UI_elements(self):
        register_screen = Register_Screen("Test_Register")

        # Show UI elements first
        register_screen.show_UI_elements()

        # Test removing UI elements
        register_screen.remove_UI_elements()

        # Assert that UI elements are hidden
        self.assertFalse(register_screen._Get_User_Info_Screen__USERNAME_INPUT.visible) 
        self.assertFalse(register_screen._Get_User_Info_Screen__PASSWORD_INPUT.visible)
        self.assertFalse(register_screen._Get_User_Info_Screen__GO_BACK_BUTTON.visible)
        self.assertFalse(register_screen._Get_User_Info_Screen__TITLE_LABEL.visible)
        

    def test_show_UI_elements(self):
        register_screen = Register_Screen("Test_Register")

        # Hide elements first 
        register_screen.remove_UI_elements()

        # Test showing UI elements
        register_screen.show_UI_elements()

        # Assert that UI elements are visible
        self.assertTrue(register_screen._Get_User_Info_Screen__USERNAME_INPUT.visible)
        self.assertTrue(register_screen._Get_User_Info_Screen__USERNAME_INPUT.visible)
        self.assertTrue(register_screen._Get_User_Info_Screen__USERNAME_INPUT.visible)
        self.assertTrue(register_screen._Get_User_Info_Screen__USERNAME_INPUT.visible)
    
    def test_register_user(self):
        register_screen = Register_Screen("Test_Register")

        # Set Username and Password
        register_screen.set_username("TestUsername")
        register_screen.set_password("TestPassword")
        test_username = register_screen.get_username()
        test_password = register_screen.get_password()

        # Check if registration was successful for the the test inputs
        self.assertTrue(register_screen.register(test_username, test_password))
    
class TestLoginScreen(unittest.TestCase):
    def test_remove_UI_elements(self):
        login_screen = Login_Screen("LOGIN")

        # Show UI elements first 
        login_screen.show_UI_elements()

        # Test removing UI elements
        login_screen.remove_UI_elements()

        # Assert that UI elements are hidden
        # Accessing a private variable from the outside 'https://stackoverflow.com/questions/31277974/accessing-private-class-variable'
        self.assertFalse(login_screen._Get_User_Info_Screen__USERNAME_INPUT.visible) 
        self.assertFalse(login_screen._Get_User_Info_Screen__PASSWORD_INPUT.visible)
        self.assertFalse(login_screen._Get_User_Info_Screen__GO_BACK_BUTTON.visible)
        self.assertFalse(login_screen._Get_User_Info_Screen__TITLE_LABEL.visible)

    def test_show_UI_elements(self):
        login_screen = Login_Screen("LOGIN")

        # Hide elements first 
        login_screen.remove_UI_elements()

        # Test showing UI elements
        login_screen.show_UI_elements()

        # Assert that UI elements are visible
        self.assertTrue(login_screen._Get_User_Info_Screen__USERNAME_INPUT.visible)
        self.assertTrue(login_screen._Get_User_Info_Screen__USERNAME_INPUT.visible)
        self.assertTrue(login_screen._Get_User_Info_Screen__USERNAME_INPUT.visible)
        self.assertTrue(login_screen._Get_User_Info_Screen__USERNAME_INPUT.visible)
        
    def test_login_user(self):
        login_screen = Login_Screen("LOGIN")

        login_screen.set_username("Alejandro_DGZ")
        login_screen.set_password("Password1")
        self.assertTrue(login_screen.login(login_screen.get_username(), login_screen.get_password()))

if __name__ == "__main__":
    unittest.main()
