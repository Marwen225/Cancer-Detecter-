import pygame
import sys
import random
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre du jeu
WIDTH = 800
HEIGHT = 600

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Création de la fenêtre du jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Le voyageur de commerce")

clock = pygame.time.Clock()

# Classe représentant une ville
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), 6)

# Classe représentant un bonus
class Bonus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, GREEN, (self.x, self.y), 6)

# Classe principale du jeu
class Game:
    def __init__(self):
        self.cities = []  # Liste des villes sélectionnées
        self.obstacles = []  # Liste des obstacles
        self.bonuses = []  # Liste des bonus
        self.path = []  # Chemin optimal
        self.score = 0  # Score du joueur
        self.time_limit = 60  # Limite de temps en secondes

    def run(self):
        running = True
        calculating = False
        game_over = False
        timer = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not calculating and not game_over:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        city = City(x, y)
                        self.cities.append(city)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not calculating and not game_over:
                        calculating = True
                        self.calculate_path()

            screen.fill(WHITE)

            if calculating:
                self.draw_path()
            elif not game_over:
                self.draw_cities()
                self.draw_obstacles()
                self.draw_bonuses()
                self.draw_score()

                # Gestion du compte à rebours
                timer += clock.get_time() / 1000  # Conversion du temps en secondes
                time_remaining = self.time_limit - timer
                if time_remaining <= 0:
                    game_over = True

                self.draw_timer(time_remaining)

                # Gestion des collisions avec les obstacles
                for obstacle in self.obstacles:
                    if self.check_collision(obstacle):
                        game_over = True

                # Gestion des collisions avec les bonus
                for bonus in self.bonuses:
                    if not bonus.collected and self.check_collision(bonus):
                        bonus.collected = True
                        self.score += 10

                # Vérification de la victoire
                if len(self.cities) == len(self.path):
                    self.score += math.floor(time_remaining) * 10
                    game_over = True

            else:
                self.draw_game_over()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw_cities(self):
        for city in self.cities:
            city.draw(screen)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)

    def draw_bonuses(self):
        for bonus in self.bonuses:
            bonus.draw(screen)

    def draw_path(self):
        for i in range(len(self.path) - 1):
            city_a = self.path[i]
            city_b = self.path[i + 1]
            pygame.draw.line(screen, BLACK, (city_a.x, city_a.y), (city_b.x, city_b.y), 2)

    def draw_score(self):
        font = pygame.font.Font(None, 30)
        score_text = font.render("Score: " + str(self.score), True, BLACK)
        screen.blit(score_text, (10, 10))

    def draw_timer(self, time_remaining):
        font = pygame.font.Font(None, 30)
        timer_text = font.render("Time: " + str(math.floor(time_remaining)), True, BLACK)
        screen.blit(timer_text, (WIDTH - 120, 10))

    def draw_game_over(self):
        font = pygame.font.Font(None, 50)
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 25))

    def calculate_path(self):
        # TODO: Implémenter l'algorithme de recherche opérationnelle pour trouver le chemin optimal
        # Ici, nous utilisons simplement un ordre aléatoire des villes comme exemple

        self.path = self.cities[:]  # Copie des villes
        random.shuffle(self.path)  # Mélange aléatoire des villes

        # Génération aléatoire des obstacles
        for _ in range(5):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            width = random.randint(20, 100)
            height = random.randint(20, 100)
            obstacle = pygame.Rect(x, y, width, height)
            self.obstacles.append(obstacle)

        # Génération aléatoire des bonus
        for _ in range(3):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            bonus = Bonus(x, y)
            self.bonuses.append(bonus)

    def check_collision(self, rect):
        for i in range(len(self.path) - 1):
            city_a = self.path[i]
            city_b = self.path[i + 1]
            line = pygame.Rect(city_a.x, city_a.y, city_b.x - city_a.x, city_b.y - city_a.y)
            if line.colliderect(rect):
                return True
        return False

if __name__ == "__main__":
    game = Game()
    game.run()
