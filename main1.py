import pygame
import sys
from game import Deck, Hand, check_winner

pygame.init()


# --- Define Card Size ---
CARD_WIDTH = 100
CARD_HEIGHT = 140

# Load and scale the back image using the defined card size
back_image = pygame.image.load("assets/cards/back.png")
back_image = pygame.transform.scale(
    back_image, (CARD_WIDTH, CARD_HEIGHT)
)  # Use CARD_WIDTH and CARD_HEIGHT

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

font = pygame.font.SysFont(None, 40)


# Function to draw text
def draw_text(text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


import random


def animate_shuffle(deck, screen):
    # Split deck roughly into two halves
    mid = len(deck.cards) // 2
    left_pile = deck.cards[:mid]
    right_pile = deck.cards[mid:]

    for _ in range(30):  # Shuffle animation steps
        screen.fill((0, 100, 0))

        # Draw left pile
        for i in range(len(left_pile)):
            x = 200 + random.randint(-20, 20)
            y = 150 + i * 2 + random.randint(-5, 5)
            screen.blit(back_image, (x, y))

        # Draw right pile
        for i in range(len(right_pile)):
            x = 500 + random.randint(-20, 20)
            y = 150 + i * 2 + random.randint(-5, 5)
            screen.blit(back_image, (x, y))

        pygame.display.update()
        pygame.time.delay(50)

    # Final deck together in center
    for _ in range(10):
        screen.fill((0, 100, 0))
        for i in range(len(deck.cards)):
            x = 300 + random.randint(-30, 30)
            y = 200 + random.randint(-30, 30)
            screen.blit(back_image, (x, y))
        pygame.display.update()
        pygame.time.delay(50)

    pygame.time.delay(300)


def check_initial_blackjack(player, dealer):
    player_blackjack = player.is_blackjack()
    dealer_blackjack = dealer.is_blackjack()

    if player_blackjack and dealer_blackjack:
        return "Both have blackjack! Tie!"
    elif player_blackjack:
        return "Blackjack! You win!"
    elif dealer_blackjack:
        return "Dealer has blackjack! You lose!"
    return None


# Deal initial 2 cards each
def deal_initial_cards(deck, player, dealer):

    global player_turn, game_over, result_text

    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())


# --- Game Start ---
deck = Deck()
deck.shuffle()
animate_shuffle(deck, screen)

player = Hand()
dealer = Hand()
deal_initial_cards(deck, player, dealer)

reveal_dealer = False
result_text = check_initial_blackjack(player, dealer)
if result_text:
    reveal_dealer = True
    # draw_screen()  # If you have a custom draw function
    # pygame.display.update()
    # pygame.time.delay(3000)
    # return  # End game if initial blackjack is detected

player_turn = True
game_over = False
result_text = ""

clock = pygame.time.Clock()

# --- Game Loop ---
while True:
    screen.fill((0, 100, 0))  # Green background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over:
            if player_turn:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:  # Hit
                        player.add_card(deck.deal())

                        if player.value > 21:
                            player_turn = False
                            game_over = True
                            result_text = check_winner(player, dealer)
                    if event.key == pygame.K_s:  # Stand
                        player_turn = False
                        # Dealer's turn
                        while dealer.value < 17:
                            dealer.add_card(deck.deal())
                        game_over = True
                        # result_text = check_final_result(player, dealer)
                        result_text = check_winner(player, dealer)

                        # **************************************************************************py
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    deck = Deck()
                    deck.shuffle()
                    animate_shuffle(deck, screen)
                    player = Hand()
                    dealer = Hand()
                    deal_initial_cards(deck, player, dealer)

                    player_turn = True
                    game_over = False
                    result_text = ""
                if event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

    # Draw Player Hand
    player.draw(screen, 50, 400)
    draw_text(f"Player: {player.value}", 50, 350)

    # Draw Dealer Hand - Ensure the first card is hidden
    for idx, card in enumerate(dealer.cards):
        x = 50 + idx * (CARD_WIDTH + 10)
        y = 100
        if (
            idx == 0 and not game_over and not dealer.is_blackjack()
        ):  # Dealer's first card is hidden

            screen.blit(back_image, (x, y))  # Show back image
        else:
            card.draw(screen, x, y)  # Show the card face up

    # draw_text(f"Dealer: {dealer_hand.value}", 50, 50)

    # Show options
    if not game_over and player_turn:
        draw_text("H: Hit", 600, 400)
        draw_text("S: Stand", 600, 450)

    if game_over:
        draw_text(f"Dealer: {dealer.value}", 50, 50)
        if result_text:
            draw_text(str(result_text), 400, 300, color=(255, 255, 0))
        draw_text("R: Restart", 600, 400)
        draw_text("Q: Quit", 600, 450)

    pygame.display.update()
    clock.tick(30)
