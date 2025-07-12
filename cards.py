import pygame

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blackjack Test")

# Colors
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up font (better for suits)
font = pygame.font.SysFont("dejavusans", 48)  # smaller font size

# Card text (example)
card_text = "A♠️"  # Ace of Spades

# Create a text surface
card_surface = font.render(card_text, True, BLACK)

# Card dimensions
card_width = 100
card_height = 150
card_x = 100
card_y = 100
card_border_radius = 12  # rounded corners

# Game loop
running = True
while running:
    screen.fill(GREEN)  # Table background color

    # Draw card rectangle (white card with black border)
    card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
    pygame.draw.rect(
        screen, WHITE, card_rect, border_radius=card_border_radius
    )  # White fill
    pygame.draw.rect(
        screen, BLACK, card_rect, width=2, border_radius=card_border_radius
    )  # Black border

    # Center the card text inside the card
    text_rect = card_surface.get_rect(center=card_rect.center)
    screen.blit(card_surface, text_rect)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
