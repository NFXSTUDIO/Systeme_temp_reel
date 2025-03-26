import pygame
import time as t
import random as rd

class Button :
    def __init__(self,x,y,size_x,size_y,color,hover_color, text, font, text_color,text_color_hover,action = None):
        self.rect = pygame.Rect(x,y,size_x,size_y)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.text_color_hover = text_color_hover
        self.action = action
        self.hover = False
        self.text_surface = self.font.render(self.text,True,self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        if self.hover:
            pygame.draw.rect(screen,self.hover_color,self.rect)
            pygame.draw.rect(screen,self.text_color_hover,self.text_rect)
        else:
            pygame.draw.rect(screen,self.color,self.rect)
            pygame.draw.rect(screen,self.text_color,self.text_rect)
        screen.blit(self.text_surface,self.text_rect)

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.hover = True
            else:
                self.hover = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()

    def set_action(self,action):
        self.action = action

    def get_rect(self):
        return self.rect

    def set_text(self,new_text):
        self.text = new_text
        self.text_surface = self.font.render(new_text,True,self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        print("Done")

    def set_hover_color(self,hover_color):
        self.hover_color = hover_color
        print("Done")

    def set_text_color(self,text_color):
        self.text_color = text_color
        self.text_surface = self.font.render(text_color,True,self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        print("Done")

    def set_text_color_hover(self,text_color_hover):
        self.text_color_hover = text_color_hover
        self.text_surface = self.font.render(text_color_hover,True,self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        print("Done")

    def set_font(self,font):
        self.font = font
        self.text_surface = self.font.render(self.text,True,self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        print("Done")


class Chronometer:
    def __init__(self,x,y,size,font,couleur = (255,255,255)):
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

    def draw(self,screen):
        if self._debut is None:
            text = "0.00"
        else:
            text = f"{self.time_up():.2f}"
        text_surface = self.font.render(text,True,self.couleur)
        text_rect = text_surface.get_rect(topleft=(self.x,self.y))
        screen.blit(text_surface,text_rect)

class Score:
    def __init__(self,x,y,font,couleur = (255,255,255)):
        self.x = x
        self.y = y
        self.font = font
        self.couleur = couleur
        self.score = 0

    def add_score(self,score):
        self.score += score

    def subtract_score(self,score):
        self.score -= score
        if self.score < 0:
            self.score = 0

    def set_score(self,score):
        self.score = score

    def get_score(self):
        return self.score

    def reset(self):
        self.score = 0

    def draw(self,screen):
        text = f"{self.score:.2f}"
        text_surface = self.font.render(text,True,self.couleur)
        text_rect = text_surface.get_rect(topleft=(self.x,self.y))
        screen.blit(text_surface,text_rect)

class Thread:
    def __init__(self,x,y,size,font,couleur = (255,255,255)):
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
        self.min_burst_time = 2
        self.max_burst_time = 15
        self.min_period = 0
        self.max_period = 15
        self.difficulty = 1

    def create_thread(self):
        number_of_process = rd.randint(self.min_thread,self.max_thread)
        for i in range(number_of_process):
            process = dict(name = "L" + str(i),arrival_time = rd.randint(self.min_arrival_time,self.max_arrival_time),burst_time = rd.randint(self.min_burst_time,self.max_burst_time),period = rd.randint(self.min_period,self.max_period))
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

    def set_difficulty(self,difficulty):
        self.difficulty = difficulty

    def get_difficulty(self):
        return self.difficulty

    def reset(self):
        self.thread = []

    def create_level(self):
        self.adjust_to_difficulty()
        self.create_thread()
        return self.thread

    def draw(self,screen):
        y_offset = self.y
        for process in self.thread:
            text = f"Name: {process['name']}, Arrival: {process['arrival_time']}, Burst: {process['burst_time']}, Period: {process['period']}"
            text_surface = self.font.render(text,True,self.couleur)
            text_rect = text_surface.get_rect(topleft=(self.x,y_offset))
            screen.blit(text_surface,text_rect)
            y_offset += self.size + 5

class Block:
    def __init__(self,x,y,size,font,text,image_path,text_color=(255,255,255)):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.size = size
        self.image = pygame.transform.scale(self.original_image,size)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.text = text
        self.font = font
        self.text_color = text_color
        self.render_text()

    def render_text(self):
        text_surface = self.font.render(self.text,True,self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.combined_image = self.image.copy()
        self.combined_image.blit(text_surface,text_rect)

    def update_text(self,text):
        self.text = text
        self.render_text()

    def update_size(self,size):
        self.size = size
        self.image = pygame.transform.scale(self.original_image,size)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.render_text()

    def draw(self,screen):
        screen.blit(self.combined_image,self.rect)

