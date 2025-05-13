import pygame
import time
import random as rd
import process as pro
from process import Process

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


def draw_algo():
    r2.draw(screen)
    rm.draw(screen)
    rr.draw(screen)
    edf.draw(screen)
    fcfs.draw(screen)
    sjn.draw(screen)
    te1.draw(screen)


def handle(event):
    B1.handle_event(event)
    B2.handle_event(event)
    rm.handle_event(event)
    rr.handle_event(event)
    edf.handle_event(event)
    fcfs.handle_event(event)
    sjn.handle_event(event)


def initialisation():
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 20)
    t1 = Thread(0, 0, 20, font, (0, 0, 0))
    t1.set_difficulty(1)
    t2 = t1.create_level()
    r1 = Rectangle(0, screen.get_height() - screen.get_height() / 1.8 + 20, 300, 10, (68, 114, 196, 255))
    r2 = Rectangle(screen.get_width() - 215, 0, 215, 320, (200, 200, 200))
    cpu = Image("element/cpu.png", screen.get_width() / 2, screen.get_height() / 2, 100, 100)
    te1 = Text(screen.get_width() - 180, 320, "Scheduling algorithm", font, (0, 0, 0))
    rm = ImageButton(screen.get_width() - 105, 5, "element/RM.png", 100, 100,"RM")
    rr = ImageButton(screen.get_width() - 210, 5, "element/round-robin.png", 100, 100,"RR")
    edf = ImageButton(screen.get_width() - 105, 110, "element/EDF.png", 100, 100, "EDF")
    fcfs = ImageButton(screen.get_width() - 210, 110, "element/FCFS.png", 100, 100, "FCFS")
    sjn = ImageButton(screen.get_width() - 155, 215, "element/SJN.png", 100, 100, "SJN")
    rm.action = lambda : selectionner_bouton(rm)
    rr.action = lambda : selectionner_bouton(rr)
    edf.action = lambda : selectionner_bouton(edf)
    fcfs.action = lambda : selectionner_bouton(fcfs)
    sjn.action = lambda : selectionner_bouton(sjn)
    result, time_t, performances, readyList = pro.fcfs_scheduling(t1.get_thread())
    L1 = outList(result, 500, performances, 0, screen.get_height() - screen.get_height() / 5, 30, (0, 0, 0))
    L2 = outList(readyList, 500, performances, 100, screen.get_height() - screen.get_height() / 1.8, 30, (0, 0, 0))
    L1.transform_list()
    L2.convert_list()
    B1 = Button(screen.get_width() - 105, screen.get_height() - 55, 100, 50, (68, 114, 196, 255), (207, 213, 234, 255),
                "Launch", font, (0, 0, 0), (255, 255, 255), lambda: launch_process())
    B2 = Button(screen.get_width() - 210, screen.get_height() - 55, 100, 50, (68, 114, 196, 255), (207, 213, 234, 255),
                "Back", font, (0, 0, 0), (255, 255, 255), lambda: print("Back"))
    return t1, t2, r1, r2, cpu, te1, rm, rr, edf, fcfs, sjn, L1, L2, B1, B2


bouton_selectionne = None
activated_boutons = []

def gerer_blocage():
    global bouton_selectionne
    global activated_boutons
    if bouton_selectionne:
        activated_boutons.append(bouton_selectionne.name)
        for bouton in boutons:
            if bouton != bouton_selectionne:
                # Logique basée sur l'image que tu as fournie
                if bouton_selectionne.name == "RM":
                    if bouton.name in ["FCFS", "SJN"]:
                        bouton.deactivate()
                    else:
                        bouton.activate()
                elif bouton_selectionne.name == "RR":
                    if bouton.name in []:  # Pas de blocage spécifique d'après l'image
                        bouton.name()
                    else:
                        bouton.activate()
                elif bouton_selectionne.name == "EDF":
                    if bouton.name in ["FCFS", "SJN"]:
                        bouton.deactivate()
                    else:
                        bouton.activate()
                elif bouton_selectionne.name == "FCFS":
                    if bouton.name in ["RM", "EDF"]:
                        bouton.deactivate()
                    else:
                        bouton.activate()
                elif bouton_selectionne.name == "SJN":
                    if bouton.name in ["RM", "EDF"]:
                        bouton.deactivate()
                    else:
                        bouton.activate()
    else:
        # Si aucun bouton n'est sélectionné, réactiver tous les boutons
        for bouton in boutons:
            bouton.activate()


# Fonction appelée lorsqu'un bouton est cliqué
def selectionner_bouton(bouton):
    global bouton_selectionne
    bouton_selectionne = bouton
    gerer_blocage()
    print(f"Bouton sélectionné : {bouton_selectionne.name}")

def launch_process():
    global t1,activated_boutons,lr,lrq,launch,tableau
    results,data = [],[]
    launch = True
    for algo in activated_boutons:
        thread_list = t1.get_thread()  # Obtenir une nouvelle copie des threads
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

        tableau = TableauAffichage(screen, screen.get_width()/2 - 100, 0, ["Algorithm","Time interval","Performances"], data)
    # Réinitialiser la liste des boutons activés
    activated_boutons = []

    # Réinitialiser l'état des boutons
    global bouton_selectionne
    bouton_selectionne = None
    for bouton in boutons:
        bouton.activate()
    print(results)
    lr,lrq = create_list_process(results)
    print(lr)
    print(lrq)

def create_list_process(results):
    list_ready_queue,list_result = [],[]
    offset = 0
    for result in results:
        l_result = outList(result['result'], 500, result['performances'], 0, screen.get_height() - screen.get_height() / 5 - offset, 30, (0, 0, 0))
        l_result.transform_list()
        list_result.append(l_result)
        l_rq = outList(result['ready_list'], 500, result['performances'], 100, screen.get_height() - screen.get_height() / 1.8 -offset, 30, (0, 0, 0))
        l_rq.convert_list()
        list_ready_queue.append(l_rq)
        offset += 20
    return list_result,list_ready_queue

def display_dict(liste):
    for item in liste:
        item.draw_dict(screen)

def display_list(liste):
    for item in liste:
        item.draw_order(screen)


def display_with_delay():
    """
    Fonction pour afficher le contenu des listes lr et lrq avec un délai
    """
    if 'lr' in globals() and 'lrq' in globals():
        current_time = 0
        for l_result, l_queue in zip(lr, lrq):
            # Mettre à jour le temps courant pour l'affichage du dictionnaire
            l_queue.current_time = current_time
            # Afficher les éléments
            l_result.draw_order(screen)
            l_queue.draw_dict(screen)

(width, height) = (1000, 400)
screen = pygame.display.set_mode((width, height))
t1, t2, r1, r2, cpu, te1, rm, rr, edf, fcfs, sjn, L1, L2, B1, B2 = initialisation()
boutons = [rm, rr, edf, fcfs, sjn]
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle(event)

    screen.fill((255, 255, 255))
    t1.draw(screen)
    cpu.draw(screen)
    r1.draw(screen)
    draw_algo()
    B1.draw(screen)
    B2.draw(screen)
    if launch:
        display_with_delay()
        tableau.draw()
    pygame.display.flip()
pygame.quit()
