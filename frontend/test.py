import pygame
import sys
from enum import Enum
import socket
import sys
import os
import time
import json
import threading

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from server.client import start_client, return_client_id, return_dto, return_client

global PISZ
PISZ=False
global IDgracz
class CardPosition(Enum):
    KARTY_STOLU = 1
    KARTY_GRACZA = 2
    KARTY_PRZECIWNIKA_1 = 3
    KARTY_PRZECIWNIKA_2 = 4
    KARTY_PRZECIWNIKA_3 = 5
# Inicjalizacja Pygame
class MainDTO(object):
    whichPlayerTurn = None
    ectsInPool = 0
    highestEctsToMatch = 0
    lastPlayerId = None
    lastPlayerAction = None
    gameState = 0
    playerCards = ''
    cardsOnTable = ''

    def __init__(self, whichPlayerTurn=None, ectsInPool=0, highestEctsToMatch=0, 
                 lastPlayerId=None, lastPlayerAction=None, gameState=None, 
                 playerCards='', cardsOnTable=''):
        self.whichPlayerTurn = whichPlayerTurn
        self.ectsInPool = ectsInPool
        self.highestEctsToMatch = highestEctsToMatch
        self.lastPlayerId = lastPlayerId
        self.lastPlayerAction = lastPlayerAction
        self.gameState = gameState
        self.playerCards = playerCards
        self.cardsOnTable = cardsOnTable
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Poker Game")

# Załadowanie grafik
table_img = pygame.image.load("././grafiki/inne elementy/stol_testowy.png")
card_back = pygame.image.load("././grafiki\\inne elementy\\tyl_karty.png")
def get_card_image(card_name):
    color,value = card_name[0], card_name[1:]
    card_image_path = f"././grafiki\\Karty\\[\'{value+color}\'].png"
    return pygame.image.load(card_image_path)
def draw_table():
    scaled_table = pygame.transform.scale(table_img, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_table, (0, 0))
def get_card_img_route(card_name):
    #dodac coś co pogodzi odpowiedź z serwera z e strukturą plików kart
    return ''
def draw_player_info(player_name, player_score):
    """
    Wyświetla nazwę gracza oraz jego wynik w prawym górnym rogu ekranu.
    """
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"{player_name} SCORE:{player_score}", True, (0, 0, 0))
    text_rect = text_surface.get_rect(topright=(screen.get_width() - 10, 10))
    box_rect = pygame.Rect(text_rect.left - 5, text_rect.top - 5, text_rect.width + 10, text_rect.height + 10)
    pygame.draw.rect(screen, (0, 230, 0), box_rect)

    screen.blit(text_surface, text_rect)

def draw_button(button_rect, text, color=(0, 0, 255), text_color=(255, 255, 255)):
    pygame.draw.rect(screen, color, button_rect)
    font = pygame.font.Font(None, 36)
    text_render = font.render(text, True, text_color)
    text_rect = text_render.get_rect(center=button_rect.center)
    screen.blit(text_render, text_rect)

# filepath: /c:/Users/krzes/OneDrive/Pulpit/pythonProject/przykladowy flask/KCKGame/test.py
# ...existing code...

def draw_action_buttons(mouse_pos, mouse_clicked, mouse_pressed, is_player_turn, client):
    """
    Rysuje cztery przyciski akcji (fold, hold, check, raise).
    """
    button_width = 100
    button_height = 50
    gap = 10
    margin = 20
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    total_width = 3 * button_width + 2 * gap
    start_x = screen_width - total_width - margin
    start_y = screen_height - button_height - margin

    # Kolory przycisków i tekstu, zależnie od tury
    active_color = (0, 0, 255)
    inactive_color = (100, 100, 100)
    pressed_color = (255, 0, 0)
    active_text = (255, 255, 255)
    inactive_text = (180, 180, 180)

    # Wybór koloru na podstawie flagi is_player_turn
    def pick_colors():
        if mouse_clicked and is_player_turn:
            return pressed_color, active_text  # Change color when
        elif is_player_turn:
            return active_color, active_text
        else:
            return inactive_color, inactive_text

    # Kolejność: fold, hold, check
    fold_rect = pygame.Rect(start_x, start_y, button_width, button_height)
    hold_rect = pygame.Rect(start_x + button_width + gap, start_y, button_width, button_height)
    check_rect = pygame.Rect(start_x + 2 * (button_width + gap), start_y, button_width, button_height)

    fold_col, fold_text_col = pick_colors()
    hold_col, hold_text_col = pick_colors()
    check_col, check_text_col = pick_colors()

    draw_button(fold_rect, "fold", fold_col, fold_text_col)
    draw_button(hold_rect, "hold", hold_col, hold_text_col)
    draw_button(check_rect, "check", check_col, check_text_col)

    # Rysowanie przycisku "Raise" w lewym dolnym rogu
    raise_button_rect = pygame.Rect(margin, screen_height - button_height - margin, button_width, button_height)
    raise_col, raise_text_col = pick_colors()
    draw_button(raise_button_rect, "Raise", raise_col, raise_text_col)

    # Obsługa kliknięcia przycisków tylko wtedy, gdy to tura gracza
    if is_player_turn and mouse_clicked:
        if client is None:
            print("Client is NONE")

        if fold_rect.collidepoint(mouse_pos):
            client.sendall("4".encode('utf-8'))
            print("fold clicked")
        elif hold_rect.collidepoint(mouse_pos):
            client.sendall("2".encode('utf-8'))
            print("call clicked")
        elif check_rect.collidepoint(mouse_pos):
            client.sendall("3".encode('utf-8'))
            print("check clicked")
        elif raise_button_rect.collidepoint(mouse_pos):
            client.sendall("1 2".encode('utf-8'))
            print("Raise clicked")

