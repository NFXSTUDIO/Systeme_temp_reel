import pygame
import sys

# Initialize Pygame
pygame.init()

# Main window settings
main_window_size = (400, 300)
main_window = pygame.display.set_mode(main_window_size)
pygame.display.set_caption("Main Window")

# Button properties
button_color = (100, 100, 255)
button_rect = pygame.Rect(150, 120, 100, 60)
button_text = pygame.font.Font(None, 32).render("Open", True, (255, 255, 255))
button_text_rect = button_text.get_rect(center=button_rect.center)

# Secondary window state
secondary_window = None
secondary_window_size = (300, 200)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and secondary_window is None:
                secondary_window = pygame.display.set_mode(secondary_window_size)
                pygame.display.set_caption("Secondary Window")

    # Draw main window
    if pygame.display.get_surface() == main_window:
        main_window.fill((200, 200, 200))
        pygame.draw.rect(main_window, button_color, button_rect)
        main_window.blit(button_text, button_text_rect)
    # Draw secondary window
    elif pygame.display.get_surface() == secondary_window:
        secondary_window.fill((150, 150, 150))

    pygame.display.flip()

pygame.quit()
sys.exit()
