import pygame
from PIL import Image, ImageSequence


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


class Rows:
    """Mixin to provide row-related helpers for insects.

    Use `set_row_from_position(position)` when you have a position,
    or `set_row(row_name)` when you already know the row string.
    """
    def set_row(self, row_name):
        self.row = row_name

    def set_row_from_position(self, position):
        self.row = get_row(position)

def load_frames(image_path, size=None):
    """Load frames from an image file.

    - If Pillow (PIL) is available and the image has multiple frames (e.g. GIF),
      extract each frame and convert to a pygame Surface.
    - Otherwise fall back to `pygame.image.load` and return a single-frame list.

    `size` is an (w,h) tuple to scale frames to; if None, leave original size.
    """
    frames = []
    try:
        pil_img = Image.open(image_path)
    except Exception:
        # fallback to pygame single frame if PIL cannot open
        surf = pygame.image.load(image_path).convert_alpha()
        if size:
            surf = pygame.transform.scale(surf, size)
        return [surf]

    for frame in ImageSequence.Iterator(pil_img):
        frame = frame.convert('RGBA')
        mode = frame.mode
        size_pil = frame.size
        data = frame.tobytes()
        surf = pygame.image.fromstring(data, size_pil, mode).convert_alpha()
        if size:
            surf = pygame.transform.scale(surf, size)
        frames.append(surf)

    if not frames:
        # empty? fall back
        surf = pygame.image.load(image_path).convert_alpha()
        if size:
            surf = pygame.transform.scale(surf, size)
        return [surf]

    return frames


class Insect(Rows, pygame.sprite.Sprite):

    insert_id = 0

    def __init__(self,health = 0):
        super().__init__()
        self.id = Insect.insert_id
        Insect.insert_id += 1
        self.health = health

class Ants(Insect):

    food_cost = 0

    # subclasses should set these two class attributes
    image_path = None
    image_size = (130, 130)

    def __init__(self, position, health=1):
        super().__init__(health)
        # common setup for all Ants: load image, set rect/position, plant time and row
        if not getattr(self, 'image_path', None):
            raise RuntimeError(f"Ant subclass {self.__class__.__name__} must define 'image_path'")
        # load frames (GIF support) and set up animation
        self.frames = load_frames(self.image_path, self.image_size)
        self.frame_index = 0
        self.anim_interval = getattr(self, 'anim_interval', 150)  # ms per frame
        self.last_anim_time = pygame.time.get_ticks()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.position = position
        self.plant_time = pygame.time.get_ticks()
        # use Rows helper to set row consistently
        self.set_row_from_position(position)

    def animate(self, current_time=None):
        """Advance animation based on elapsed time.

        If current_time is given (ms), use it; otherwise use pygame.time.get_ticks().
        """
        if not getattr(self, 'frames', None) or len(self.frames) <= 1:
            return
        now = current_time if current_time is not None else pygame.time.get_ticks()
        if now - self.last_anim_time >= self.anim_interval:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            center = self.rect.center
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.last_anim_time = now

    def place_ants(self):
        GameState.food -= self.food_cost



class Thrower(Ants):

    name = "Thrower"
    food_cost = 3  #property override
    damage = 1

    # specify image info as class attributes so parent can initialize
    image_path = "assets/ants/Thrower.gif"
    image_size = (130, 130)

    def __init__(self, position):
        super().__init__(position)

    def update(self,current_time):
        # animate first
        try:
            self.animate(current_time)
        except Exception:
            pass

        if current_time - self.plant_time >= 4000:
            # only fire if there is at least one Bee in the same row
            if any(getattr(b, 'row', None) == self.row for b in Bees_group):
                # noinspection PyTypeChecker
                bullet_group.add(Bullet(self.position))
            self.plant_time = current_time

#create Thrower's group
Throwers = pygame.sprite.Group()


class Harvester(Ants):

    name = "Harvester"
    food_cost = 2

    image_path = "assets/ants/Harvester.gif"
    image_size = (130, 130)

    def __init__(self, position):
        super().__init__(position)

    #get food logic
    def update(self,current_time):
        # animate first
        try:
            self.animate(current_time)
        except Exception:
            pass

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
        # support animated bee GIFs
        self.image_path = "assets/bees/Bee.gif"
        self.image_size = (150, 150)
        self.frames = load_frames(self.image_path, self.image_size)
        self.frame_index = 0
        self.anim_interval = getattr(self, 'anim_interval', 120)
        self.last_anim_time = pygame.time.get_ticks()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        # set row via Rows mixin and position the bee accordingly
        self.set_row(row)
        self.rect.bottomleft = (1620, row_y_dic[self.row])
        self.born_time = pygame.time.get_ticks()

    def update(self):
        # animate
        try:
            self.animate()
        except Exception:
            pass

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
        self.speed = 6

    def update(self):
        self.rect.x += self.speed
        s = bullet_collide_bees(self, Bees_group)
        if s:
            s.health -= self.damage
            self.kill()
        if self.rect.left >= 1620:
            self.kill()

bullet_group = pygame.sprite.Group()