import pygame
import block

pygame.init()

# Définir la taille de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Mon Interface Graphique")

# Définir des couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (255, 0, 0)
vert = (0, 255, 0)
bleu = (0, 0, 255)
sprite_sheet = pygame.image.load('img.png').convert()

# Police de caractères
font = pygame.font.Font(None, 36)

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

# Création d'une instance du bouton
bouton1 = Bouton(100, 100, 150, 50, "Cliquez-moi", vert, (0, 150, 0), action_bouton)
block1 = block.Block(10,10,sprite_sheet,"round-robin")
def afficher_texte(surface, texte, x, y, couleur):
    texte_surface = font.render(texte, True, couleur)
    surface.blit(texte_surface, (x, y))

en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

        # Gérer les événements des boutons
        bouton1.gerer_evenement(event)

    # Remplir l'arrière-plan
    fenetre.fill(blanc)

    # Dessiner les éléments de l'interface
    bouton1.dessiner(fenetre)
    block1.draw(fenetre)
    afficher_texte(fenetre, "Bienvenue dans mon interface !", 50, 50, noir)

    # Mettre à jour l'affichage
    pygame.display.flip()

pygame.quit()