from flaskr.db import get_db

# db.execute return type is TUPLE or None

# remember to display exception + function name

def get_game_instance():
    try:
        db = get_db()
        game = db.execute('SELECT * FROM GameInstance').fetchone()
        return 'Your game id is: {}'.format(game['gameID'])
    except BaseException as error:
        return 'An exception occurred while performing get_game_instance: {}'.format(error)