def draw_card(x, y, card, face_up=True, rotate=False):
    """
    Rysuje pojedynczą kartę.
    Jeśli face_up jest True – karta jest odkryta (wyświetla obraz karty),
    w przeciwnym wypadku wyświetlany jest obrazek tylnej strony karty.
    """
    card_width = 71
    card_height = 96

    if face_up:
        # Pobieranie obrazu karty
        card_image = get_card_image(card)
        scaled_card_image = pygame.transform.scale(card_image, (card_width, card_height))
        if rotate:
            scaled_card_image = pygame.transform.rotate(scaled_card_image, 90)
        screen.blit(scaled_card_image, (x, y))
    else:
        # Rysowanie zakrytej karty (obrazek tylnej strony)
        scaled_card_back = pygame.transform.scale(card_back, (card_width, card_height))
        if rotate:
            scaled_card_back = pygame.transform.rotate(scaled_card_back, 90)
        screen.blit(scaled_card_back, (x, y))

def draw_cards(cards, position, face_up=True):
    """
    Rysuje listę kart w zależności od pozycji.
    Parametr face_up określa, czy karty mają być odkryte, czy zakryte.
    """
    card_width = 71
    card_height = 96
    gap = 10
    total_width = len(cards) * (card_width + gap) - gap

    if position == CardPosition.KARTY_STOLU:
        start_x = (screen.get_width() - total_width) // 2
        start_y = screen.get_height() // 2 - card_height // 2
    elif position == CardPosition.KARTY_GRACZA:
        start_x = (screen.get_width() - total_width) // 2
        start_y = screen.get_height() - card_height - 20
    elif position == CardPosition.KARTY_PRZECIWNIKA_1:
        start_x = 20
        start_y = (screen.get_height() - total_width) // 2
    elif position == CardPosition.KARTY_PRZECIWNIKA_2:
        start_x = screen.get_width() - card_height - 20
        start_y = (screen.get_height() - total_width) // 2
    elif position == CardPosition.KARTY_PRZECIWNIKA_3:
        start_x = (screen.get_width() - total_width) // 2
        start_y = 20

    for i, card in enumerate(cards):
        if position in [CardPosition.KARTY_PRZECIWNIKA_1, CardPosition.KARTY_PRZECIWNIKA_2]:
            x = start_x
            y = start_y + i * (card_width + gap)
            draw_card(x, y, card, face_up, rotate=True)
        else:
            x = start_x + i * (card_width + gap)
            y = start_y
            draw_card(x, y, card, face_up, rotate=False)
def start_screen():
    background = pygame.image.load("././grafiki\\inne elementy\\EkranStart.png")
    input_box = pygame.Rect(300, 300, 200, 40)
    font = pygame.font.Font(None, 32)
    play_button = pygame.Rect(350, 400, 100, 50)
    text = ''
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    holder = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    pygame.mixer.init()  # Inicjalizacja modułu mixer
    pygame.mixer.music.load("././grafiki/music/poczatek.mp3")  # Załaduj plik muzyczny
    pygame.mixer.music.play(-1) 
    while True:
 
        screen.blit(holder, (0, 0))
        # Rysowanie pola tekstowego
        pygame.draw.rect(screen, (255, 255, 255), input_box, 0)
        txt_surface = font.render(text, True, (0, 0, 0))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Rysowanie przycisku Play
        pygame.draw.rect(screen, (0, 128, 0), play_button)
        play_text_surface = font.render("PLAY", True, (255, 255, 255))
        play_text_rect = play_text_surface.get_rect(center=play_button.center)
        screen.blit(play_text_surface, play_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(text) > 0:
                    pygame.mixer.music.stop()
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos) and len(text) > 0:
                    pygame.mixer.music.stop()
                    return text
 
        clock.tick(60)
        pygame.display.flip()
