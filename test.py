import pygame
import time

def display_list_gradually(data_list, screen_width=800, screen_height=600, background_color=(255, 255, 255), text_color=(0, 0, 0), font_size=36, display_interval_ms=500):
    """
    Displays a list of strings on a Pygame screen, adding one element at a time at a specified interval,
    positioned at the top-left corner.

    Args:
        data_list (list): The list of strings to display.
        screen_width (int): The width of the Pygame screen.
        screen_height (int): The height of the Pygame screen.
        background_color (tuple): The RGB color of the background.
        text_color (tuple): The RGB color of the text.
        font_size (int): The size of the font.
        display_interval_ms (int): The interval in milliseconds between adding each element.
    """
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Gradual List Display")
    font = pygame.font.Font(None, font_size)
    displayed_text = ""
    start_time = time.time()
    index = 0

    running = True
    while running:
        current_time = time.time()
        elapsed_time_ms = (current_time - start_time) * 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)

        if index < len(data_list) and elapsed_time_ms >= index * display_interval_ms:
            displayed_text += data_list[index]
            index += 1

        text_surface = font.render(displayed_text, True, text_color)
        text_rect = text_surface.get_rect(topleft=(0, 0))  # Position at top-left
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == '__main__':
    my_list = ['L0', 'L0', 'L0', 'L0', 'L0', 'L0', 'L2', 'L2', 'L2', 'L2', 'L1', 'L1', 'L1', 'L1', 'L1', 'L1']
    display_list_gradually(my_list)