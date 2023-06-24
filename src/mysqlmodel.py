# import necessary modules
import mysql.connector
import argon2
from abc import ABC

class MySQLDatabaseConnection:
    """A class that represents a connection to the DB."""
    def __init__(self):
        """Makes a DB connection as an attribute, returns nothing."""
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="MainDB"
        )

    def get_cursor(self):
        """used to get the cursor allowing executiong of SQL commands, returns cursor() object."""
        return self.db.cursor()

class MySQLDatabaseModel(ABC):
    """A class that represents the DB Model and takes the parameter of the DB connection, returns nothing."""
    def __init__(self, DBC: MySQLDatabaseConnection):
        """sets up the DB connection attribute, returs nothing"""
        self._DBC = DBC

class PlayerDataManager(MySQLDatabaseModel):
    """
    A class to represent the Player's Data Manager and connection to the MySQL DB.

    ...

    Attributes
    ----------
    ph : argon2 object
        Password Hasher object used to hash passwords for the DB.
    
    Methods
    -------
    register_new_player_data(username, password):
        registers the new player's relevant data onto the database.
    register_weights_onto_db(weights):
        registers the corresponding weight values from player onto database.
    retireve_player_id():
        returns the most recently added player's PlayerID.
    check_user_login(username, password):
        checks and authorises the user when they are logging in.
    """
    def __init__(self, DBC: MySQLDatabaseConnection):
        """Sets up the argon2 password hasher, returns nothing."""
        super().__init__(DBC)
        self.ph = argon2.PasswordHasher()
    
    def register_new_player_data(self, username, password):
        """
        Registers the new player on the database.

        Inserts relevant information into the entities: 'Player', 'Weights', and 'Performance'

        Parameters
        ----------
        username : str
            username of player
        password : str 
            password of player
        
        Returns
        -------
        None
        """
        mycursor = self._DBC.get_cursor()

        hashed_pw = self.ph.hash(password)

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

        mycursor.execute(
            """
            SELECT * 
            FROM Player;
            """
        )

        for record in mycursor:
            print(record)
        
        self._DBC.db.commit()
    
    def register_weights_onto_DB(self, weights):
        """
        Registers the corresponding weight values onto the database.

        Each weight value corresponds to the importance of each cognitive area.

        Parameters
        ----------
        weights : array
            array of the weight values.
        
        Returns
        -------
        None
        """
        mycursor = self._DBC.get_cursor()
        # Get Player_ID
        player_id = self.retrieve_player_id()

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
        
    def retrieve_player_id(self):
        """
        Retrieves the most recently added player's PlayerID.

        Parameters
        ----------
        None

        Returns
        -------
        current_player_id : int
            the player's PlayerID.
        """
        mycursor = self._DBC.get_cursor()
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
        
        return current_player_id

    def check_user_login(self, username, password):
        """
        Checks and authorises the users inputted details to the info stored within the database.
        

        Parameters
        ----------
        username : str 
            input username from user.
        password : str 
            input password from user.
        
        Returns
        -------
        valid_details : bool
            bool variable that signifies if the details inputted were value or not.
        """
        mycursor = self._DBC.get_cursor()

        valid_details = False
        # check if username and password is valid (replace + decrypt salted passwords)
        mycursor.execute(f"""
        SELECT Username, Password 
        FROM Player
        WHERE Username = %s;
        """, (username, ))

        result = mycursor.fetchone()
        if result:
            if result[0] == username:
                stored_hash = result[1]
                try: 
                    self.ph.verify(stored_hash, password)
                    print("password match")
                    valid_details = True
                except argon2.exceptions.VerifyMismatchError:
                    print("password do not match")

        return valid_details

    