import pygame


class GameState:

    food = 5
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
        self.position = position

#create Thrower's group
Throwers = pygame.sprite.Group()


class Harvester(Ants):

    name = "Harvester"
    food_cost = 2

    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("assets/ants/Harvester.gif")
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.plant_time = pygame.time.get_ticks()
        self.position = position

    #get food logic
    def update(self,current_time):
        #current_time was get in main game loop
        if current_time - self.plant_time >= 7000:
            GameState.food += 1
            #refresh waiting time
            self.plant_time = current_time
            # noinspection PyTypeChecker
            food_group.add(Food(self.position))

#create Harvester's group
Harvesters = pygame.sprite.Group()


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

class Food(pygame.sprite.Sprite):

    def __init__(self,position):
        super().__init__()
        self.image = pygame.image.load("assets/food.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        #create a copy image .In order not to alter the original image
        self.copy_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = 2
        self.fade_speed = 5
        #Completely opaque at the beginning
        self.alpha = 255

    def update(self):
        self.rect.y -= self.speed
        self.alpha -= self.fade_speed
        self.copy_image = self.image.copy()
        self.image.set_alpha(self.alpha)
        if self.alpha <= 0:
            self.kill()

food_group = pygame.sprite.Group()