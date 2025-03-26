import pygame

class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur_normal, couleur_survol, action=None):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur_normal = couleur_normal
        self.couleur_survol = couleur_survol
        self.couleur_actuelle = couleur_normal
        self.action = action
        self.font = pygame.font.Font(None, 30)
        self.texte_surface = self.font.render(self.texte, True, noir)
        self.texte_rect = self.texte_surface.get_rect(center=self.rect.center)

    def dessiner(self, surface):
        pygame.draw.rect(surface, self.couleur_actuelle, self.rect)
        surface.blit(self.texte_surface, self.texte_rect)

    def gerer_evenement(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.couleur_actuelle = self.couleur_survol
            else:
                self.couleur_actuelle = self.couleur_normal
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()

# Fonction à exécuter lorsque le bouton est cliqué
def action_bouton():
    print("Bouton cliqué !")