DROP TABLE IF EXIST House;
DROP TABLE IF EXIST Player;
DROP TABLE IF EXIST GameInstace;

CREATE TABLE House {
	tableID integer pk increments unique
	cardsOnTable varchar(20) null unique
	ectsPool integer(2) null unique
	whoWon integer > Player.playerID
}

CREATE TABLE Player {
	playerID integer(3) pk increments unique
	ectsPoints integer(4) def(30)
	hand varchar(7) unique
	playerState integer
	isStarting integer(1)
	gameID integer *> GameInstace.gameID
}

CREATE TABLE GameInstace {
	gameID integer pk increments unique
	playerCount integer(2) null unique
	playerInfo integer(2) unique >* PlayersInfo.infoID
	whichPlayerTurn integer(2) unique
}