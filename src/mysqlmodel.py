# import necessary modules
import mysql.connector
import json # used for loading and creating the settings file for each user/player, tutorial: https://www.youtube.com/watch?v=__mZO-53PPM
import argon2 # used for the password hashing and encryption
import os
from abc import ABC # abstract base class used to create the 'template' class 

class MySQLDatabaseConnection: # A class that represents a connection to the DB.
    def __init__(self): # Makes a DB connection as an attribute, returns nothing.
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="MainDB"
        )

    def get_cursor(self): # used to get the cursor allowing executiong of SQL commands, returns cursor() object.
        return self.db.cursor()

class MySQLDatabaseModel(ABC): # A class that represents the DB Model and takes the parameter of the DB connection, returns nothing.
    def __init__(self, DBC: MySQLDatabaseConnection): # sets up the DB connection attribute, returns nothing
        self._DBC = DBC

class PlayerDataManager(MySQLDatabaseModel):
    def __init__(self, DBC: MySQLDatabaseConnection):
        super().__init__(DBC)
        self.ph = argon2.PasswordHasher() # password hasher module used to hash the user passwords

        # attributes used to temporarily store necessary player information in order to retireve information later after user registration/login 
        # e.g., calculating and storing user CPS
        self.__username = "" 
        self.__player_id = None

        self.__username_available = False # boolean value used for player registration to check if user input username is available or not

        with open('src/setting save files/default_settings.txt') as file:
            self.__exercise_settings = json.load(file) # loads the default settings file automatically for each user
        
    def get_question_answer_from_settings(self):
        return self.__exercise_settings['Question Recall']['Question'], self.__exercise_settings['Question Recall']['Answer']

    def change_settings_according_to_user(self, difficulty_mm, difficulty_a, difficulty_st, question, answer):
        changed_settings = {} # https://www.w3schools.com/python/gloss_python_dictionary_add_item.asp, settings file is just a dictionary with loads of other dictionaries inside of it
                                # each representing a difficulty fo each exercise and their corrsponding parameters

        # essentially adding each dictionary within the main 'changed_settings' dictionary
        # Change Difficulty of Memory Matrix
        if difficulty_mm == 'Easy':
            changed_settings['Memory Matrix'] = {'Difficulty': f'{difficulty_mm}',
                                                 'Parameters': [
                                                     [3, 6], # first trail
                                                     [10, 14], # second trail 
                                                     [19, 22] # third trail
                                                 ]}
        elif difficulty_mm == 'Medium':
            changed_settings['Memory Matrix'] = {'Difficulty': f'{difficulty_mm}',
                                                 'Parameters': [
                                                     [5, 10], # first trail
                                                     [13, 18], # second trail 
                                                     [20, 26] # third trail
                                                 ]}
        elif difficulty_mm == 'Hard':
            changed_settings['Memory Matrix'] = {'Difficulty': f'{difficulty_mm}',
                                                 'Parameters': [
                                                     [7, 13], # first trail
                                                     [16, 20], # second trail 
                                                     [26, 30] # third trail
                                                 ]}
        
        # Change difficulty of Aiming
        if difficulty_a == 'Easy (15s, +25pts)':
            changed_settings['Aiming'] = {'Difficulty': f'{difficulty_a}',
                                          'Parameters': [[15, 25]]}
        elif difficulty_a == 'Medium (10s, +50pts)':
            changed_settings['Aiming'] = {'Difficulty': f'{difficulty_a}',
                                          'Parameters': [[10, 50]]}
        elif difficulty_a == 'Hard (5s, +100pts)':
            changed_settings['Aiming'] = {'Difficulty': f'{difficulty_a}',
                                          'Parameters': [[5, 100]]}
        
        # Change difficulty of Shulte Table
        if difficulty_st == 'Easy (4*4)':
            changed_settings['Schulte Table'] = {'Difficulty': f'{difficulty_st}',
                                                 'Grid Dimension': 4,
                                                 'Colour': False}
        elif difficulty_st == 'Hard (5*5)':
            changed_settings['Schulte Table'] = {'Difficulty': f'{difficulty_st}',
                                                 'Grid Dimension': 5,
                                                 'Colour': False}
        elif difficulty_st == 'Hard (5*5 + colour)':
            changed_settings['Schulte Table'] = {'Difficulty': f'{difficulty_st}',
                                                        'Grid Dimension': 5,
                                                        'Colour': True}
        elif difficulty_st == 'Easy (4*4 + colour)':
            changed_settings['Schulte Table'] = {'Difficulty': f'{difficulty_st}',
                                                 'Grid Dimension': 4,
                                                 'Colour': True}
        
        # Add Question + Answer to Settings
        changed_settings['Question Recall'] = {'Question': question,
                                               'Answer': answer}

        # creates a new file with the file naming system as: {username}_settings.txt 
        # dumps said contents of the dictionary 'changed_settings' into the newly created file
        with open(f'src/setting save files/{self.__username}_settings.txt', 'w') as file:
            json.dump(changed_settings, file)
        
        self.load_settings() # load settings
    
    def check_for_user_settings(self, file_name, path, username):
        # https://stackoverflow.com/questions/1724693/find-a-file-in-python, used to find said file in python
        
        # checks if the user that has logged in already has a customised settings file

        found = False
        for root, dirs, files in os.walk(path):
            if file_name in files:
                found = True
        
        if found:
            with open(f'src/setting save files/{username}_settings.txt') as file:
                self.__exercise_settings = json.load(file)
            print("Loaded Customised Settings!")
        else:
            print("Could not find customised settings!")

    def load_settings(self):
        with open(f'src/setting save files/{self.__username}_settings.txt') as file:
            self.__exercise_settings = json.load(file)

    def get_settings(self, exercise_name: str):
        return self.__exercise_settings[exercise_name]

    def set_username(self, username_to_be_set):
        self.__username = username_to_be_set

    def set_player_id(self, player_id_to_be_set):
        self.__player_id = player_id_to_be_set
    
    def get_player_id(self):
        return self.__player_id
    
    def check_if_username_is_available(self, username):
        # retireves all usernames from DB and checks if the username is available via linear search
        mycursor = self._DBC.get_cursor()
        mycursor.execute(
            """
            SELECT Username
            FROM Player;
            """
        )

        records = mycursor.fetchall()
        print(records)

        self.__username_available = True

        for db_username in records:
            if db_username[0] == username:
                self.__username_available = False
        
        mycursor.close()

    def get_username_available(self):
        return self.__username_available

    def register_new_player_data(self, username, password):
        mycursor = self._DBC.get_cursor()

        hashed_pw = self.ph.hash(password) # hashes password

        # inserts user Username + Password into DB
        mycursor.execute(
            f"""
            INSERT INTO Player (Username, Password)
            VALUES (%s, %s)
            """, (username, hashed_pw)
        )

        # Set up default information in Weights Entity 
        current_player_id = self.retrieve_player_id()
        mycursor.execute(
            f"""
            INSERT INTO Weights (PlayerID, CognitiveAreaID, WeightValue)
            VALUES ({current_player_id}, 1, 0.25),
            ({current_player_id}, 2, 0.25),
            ({current_player_id}, 3, 0.25),
            ({current_player_id}, 4, 0.25);
            """
        )

        # Set up default information in Performance Entity
        mycursor.execute(
            f"""
            INSERT INTO Performance (PlayerID, CognitiveAreaID, Score)
            VALUES ({current_player_id}, 1, 0),
            ({current_player_id}, 2, 0),
            ({current_player_id}, 3, 0),
            ({current_player_id}, 4, 0)
            """
        )

        # only used to print info (no actual functionality used for the application, or subroutine)
        mycursor.execute(
            """
            SELECT * 
            FROM Player;
            """
        )

        for record in mycursor:
            print(record)
        
        # commit to the DB
        self._DBC.db.commit()
        mycursor.close()
    
    def register_weights_onto_DB(self, weights):
        mycursor = self._DBC.get_cursor()
        # Get Player_ID
        player_id = self.retrieve_player_id()

        # 'weights' is an array that has all the weight values that will be calculated by the Skill Selection Screen
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
        
        self._DBC.db.commit()
        mycursor.close()
        
    def retrieve_player_id(self):
        mycursor = self._DBC.get_cursor()

        # gets the PlayerID during user registration as the registered user is the most recently added record to the DB
        mycursor.execute(
            """
            SELECT *
            FROM Player
            ORDER BY PlayerID DESC
            """
        )

        records = mycursor.fetchall()
        for record in records:
            current_player_id = record[0]
            break
        
        mycursor.close()
        return current_player_id

    def check_user_login(self, username, password):
        mycursor = self._DBC.get_cursor()

        valid_details = False
        # check if username and password is valid (replace + decrypt passwords)
        mycursor.execute(f"""
        SELECT PlayerID, Username, Password 
        FROM Player
        WHERE Username = %s;
        """, (username, ))

        result = mycursor.fetchone()
        if result:
            if result[1] == username:
                stored_hash = result[2]
                try: 
                    # Decrypting and verifying user input password with hashed password from Database
                    self.ph.verify(stored_hash, password)
                    print("password match")

                    # Check if there is an already pre-existing setting save file and load it, else load default settings
                    self.check_for_user_settings(f'{username}_settings.txt', 'src/setting save files', username)

                    valid_details = True
                    self.set_username(username)
                    self.set_player_id(result[0])
                    print(f"Username: {self.__username}")
                    print(f"Player ID: {self.__player_id}")
                except argon2.exceptions.VerifyMismatchError:
                    print("password do not match")

        mycursor.close()
        return valid_details

    def record_points_from_exercises_on_DB(self, points: int, CognitiveAreaID: int):
        mycursor = self._DBC.get_cursor()

        # updates the scores for corresponding Cognitive Area in the Performance entity for according User
        # this is the method that is called when the record_points_on_DB() from the exercise object is called from that exercise object's scope
        mycursor.execute(f"""
        UPDATE Performance
        SET Score = Score + {points}
        WHERE CognitiveAreaID = {CognitiveAreaID}
        AND PlayerID = {self.__player_id};
        """)
        
        self._DBC.db.commit()
        mycursor.close()

    def extract_corresponding_weights(self):
        mycursor = self._DBC.get_cursor()
        mycursor.execute(f"""
        SELECT WeightValue
        FROM Weights
        WHERE PlayerID = {self.__player_id}
        """)

        weight_values = []
        records = mycursor.fetchall()
        for record in records:
            weight_values.append(record[0])
        mycursor.close()
        return weight_values
    
    def get_CPS(self):
        # method used for the Stats and Performance Screen
        cps_values = []
        mycursor = self._DBC.get_cursor()

        # SQL command essentially gets the the CPS values for the last 5 days
        # https://www.w3schools.com/sql/func_mysql_date_sub.asp, date_sub how-to
        mycursor.execute(f"""
        SELECT CPS, DateCalculated 
        FROM CPS
        WHERE PlayerID = {self.__player_id}
        AND DateCalculated BETWEEN DATE_SUB(CURDATE(), INTERVAL 5 DAY) AND CURDATE() 
        LIMIT 5;
        """)

        cps_values_last_5_days = mycursor.fetchall()
        # appends each value (being a CPS value and a corresponding Date) into an array
        for cps_value in cps_values_last_5_days:
            formatted_date = cps_value[1].strftime("%Y-%m-%d") # formats the date into a nicer YEAR/MONTH/DAY format
            cps_values.append([str(cps_value[0]), formatted_date])
        
        mycursor.close()
        return cps_values
        
    def calculate_CPS(self):
        weight_values = []
        score_values = []
        invalid_stats = False
        
        # extract the score values from the DB
        mycursor = self._DBC.get_cursor()
        mycursor.execute(f"""
        SELECT Score
        FROM Performance
        WHERE PlayerID = {self.__player_id}
        """)

        # only used for printing information...
        records = mycursor.fetchall()
        for score_value in records:
            score_values.append(score_value[0])
        
        print(f"Score Values: {score_values}")
        
        # extract the corresponding weight values
        mycursor.execute(f"""
        SELECT WeightValue
        FROM Weights
        WHERE PlayerID = {self.__player_id}
        """)

        records = mycursor.fetchall()
        for weight_value in records:
            weight_values.append(weight_value[0])
        
        print(f"Weight Values: {weight_values}")

        # calculate the CPS

        # checks if the user stats from the Performance entity are valid, aka, each score value is above 0
        for score_value in score_values:
            if score_value == 0:
                invalid_stats = True
        
        if not invalid_stats:
            # Calculates the weighted sum CPS value
            CPS = (score_values[0] * weight_values[0]) + (score_values[1] * weight_values[1]) + (score_values[2] * weight_values[2]) + (score_values[3] * weight_values[3])
            print(f"CPS: {CPS}")

            # Checks if the CPS has already been calculated for today
            mycursor.execute(f"""
            SELECT *
            FROM CPS
            WHERE DateCalculated = CURDATE()
            AND PlayerID = {self.__player_id}
            """)
            dates = mycursor.fetchall()
            temp_dates = []
            for date in dates:
                temp_dates.append(date)
            if len(temp_dates) >= 1:
                print("can't calculate cps today as you have already calculated it!")
            else:
                # if it has not been calculated today, then record the CPS value onto the database
                mycursor.execute(f"""
                INSERT INTO CPS (PlayerID, DateCalculated, CPS)
                VALUES ({self.__player_id}, CURDATE(), {CPS})
                """)

        else:
            print("You need to have scores in each cognitive area! (that is not 0)")
        self._DBC.db.commit()
        mycursor.close()

    def retrieve_top_5_players(self):
        # retrieves the top 5 players with the highest CPS for today
        # used for extracting information needed to display the Leaderboard
        top_5 = []
        mycursor = self._DBC.get_cursor()

        mycursor.execute(f"""
        SELECT Username, CPS
        FROM Player, CPS
        WHERE CPS.PlayerID = Player.PlayerID
        AND CPS.DateCalculated = CURDATE()
        ORDER BY CPS DESC
        LIMIT 5
        """)

        records = mycursor.fetchall()

        for record in records:
            top_5.append(record)

        mycursor.close()
        return top_5