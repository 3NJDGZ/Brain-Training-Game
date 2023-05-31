-- KEY = "encryptionkey1234"
-- SALTS randomly generated within the Python Code and then hashed via MD5

-- Creating Tables:
CREATE TABLE Player (
    PlayerID int NOT NULL AUTO_INCREMENT,
    Username varchar(50),
    Password varbinary(100),
    Salt varchar(100),
    PRIMARY KEY (PlayerID)
);
CREATE TABLE CognitiveArea (
    CognitiveAreaID int NOT NULL AUTO_INCREMENT,
    Name varchar(50),
    PRIMARY KEY(CognitiveAreaID)
);
CREATE TABLE CPS (
    PlayerID int NOT NULL,
    DateCalculated date,
    CPS real,
    PRIMARY KEY (PlayerID),
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
);
CREATE TABLE Performance (
    PlayerID int NOT NULL,
    CognitiveAreaID int NOT NULL,
    Score int,
    PRIMARY KEY (PlayerID, CognitiveAreaID),
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
    FOREIGN KEY (CognitiveAreaID) REFERENCES CognitiveArea(CognitiveAreaID)
);
CREATE TABLE Weights (
    PlayerID int NOT NULL,
    CognitiveAreaID int NOT NULL,
    WeightValue real,
    PRIMARY KEY (PlayerID, CognitiveAreaID),
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
    FOREIGN KEY (CognitiveAreaID) REFERENCES CognitiveArea(CognitiveAreaID)
);

-- Inserting Records into the DB:
INSERT INTO Player (Username, Password, Salt) 
VALUES 
	('AlejandroDGZ', aes_encrypt(concat('Password1', md5('salt1')), 'encryptionkey1234'), md5('salt1')),
    ('Meso', aes_encrypt(concat('Password2', md5('salt2')), 'encryptionkey1234'), md5('salt2'));

INSERT INTO CPS (PlayerID, DateCalculated, CPS)
VALUES (1, '2023-04-15', 58.32), -- Player 1 with PlayerID 1
	   (2, '2023-04-15', 66.74); -- Player 2 with PlayerID 2

INSERT INTO CognitiveArea (Name)
VALUES ('Memory');
INSERT INTO CognitiveArea (Name)
VALUES ('Attention');
INSERT INTO CognitiveArea (Name)
VALUES ('Speed');
INSERT INTO CognitiveArea (Name)
VALUES ('ProblemSolving');

INSERT INTO Weights (PlayerID, CognitiveAreaID, WeightValue)
VALUES (1, 1, 0.36), (1, 2, 0.20), (1, 3, 0.30), (1, 4, 0.14), -- Player 1 with PlayerID 1
	   (2, 1, 0.02), (2, 2, 0.18), (2, 3, 0.38), (2, 4, 0.42); -- Player 2 with PlayerID 2

INSERT INTO Performance (PlayerID, CognitiveAreaID, Score)
VALUES (1, 1, 30), (1, 2, 74), (1, 3, 96), (1, 4, 28), -- Player 1 with PlayerID 1
	   (2, 1, 54), (2, 2, 69), (2, 3, 97), (2, 4, 39); -- Player 2 with PlayerID 2

