import pygame
import button
import time
from random import randint
from pygame.draw import *
import pygame_gui
from pygame_widgets.slider import Slider
import pygame_widgets
from pygame_gui.elements.ui_panel import UIPanel
from pygame_gui.elements.ui_horizontal_slider import UIHorizontalSlider

pygame.init()
pygame.mixer.init()
#pygame.mixer.music.load('67c5c9a1e518177.mp3')

'''pygame.mixer.Channel(2).play(pygame.mixer.Sound('67c5c9a1e518177.mp3'), -1)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.Channel(2).pause()'''


# functions
def print_text(message, x, y, font_color=(0, 0, 0), font_type='DS_Pixel_Cyr.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


# рисование шарика
def new_ball():
    global crcl
    r = randint(20, 100)
    x = randint(1+r, 800-r)
    y = randint(100+r, 600-r)

    color = COLORS[randint(0, 5)]
    crcl = circle(screen, color, (x, y), r)
    return x, y, r


# рисование квадратика
def new_square():
    global sq
    side = randint(20, 100)
    x = randint(1+ side, 800-side)
    y = randint(100+side, 600-side)

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
vol1 = 0.25
vol2 = 0.25
vol3 = 0.25
weight = 800
height = 600
COLORS = []
game_stage = 0  # 0-start_menu, 1-game_process, 2-pause, 3-game_over_menu
score = 0
game_paused = False
screen = pygame.display.set_mode((weight, height))
pygame.display.set_caption("game")
font = pygame.font.SysFont("arialblack", 40)
text_color = (255, 255, 255)
slider1 = Slider(screen, 420, 255, 150, 40, min=0, max=1.0, step=0.25)
slider2 = Slider(screen, 520, 320, 150, 40, min=0, max=1.0, step=0.25)
slider3 = Slider(screen, 450, 385, 150, 40, min=0, max=1.0, step=0.25)


# load button images
start_game_img = pygame.image.load('button_images/start_game_button.jpg').convert_alpha()
pause_img = pygame.image.load('button_images/pause_button.jpg').convert_alpha()
global_quit_img = pygame.image.load('button_images/global_quit_button.jpg')
menu_quit_img = pygame.image.load('button_images/quit_menu_button.jpg')
resume_img = pygame.image.load('button_images/resume.jpg').convert_alpha()
exit_img = pygame.image.load('button_images/quit_menu_button.jpg').convert_alpha()

# create button instances
start_game_button = button.Button(270, 450, start_game_img, 1)
pause_img_button = button.Button(25, 25, pause_img, 1)
global_quit_button = button.Button(140, 430, global_quit_img, 1)
menu_quit_button = button.Button(140, 500, menu_quit_img, 1)
resume_button = button.Button(165, 165, resume_img, 1)
exit_button = button.Button(165, 465, exit_img, 1)

user_text = ''


def show_start_menu():
    global user_text, game_stage

    pygame.mixer.Channel(2).play(pygame.mixer.Sound('67c5c9a1e518177.mp3'), -1)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.Channel(2).pause()

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
            pygame.mixer.Channel(2).unpause()
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, ((84, 84, 84)))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.update()


