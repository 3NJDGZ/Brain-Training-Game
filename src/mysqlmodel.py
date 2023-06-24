import mysql.connector
from abc import ABC

class MySQLDatabaseConnection:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="MainDB"
        )

    def get_cursor(self):
        return self.db.cursor()

class MySQLDatabaseModel(ABC):
    def __init__(self, DBC: MySQLDatabaseConnection):
        self._DBC = DBC

class PlayerDataManager(MySQLDatabaseModel):
    def __init__(self, DBC: MySQLDatabaseConnection):
        super().__init__(DBC)
    
    def register_new_player_data(self, username, password, salt):
        mycursor = self._DBC.get_cursor()
        mycursor.execute(
            f"""
            INSERT INTO Player (Username, Password, Salt)
            VALUES ('{username}', aes_encrypt(concat('{password}', md5('{salt}')), 'encryptionkey1234'), md5('{salt}'));
            """
        )

        # Set up default information in Weights Entity 
        current_player_id = self.retrieve_player_id()
        mycursor.execute(
            f"""
            INSERT INTO WEIGHTS (PlayerID, CognitiveAreaID, WeightValue)
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
        mycursor = self._DBC.get_cursor()

        valid_details = False
        # check if username and password is valid (replace + decrypt salted passwords)
        mycursor.execute(f"""
        SELECT Username, replace(cast(aes_decrypt(Password, 'encryptionkey1234') as char(100)), Salt, '') 
        FROM Player
        WHERE Username = %s;
        """, (username, ))

        result = mycursor.fetchone()
        if result:
            if result[0] == username and result[1] == password:
                valid_details = True

        return valid_details

    