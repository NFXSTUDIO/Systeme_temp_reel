import pygame
import time as t
import random as rd
import process as pro
from process import Process


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
            pygame.draw.rect(screen, self.text_color_hover, self.text_rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, self.text_color, self.text_rect)
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


class Chronometer:
    """
        A Chronometer class for measuring elapsed time and displaying it on a graphical interface.

        Methods:
            __init__(self, x, y, size, font, couleur=(255, 255, 255)):
                Initializes a Chronometer instance with specified position, size, font, and color.

            start(self):
                Starts the chronometer by recording the current time.

            stop(self):
                Stops the chronometer by recording the current time. Raises an error if the chronometer has not been started.

            time_up(self):
                Calculates the elapsed time since the chronometer was started. Returns the current elapsed time, or if stopped, the total elapsed time. Raises an error if the chronometer has not been started.

            reset(self):
                Resets the chronometer by clearing the start and stop times.

            draw(self, screen):
                Draws the current elapsed time on the specified screen using the provided font and color, starting from the initial position defined during initialization.
    """

    def __init__(self, x, y, size, font, couleur=(255, 255, 255)):
        self._debut = None
        self._fin = None
        self.x = x
        self.y = y
        self.font = font
        self.couleur = couleur
        self.size = size

    def start(self):
        self._debut = t.time()

    def stop(self):
        if self._debut is None:
            raise ValueError("Chronometer has not been started")
        self._fin = t.time()

    def time_up(self):
        if self._debut is None:
            raise ValueError("Chronometer has not been started")
        if self._fin is None:
            return t.time() - self._debut
        return self._fin - self._debut

    def reset(self):
        self._debut = None
        self._fin = None

    def draw(self, screen):
        if self._debut is None:
            text = "0.00"
        else:
            text = f"{self.time_up():.2f}"
        text_surface = self.font.render(text, True, self.couleur)
        text_rect = text_surface.get_rect(topleft=(self.x, self.y))
        screen.blit(text_surface, text_rect)


