import pygame
import random
import time
import os

CARD_WIDTH = 100
CARD_HEIGHT = 140

suits = ["hearts", "spades", "clover", "diamonds"]

ranks = {
    "ace": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "jack": 10,
    "queen": 10,
    "king": 10,
}


# class Card:
#     def __init__(self, rank, suit):
#         self.rank = rank
#         self.suit = suit
#         self.value = ranks[rank]
#         filename = f"{rank}_of_{suit}.png"
#         self.image = pygame.image.load(os.path.join("assets", "cards", filename))
#         self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))

#     def draw(self, surface, x, y):
#         surface.blit(self.image, (x, y))


class Card:
    def __init__(self, rank, suit):

        self.flipped = False  # add this in __init__
        self.rank = rank
        self.suit = suit
        self.value = ranks[rank]
        self.image = pygame.image.load(
            os.path.join("assets", "cards", f"{rank}_of_{suit}.png")
        )
        self.back_image = pygame.image.load(os.path.join("assets", "cards", "back.png"))
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.back_image = pygame.transform.scale(
            self.back_image, (CARD_WIDTH, CARD_HEIGHT)
        )
        self.rect = self.image.get_rect()

    def draw(self, surface, x, y, face_up=True):
        """
        Draw the card on the screen. If face_up is False, draw the back.
        """
        if face_up:
            surface.blit(self.image, (x, y))
        else:
            surface.blit(self.back_image, (x, y))

    def flip(self, surface, x, y, flip_duration=0.5):
        """
        Animate the flip of the card. Shrinks width to 0, then grows it back showing the face.
        """
        frames = 20
        delay = flip_duration / frames

        for i in range(frames):
            progress = i / frames
            surface.fill((0, 128, 0))  # Clear screen with green background

            # Shrink width (0.5 halfway)
            if progress < 0.5:
                scale = 1 - progress * 2
                image = self.back_image
            else:
                scale = (progress - 0.5) * 2
                image = self.image

            new_width = max(1, int(CARD_WIDTH * scale))
            scaled = pygame.transform.scale(image, (new_width, CARD_HEIGHT))
            rect = scaled.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
            surface.blit(scaled, rect.topleft)

            pygame.display.update()
            time.sleep(delay)


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in suits:
            for rank in ranks.keys():
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # track aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == "ace":  # not '1'
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        # if over 21 and have an Ace, adjust
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def is_blackjack(self):
        return self.value == 21

    def draw(self, surface, x, y):
        for idx, card in enumerate(self.cards):
            card.draw(surface, x + idx * (CARD_WIDTH + 10), y)


def game_loop(screen):
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()

    # Deal 2 cards each
    for _ in range(2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())

    # Check for immediate winner before player takes action
    result_text = check_winner(player, dealer)
    if result_text:
        reveal_dealer = True
        pygame.display.update()
        pygame.time.delay(3000)
        return  # End the game if there is a winner immediately

    running = True
    player_turn = True
    reveal_dealer = False
    result_text = None

    # Font setup for text
    font = pygame.font.SysFont(None, 36)

    while running:
        screen.fill((0, 128, 0))  # green background

        # # Draw dealer's cards
        # for idx, card in enumerate(dealer.cards):
        #     x = 50 + idx * (CARD_WIDTH + 10)
        #     y = 100
        #     if idx == 0 and not reveal_dealer:
        #         card.draw(screen, x, y, face_up=False)  # hide first card
        #     else:
        #         card.draw(screen, x, y)

        # **********************************

        # # Draw dealer's cards
        # for idx, card in enumerate(dealer.cards):
        #     x = 50 + idx * (CARD_WIDTH + 10)
        #     y = 100
        #     if idx == 0:
        #         if not reveal_dealer:
        #             card.draw(screen, x, y, face_up=False)  # still hidden
        #         else:
        #             if not hasattr(card, "flipped"):  # only flip once
        #                 card.flip(screen, x, y)
        #                 card.flipped = True  # prevent re-flipping
        #             card.draw(screen, x, y, face_up=True)
        #     else:
        #         card.draw(screen, x, y)

        # ****************************

        for idx, card in enumerate(dealer.cards):
            x = 50 + idx * (CARD_WIDTH + 10)
            y = 100
            if idx == 0:
                if not reveal_dealer:
                    card.draw(screen, x, y, face_up=False)  # show back
                else:
                    if not card.flipped:
                        card.flip(screen, x, y)  # play flip animation
                        card.flipped = True
                    card.draw(screen, x, y, face_up=True)  # show front after flip
            else:
                card.draw(screen, x, y)

        # *****************************************

        # Draw player's cards
        player.draw(screen, 50, 400)

        # Draw info text
        if player_turn:
            instruction = font.render(
                "Press [H] to Hit or [S] to Stand", True, (255, 255, 255)
            )
            screen.blit(instruction, (50, 20))
        elif result_text:
            result_surface = font.render(result_text, True, (255, 215, 0))  # gold color
            screen.blit(result_surface, (50, 20))

        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if player_turn:
                    if event.key == pygame.K_h:  # Hit
                        player.add_card(deck.deal())
                        if player.value > 21:
                            result_text = "Player busts! Dealer wins!"
                            reveal_dealer = True
                            player_turn = False
                    elif event.key == pygame.K_s:  # Stand
                        player_turn = False
                        reveal_dealer = True

        if not player_turn and result_text is None:
            # Dealer's turn after player stands
            while dealer.value < 17:
                dealer.add_card(deck.deal())

            # Check winner
            result_text = check_winner(player, dealer)

        if result_text:
            # Once result_text is set, give player time to read
            pygame.display.update()
            pygame.time.delay(3000)
            running = False


def check_winner(player, dealer):
    if player.value > 21:
        return "You busted. Dealer wins."
    elif dealer.value > 21:
        return "Dealer busted. You win!"
    elif player.value > dealer.value:
        return "You win!"
    elif player.value < dealer.value:
        return "You lose!"
    else:
        return "Tie!"
