DROP TABLE IF EXISTS House;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS GameInstance;

CREATE TABLE GameInstance (
	gameID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	playerCount INTEGER(2) UNIQUE,
	whichPlayerTurn INTEGER(2) NULL UNIQUE
);

CREATE TABLE Player (
	playerID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	ectsPoints INTEGER,
	hand VARCHAR(7) UNIQUE,
	playerState INTEGER(2),
	isStarting INTEGER(1),
	gameID INTEGER,
	FOREIGN KEY (gameID) REFERENCES GameInstance (gameID)
);

CREATE TABLE House (
	tableID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	cardsOnTable VARCHAR(20) NULL UNIQUE,
	ectsPool INTEGER(2) NULL UNIQUE,
	whoWon INTEGER,
	FOREIGN KEY (whoWon) REFERENCES Player (play