class Score:
    """
        Class representing a Score system to manage and display scores.

        Methods:
            __init__(x, y, font, couleur=(255, 255, 255)):
                Initializes the score system with position, font, color, and initializes score to 0.

            add_score(score):
                Adds a specified score to the current score.

            subtract_score(score):
                Subtracts a specified score from the current score, ensuring the score does not go below zero.

            set_score(score):
                Updates the current score to a specified value.

            get_score():
                Retrieves the current score value.

            reset():
                Resets the score to zero.

            draw(screen):
                Draws the current score as text onto the specified screen using the given font and color.
    """

    def __init__(self, x, y, font, couleur=(255, 255, 255)):
        self.x = x
        self.y = y
        self.font = font
        self.couleur = couleur
        self.score = 0

    def add_score(self, score):
        self.score += score

    def subtract_score(self, score):
        self.score -= score
        if self.score < 0:
            self.score = 0

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def reset(self):
        self.score = 0

    def draw(self, screen):
        text = f"{self.score:.2f}"
        text_surface = self.font.render(text, True, self.couleur)
        text_rect = text_surface.get_rect(topleft=(self.x, self.y))
        screen.blit(text_surface, text_rect)


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
                           deadline=2*burst_time )
            self.thread.append(process)

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
            thread_list.append(Process(i['name'],i['arrival_time'],i['burst_time'],i['period'],i['deadline']))
        return thread_list

    def draw(self, screen):
        header_color = (68,114,196,255)
        row_color = (207,213,234,255)
        # Dessiner l'en-tête du tableau
        header_labels = ["Name", "Arrival time", "Burst time", "Period","Deadline"]
        x_offset = self.x
        padding = 10
        column_widths = [50, 80, 80, 50,80]
        header_height = self.size + 10

        # Dessiner le rectangle de l'en-tête
        pygame.draw.rect(screen, header_color, (self.x, self.y, sum(column_widths) + padding * (len(header_labels) - 1), header_height))

        # Afficher le texte de l'en-tête
        header_text_color = (0, 0, 0)  # Couleur du texte de l'en-tête
        for i, label in enumerate(header_labels):
            text_surface = self.font.render(label, True, header_text_color)
            text_rect = text_surface.get_rect(topleft=(x_offset + padding // 2, self.y + (header_height - text_surface.get_height()) // 2))
            screen.blit(text_surface, text_rect)
            x_offset += column_widths[i] + padding

        # Dessiner les données des processus
        y_offset = self.y + header_height + 5
        for i, process in enumerate(self.thread):
            x_offset = self.x
            data = [process['name'], str(process['arrival_time']), str(process['burst_time']),str(process['period']),str(process['deadline'])]

            # Dessiner le fond de la ligne
            row_rect = pygame.Rect(self.x, y_offset - 2, sum(column_widths) + padding * (len(header_labels) - 1), self.size + 4)
            pygame.draw.rect(screen, row_color, row_rect)

            for j, value in enumerate(data):
                text_surface = self.font.render(value, True, self.couleur)
                text_rect = text_surface.get_rect(topleft=(x_offset + padding // 2, y_offset + (self.size - text_surface.get_height()) // 2))
                screen.blit(text_surface, text_rect)
                x_offset += column_widths[j] + padding
            y_offset += self.size + 5


class Block:
    """
    Block class represents a graphical object that displays an image and accompanying text.

    Attributes:
        original_image: Original image loaded from the specified file path.
        size: Tuple representing the dimensions (width, height) of the block.
        image: Scaled version of the original image based on the specified size.
        rect: Rectangle representation of the block for positioning and collision purposes.
        text: String text displayed on the block.
        font: Pygame font object used for rendering text.
        text_color: Tuple representing RGB values of the text color.
        combined_image: Image object combining the block's scaled image and rendered text.

    Methods:
        render_text:
            Renders the associated text onto the image at the center of the block.

        update_text:
            Updates the text displayed on the block and re-renders it.

        update_size:
            Updates the block's size, rescales the image, and adjusts its position.

        draw:
            Draws the block's combined image (image and text) onto a Pygame surface.
    """

    def __init__(self, x, y, size, font, text, image_path, text_color=(255, 255, 255)):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.size = size
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.font = font
        self.text_color = text_color
        self.render_text()

    def render_text(self):
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.combined_image = self.image.copy()
        self.combined_image.blit(text_surface, text_rect)

    def update_text(self, text):
        self.text = text
        self.render_text()

    def update_size(self, size):
        self.size = size
        self.image = pygame.transform.scale(self.original_image, size)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.render_text()

    def draw(self, screen):
        screen.blit(self.combined_image, self.rect)

class Image:
    def __init__(self,filephath,x,y,size_x,size_y,alpha=None):
        self.filepath = filephath
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.alpha = alpha
        self.image = self._load_image()
        self.rect = self.image.get_rect(topleft=(x,y))

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
            self.rect.topleft = (self.x, self.y)  # Utilise la position de l'objet
        else:
            self.rect.topleft = position  # Utilise la position donnée
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
    def __init__(self,list,time,performances,x,y,size,color=(255,255,255)):
        self.list = list
        self.time = time
        self.performances = performances
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.ordered_list = []
        self.font = pygame.font.Font(None, self.size)  # Initialise la police
    def transform_list(self):
        for i in self.list:
            for j in range(i[2] - i[1]):
                self.ordered_list.append(i[0])
    def draw(self,screen):
        background_color = (207,213,234,255)
        x_offset = 0
        for item in self.ordered_list:
            text_surface = self.font.render(str(item), True, self.color,background_color)
            screen.blit(text_surface, (self.x + x_offset, self.y))
            x_offset += self.font.get_linesize()  # Déplace le texte vers le bas pour la ligne suivante



pygame.font.init()
font = pygame.font.SysFont("Arial", 20)
(width, height) = (1000, 800)
screen = pygame.display.set_mode((width, height))
t1 = Thread(0, 0, 20, font,(0,0,0))
t1.set_difficulty(1)
t2 = t1.create_level()
t1.draw(screen)
running = True
cpu = Image("element/cpu.png",screen.get_width()/2,screen.get_height()/2,100,100)
print(t1.get_thread())
result,time,performances = pro.sjn_scheduling(t1.get_thread())
print(result)
L1 = outList(result,time,performances,0,screen.get_height()-200,30,(0,0,0))
L1.transform_list()
B1 = Button(screen.get_width()-150,screen.get_height()-100,100,50,(0,0,0),(200,200,200),"Launch",font,(0,0,0),(255,255,255),lambda:print("Launch"))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255,255,255))
    t1.draw(screen)
    cpu.draw(screen)
    L1.draw(screen)
    B1.draw(screen)
    pygame.display.flip()
pygame.quit()
