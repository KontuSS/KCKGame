from typing import List

def check_if_name_is_used(name: str, players):
    for player in players:
        if player.player_name == name:
            return True
    
    return False