def start_game():
    global COLORS, game_stage, score, vol1, vol2, vol3, slider1, slder2, slider3
    FPS = 2
    screen = pygame.display.set_mode((weight, height))
    print_text("SCORE:0", 25, 25, font_color=(250, 250, 250), font_size=50)
    print_text("ESC FOR PAUSE", 475, 25, font_color=(250, 250, 250), font_size=50)
    #pause_img_button.draw(screen)
    '''RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)'''
    BLACK = (0, 0, 0)
    COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255), (0, 255, 255)]
    clock = pygame.time.Clock()
    volume = 0.5
    finished = False
    # scenario=0 - статичный шарик; scenario=1 - статичный квадрат, scenario=2 - ; scenario=3 - квадрат, двигающийся по диагонали
    scenario = randint(0, 1)
    if scenario == 0:
        x_figure, y_figure, feature_figure = new_ball()
    else:
        x_figure, y_figure, feature_figure = new_square()
    score = 0
    # звук в игре
    pygame.mixer.Channel(2).unpause()
    pygame.mixer.Channel(2).set_volume(vol3)
    # звук попадания по мишени
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('touch_target.mp3'), -1)
    #pygame.mixer.Channel(1).set_volume(1)
    pygame.mixer.Channel(1).pause()
    pygame.mixer.Channel(1).set_volume(vol2)
    #pygame.mixer.music.Channel(2).load("sounds/bird.mp3")
    #pygame.mixer.music.play(-1)  # -1 бесконечное воспроизведение


    pygame.display.update()
    while not finished:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.Channel(2).pause()
                    pause()


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
                    pygame.mixer.Channel(1).unpause()
                    time.sleep(0.7)
                    pygame.mixer.Channel(1).pause()
                    #pygame.mixer.Channel(1).sleep(2)
                    #pygame.mixer.Channel(1).pause()
                    print(score)
                    screen.fill(BLACK)
                    print_text(f"SCORE:{score}", 25, 25, font_color=(250, 250, 250), font_size=50)
                    print_text("ESC FOR PAUSE", 475, 25, font_color=(250, 250, 250), font_size=50)
                    #pause_img_button.draw(screen)
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
                    pygame.mixer.Channel(2).pause()

        screen.fill(BLACK)
        #pause_img_button.draw(screen)
        print_text("ESC FOR PAUSE", 475, 25, font_color=(250, 250, 250), font_size=50)
        print_text(f"SCORE:{score}", 25, 25, font_color=(250, 250, 250), font_size=50)
        if scenario == 0:
            x_figure, y_figure, feature_figure = new_ball()
        else:
            x_figure, y_figure, feature_figure = new_square()

        pygame.display.update()


def show_game_over():
    global game_stage, score, user_text

    screen.fill((169, 169, 171))

    user_text = user_text.upper()
    if user_text != 'PLAYER':
        scores_of_players = {}
        flag = 0
        save_score = 0
        with open("leaderboard.txt", "r") as f:
            for line in f:
                #print(line.split())
                s1 = line.split()
                scores_of_players[str(s1[0])] = int(s1[1])
                if s1[0] == user_text:
                    flag = 1
                    save_score = int(s1[1])


        if flag == 1:
            if score > save_score:
                scores_of_players[user_text] = score
        else:
            scores_of_players[user_text] = score

        scores_of_players = sorted(scores_of_players.items(), key=lambda x: x[1], reverse=True)
        print(scores_of_players)

        f1 = open('leaderboard.txt', 'w')
        for line in scores_of_players:
            nm, sc = line
            f1.write(f'{nm} {sc}\n')
        f1.close()

    counter = 0
    name_lb = []
    score_lb = []

    with open("leaderboard.txt", "r") as f:
        for line in f:
            s1 = line.split()
            name_lb.append(str(s1[0]))
            score_lb.append(int(s1[1]))
            counter += 1
            if counter == 3:
                break



    print_text("GAME OVER", 220, 25, font_color=((162, 107, 172)), font_size=70)
    print_text(f"YOUR SCORE:{score}", 295, 110, font_color=((49, 95, 170)), font_size=35)
    print_text("LEADERBOARD:", 220, 170, font_color=((49, 95, 170)), font_size=35)

    print_text(f"1.{name_lb[0]} SCORE:{score_lb[0]}", 220, 225, font_color=((49, 95, 170)), font_size=35)
    print_text(f"2.{name_lb[1]} SCORE:{score_lb[1]}", 220, 280, font_color=((49, 95, 170)), font_size=35)
    print_text(f"3.{name_lb[2]} SCORE:{score_lb[2]}", 220, 335, font_color=((49, 95, 170)), font_size=35)
    game_over = True
    while game_over or game_stage == 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = False
        #global_quit_button.draw(screen)
        #menu_quit_button.draw(screen)

        if global_quit_button.draw(screen):
            game_over = False
            pygame.quit()

        if menu_quit_button.draw(screen):
            game_stage = 0
            game_over = False

        pygame.display.update()


