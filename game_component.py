import pygame
import time
import random as rd
import process as pro
from process import Process
import window as wd
import sys
import os

launch = False

class Button:
    """
    Button class provides functionality for creating interactive buttons in a Pygame application. It supports rendering buttons with customized styles, handling mouse events, and performing actions.

    Methods:
        - __init__(self, x, y, size_x, size_y, color, hover_color, text, font, text_color, text_color_hover, action=None): Initializes the button with position, size, color, text, font, and an optional action.
        - draw(self, screen): Renders the button on the given Pygame screen. Changes appearance when hovered.
        - handle_event(self, event): Handles mouse events to set hover state and execute the action when clicked.
        - set_action(self, action): Assigns an action to be executed when the button is clicked.
        - get_rect(self): Returns the rectangular area of the button for collision detection.
        - set_text(self, new_text): Updates the button's text and adjusts its appearance accordingly.
        - set_hover_color(self, hover_color): Updates the button's hover color.
        - set_text_color(self, text_color): Updates the button's text color.
        - set_text_color_hover(self, text_color_hover): Updates the button's text hover color.
        - set_font(self, font): Updates the button's font and recalculates text rendering.
    """

    def __init__(self, x, y, size_x, size_y, color, hover_color, text, font, text_color, text_color_hover, action=None):
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_color_hover = text_color_hover
        self.action = action
        self.hover = False
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        if self.hover:
            pygame.draw.rect(screen, self.hover_color, self.rect)
            screen.blit(self.text_surface, self.text_rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.text_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.hover = True
            else:
                self.hover = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()

    def set_action(self, action):
        self.action = action

    def get_rect(self):
        return self.rect

    def set_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        print("Done")

    def set_hover_color(self, hover_color):
        self.hover_color = hover_color
        print("Done")

    def set_text_color(self, text_color):
        self.text_color = text_color
        self.text_surface = self.font.render(text_color, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        print("Done")

    def set_text_color_hover(self, text_color_hover):
        self.text_color_hover = text_color_hover
        self.text_surface = self.font.render(text_color_hover, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        print("Done")

    def set_font(self, font):
        self.font = font
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        print("Done")

class ImageButton:
    def __init__(self, x, y, file, size_x, size_y,name, action = None):
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.image = pygame.image.load(file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.action = action
        self.actif = True
        self.is_clicked = False
        self.name = name

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.actif and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                    return True
        return False

    def activate(self):
        self.actif = True

    def deactivate(self):
        self.actif = False

class Thread:
    """
    Thread class representing a level-based thread generation system, with adjustable difficulty and graphical representation capabilities.

    Attributes:
        x (int): Horizontal position for thread rendering.
        y (int): Vertical position for thread rendering.
        size (int): Font size used for rendering the threads.
        font (Font): Font object used for text rendering.
        couleur (tuple): RGB tuple representing the color of rendered text.
        thread (list): A list of generated process dictionaries.
        min_thread (int): Minimum number of threads in a level.
        max_thread (int): Maximum number of threads in a level.
        min_arrival_time (int): Minimum arrival time for process generation.
        max_arrival_time (int): Maximum arrival time for process generation.
        min_burst_time (int): Minimum burst time for process generation.
        max_burst_time (int): Maximum burst time for process generation.
        min_period (int): Minimum period for process generation.
        max_period (int): Maximum period for process generation.
        difficulty (int): Current difficulty level of the thread generation system.

    Methods:
        create_thread():
            Generates a list of processes with random properties based on defined constraints.

        adjust_to_difficulty():
            Adjusts thread generation constraints such as number and arrival time based on the current difficulty level.

        set_difficulty(difficulty):
            Sets the difficulty level for thread generation.

        get_difficulty():
            Returns the current difficulty level.

        reset():
            Resets the generated thread list to an empty state.

        create_level():
            Adjusts constraints based on difficulty and generates a new list of threads. Returns the updated thread list.

        draw(screen):
            Renders the list of threads on the specified screen surface, with each thread displayed as a formatted text with specified font and color.
    """

    def __init__(self, x, y, size, font, couleur=(255, 255, 255)):
        self.x = x
        self.y = y
        self.size = size
        self.font = font
        self.couleur = couleur
        self.thread = []
        self.min_thread = 3
        self.max_thread = 20
        self.min_arrival_time = 0
        self.max_arrival_time = 30
        self.min_burst_time = 1
        self.max_burst_time = 8
        self.min_period = 0
        self.max_period = 15
        self.difficulty = 1

    def create_thread(self):
        number_of_process = rd.randint(self.min_thread, self.max_thread)
        for i in range(number_of_process):
            burst_time = rd.randint(self.min_burst_time, self.max_burst_time)
            process = dict(name="L" + str(i),
                           arrival_time=rd.randint(self.min_arrival_time, self.max_arrival_time),
                           burst_time=burst_time,
                           period=rd.randint(self.min_period, self.max_period),
                           deadline=2 * burst_time)
            self.thread.append(process)

    def create_custom_thread(self,data):
        self.thread = data

    def adjust_to_difficulty(self):
        if self.difficulty == 1:
            self.min_thread = 3
            self.max_thread = 5
            self.max_arrival_time = 5
            self.max_period = 0
        elif self.difficulty == 2:
            self.min_thread = 5
            self.max_thread = 10
            self.max_arrival_time = 10
            self.max_period = 0
        elif self.difficulty == 3:
            self.min_thread = 10
            self.max_thread = 15
            self.max_arrival_time = 20
            self.max_period = 5
        elif self.difficulty == 4:
            self.min_thread = 15
            self.max_thread = 20
            self.max_arrival_time = 30
            self.max_period = 15

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.adjust_to_difficulty()

    def get_difficulty(self):
        return self.difficulty

    def reset(self):
        self.thread = []

    def create_level(self):
        self.adjust_to_difficulty()
        self.create_thread()
        return self.thread

    def get_thread(self):
        thread_dict = self.thread
        thread_list = []
        for i in thread_dict:
            thread_list.append(Process(i['name'], i['arrival_time'], i['burst_time'], i['period'], i['deadline']))
        return thread_list

    def draw(self, screen):
        header_color = (68, 114, 196, 255)
        row_color = (207, 213, 234, 255)
        # Dessiner l'en-tête du tableau
        header_labels = ["Name", "Arrival time", "Burst time", "Period", "Deadline"]
        x_offset = self.x
        padding = 10
        column_widths = [50, 80, 80, 50, 80]
        header_height = self.size + 10

        # Dessiner le rectangle de l'en-tête
        pygame.draw.rect(screen, header_color,
                         (self.x, self.y, sum(column_widths) + padding * (len(header_labels) - 1), header_height))

        # Afficher le texte de l'en-tête
        header_text_color = (0, 0, 0)  # Couleur du texte de l'en-tête
        for i, label in enumerate(header_labels):
            text_surface = self.font.render(label, True, header_text_color)
            text_rect = text_surface.get_rect(
                topleft=(x_offset + padding // 2, self.y + (header_height - text_surface.get_height()) // 2))
            screen.blit(text_surface, text_rect)
            x_offset += column_widths[i] + padding

        # Dessiner les données des processus
        y_offset = self.y + header_height + 5
        for i, process in enumerate(self.thread):
            x_offset = self.x
            data = [process['name'], str(process['arrival_time']), str(process['burst_time']), str(process['period']),
                    str(process['deadline'])]

            # Dessiner le fond de la ligne
            row_rect = pygame.Rect(self.x, y_offset - 2, sum(column_widths) + padding * (len(header_labels) - 1),
                                   self.size + 4)
            pygame.draw.rect(screen, row_color, row_rect)

            for j, value in enumerate(data):
                text_surface = self.font.render(value, True, self.couleur)
                text_rect = text_surface.get_rect(
                    topleft=(x_offset + padding // 2, y_offset + (self.size - text_surface.get_height()) // 2))
                screen.blit(text_surface, text_rect)
                x_offset += column_widths[j] + padding
            y_offset += self.size + 5

class Image:
    def __init__(self, filephath, x, y, size_x, size_y, alpha=None):
        self.filepath = filephath
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.alpha = alpha
        self.image = self._load_image()
        self.rect = self.image.get_rect(topleft=(x, y))

    def _load_image(self):
        try:
            if self.alpha:
                image = pygame.image.load(self.filepath).convert_alpha()
            else:
                image = pygame.image.load(self.filepath).convert()
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image : {self.filepath}")
            print(f"Erreur Pygame : {e}")
            # Retourne une surface noire de 1x1 pour éviter les erreurs.
            return pygame.Surface((1, 1))

        if self.size_x is not None and self.size_y is not None:
            try:
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
            except TypeError:
                print(
                    f"Erreur : Les arguments 'size_x' et 'size_y' doivent être des entiers. Image : {self.filepath}")
                # Retourne l'image originale
                return image
            except ValueError:
                print(
                    f"Erreur : Les arguments 'size_x' et 'size_y' doivent être positifs. Image: {self.filepath}")
                return image
        return image

    def draw(self, surface, position=None):  # position est maintenant optionnel
        if position is None:
            self.rect.center = (self.x, self.y)  # Utilise la position de l'objet
        else:
            self.rect.center = position  # Utilise la position donnée
        surface.blit(self.image, self.rect)

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def get_size(self):
        return self.image.get_size()

    def get_rect(self):
        """
        Retourne le rectangle (pygame.Rect) de l'image.  Utile pour la collision
        et le positionnement.
        """
        return self.rect

    def copy(self):
        """
        Retourne une copie de l'objet PygameImage.
        """
        new_image = Image(self.filepath, self.x, self.y, self.size_x, self.size_y, self.alpha)
        new_image.rect = self.rect.copy()
        return new_image

    def fill(self, color):
        """
        Remplit l'image avec une couleur spécifiée.
        """
        self.image.fill(color)

    def rotate(self, angle):
        """
        Rotate the image by the specified angle in degrees.
        """
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep center.

    def scale_image(self, scale):
        """
        Scales the image
        """
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_image(self):
        """
        Returns the pygame image
        """
        return self.image

class outList:
    def __init__(self, list_data, time_interval, performances, x, y, size, color=(255, 255, 255)):
        self.dict = {}
        self.list = list_data
        self.time = time_interval
        self.performances = performances
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.ordered_list = []
        self.font = pygame.font.Font(None, self.size)  # Initialize the font
        self.current_time = 0
        self.start_display_time = time.time()
        self.displayed_index = 0

    def transform_list(self):
        for item in self.list:
            if len(item) >= 3:
                label = item[0]
                start = item[1]
                end = item[2]
                for _ in range(end - start):
                    self.ordered_list.append(label)
        print(self.ordered_list)

    def convert_list(self):
        dictionnaire_sortie = {}
        for sous_liste in self.list:
            if sous_liste:
                cle = sous_liste[0]
                valeurs = [valeur for valeur in sous_liste[1:] if valeur != -10]
                if cle not in dictionnaire_sortie:
                    dictionnaire_sortie[cle] = []
                dictionnaire_sortie[cle].extend(valeurs)
        self.dict = {k: v for k, v in dictionnaire_sortie.items() if v}

    def draw_order(self, screen):
        background_color = (207, 213, 234, 255)
        x_offset = 0
        current_display_time = time.time()
        elapsed_time = (current_display_time - self.start_display_time) * 1000  # Convert to milliseconds

        items_to_display = int(elapsed_time // self.time)

        for i in range(min(items_to_display, len(self.ordered_list))):
            item = self.ordered_list[i]
            text_surface = self.font.render(str(item), True, self.color, background_color)
            screen.blit(text_surface, (self.x + x_offset, self.y))
            x_offset += self.font.get_linesize()

    def draw_dict(self, screen):
        background_color = (207, 213, 234, 255)
        x_offset = 0

        # Calculer le temps écoulé depuis le début de l'affichage
        current_display_time = time.time()
        elapsed_time = int((current_display_time - self.start_display_time) * 1000 / self.time)

        for key, times in self.dict.items():
            if len(times) >= 2:
                start_time = times[0]
                end_time = times[1]

                # Utiliser le temps écoulé pour déterminer quoi afficher
                if start_time <= elapsed_time <= end_time:
                    text_surface = self.font.render(f"{key}", True, self.color, background_color)
                    screen.blit(text_surface, (self.x + x_offset, self.y))
                    x_offset += self.font.get_linesize()

        # Si c'est la première fois qu'on appelle draw_dict, initialiser le temps de départ
        if not hasattr(self, 'start_display_time'):
            self.start_display_time = time.time()

class Rectangle:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Text:
    def __init__(self, x, y, text, font, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.x, self.y))

class TableauAffichage:
    def __init__(self, screen, x, y, headers, data, header_color=(68, 114, 196, 255), row_color=(207, 213, 234, 255)):
        """
        Initialise la classe TableauAffichage.

        Args:
            screen: La surface Pygame sur laquelle dessiner le tableau.
            x: La position x du coin supérieur gauche du tableau.
            y: La position y du coin supérieur gauche du tableau.
            headers: Une liste de chaînes de caractères représentant les titres des colonnes.
            data: Une liste de dictionnaires, où chaque dictionnaire représente une ligne de données
                  et les clés correspondent aux titres des colonnes.
            header_color: La couleur RVBA de l'arrière-plan des en-têtes.
            row_color: La couleur RVBA de l'arrière-plan des lignes de données.
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.headers = headers
        self.data = data
        self.header_color = header_color
        self.row_color = row_color
        self.font = pygame.font.Font(None, 24)  # Vous pouvez choisir une autre police et taille

        self.cell_padding = 5
        self.column_widths = self._calculate_column_widths()
        self.row_height = self.font.get_linesize() + 2 * self.cell_padding

    def _calculate_column_widths(self):
        """
        Calcule la largeur de chaque colonne en fonction du contenu des en-têtes et des données.
        """
        column_widths = [self.font.size(header)[0] + 2 * self.cell_padding for header in self.headers]
        for row in self.data:
            for i, header in enumerate(self.headers):
                cell_width = self.font.size(str(row.get(header, "")))[0] + 2 * self.cell_padding
                column_widths[i] = max(column_widths[i], cell_width)
        return column_widths

    def draw(self):
        """
        Dessine le tableau sur l'écran.
        """
        current_x = self.x
        current_y = self.y

        # Dessiner les en-têtes
        for i, header in enumerate(self.headers):
            header_rect = pygame.Rect(current_x, current_y, self.column_widths[i], self.row_height)
            pygame.draw.rect(self.screen, self.header_color, header_rect)
            text_surface = self.font.render(header, True, (0, 0, 0))  # Couleur du texte noir
            text_rect = text_surface.get_rect(center=header_rect.center)
            self.screen.blit(text_surface, text_rect)
            current_x += self.column_widths[i]

        current_y += self.row_height
        # Dessiner les données
        for row_data in self.data:
            current_x = self.x
            for i, header in enumerate(self.headers):
                cell_rect = pygame.Rect(current_x, current_y, self.column_widths[i], self.row_height)
                pygame.draw.rect(self.screen, self.row_color, cell_rect)
                cell_value = str(row_data.get(header, ""))
                text_surface = self.font.render(cell_value, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=cell_rect.center)
                self.screen.blit(text_surface, text_rect)
                current_x += self.column_widths[i]
            current_y += self.row_height

class ProcessCreator:
    """
    Une classe qui gère la création et l'affichage de processus personnalisés dans une fenêtre Pygame.
    """
    def __init__(self):
        """
        Initialise Pygame, définit les dimensions de la fenêtre, les couleurs, les polices,
        la taille du tableau, les en-têtes de colonne, les rectangles des zones de saisie et des boutons,
        et les variables pour stocker les données et l'état de l'entrée.
        """
        pygame.init()
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Create custom process")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (200, 200, 200)
        self.green = (0, 255, 0)

        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 30)

        self.cell_width = 120
        self.cell_height = 30
        self.table_x = 50
        self.table_y = 50
        self.table_width = self.cell_width * 5
        self.table_height = self.cell_height * 6

        self.column_headers = ["Name", "Arrival Time", "Burst Time", "Period", "Deadline"]
        self.process_data = []

        self.input_rects = [
            pygame.Rect(50, 400, 100, 30),  # Name
            pygame.Rect(160, 400, 100, 30),  # Arrival Time
            pygame.Rect(270, 400, 100, 30),  # Burst Time
            pygame.Rect(380, 400, 100, 30),  # Period
            pygame.Rect(490, 400, 100, 30),  # Deadline
        ]
        self.button_rect = pygame.Rect(600, 400, 100, 30)
        self.validate_button_rect = pygame.Rect(600, 440, 100, 30)

        self.input_text = ["", "", "", "", ""]
        self.active_input = -1

    def draw_table(self):
        """
        Dessine le tableau, y compris les en-têtes et les données.
        """
        pygame.draw.rect(self.screen, self.black, (self.table_x, self.table_y, self.table_width, self.table_height), 2)

        for i, header in enumerate(self.column_headers):
            text = self.font.render(header, True, self.black)
            text_rect = text.get_rect(center=(self.table_x + i * self.cell_width + self.cell_width // 2, self.table_y + self.cell_height // 2))
            self.screen.blit(text, text_rect)
            pygame.draw.line(self.screen, self.black, (self.table_x + i * self.cell_width, self.table_y), (self.table_x + i * self.cell_width, self.table_y + self.table_height), 1)
        pygame.draw.line(self.screen, self.black, (self.table_x + self.table_width, self.table_y), (self.table_x + self.table_width, self.table_y + self.table_height), 1)
        pygame.draw.line(self.screen, self.black, (self.table_x, self.table_y + self.cell_height), (self.table_x + self.table_width, self.table_y + self.cell_height), 1)

        # Dessine les données des processus
        for i, row in enumerate(self.process_data):
            for j, cell_data in enumerate(row.values()):
                text = self.font.render(str(cell_data), True, self.black)
                text_rect = text.get_rect(center=(self.table_x + j * self.cell_width + self.cell_width // 2, self.table_y + (i + 1) * self.cell_height + self.cell_height // 2))
                self.screen.blit(text, text_rect)

    def draw_input_boxes(self):
        """
        Dessine les zones de saisie de texte.
        """
        for i, rect in enumerate(self.input_rects):
            if self.active_input == i:
                pygame.draw.rect(self.screen, self.green, rect, 2)
            else:
                pygame.draw.rect(self.screen, self.black, rect, 2)
            text = self.font.render(self.input_text[i], True, self.black)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_buttons(self):
        """
        Dessine les boutons.
        """
        pygame.draw.rect(self.screen, self.gray, self.button_rect)
        text = self.font.render("Add Process", True, self.black)
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, self.gray, self.validate_button_rect)
        validate_text = self.font.render("Validate", True, self.black)
        validate_text_rect = validate_text.get_rect(center=self.validate_button_rect.center)
        self.screen.blit(validate_text, validate_text_rect)

    def add_process(self):
        """
        Ajoute les données du processus à la liste.
        """
        try:
            name = self.input_text[0]
            arrival_time = int(self.input_text[1])
            burst_time = int(self.input_text[2])
            period = int(self.input_text[3])
            deadline = int(self.input_text[4])
            # Stocke les données du processus sous forme de dictionnaire
            self.process_data.append({
                "name": name,
                "arrival_time": arrival_time,
                "burst_time": burst_time,
                "period": period,
                "deadline": deadline
            })
            for i in range(5):
                self.input_text[i] = ""
        except ValueError:
            print("Veuillez entrer des valeurs numériques pour Arrival Time, Burst Time, Period et Deadline.")

    def validate_processes(self):
        """
        Valide les processus et affiche les données.
        """
        print("Processus validés :")
        for row in self.process_data:
            print(f"Name: {row['name']}, Arrival Time: {row['arrival_time']}, Burst Time: {row['burst_time']}, Period: {row['period']}, Deadline: {row['deadline']}")

    def run(self):
        """
        Exécute la boucle principale du jeu.
        """
        running = True
        while running:
            self.screen.fill(self.white)
            self.draw_table()
            self.draw_input_boxes()
            self.draw_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(self.input_rects):
                        if rect.collidepoint(event.pos):
                            self.active_input = i
                            break
                    else:
                        self.active_input = -1
                    if self.button_rect.collidepoint(event.pos):
                        self.add_process()
                    elif self.validate_button_rect.collidepoint(event.pos):
                        self.validate_processes()
                        wd.process_windows_with_custom(self.process_data)
                elif event.type == pygame.KEYDOWN:
                    if self.active_input != -1:
                        if event.key == pygame.K_RETURN:
                            self.active_input = -1
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text[self.active_input] = self.input_text[self.active_input][:-1]
                        else:
                            self.input_text[self.active_input] += event.unicode
            pygame.display.flip()
        pygame.quit()

class ProcessClass:
    def __init__(self):
        self.rr = None
        pygame.init()
        pygame.font.init()
        self.custom = False
        self.difficulty = 1
        self.data = None
        self.width, self.height = (1000, 400)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("Arial", 20)
        self.bouton_selectionne = None
        self.activated_boutons = []
        self.launch = False
        self.lr = []
        self.lrq = []
        self.tableau = None

    def initialisation(self):
        print(self.custom)
        if self.custom == False :
            print("Not custom")
            t1 = Thread(0, 0, 20, self.font, (0, 0, 0))
            t1.set_difficulty(self.difficulty)
            t2 = t1.create_level()
            r1 = Rectangle(0, self.screen.get_height() - self.screen.get_height() / 1.8 + 20, 300, 10, (68, 114, 196, 255))
            r2 = Rectangle(self.screen.get_width() - 215, 0, 215, 320, (200, 200, 200))
            cpu = Image("element/cpu.png", self.screen.get_width() / 2, self.screen.get_height() / 2, 100, 100)
            te1 = Text(self.screen.get_width() - 180, 320, "Scheduling algorithm", self.font, (0, 0, 0))
            rm = ImageButton(self.screen.get_width() - 105, 5, "element/RM.png", 100, 100,"RM")
            rr = ImageButton(self.screen.get_width() - 210, 5, "element/round-robin.png", 100, 100,"RR")
            edf = ImageButton(self.screen.get_width() - 105, 110, "element/EDF.png", 100, 100, "EDF")
            fcfs = ImageButton(self.screen.get_width() - 210, 110, "element/FCFS.png", 100, 100, "FCFS")
            sjn = ImageButton(self.screen.get_width() - 155, 215, "element/SJN.png", 100, 100, "SJN")
            rm.action = lambda : self.selectionner_bouton(rm)
            rr.action = lambda : self.selectionner_bouton(rr)
            edf.action = lambda : self.selectionner_bouton(edf)
            fcfs.action = lambda : self.selectionner_bouton(fcfs)
            sjn.action = lambda : self.selectionner_bouton(sjn)
            result, time_t, performances, readyList = pro.fcfs_scheduling(t1.get_thread())
            L1 = outList(result, 500, performances, 0, self.screen.get_height() - self.screen.get_height() / 5, 30, (0, 0, 0))
            L2 = outList(readyList, 500, performances, 100, self.screen.get_height() - self.screen.get_height() / 1.8, 30, (0, 0, 0))
            L1.transform_list()
            L2.convert_list()
            B1 = Button(self.screen.get_width() - 105, self.screen.get_height() - 55, 100, 50, (68, 114, 196, 255), (207, 213, 234, 255),
                        "Launch", self.font, (0, 0, 0), (255, 255, 255), lambda: self.launch_process())
            B2 = Button(self.screen.get_width() - 210, self.screen.get_height() - 55, 100, 50, (68, 114, 196, 255), (207, 213, 234, 255),
                        "Back", self.font, (0, 0, 0), (255, 255, 255), lambda:wd.main_window())
            self.t1, self.t2, self.r1, self.r2, self.cpu, self.te1, self.rm, self.rr, self.edf, self.fcfs, self.sjn, self.L1, self.L2, self.B1, self.B2 = t1, t2, r1, r2, cpu, te1, rm, rr, edf, fcfs, sjn, L1, L2, B1, B2
            self.boutons = [self.rm, self.rr, self.edf, self.fcfs, self.sjn]
        elif self.custom == True:
            print("Custom")
            t1 = Thread(0, 0, 20, self.font, (0, 0, 0))
            t1.create_custom_thread(self.data)
            t2 = t1
            r1 = Rectangle(0, self.screen.get_height() - self.screen.get_height() / 1.8 + 20, 300, 10,
                           (68, 114, 196, 255))
            r2 = Rectangle(self.screen.get_width() - 215, 0, 215, 320, (200, 200, 200))
            cpu = Image("element/cpu.png", self.screen.get_width() / 2, self.screen.get_height() / 2, 100, 100)
            te1 = Text(self.screen.get_width() - 180, 320, "Scheduling algorithm", self.font, (0, 0, 0))
            rm = ImageButton(self.screen.get_width() - 105, 5, "element/RM.png", 100, 100, "RM")
            rr = ImageButton(self.screen.get_width() - 210, 5, "element/round-robin.png", 100, 100, "RR")
            edf = ImageButton(self.screen.get_width() - 105, 110, "element/EDF.png", 100, 100, "EDF")
            fcfs = ImageButton(self.screen.get_width() - 210, 110, "element/FCFS.png", 100, 100, "FCFS")
            sjn = ImageButton(self.screen.get_width() - 155, 215, "element/SJN.png", 100, 100, "SJN")
            rm.action = lambda: self.selectionner_bouton(rm)
            rr.action = lambda: self.selectionner_bouton(rr)
            edf.action = lambda: self.selectionner_bouton(edf)
            fcfs.action = lambda: self.selectionner_bouton(fcfs)
            sjn.action = lambda: self.selectionner_bouton(sjn)
            result, time_t, performances, readyList = pro.fcfs_scheduling(t1.get_thread())
            L1 = outList(result, 500, performances, 0, self.screen.get_height() - self.screen.get_height() / 5, 30,
                         (0, 0, 0))
            L2 = outList(readyList, 500, performances, 100, self.screen.get_height() - self.screen.get_height() / 1.8,
                         30, (0, 0, 0))
            L1.transform_list()
            L2.convert_list()
            B1 = Button(self.screen.get_width() - 105, self.screen.get_height() - 55, 100, 50, (68, 114, 196, 255),
                        (207, 213, 234, 255),
                        "Launch", self.font, (0, 0, 0), (255, 255, 255), lambda: self.launch_process())
            B2 = Button(self.screen.get_width() - 210, self.screen.get_height() - 55, 100, 50, (68, 114, 196, 255),
                        (207, 213, 234, 255),
                        "Back", self.font, (0, 0, 0), (255, 255, 255), lambda: wd.main_window())
            self.t1, self.t2, self.r1, self.r2, self.cpu, self.te1, self.rm, self.rr, self.edf, self.fcfs, self.sjn, self.L1, self.L2, self.B1, self.B2 = t1, t2, r1, r2, cpu, te1, rm, rr, edf, fcfs, sjn, L1, L2, B1, B2
            self.boutons = [self.rm, self.rr, self.edf, self.fcfs, self.sjn]

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def set_custom(self, custom,data):
        self.custom = custom
        self.data = data

    def draw_algo(self):
        self.r2.draw(self.screen)
        self.rm.draw(self.screen)
        self.rr.draw(self.screen)
        self.edf.draw(self.screen)
        self.fcfs.draw(self.screen)
        self.sjn.draw(self.screen)
        self.te1.draw(self.screen)

    def handle(self, event):
        self.B1.handle_event(event)
        self.B2.handle_event(event)
        self.rm.handle_event(event)
        self.rr.handle_event(event)
        self.edf.handle_event(event)
        self.fcfs.handle_event(event)
        self.sjn.handle_event(event)

    def gerer_blocage(self):
        if self.bouton_selectionne:
            self.activated_boutons.append(self.bouton_selectionne.name)
            for bouton in self.boutons:
                if bouton != self.bouton_selectionne:
                    if self.bouton_selectionne.name == "RM":
                        if bouton.name in ["FCFS", "SJN"]:
                            bouton.deactivate()
                        else:
                            bouton.activate()
                    elif self.bouton_selectionne.name == "RR":
                        bouton.activate() # No specific blocking based on the provided info
                    elif self.bouton_selectionne.name == "EDF":
                        if bouton.name in ["FCFS", "SJN"]:
                            bouton.deactivate()
                        else:
                            bouton.activate()
                    elif self.bouton_selectionne.name == "FCFS":
                        if bouton.name in ["RM", "EDF"]:
                            bouton.deactivate()
                        else:
                            bouton.activate()
                    elif self.bouton_selectionne.name == "SJN":
                        if bouton.name in ["RM", "EDF"]:
                            bouton.deactivate()
                        else:
                            bouton.activate()
        else:
            for bouton in self.boutons:
                bouton.activate()

    def selectionner_bouton(self, bouton):
        self.bouton_selectionne = bouton
        self.gerer_blocage()
        print(f"Bouton sélectionné : {self.bouton_selectionne.name}")

    def launch_process(self):
        self.launch = True
        results, data = [], []
        for algo in self.activated_boutons:
            thread_list = self.t1.get_thread()
            if algo == "RM":
                result, time_interval, performances, ready_list = pro.rm_scheduling(thread_list)
            elif algo == "RR":
                result, time_interval, performances, ready_list = pro.rr_scheduling(thread_list)
            elif algo == "EDF":
                result, time_interval, performances, ready_list = pro.edf_scheduling(thread_list)
            elif algo == "FCFS":
                result, time_interval, performances, ready_list = pro.fcfs_scheduling(thread_list)
            elif algo == "SJN":
                result, time_interval, performances, ready_list = pro.sjn_scheduling(thread_list)

            results.append({
                'algorithm': algo,
                'result': result,
                'time_interval': time_interval,
                'performances': performances,
                'ready_list': ready_list
            })

            data.append({
                'Algorithm': algo,
                'Time interval': time_interval,
                'Performances': performances
            })

            print(data)

        self.tableau = TableauAffichage(self.screen, self.screen.get_width()/2 - 100, 0, ["Algorithm","Time interval","Performances"], data)
        self.activated_boutons = []
        self.bouton_selectionne = None
        for bouton in self.boutons:
            bouton.activate()
        print(results)
        self.lr, self.lrq = self.create_list_process(results)
        print(self.lr)
        print(self.lrq)

    def create_list_process(self, results):
        list_ready_queue, list_result = [], []
        offset = 0
        for result in results:
            l_result = outList(result['result'], 500, result['performances'], 0, self.screen.get_height() - self.screen.get_height() / 5 - offset, 30, (0, 0, 0))
            l_result.transform_list()
            list_result.append(l_result)
            l_rq = outList(result['ready_list'], 500, result['performances'], 100, self.screen.get_height() - self.screen.get_height() / 1.8 - offset, 30, (0, 0, 0))
            l_rq.convert_list()
            list_ready_queue.append(l_rq)
            offset += 20
        return list_result, list_ready_queue

    def display_dict(self, liste):
        for item in liste:
            item.draw_dict(self.screen)

    def display_list(self, liste):
        for item in liste:
            item.draw_order(self.screen)

    def display_with_delay(self):
        if self.lr and self.lrq:
            current_time = 0
            for l_result, l_queue in zip(self.lr, self.lrq):
                l_queue.current_time = current_time
                l_result.draw_order(self.screen)
                l_queue.draw_dict(self.screen)

    def run(self):
        running = True
        self.initialisation()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle(event)

            self.screen.fill((255, 255, 255))
            self.t1.draw(self.screen)
            self.cpu.draw(self.screen)
            self.r1.draw(self.screen)
            self.draw_algo()
            self.B1.draw(self.screen)
            self.B2.draw(self.screen)
            if self.launch:
                self.display_with_delay()
                if self.tableau:
                    self.tableau.draw()
            pygame.display.flip()
        pygame.quit()

class Help:
    """
    Help class represents a graphical object that displays a window with scrollable text to help users understand the application.

    Attributes:
        rect: Rectangle representing the position and size of the help window.
        font: Pygame font object used for rendering text.
        text: List of strings representing the lines of text to be displayed.
        bg_color: Background color of the help window.
        text_color: Color of the text displayed in the help window.
        scroll_y: Current vertical scroll position.
        line_height: Height of each line of text.
        visible_lines: Number of lines that can be displayed within the window's height.
        dragging: Boolean indicating if the scrollbar is being dragged.
        scrollbar_width: Width of the scrollbar.    
    
    Methods:
        handle_event(event):
            Handles mouse events for scrolling and dragging the scrollbar.

        get_scrollbar_height():
            Calculates the height of the scrollbar based on the number of lines and window height.

        get_scrollbar_rect():
            Returns the rectangle representing the scrollbar's position and size.

        draw(screen):
            Draws the help window, text, and scrollbar on the specified Pygame surface.    
    
    """
    def __init__(self, x, y, width, height, font, text, bg_color=(240,240,240), text_color=(0,0,0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = text.split('\n')
        self.bg_color = bg_color
        self.text_color = text_color
        self.scroll_y = 0
        self.line_height = self.font.get_linesize()
        self.visible_lines = height // self.line_height
        self.dragging = False
        self.scrollbar_width = 15

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.get_scrollbar_rect().collidepoint(event.pos):
                self.dragging = True
                self.mouse_y_start = event.pos[1]
                self.scroll_y_start = self.scroll_y
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            delta = event.pos[1] - self.mouse_y_start
            max_scroll = max(0, len(self.text) - self.visible_lines)
            scroll_pixels = self.rect.height - self.get_scrollbar_height()
            if scroll_pixels > 0:
                self.scroll_y = int(self.scroll_y_start + delta * max_scroll / scroll_pixels)
                self.scroll_y = max(0, min(self.scroll_y, max_scroll))
        elif event.type == pygame.MOUSEWHEEL:
            max_scroll = max(0, len(self.text) - self.visible_lines)
            self.scroll_y -= event.y
            self.scroll_y = max(0, min(self.scroll_y, max_scroll))

    def get_scrollbar_height(self):
        total_lines = len(self.text)
        if total_lines <= self.visible_lines:
            return self.rect.height
        return max(20, int(self.rect.height * self.visible_lines / total_lines))

    def get_scrollbar_rect(self):
        bar_height = self.get_scrollbar_height()
        max_scroll = max(0, len(self.text) - self.visible_lines)
        if max_scroll == 0:
            bar_y = self.rect.y
        else:
            bar_y = self.rect.y + int((self.scroll_y / max_scroll) * (self.rect.height - bar_height))
        return pygame.Rect(self.rect.right - self.scrollbar_width, bar_y, self.scrollbar_width, bar_height)

    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        # Draw text
        start = self.scroll_y
        end = min(len(self.text), start + self.visible_lines)
        for i, line in enumerate(self.text[start:end]):
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + i * self.line_height))
        # Draw scrollbar
        pygame.draw.rect(screen, (200,200,200), (self.rect.right - self.scrollbar_width, self.rect.y, self.scrollbar_width, self.rect.height))
        pygame.draw.rect(screen, (120,120,120), self.get_scrollbar_rect())

"""Au cas ou"""
# Exemple d'utilisation :
# help_text = """Bienvenue dans l'interface !
# - Cliquez sur les boutons pour choisir un algorithme.
# - Les processus sont affichés dans le tableau.
# - Lancez la simulation avec 'Launch'.
# - Utilisez la barre pour faire défiler ce texte si besoin.
# """
# help_window = Help(100, 50, 400, 300, pygame.font.SysFont("Arial", 20), help_text)
# Dans la boucle principale :
# help_window.handle_event(event)
# help_window.draw(screen)



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

        self.help_icon = pygame.image.load(os.path.join(self.ASSETS_PATH, "help_icon.png"))
        self.help_icon = pygame.transform.scale(self.help_icon, (28, 28))

        self.settings_icon = pygame.image.load(os.path.join(self.ASSETS_PATH, "settings_icon.png"))
        self.settings_icon = pygame.transform.scale(self.settings_icon, (28, 28))

        self.quit_icon = pygame.image.load(os.path.join(self.ASSETS_PATH, "quit_icon.png"))
        self.quit_icon = pygame.transform.scale(self.quit_icon, (28, 28))

        # State variables
        self.clock = pygame.time.Clock()
        self.running = True
        self.show_difficulty = False
        self.show_help_menu = False
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
            "Static priorities? → RM      ",
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
                                if level == "Beginner":
                                    wd.process_window_with_difficulty(1)
                                    self.show_difficulty = False
                                    self.show_game = True
                                elif level == "Easy":
                                    wd.process_window_with_difficulty(2)
                                    self.show_difficulty = False
                                    self.show_game = True
                                elif level == "Intermediate":
                                    wd.process_window_with_difficulty(3)
                                    self.show_difficulty = False
                                    self.show_game = True
                                elif level == "Difficult":
                                    wd.process_window_with_difficulty(4)
                                    self.show_difficulty = False
                                    self.show_game = True
                                elif level == "Custom":
                                    wd.custom_process_window()
                                    self.show_difficulty = False
                                    self.show_game = True
                    else:
                        if not self.show_game:
                            play_button = self.draw_button("Play", self.play_icon, 370, 320, 260, 60, mouse_pos)
                            algo_button = self.draw_button("Informations about all algorithms", self.settings_icon, 270, 410, 460, 60, mouse_pos)
                            help_button = self.draw_button("Help",self.help_icon,370,500,260,60,mouse_pos)
                            quit_button = self.draw_button("Exit", self.quit_icon, 370, 590, 260, 60, mouse_pos)

                            if play_button.collidepoint(event.pos):
                                self.show_difficulty = True
                            elif algo_button.collidepoint(event.pos):
                                self.show_info_menu = True
                            elif help_button.collidepoint(event.pos):
                                self.show_help_menu = True
                            elif quit_button.collidepoint(event.pos):
                                self.running = False

            if self.show_algo_detail:
                self.draw_algo_detail(self.selected_algorithm)
            elif self.show_info_menu:
                algo_buttons, back_btn = self.draw_info_menu()
            elif self.show_help_menu:
                print("Help menu")
                self.show_help_menu = False
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
                help_button = self.draw_button("Help",self.help_icon,370,500,260,60,mouse_pos)
                quit_button = self.draw_button("Exit", self.quit_icon, 370, 590, 260, 60, mouse_pos)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()