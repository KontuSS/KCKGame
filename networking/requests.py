from flask import request, jsonify

import json

from flaskr.db import get_db
from logic.game_classes import Game
from networking.errors import PokerError

# db.execute return type is TUPLE or None

# remember to display exception + function name

# IMPORTANT - all requests must have application/json content type header from client
# and use jsonify to parse data sent to client as json

# sample request with db call
def get_game_instance():
    try:
        db = get_db()
        game = db.execute('SELECT * FROM GameInstance').fetchone()
        return 'Your game id is: {}'.format(game['gameID'])
    except BaseException as error:
        return 'An exception occurred while performing get_game_instance: {}'.format(error)
    


class JoinGameBody:
    name: str

    def __init__(self, body):
        self.__dict__ = body

# body: { name: str }
# response: { player_id: int }
def join_game_request(game: Game):
    try:
        body = JoinGameBody(request.json)

        if(len(body.name) == 0):
            raise PokerError('Name is required', 400)
        
        player_id = game.add_new_player(body.name)

        return jsonify({'player_id': player_id, 'hand': []}), 200
    except PokerError as error:
        return error.message, error.status_code
    except:
        return 'Name is required', 400