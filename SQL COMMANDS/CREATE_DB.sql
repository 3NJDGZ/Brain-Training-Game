
-- use TestDB;
USE MainDB;
-- Creating Tables:
CREATE TABLE Player (
    PlayerID int NOT NULL AUTO_INCREMENT,
    Username varchar(50),
    Password varchar(100),
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
    PRIMARY KEY (PlayerID, DateCalculated),
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

INSERT INTO CognitiveArea (Name)
VALUES ('Memory');
INSERT INTO CognitiveArea (Name)
VALUES ('Attention');
INSERT INTO CognitiveArea (Name)
VALUES ('Speed');
INSERT INTO CognitiveArea (Name)
VALUES ('ProblemSolving');