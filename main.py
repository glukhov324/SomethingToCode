import pygame
import button
from random import randint
from pygame.draw import *

pygame.init()


# functions
def print_text(message, x, y, font_color=(0, 0, 0), font_type='DS_Pixel_Cyr.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


# рисование шарика
def new_ball():
    global crcl
    x = randint(1, 800)
    y = randint(100, 600)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    crcl = circle(screen, color, (x, y), r)
    return x, y, r


# рисование квадратика
def new_square():
    global sq
    x = randint(1, 800)
    y = randint(100, 600)
    side = randint(10, 100)
    color = COLORS[randint(0, 5)]
    sq = pygame.draw.rect(screen, color, ((x, y), (side, side)))
    return x, y, side


# проверка на попадение по шарику
def check_points_ball(x_m, y_m, x_figure, y_figure, feature_figure):
    if (((x_figure - x_m) ** 2 + (y_figure - y_m) ** 2) ** 0.5) <= feature_figure:
        print('You clicked on the ball!')
        return 1
    else:
        print('You missed the ball :c')
        return 0


# проверка на попадение по квадратику
def check_points_square(x_m, y_m, sq):
    if sq.collidepoint(x_m, y_m):
        print('You clicked on the square!')
        return 1
    else:
        print('You missed the square :c')
        return 0


# global game variables
weight = 800
height = 600
COLORS = []
game_stage = 0  # 0-start_menu, 1-game_process, 2-pause, 3-game_over_menu
score = 0
game_paused = False
screen = pygame.display.set_mode((weight, height))
pygame.display.set_caption("Main Menu")
font = pygame.font.SysFont("arialblack", 40)
text_color = (255, 255, 255)

# load button images
start_game_img = pygame.image.load('button_images/start_game_button.jpg').convert_alpha()
pause_img = pygame.image.load('button_images/pause_button.jpg').convert_alpha()
global_quit_img = pygame.image.load('button_images/global_quit_button.jpg')
menu_quit_img = pygame.image.load('button_images/quit_menu_button.jpg')

# create button instances
start_game_button = button.Button(270, 450, start_game_img, 1)
pause_img_button = button.Button(25, 25, pause_img, 1)
global_quit_button = button.Button(140, 430, global_quit_img, 1)
menu_quit_button = button.Button(140, 500, menu_quit_img, 1)
user_text = ''


def show_start_menu():
    global user_text, game_stage
    base_font = pygame.font.Font('DS_Pixel_Cyr.ttf', 32)
    user_text = 'Player'
    input_rect = pygame.Rect(255, 150, 250, 50)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color((226, 226, 224))
    color = color_passive
    active = False
    screen.fill((169, 169, 171))
    print_text("ВВЕДИТЕ ИМЯ ПОЛЬЗОВАТЕЛЯ", 215, 100, font_color=(49, 95, 170), font_size=23)
    show_menu = True
    while show_menu or game_stage == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                show_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text + event.unicode) <= 12:
                        user_text += event.unicode
        if start_game_button.draw(screen):
            game_stage = 1
            show_menu = False
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, ((84, 84, 84)))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.update()


def start_game():
    global COLORS, game_stage, score
    FPS = 0.2
    screen = pygame.display.set_mode((weight, height))
    print_text("SCORE:0", 605, 25, font_color=(250, 250, 250), font_size=50)
    pause_img_button.draw(screen)
    '''RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)'''
    BLACK = (0, 0, 0)
    COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255), (0, 255, 255)]
    clock = pygame.time.Clock()
    finished = False
    # scenario=0 - статичный шарик; scenario=1 - статичный квадрат, scenario=2 - ; scenario=3 - квадрат, двигающийся по диагонали
    scenario = randint(0, 1)
    if scenario == 0:
        x_figure, y_figure, feature_figure = new_ball()
    else:
        x_figure, y_figure, feature_figure = new_square()
    score = 0

    pygame.display.update()
    while not finished:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # координаты щелчка мыши
                x_mouse, y_mouse = event.pos
                # проверка, попал ли пользователь по фигуре
                if scenario == 0:
                    checked = check_points_ball(x_mouse, y_mouse, x_figure, y_figure, feature_figure)
                else:
                    checked = check_points_square(x_mouse, y_mouse, sq)
                if checked == 1:
                    if scenario == 0:
                        score += 100
                    if scenario == 1:
                        score += 120
                    print(score)
                    screen.fill(BLACK)
                    print_text(f"SCORE:{score}", 605, 25, font_color=(250, 250, 250), font_size=50)
                    pause_img_button.draw(screen)
                    scenario = randint(0, 1)
                    '''scenario = randint(0, 1)
                    if scenario == 0:
                        x_figure, y_figure, feature_figure = new_ball()
                    else:
                        x_figure, y_figure, feature_figure = new_square()'''
                else:
                    finished = True
                    print(f'\nGame Over\nTotal score:{score}')
                    print(
                        f'mouse:{x_mouse, y_mouse}; object:{x_figure, y_figure}\n{((x_figure - x_mouse) ** 2 - (y_figure - y_mouse) ** 2) ** 0.5}\n{feature_figure}')
                    game_stage = 3

        screen.fill(BLACK)
        pause_img_button.draw(screen)
        print_text(f"SCORE:{score}", 605, 25, font_color=(250, 250, 250), font_size=50)
        if scenario == 0:
            x_figure, y_figure, feature_figure = new_ball()
        else:
            x_figure, y_figure, feature_figure = new_square()

        pygame.display.update()


def show_game_over():
    global game_stage, score
    screen.fill((169, 169, 171))
    print_text("GAME OVER", 220, 25, font_color=((162, 107, 172)), font_size=70)
    print_text(f"YOUR SCORE:{score}", 295, 110, font_color=((49, 95, 170)), font_size=35)
    print_text("LEADERBOARD:", 220, 170, font_color=((49, 95, 170)), font_size=35)
    # из файла leaderboard.txt будем брать первых троих, пока просто текстом написал
    print_text("1.PLAYER1 SCORE:1000", 220, 225, font_color=((49, 95, 170)), font_size=35)
    print_text("2.PLAYER2 SCORE:950", 220, 280, font_color=((49, 95, 170)), font_size=35)
    print_text("3.PLAYER3 SCORE:900", 220, 335, font_color=((49, 95, 170)), font_size=35)
    game_over = True
    while game_over or game_stage == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = False
        global_quit_button.draw(screen)
        menu_quit_button.draw(screen)
        '''if start_game_button.draw(screen):
            game_stage = 1'''
        pygame.display.update()


run = True
while run:
    if game_stage == 0:
        show_start_menu()
    elif game_stage == 1:
        start_game()
    elif game_stage == 3:
        show_game_over()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
    pygame.display.update()
pygame.quit()
