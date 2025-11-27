from object import *
import pygame
import random

# initialize
pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("Ants-remake by 22z")
clock = pygame.time.Clock()

waiting_to_start = True
game_start = False
the_end = False

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

Thrower_ants = pygame.image.load("assets/ants/Thrower.gif")
Thrower_ants = pygame.transform.scale(Thrower_ants, (150, 150))
Thrower_ants_rect = Thrower_ants.get_rect()
Thrower_ants_rect.center = (250, 230)

# showcase GameState.food
font = pygame.font.Font("assets/fond/MountainsOfChristmas/MountainsofChristmas-Bold.ttf", 70)
# text_surface are defined in game loop because it needs to be refreshed
text_rect = text_surface.get_rect()
text_rect.topleft = (50, 50)

lawn_list = []
for i in range(9):
    for j in range(4):
        position = (5 + 180 * i, 365 + 180 * j)
        n = Lawn(position)
        lawn_list.append(n)
        # noinspection PyTypeChecker
        lawn_sprites.add(n)

# state : the y_range of each row is (370, 530), (550, 710), (730, 890), (910, 1070)
row_list = ['row1','row2','row3','row4']

def draw_border(s):
    """draw the borders of each type of optional ants"""
    pygame.draw.rect(screen, (255, 0, 0), s.inflate(2, 2),2)

# To Set the interval for bee generation
wave1_start_time = None

while game_start:

    # Get timestamp
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_start = False

        mouse_pos = pygame.mouse.get_pos()

        if not GameState.game_win and not GameState.game_over:

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

    # wave 1
    if current_time >= 15000:
        if not wave1_start_time:
            wave1_start_time = current_time
        elif current_time - wave1_start_time > 5000:
            n = row_list[random.randint(0,3)]
            Bees_group.add(Bees(n))
            wave1_start_time = current_time

    #    elif GameState.game_win :

        elif GameState.game_over:
            game_start = False
            the_end = True


    screen.blit(game_background, (0, 0))
    screen.blit(fog, fog_rect)
    text_surface = font.render(f"FOOD : {GameState.food}", True, (255, 0, 0))
    screen.blit(text_surface, text_rect)

    pygame.draw.line(screen, (255, 0, 0), (0,360),(1980,360) )

    lawn_sprites.draw(screen)
    Harvesters.draw(screen)
    Harvesters.update(current_time)
    Throwers.draw(screen)
    Throwers.update(current_time)
    Bees_group.draw(screen)
    Bees_group.update()
    food_group.draw(screen)
    food_group.update()
    bullet_group.draw(screen)
    bullet_group.update()

    screen.blit(Harvester_ants, Harvester_ants_rect)
    if GameState.chosen_ants == Harvester:
        draw_border(Harvester_ants_rect)

    screen.blit(Thrower_ants, Thrower_ants_rect)
    if GameState.chosen_ants == Thrower:
        draw_border(Thrower_ants_rect)

    pygame.display.flip()
    clock.tick(60)



# end the game

font = pygame.font.Font("assets/fond/MountainsOfChristmas/MountainsofChristmas-Bold.ttf", 300)
text_surface = font.render("GAME   OVER", False, (255, 0, 0))
text_rect = text_surface.get_rect()
text_rect.center = (960, 540)

while the_end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            the_end = False

    screen.fill((0, 0, 0))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()