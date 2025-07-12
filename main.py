import pygame
import sys
from game import Deck, Hand, check_winner
import random

pygame.init()

# --- Define Card Size ---
CARD_WIDTH = 100
CARD_HEIGHT = 140

# Load and scale the back image
back_image = pygame.image.load("assets/cards/back.png")
back_image = pygame.transform.scale(back_image, (CARD_WIDTH, CARD_HEIGHT))

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")
font = pygame.font.SysFont(None, 40)


# Function to draw text
def draw_text(text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# *********************************************************
# # Shuffle animation
# def animate_shuffle(deck, screen):
#     mid = len(deck.cards) // 2
#     left_pile = deck.cards[:mid]
#     right_pile = deck.cards[mid:]

#     for _ in range(30):
#         screen.fill((0, 100, 0))
#         for i in range(len(left_pile)):
#             x = 200 + random.randint(-20, 20)
#             y = 150 + i * 2 + random.randint(-5, 5)
#             screen.blit(back_image, (x, y))
#         for i in range(len(right_pile)):
#             x = 500 + random.randint(-20, 20)
#             y = 150 + i * 2 + random.randint(-5, 5)
#             screen.blit(back_image, (x, y))
#         pygame.display.update()
#         pygame.time.delay(50)

#     for _ in range(10):
#         screen.fill((0, 100, 0))
#         for i in range(len(deck.cards)):
#             x = 300 + random.randint(-30, 30)
#             y = 200 + random.randint(-30, 30)
#             screen.blit(back_image, (x, y))
#         pygame.display.update()
#         pygame.time.delay(50)

#     pygame.time.delay(300)


# *************************************************************************************


def animate_shuffle(surface, cards, y=300):
    surface.fill((0, 128, 0))  # clear with green background
    pygame.display.update()

    for i, card in enumerate(cards):
        for x in range(0, 600, 20):  # move card from left to right
            surface.fill((0, 128, 0))  # clear screen

            # Draw already "shuffled" cards (face down)
            for j in range(i):
                prev_x = 100 + j * 30
                cards[j].draw(surface, prev_x, y, face_up=False)

            # Draw current card in motion (face down)
            scaled_back = pygame.transform.scale(
                card.back_image, (CARD_WIDTH, CARD_HEIGHT)
            )
            surface.blit(scaled_back, (x, y))

            pygame.display.update()
            pygame.time.delay(10)


# *************************************************************************************


# Blackjack check
def check_initial_blackjack(player, dealer):
    if player.is_blackjack() and dealer.is_blackjack():
        return "Both have blackjack! Tie!"
    elif player.is_blackjack():
        return "Blackjack! You win!"
    elif dealer.is_blackjack():
        return "Dealer has blackjack! You lose!"
    return None


# Deal 2 cards each
def deal_initial_cards(deck, player, dealer):
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())


# Start new game
def start_new_game():
    global deck, player, dealer, player_turn, game_over, result_text, reveal_dealer

    deck = Deck()
    # deck.shuffle()
    # animate_shuffle(deck, screen)

    # ***********************

    # Suppose deck.cards holds Card instances
    deck.shuffle()  # actually shuffle the order of cards in list
    animate_shuffle(screen, deck.cards[:10])  # animate the first 10 for effect

    # *********************

    player = Hand()
    dealer = Hand()
    deal_initial_cards(deck, player, dealer)

    result_text = check_initial_blackjack(player, dealer)
    if result_text:
        reveal_dealer = True
        game_over = True
        player_turn = False
    else:
        reveal_dealer = False
        game_over = False
        player_turn = True
        result_text = ""


# --- Initialize game ---
start_new_game()
clock = pygame.time.Clock()

# --- Main Loop ---
while True:
    screen.fill((0, 100, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if player_turn and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # Hit
                    player.add_card(deck.deal())
                    if player.value > 21:
                        player_turn = False
                        game_over = True
                        reveal_dealer = True
                        result_text = check_winner(player, dealer)
                if event.key == pygame.K_s:  # Stand
                    player_turn = False
                    while dealer.value < 17:
                        dealer.add_card(deck.deal())
                    game_over = True
                    reveal_dealer = True
                    result_text = check_winner(player, dealer)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    start_new_game()
                if event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

    # Draw player hand
    player.draw(screen, 50, 400)
    draw_text(f"Player: {player.value}", 50, 350)

    # Draw dealer hand
    for idx, card in enumerate(dealer.cards):
        x = 50 + idx * (CARD_WIDTH + 10)
        y = 100
        if idx == 0 and not reveal_dealer:
            screen.blit(back_image, (x, y))
        else:
            card.draw(screen, x, y)

    # Options display
    if not game_over and player_turn:
        draw_text("H: Hit", 600, 400)
        draw_text("S: Stand", 600, 450)

    if game_over:
        draw_text(f"Dealer: {dealer.value}", 50, 50)
        if result_text:
            lines = result_text.split("! ")
            y_offset = 20
            for i, line in enumerate(lines):
                if i < len(lines) - 1:
                    line += "!"
                draw_text(
                    line,
                    SCREEN_WIDTH // 2 - font.size(line)[0] // 2,
                    y_offset + i * 40,
                    color=(255, 255, 0),
                )
        draw_text("R: Restart", 600, 400)
        draw_text("Q: Quit", 600, 450)

    pygame.display.update()
    clock.tick(30)
