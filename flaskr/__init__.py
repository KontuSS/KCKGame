import os

from flask import Flask
import json

from networking.requests import get_game_instance
from logic.game_classes import Game
from networking.requests import *

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Registering db functions into app
    from . import db
    db.init_app(app)

    # ======== GAME CODE START ========
    game = Game()
    # ======== GAME CODE END ========
    
    
    # ======== ENDPOINTS START ========
    
    @app.route('/get-game')
    def get_game():
        return get_game_instance()
    
    @app.route('/get-players-count')
    def get_players_count():
        return str(game.player_count)
    
    @app.route('/join-game', methods=['POST'])
    def join_game():
        return join_game_request(game)

    # ======== ENDPOINTS END ========

    return app
