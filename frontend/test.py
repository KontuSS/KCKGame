import pygame
import sys
from enum import Enum
from time import sleep
class CardPosition(Enum):
    KARTY_STOLU = 1
    KARTY_GRACZA = 2
    KARTY_PRZECIWNIKA_1 = 3
    KARTY_PRZECIWNIKA_2 = 4
    KARTY_PRZECIWNIKA_3 = 5
# Inicjalizacja Pygame
pygame.init()
player_score=10
# Przykładowa lista kart gracza
player_cards = ['2C', '3C', '4C']
player1_cards = ['2C', '3C', '4C']
player2_cards = ['2C', '3C', '4C']
player3_cards = ['2C', '3C', '4C']
hause_cards = ['2C', '3C', '4C','6C']
liczba_graczy = 4
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Poker Game")

# Załadowanie grafik
table_img = pygame.image.load("C:\\Users\\krzes\\OneDrive\\Pulpit\\pythonProject\\przykladowy flask\\KCKGame\\grafiki\\inne elementy\\stol_testowy.png")
card_back = pygame.image.load("C:\\Users\\krzes\\OneDrive\\Pulpit\\pythonProject\\przykladowy flask\\KCKGame\\grafiki\\inne elementy\\tyl_karty.png")
def get_card_image(card_name):
    card_image_path = f"C:\\Users\\krzes\\OneDrive\\Pulpit\\pythonProject\\przykladowy flask\\KCKGame\\grafiki\\Karty\\[\'{card_name}\'].png"
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

def draw_button(button_rect, text):
    pygame.draw.rect(screen, (0, 0, 255), button_rect)
    font = pygame.font.Font(None, 36)
    text_render = font.render(text, True, (255, 255, 255))
    # Wyśrodkowanie tekstu w przycisku
    text_rect = text_render.get_rect(center=button_rect.center)
    screen.blit(text_render, text_rect)

def draw_action_buttons(mouse_pos, mouse_clicked):
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

    # Kolejność: fold, hold, check
    fold_rect = pygame.Rect(start_x, start_y, button_width, button_height)
    hold_rect = pygame.Rect(start_x + button_width + gap, start_y, button_width, button_height)
    check_rect = pygame.Rect(start_x + 2 * (button_width + gap), start_y, button_width, button_height)

    # Rysowanie przycisków
    draw_button(fold_rect, "fold")
    draw_button(hold_rect, "hold")
    draw_button(check_rect, "check")

    # Rysowanie przycisku "Raise" w lewym dolnym rogu
    raise_button_rect = pygame.Rect(margin, screen_height - button_height - margin, button_width, button_height)
    draw_button(raise_button_rect, "Raise")

    # Obsługa kliknięcia przycisków
    if mouse_clicked:
        if fold_rect.collidepoint(mouse_pos):
            print("fold clicked")
        elif hold_rect.collidepoint(mouse_pos):
            print("hold clicked")
        elif check_rect.collidepoint(mouse_pos):
            print("check clicked")
        elif raise_button_rect.collidepoint(mouse_pos):
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
    background = pygame.image.load("C:\\Users\\krzes\\OneDrive\\Pulpit\\pythonProject\\przykladowy flask\\KCKGame\\grafiki\\inne elementy\\EkranStart.png")
    input_box = pygame.Rect(300, 300, 200, 40)
    font = pygame.font.Font(None, 32)
    play_button = pygame.Rect(350, 400, 100, 50)
    text = ''
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    holder = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

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
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos) and len(text) > 0:
                    return text
 
        clock.tick(60)
        pygame.display.flip()
def display_win():
    """
    Wyświetla obraz o wygranej na środku ekranu.
    """
    win_image = pygame.image.load("C:\\Users\\krzes\\OneDrive\\Pulpit\\pythonProject\\przykladowy flask\\KCKGame\\grafiki\\inne elementy\\Wygrana.png")
    win_image = pygame.transform.scale(win_image, (screen.get_width(), screen.get_height()))
    screen.blit(win_image, (0, 0))
    pygame.display.flip()

def display_loss():
    """
    Wyświetla obraz o przegranej na środku ekranu.
    """
    loss_image = pygame.image.load("C:\\Users\\krzes\\OneDrive\\Pulpit\\pythonProject\\przykladowy flask\\KCKGame\\grafiki\\inne elementy\\Przegrana.png")
    loss_image = pygame.transform.scale(loss_image, (screen.get_width(), screen.get_height()))
    screen.blit(loss_image, (0, 0))
    pygame.display.flip()

def start_pygame_ui(game):
    nick = start_screen()
    # tu wpisuje imię gracza i robię pentelkę aż reszta graczy wkroczy 
    while True:
        liczba_graczy = 4  #zapytanie do serwera o liste graczy
        if liczba_graczy == 4:
            break
        sleep(100)
    clock = pygame.time.Clock()
    # game.add_player(nick)
    # Dane dotyczące kart – szerokość, wysokość, odstęp
    card_width = 71
    card_height = 96
    gap = 10
    num_cards = len(player_cards)
    total_cards_width = num_cards * card_width + (num_cards - 1) * gap

    # Obliczenie pozycji, aby wyśrodkować karty na ekranie (stół)

    #zapytanie o karty do konkretnego gracza i ustawienie ich
    while True:

        #update odnośnie co się dzieje
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
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
            # Rysowanie kart przeciwnika 2
            draw_cards(player2_cards, position=CardPosition.KARTY_PRZECIWNIKA_2, face_up=False)
        except:
            pass
        try:
            # Rysowanie kart przeciwnika 1
            draw_cards(player3_cards, position=CardPosition.KARTY_PRZECIWNIKA_3, face_up=False)
        except:
            pass
        # Rysowanie przycisków akcji w prawym dolnym rogu
        draw_action_buttons(mouse_pos, mouse_clicked)
        draw_player_info(nick, player_score)
        pygame.display.flip()
        clock.tick(60)

start_pygame_ui(None)
