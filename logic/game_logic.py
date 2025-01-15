from logic.game_classes import Game, GameState, PlayerState
from time import sleep

def wait_for_players_to_pool(game: Game):
    players_ready = game.get_players_of_state(PlayerState.READY)

    if(game.player_count > 2 and len(players_ready) == game.player_count):
        game.change_game_state(GameState.STARTED)

    print('Waiting for players')
    sleep(10)

def start_main_game_loop(game: Game):
    while(1):
        if(game.state == GameState.WAITING):
            wait_for_players_to_pool(game)
        if(game.state == GameState.STARTED):
            print('Game is running')
            sleep(10)
            