-- Creating Tables:
CREATE TABLE Player (
    PlayerID int NOT NULL AUTO_INCREMENT,
    Username varchar(50),
    Password varchar(50),
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
INSERT INTO Player (Username, Password) 
VALUES 
	('Alejandro_DGZ', 'Password1'),
    ('Meso', 'Password2'),
    ('Pluto', 'Password3'),
    ('Russo', 'Password4');

INSERT INTO CPS (PlayerID, DateCalculated, CPS)
VALUES (1, '2023-04-15', 58.32), -- Player 1 with PlayerID 1
	   (2, '2023-04-15', 66.74), -- Player 2 with PlayerID 2
	   (3, '2023-04-15', 40.40), -- Player 3 with PlayerID 3
	   (4, '2023-04-15', 86.60) -- Player 4 with PlayerID 4
;

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
	   (2, 1, 0.02), (2, 2, 0.18), (2, 3, 0.38), (2, 4, 0.42), -- Player 2 with PlayerID 2
	   (3, 1, 0.38), (3, 2, 0.33), (3, 3, 0.21), (3, 4, 0.08), -- Player 3 with PlayerID 3
	   (4, 1, 0.10), (4, 2, 0.11), (4, 3, 0.50), (4, 4, 0.29) -- Player 4 with PlayerID 4
;

INSERT INTO Performance (PlayerID, CognitiveAreaID, Score)
VALUES (1, 1, 30), (1, 2, 74), (1, 3, 96), (1, 4, 28), -- Player 1 with PlayerID 1
	   (2, 1, 54), (2, 2, 69), (2, 3, 97), (2, 4, 39), -- Player 2 with PlayerID 2
	   (3, 1, 42), (3, 2, 20), (3, 3, 64), (3, 4, 55), -- Player 3 with PlayerID 3 
	   (4, 1, 93), (4, 2, 75), (4, 3, 83), (4, 4, 95) -- Player 4 with PlayerID 4
;

