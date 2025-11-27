import pygame


class GameState:

    food = 5
    game_over = False
    game_win = False
    chosen_ants = None

def get_row(position):
    if position[1] < 720:
        if position[1] > 540:
            return 'row2'
        elif position[1] > 360:
            return 'row1'
    elif position[1] > 720:
        if position[1] < 900:
            return 'row3'
        elif position[1] < 1080:
            return 'row4'

# the y_range of each row is (370, 530), (550, 710), (730, 890), (910, 1070)
row_y_dic = {'row1': 450, 'row2': 630, 'row3': 810, 'row4': 990}


class Insect(pygame.sprite.Sprite):

    insert_id = 0

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
        self.plant_time = pygame.time.get_ticks()
        self.row = get_row(position)

    def update(self,current_time):
        if current_time - self.plant_time >= 4000:
            # noinspection PyTypeChecker
            bullet_group.add(Bullet(self.position))
            self.plant_time = current_time

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
        self.row = get_row(position)

    #get food logic
    def update(self,current_time):
        #current_time was get in main game loop
        if current_time - self.plant_time >= 6000:
            GameState.food += 1
            #refresh waiting time
            self.plant_time = current_time
            # noinspection PyTypeChecker
            food_group.add(Food(self.position))

#create Harvester's group
Harvesters = pygame.sprite.Group()


class Bees(Insect):

    name = "Bee"
    speed = 1
    damage = 1

    def __init__(self, row, health = 3):
        super().__init__(health)
        self.image = pygame.image.load("assets/bees/Bee.gif")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.row = row
        self.rect.bottomleft = (1620, row_y_dic[self.row])
        self.born_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x -= self.speed
        if self.health <= 0:
            self.kill()
        if self.rect.right < 0:
            GameState.game_over = True


Bees_group = pygame.sprite.Group()


class Lawn(pygame.sprite.Sprite):

    have_ants = None

    def __init__(self,position):
        super().__init__()
        self.image = pygame.image.load("assets/tiles/1.png")
        self.image = pygame.transform.scale(self.image, (170, 170))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

lawn_sprites = pygame.sprite.Group()

class Food(pygame.sprite.Sprite):

    def __init__(self,position):
        super().__init__()
        self.image = pygame.image.load("assets/food.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
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

def bullet_collide_bees(bullet,bees_group):
    """take two arguments and return the Bee object that got hit"""
    for x in bees_group:
        if bullet.rect.colliderect(x.rect):
            return x
    return None

class Bullet(pygame.sprite.Sprite):

    damage = 1

    def __init__(self,position):
        super().__init__()
        self.image = pygame.image.load("assets/testLeaf.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.bottomleft  = position
        self.speed = 3

    def update(self):
        self.rect.x += self.speed
        s = bullet_collide_bees(self, Bees_group)
        if s:
            s.health -= self.damage
            self.kill()
        if self.rect.left >= 1620:
            self.kill()
        self.rect.x += self.speed

bullet_group = pygame.sprite.Group()