def show_pause_menu():

    global game_paused, vol1, vol2, vol3, slider1, slider2, slider3
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    screen.fill(BLACK)
    manager = pygame_gui.UIManager((weight, height))
    # volume_slider = UIHorizontalSlider(relative_rect=pygame.Rect((10, 10), (180, 20)),start_value=volume,
    #                                value_range=(0.0, 1.0),
    #                                manager=manager)

    #pygame_gui.elements.voldsa.enable()
    manager.update(0.0)
    manager.draw_ui(screen)

    # panel = UIPanel(relative_rect=pygame.Rect((10, 10), (200, 70)), starting_layer_height=0, manager=manager)

    if game_paused == True:
        if resume_button.draw(screen):
            game_paused = False
            pygame.mixer.Channel(2).unpause()
            # vol1 - общая громкость, vol2 - громкость спецэффектов, vol3 - громкость музыки
            if vol1 < vol2:
                vol2 = vol1
            if vol1 < vol3:
                vol3 = vol1
            pygame.mixer.Channel(1).set_volume(vol2)
            slider2.setValue(vol2)
            pygame.mixer.Channel(2).set_volume(vol3)
            slider3.setValue(vol3)

        if exit_button.draw(screen):
            game_paused = False
            #pygame.mixer.Channel(2).unpause()
            show_start_menu()
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                #if event.ui_element == pygame_gui.elements.voldsa:
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                    manager.process_events(event)
        clock = pygame.time.Clock()
        time_delta = clock.tick(60) / 1000.0
        manager.update(time_delta)
        manager.draw_ui(screen)

        # print_text("Игра на паузе", 50, weight // 2, height // 4)
    # print_text("Нажмите Enter для продолжения", 30, weight // 2, height // 2)
    pygame.display.flip()


def pause():
    global vol1, vol2, vol3, slider1, slder2, slider3

    #slider1 = Slider(screen, 420, 255, 150, 40, min=0, max=1.0, step=0.25)
    slider1.setValue(vol1)
    #slider2 = Slider(screen, 520, 320, 150, 40, min=0, max=1.0, step=0.25)
    slider2.setValue(vol2)
    #slider3 = Slider(screen, 450, 385, 150, 40, min=0, max=1.0, step=0.25)
    slider3.setValue(vol3)
    #slider.enable()
    global game_paused
    clock = pygame.time.Clock()
    game_paused = True
    while game_paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        show_pause_menu()
        #slider1.draw()
        slider2.draw()
        slider3.draw()
        #print(slider.getValue())
        vol1 = slider1.getValue()
        vol2 = slider2.getValue()
        vol3 = slider3.getValue()

        print_text("ПАУЗА", 310, 70, font_color=((255, 255, 255)), font_size=60)
        print_text("Общая громкость", 160, 265, font_color=((255, 255, 255)), font_size=24)
        print_text("Громкость спецэффектов", 160, 330, font_color=((255, 255, 255)), font_size=24)
        print_text("Громкость музыки", 160, 395, font_color=((255, 255, 255)), font_size=24)

        keys = pygame.key.get_pressed()

        # if keys[pygame.K_RETURN]:
        #game_paused = False
        pygame_widgets.update(pygame.event.get())
        pygame.display.update()
        clock.tick(15)


run = True
while run:
    if game_stage == 0:
        show_start_menu()
    elif game_stage == 1:
        start_game()
    elif game_stage == 2:
        pause()
    elif game_stage == 3:
        show_game_over()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause()
    pygame.display.update()
pygame.quit()
