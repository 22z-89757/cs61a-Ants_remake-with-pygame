from object import *
import pygame

# initialize
pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("Ants-remake by 22z")
clock = pygame.time.Clock()

waiting_to_start = True
game_start = False



## Make a Start Menu ##

start_background = pygame.image.load("assets/splash.png")
start_background = pygame.transform.scale(start_background, (1920, 1080))

font = pygame.font.Font("assets/fond/MountainsOfChristmas/MountainsofChristmas-Bold.ttf", 100)
text_surface = font.render("CLick To Start !!", True, (255, 217, 63))
text_rect = text_surface.get_rect()
text_rect.center = (1300, 800)

while waiting_to_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_to_start = False
        if pygame.mouse.get_pressed()[0]:
            waiting_to_start = False
            game_start = True

    screen.blit(start_background, (0, 0))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(30)



## Run Game ##

pygame.mixer.music.load("assets/backgroundmusic.mp3")
pygame.mixer.music.play(-1)

game_background = pygame.image.load("assets/background.png")
game_background = pygame.transform.scale(game_background, (1920, 1080))

fog = pygame.image.load("assets/fog.jpg")
fog = pygame.transform.scale(fog, (300, 720))
fog_rect = fog.get_rect()
fog_rect.bottomright = (1920, 1080)

#these two ant images here are meant to showcase at the top
Harvester_ants = pygame.image.load("assets/ants/Harvester.gif")
Harvester_ants = pygame.transform.scale(Harvester_ants, (150, 150))
Harvester_ants_rect = Harvester_ants.get_rect()
Harvester_ants_rect.center = (100, 230)

#create Harvester's group
Harvesters = pygame.sprite.Group()

Thrower_ants = pygame.image.load("assets/ants/Thrower.gif")
Thrower_ants = pygame.transform.scale(Thrower_ants, (150, 150))
Thrower_ants_rect = Thrower_ants.get_rect()
Thrower_ants_rect.center = (250, 230)

#create Thrower's group
Throwers = pygame.sprite.Group()

lawn_sprites = pygame.sprite.Group()
lawn_list = []
for i in range(9):
    for j in range(4):
        position = (5 + 180 * i, 365 + 180 * j)
        n = Lawn(position)
        lawn_list.append(n)
        lawn_sprites.add(n)

def draw_border(n):
    """draw the borders of each type of optional ants"""
    pygame.draw.rect(screen, (255, 0, 0), n.inflate(2, 2),2)

while game_start:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_start = False

        mouse_pos = pygame.mouse.get_pos()

        # switch the selected ants
        if not(mouse_pos[0] < 1620 and mouse_pos[1] > 360):
            if pygame.mouse.get_pressed()[0]:
                if Harvester_ants_rect.collidepoint(mouse_pos):
                    GameState.chosen_ants = Harvester
                if Thrower_ants_rect.collidepoint(mouse_pos):
                    GameState.chosen_ants = Thrower

        # generate an ant on lawn by clicking
        elif pygame.mouse.get_pressed()[0]:
            for x in lawn_list:
                if x.rect.collidepoint(mouse_pos) and GameState.chosen_ants == Harvester and  not x.have_ants  :
                    if GameState.chosen_ants.food_cost <= GameState.food:
                        GameState.food -= GameState.chosen_ants.food_cost
                        x.have_ants = Harvester
                        Harvesters.add(Harvester(x.rect.center))
                elif x.rect.collidepoint(mouse_pos) and GameState.chosen_ants == Thrower and  not x.have_ants  :
                    if GameState.chosen_ants.food_cost <= GameState.food:
                        GameState.food -= GameState.chosen_ants.food_cost
                        x.have_ants = Thrower
                        Throwers.add(Thrower(x.rect.center))



    screen.blit(game_background, (0, 0))
    screen.blit(fog, fog_rect)

    lawn_sprites.draw(screen)
    Harvesters.draw(screen)
    Throwers.draw(screen)

    screen.blit(Harvester_ants, Harvester_ants_rect)
    if GameState.chosen_ants == Harvester:
        draw_border(Harvester_ants_rect)

    screen.blit(Thrower_ants, Thrower_ants_rect)
    if GameState.chosen_ants == Thrower:
        draw_border(Thrower_ants_rect)

    pygame.draw.line(screen, (255, 0, 0), (0,360),(1980,360) )

    pygame.display.flip()
    clock.tick(60)


pygame.quit()