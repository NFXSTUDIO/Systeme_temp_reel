import pygame
import sys
import os

class SchedulingMaster:
    def __init__(self):
        pygame.init()

        # --- Path to images ---
        self.ASSETS_PATH = os.path.join(os.path.dirname(__file__), "element")

        # --- Colors ---
        self.BACKGROUND_COLOR = (15, 23, 42)
        self.BUTTON_COLOR = (30, 64, 175)
        self.BUTTON_HOVER_COLOR = (37, 99, 235)
        self.TEXT_COLOR = (255, 255, 255)
        self.GRAY_BACKGROUND = (100, 100, 100)
        self.INFO_BG_COLOR = (25, 32, 50)
        self.HELP_BOX_COLOR = (30, 41, 59)

        # --- Window ---
        self.WIDTH, self.HEIGHT = 1000, 650
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Master of scheduling")

        # --- Font ---
        self.title_font = pygame.font.SysFont("Segoe UI", 56, bold=True)
        self.button_font = pygame.font.SysFont("Segoe UI", 28)
        self.info_font = pygame.font.SysFont("Segoe UI", 20)
        self.help_font = pygame.font.SysFont("Segoe UI", 18)

        # --- Load images ---
        self.robot_img = pygame.image.load(os.path.join(self.ASSETS_PATH, "robot.png"))
        self.robot_img = pygame.transform.scale(self.robot_img, (150, 150))

        self.play_icon = pygame.image.load(os.path.join(self.ASSETS_PATH, "play_icon.png"))
        self.play_icon = pygame.transform.scale(self.play_icon, (28, 28))

        self.settings_icon = pygame.image.load(os.path.join(self.ASSETS_PATH, "settings_icon.png"))
        self.settings_icon = pygame.transform.scale(self.settings_icon, (28, 28))

        self.quit_icon = pygame.image.load(os.path.join(self.ASSETS_PATH, "quit_icon.png"))
        self.quit_icon = pygame.transform.scale(self.quit_icon, (28, 28))

        # State variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.show_difficulty = False
        self.show_game = False
        self.show_info_menu = False
        self.show_algo_detail = False
        self.selected_algorithm = None

        # Description of algorithms
        self.algorithm_descriptions = {
            "FCFS": "First-Come, First-Served (FCFS) is a simple scheduling algorithm that processes tasks in the order they arrive. It is easy to implement but can lead to long wait times for short tasks if a long task arrives first.",
            "SJN": "Shortest Job First (SJF) selects the task with the shortest burst time. This non-preemptive algorithm minimizes average waiting time but can starve longer tasks if short ones keep arriving.",
            "RR": "Round Robin (RR) assigns a fixed time quantum to each task and cycles through them. It's preemptive and fair, especially suited for time-sharing systems.",
            "RM": "Rate Monotonic (RM) assigns priorities based on task periods: shorter periods mean higher priority. It is optimal for fixed-priority scheduling of periodic tasks.",
            "EDF": "Earliest Deadline First (EDF) assigns priorities based on deadlines. It is optimal for dynamic-priority scheduling of periodic tasks but can be complex to implement."
        }

    def draw_button(self, text, icon, x, y, w, h, mouse_pos):
        button_rect = pygame.Rect(x, y, w, h)
        color = self.BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, button_rect, border_radius=12)
        if icon:
            self.screen.blit(icon, (x + 10, y + (h - icon.get_height()) // 2))
        text_surf = self.button_font.render(text, True, self.TEXT_COLOR)
        if icon:
            text_rect = text_surf.get_rect(midleft=(x + 55, y + h // 2))
        else:
            text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
        self.screen.blit(text_surf, text_rect)
        return button_rect

    def draw_difficulty_selection(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        title_surf = self.title_font.render("Choose the difficulty", True, self.TEXT_COLOR)
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.WIDTH // 2, 100)))
        subtitle_font = pygame.font.SysFont("Segoe UI", 24, italic=True)
        subtitle_surf = subtitle_font.render("Ready for the challenge? Select your level!", True, self.TEXT_COLOR)
        subtitle_rect = subtitle_surf.get_rect(center=(self.WIDTH // 2, 150))
        self.screen.blit(subtitle_surf, subtitle_rect)

        mouse_pos = pygame.mouse.get_pos()
        buttons = []
        levels = ["Beginner", "Easy", "Intermediate", "Difficult","Custom"]
        start_y = 220
        for i, level in enumerate(levels):
            btn = pygame.Rect(self.WIDTH // 2 - 130, start_y + i * 90, 260, 60)
            color = self.BUTTON_HOVER_COLOR if btn.collidepoint(mouse_pos) else self.BUTTON_COLOR
            pygame.draw.rect(self.screen, color, btn, border_radius=10)
            text_surf = self.button_font.render(level, True, self.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=btn.center)
            self.screen.blit(text_surf, text_rect)
            buttons.append((btn, level))
        return buttons

    def draw_info_menu(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        title_surf = self.title_font.render("Scheduling Algorithms", True, self.TEXT_COLOR)
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.WIDTH // 2, 60)))
        mouse_pos = pygame.mouse.get_pos()
        buttons = []
        algos = ["FCFS", "SJN", "RR", "RM", "EDF"]
        for i, name in enumerate(algos):
            btn = self.draw_button(name, None, self.WIDTH // 2 - 100, 120 + i * 60, 200, 50, mouse_pos)
            buttons.append((btn, name))

        # Pedagogical help
        pygame.draw.rect(self.screen, self.HELP_BOX_COLOR, (100, 450, 800, 150), border_radius=10)
        help_text = [
            "Which algorithm should I choose?",
            "Need simplicity? → FCFS or SJN (non-preemptive)",
            "Want fairness & preemption? → Round Robin (RR)",
            "Hard deadlines? → RM or EDF (real-time)",
            "Static priorities? → RM      "
            "Dynamic? → EDF"
        ]
        for i, line in enumerate(help_text):
            txt = self.help_font.render(line, True, self.TEXT_COLOR)
            self.screen.blit(txt, (120, 465 + i * 22))

        # Back button
        back_btn = self.draw_button("Back", None, 40, self.HEIGHT - 60, 100, 40, mouse_pos)
        return buttons, back_btn

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)
        return lines

    def draw_algo_detail(self, algo_name):
        self.screen.fill(self.INFO_BG_COLOR)
        title_surf = self.title_font.render(algo_name + " Algorithm", True, self.TEXT_COLOR)
        self.screen.blit(title_surf, title_surf.get_rect(topleft=(40, 30)))

        pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (40, 120, 920, 480), border_radius=12)
        description = self.algorithm_descriptions.get(algo_name, "Description coming soon...")
        wrapped_text = self.wrap_text(description, self.info_font, 880)

        for i, line in enumerate(wrapped_text):
            text_surf = self.info_font.render(line, True, self.TEXT_COLOR)
            self.screen.blit(text_surf, (60, 140 + i * 28))

        mouse_pos = pygame.mouse.get_pos()
        return self.draw_button("Back", None, 40, self.HEIGHT - 60, 100, 40, mouse_pos)

    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_algo_detail:
                        back_btn = self.draw_algo_detail(self.selected_algorithm)
                        if back_btn.collidepoint(event.pos):
                            self.show_algo_detail = False
                            self.show_info_menu = True
                    elif self.show_info_menu:
                        algo_buttons, back_btn = self.draw_info_menu()
                        for btn, name in algo_buttons:
                            if btn.collidepoint(event.pos):
                                self.selected_algorithm = name
                                self.show_info_menu = False
                                self.show_algo_detail = True
                        if back_btn.collidepoint(event.pos):
                            self.show_info_menu = False
                    elif self.show_difficulty:
                        difficulty_buttons = self.draw_difficulty_selection()
                        for btn, level in difficulty_buttons:
                            if btn.collidepoint(event.pos):
                                print(f"Difficulty chosen: {level}")
                                self.show_difficulty = False
                                self.show_game = True
                    else:
                        if not self.show_game:
                            play_button = self.draw_button("Play", self.play_icon, 370, 320, 260, 60, mouse_pos)
                            algo_button = self.draw_button("Informations about all algorithms", self.settings_icon, 270, 410, 460, 60, mouse_pos)
                            quit_button = self.draw_button("Exit", self.quit_icon, 370, 500, 260, 60, mouse_pos)

                            if play_button.collidepoint(event.pos):
                                self.show_difficulty = True
                            elif algo_button.collidepoint(event.pos):
                                self.show_info_menu = True
                            elif quit_button.collidepoint(event.pos):
                                self.running = False

            if self.show_algo_detail:
                self.draw_algo_detail(self.selected_algorithm)
            elif self.show_info_menu:
                algo_buttons, back_btn = self.draw_info_menu()
            elif self.show_game:
                self.screen.fill(self.GRAY_BACKGROUND)
            elif self.show_difficulty:
                difficulty_buttons = self.draw_difficulty_selection()
            else:
                self.screen.fill(self.BACKGROUND_COLOR)
                title_surf = self.title_font.render("Maître de l'Ordonnancement", True, self.TEXT_COLOR)
                title_rect = title_surf.get_rect(center=(self.WIDTH // 2, 80))
                self.screen.blit(title_surf, title_rect)
                self.screen.blit(self.robot_img, (self.WIDTH // 2 - self.robot_img.get_width() // 2, 150))
                play_button = self.draw_button("Play", self.play_icon, 370, 320, 260, 60, mouse_pos)
                algo_button = self.draw_button("Informations about all algorithms", self.settings_icon, 270, 410, 460, 60, mouse_pos)
                quit_button = self.draw_button("Exit", self.quit_icon, 370, 500, 260, 60, mouse_pos)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = SchedulingMaster()
    game.run()