from enum import Enum
from typing import List

from logic.game_helpers import check_if_name_is_used
from networking.errors import PokerError

class GameState(Enum):
    WAITING = 0
    STARTED = 1
    FINISHED = 2

class PlayerState(Enum):
    WAITING = 0
    PLAYING = 1
    FOLDED = 2
    LOST = 3
    JOINED = 4
    READY = 5

class Player:
    def __init__(self, player_id: int, player_name: str, hand: list, player_state: PlayerState, is_starting: bool):
        self.player_id = player_id
        self.player_name = player_name
        self.hand = hand
        self.player_state = player_state
        self.is_starting = is_starting

class House:
    cards: List[str]
    def __init__(self):
        # cards notation - see README
        self.cards = ['H_2', 'H_3', 'H_4', 'H_5', 'H_6', 'H_7', 'H_8', 'H_9', 'H_10', 'H_J', 'H_Q', 'H_K', 'H_A',
 'D_2', 'D_3', 'D_4', 'D_5', 'D_6', 'D_7', 'D_8', 'D_9', 'D_10', 'D_J', 'D_Q', 'D_K', 'D_A',
 'C_2', 'C_3', 'C_4', 'C_5', 'C_6', 'C_7', 'C_8', 'C_9', 'C_10', 'C_J', 'C_Q', 'C_K', 'C_A',
 'S_2', 'S_3', 'S_4', 'S_5', 'S_6', 'S_7', 'S_8', 'S_9', 'S_10', 'S_J', 'S_Q', 'S_K', 'S_A']


class Game:
    players: List[Player]
    def __init__(self):
        self.game_id = 0
        self.player_count = 0
        self.which_player_turn = None
        self.state = GameState.WAITING
        self.players = []
        self.house = House()
    
    def add_new_player(self, player_name: str):
        name_is_used = check_if_name_is_used(player_name, self.players)
        if(name_is_used):
            raise PokerError('Name is already used', 409)

        player_id = self.player_count
        newPlayer = Player(player_id, player_name, [], PlayerState.JOINED, self.player_count == 0)
        self.players.append(newPlayer)

        self.player_count += 1
        return player_id

    def get_players_of_state(self, state: PlayerState):
        players_with_state = []

        for player in self.players:
            if player.player_state == state:
                players_with_state.append(player)
        return players_with_state

    def change_game_state(self, game_state: GameState):
        self.state = game_state

    def set_player_turn(self, player_id: int):
        self.which_player_turn = player_id

    def set_player_state(self, player_id: int, player_state: PlayerState):
        player_index

        for index, player in enumerate(self.players):
            if(player.player_id == player_id):
                player_index = index
        
        self.players[index].player_state = player_state