def display_win():
    """
    Wyświetla obraz o wygranej na środku ekranu.
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load("././grafiki/music/wygrana.mp3")  # 
    win_image = pygame.image.load("././grafiki\\inne elementy\\Wygrana.png")
    win_image = pygame.transform.scale(win_image, (screen.get_width(), screen.get_height()))
    screen.blit(win_image, (0, 0))
    pygame.display.flip()

def display_loss():
    """
    Wyświetla obraz o przegranej na środku ekranu.
    """
    pygame.mixer.music.stop()
    pygame.mixer.music.load("././grafiki/music/przegrana.mp3")  # 
    loss_image = pygame.image.load("././grafiki\\inne elementy\\Przegrana.png")
    loss_image = pygame.transform.scale(loss_image, (screen.get_width(), screen.get_height()))
    screen.blit(loss_image, (0, 0))
    pygame.display.flip()
#zmaina folntu
def cokolwiek():
    start_client("ADAM")

    pass
def listin_for_changrs_dto():




    pass
def start_pygame_ui():
    hause_cards = []
    player_cards = ['C4', 'D5']
    liczba_graczy = 1
    nick = start_screen()
    print(nick)
    #print(nick.type())
    threading.Thread(target=start_client, args=(nick,)).start()
    time.sleep(2)
    IDgracz = return_client_id()
    client = return_client()
    # tu wpisuje imię gracza i robię pentelkę aż reszta graczy wkroczy 
    #IDgracz = int(client.recv(1024).decode('utf-8'))
    time.sleep(5)
    dto = return_dto()
    clock = pygame.time.Clock()
    # game.add_player(nick)
    # Dane dotyczące kart – szerokość, wysokość, odstęp
    #player_cards = []
    print("check dto")
    if dto!=None: #and dto.whichPlayerTurn==IDgracz:
        player_cards = dto.playerCards.split(', ')
        print("nie jest none")
        #hause_cards = dto.cardsOnTable.split(', ')
    print(player_cards)
    card_width = 71
    card_height = 96
    gap = 10
    num_cards = len(player_cards)
    total_cards_width = num_cards * card_width + (num_cards - 1) * gap

    # Obliczenie pozycji, aby wyśrodkować karty na ekranie (stół)
    
    #zapytanie o karty do konkretnego gracza i ustawienie ich
    pygame.mixer.music.load("././grafiki/music/rozgrywka.mp3")  # Załaduj plik muzyczny
    pygame.mixer.music.play(-1) 
    #stop jak wyjdzie decyzja o rzogrywce
    player_score = 0
    #player_cards=[]
    while True:
        time.sleep(0.1)
        dto_UI = return_dto()
        #update odnośnie co się dzieje
        mouse_clicked = False
        mouse_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
                mouse_pressed = True
                
        mouse_pos = pygame.mouse.get_pos()

        draw_table()
        try:
            draw_cards(hause_cards, position=CardPosition.KARTY_STOLU, face_up=True)
        except:
            pass
        try:
            # Rysowanie kart gracza
            draw_cards(player_cards, position=CardPosition.KARTY_GRACZA, face_up=True)
        except:
            pass
        try:
            # Rysowanie kart przeciwnika 1
            draw_cards(player1_cards, position=CardPosition.KARTY_PRZECIWNIKA_1, face_up=False)
        except:
            pass
        try:
            # Rysowanie kart przeciwnika 1
            draw_cards(player2_cards, position=CardPosition.KARTY_PRZECIWNIKA_2, face_up=False)
        except:
            pass

        if dto_UI!=None and len(dto_UI.playerCards.split(','))>0 and len(player_cards)!=2 :
            # wyn=get_card(dto_UI.playerCards)
            player_cards=dto_UI.playerCards.split(',')
            #hause_cards = dto_UI.cardsOnTable.split(', ')
        if dto_UI!=None and len(dto_UI.cardsOnTable.split(','))>0 and len(hause_cards)!=3 :
            # wyn=get_card(dto_UI.playerCards)
            hause_cards = dto_UI.cardsOnTable.split(', ')
        if dto_UI is not None and dto_UI.whichPlayerTurn is not None:
            if int(IDgracz) == int(dto_UI.whichPlayerTurn):
                my_turn = True
            else:
                my_turn = False
        else:
            my_turn = False
        #tu trzeba wstawić check czy wygrana czy przegrana i wyświetlić funkcje tylko plus wyswietlenie kart domu Przemek
        # Rysowanie przycisków akcji w prawym dolnym rogu
        draw_action_buttons(mouse_pos, mouse_clicked, mouse_pressed, my_turn, client)
        draw_player_info(nick,0)
        pygame.display.flip()
        clock.tick(60)
        player1_cards = player_cards
        player2_cards = player_cards
        

start_pygame_ui()
# def get_card(res):
#     for id_i_czards in res.split(':'):
#         id= id_i_czards.split(' ')[0]
#         if id == IDgracz:
#             return id_i_czards.split(' ')[1]
        
#     return ''