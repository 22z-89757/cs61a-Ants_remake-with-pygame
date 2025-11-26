import pygame

class GameState:

    food = 100
    game_over = False
    game_win = False
    chosen_ants = None

class Insect(pygame.sprite.Sprite):

    insert_id = 0
    damage = 0

    def __init__(self,health = 0):
        super().__init__()
        self.id = Insect.insert_id
        Insect.insert_id += 1
        self.health = health

class Ants(Insect):

    food_cost = 0

    def __init__(self, health = 1):
        super().__init__(health)

    def place_ants(self):
        GameState.food -= self.food_cost



class Thrower(Ants):

    name = "Thrower"
    food_cost = 3  #property override
    damage = 1

    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("assets/ants/Thrower.gif")
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.rect = self.image.get_rect()
        self.rect.center = position


class Harvester(Ants):

    name = "Harvester"
    food_cost = 2

    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("assets/ants/Harvester.gif")
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.rect = self.image.get_rect()
        self.rect.center = position

    @staticmethod
    def get_food():
        GameState.food += 1


class Bees(Insect):

    name = "Bee"
    speed = pygame.Vector2(-20,0)
    damage = 1

    def __init__(self, health = 3):
        super().__init__(health)


class Lawn(pygame.sprite.Sprite):

    have_ants = None

    def __init__(self,position):
        super().__init__()
        self.image = pygame.image.load("assets/tiles/1.png")
        self.image = pygame.transform.scale(self.image, (170, 170))
        self.rect = self.image.get_rect()
        self.rect.topleft = position