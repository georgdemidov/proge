import pygame
from pygame.locals import *
from random import randint, choice
import os

pygame.init()

W, H = 744, 256
window = pygame.display.set_mode((W, H))
icon = pygame.image.load(os.path.join('images', 'icon.png'))
pygame.display.set_icon(icon)
pygame.display.set_caption('Proto')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bg_size = bg.get_size()
bgX = 0
bgX2 = bg.get_width()
lives = 3

clock = pygame.time.Clock()

class Player(object):
    run = [pygame.image.load(os.path.join('images', '1.png')),
           pygame.image.load(os.path.join('images', '2.png')),
           pygame.image.load(os.path.join('images', '3.png'))]
    jump = pygame.image.load(os.path.join('images', 'jump.png'))
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jump_list = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.falling = False
        self.jump_count = 0
        self.run_count = 0

    def draw(self, window):
        if self.falling:
            window.blit(pygame.transform.scale(self.fall, (self.width, self.height)), (self.x, self.y))
        elif self.jumping:
            self.y -= self.jump_list[self.jump_count] * 1.3
            window.blit(pygame.transform.scale(self.jump, (self.width, self.height)), (self.x, self.y))
            self.jump_count += 1
            if self.jump_count > 108:
                self.jump_count = 0
                self.jumping = False
                self.run_count = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)

        else:
            if self.run_count >= 6:
                self.run_count = 0
            window.blit(pygame.transform.scale(self.run[int(self.run_count) // 2], (self.width, self.height)), (self.x, self.y))
            self.run_count += 0.5
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)


class Enemy(object):
    animate = [pygame.image.load(os.path.join('images', 'enemy1.png')),
               pygame.image.load(os.path.join('images', 'enemy2.png')),
               pygame.image.load(os.path.join('images', 'enemy3.png')),
               pygame.image.load(os.path.join('images', 'enemy4.png'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animate_count = 0
        self.vel = 1.4

    def draw(self, window):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        if self.animate_count >= 8:
            self.animate_count = 0
        window.blit(pygame.transform.scale(self.animate[int(self.animate_count // 2)], (self.width, self.height)), (self.x, self.y))
        self.animate_count += 0.5

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

def game_font(size, bold=False):
    return pygame.font.Font("munro.ttf", size, bold=bold)

def maths(level=3):
    if level == 3:
        integers = (randint(0, 100), randint(0, 100))
    elif level == 2:
        integers = (randint(3, 20), randint(3, 20))

    if level == 3:
        type = choice(['+', '-'])

        question = "%i %s %i = ?" % (integers[0], type, integers[1])
        if type == '+':
            answer = integers[0] + integers[1]
        elif type == '-':
            answer = integers[0] - integers[1]
    elif level == 2:
        answer = integers[0] * integers[1]
        question = "%i * %i = ?" % (integers[0], integers[1])
    elif level == 1:
        integer = randint(1, 10)
        if integer == 1 or integer == 2:
            integer2 = randint(3, 8)
        else:
            integer2 = randint(2, 4)

        question = "log (alusel: %i) ? = %i" % (integer, integer2)
        answer = integer ** integer2

    return (question, answer)

def start_screen():
    global started, pause
    pause = 0
    started = True

    run = True

    start_bgX = 0
    start_bgX2 = bg.get_width()

    blink = 0

    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.jumping = False

        start_bgX -= 2
        start_bgX2 -= 2

        if start_bgX < bg.get_width() * -1:
            start_bgX = bg.get_width()
        if start_bgX2 < bg.get_width() * -1:
            start_bgX2 = bg.get_width()

        window.blit(pygame.transform.scale(bg, (int(bg_size[0]), int(bg_size[1]))), (start_bgX, 0))
        window.blit(pygame.transform.scale(bg, (int(bg_size[0]), int(bg_size[1]))), (start_bgX2, 0))

        large_font = game_font(50, bold=True)
        start_font = game_font(25)
        window.blit(pygame.transform.scale(icon, (64, 64)), (342, 40))
        game_name = large_font.render('PROTO', 1, (255, 255, 255))
        window.blit(game_name, (W / 2 - game_name.get_width() / 2, 105))

        if blink >= 8 and blink <= 16:
            start_msg = start_font.render('', 1, (255, 255, 255))
            blink += 1
        elif blink < 8:
            start_msg = start_font.render('Kliki, et alustada!', 1, (255, 255, 255))
            blink += 1
        elif blink > 16:
            blink = 0

        window.blit(start_msg, (W / 2 - start_msg.get_width() / 2, 165))

        pygame.display.update()

def maths_screen(maths_tuple):
    global runner, pause, obstacles, lives
    runner = Player(50, 175, 64, 64)
    pause = 0
    obstacles = []
    lives -= 1

    run = True

    input = ''
    keys = {pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2', pygame.K_3: '3',
            pygame.K_4: '4', pygame.K_5: '5', pygame.K_6: '6', pygame.K_7: '7',
            pygame.K_8: '8', pygame.K_9: '9', pygame.K_MINUS: '-'}
    while run:
        pygame.time.delay(100)

        window.blit(pygame.transform.scale(bg, (int(bg_size[0]), int(bg_size[1]))), (0, 0))
        large_font = game_font(30, bold=True)
        question = large_font.render(maths_tuple[0], 1, (255, 255, 255))

        window.blit(question, (W / 2 - question.get_width() / 2, 75))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if not event.key == pygame.K_RETURN:
                    if not event.key == pygame.K_BACKSPACE:
                        if not len(input) > 10:
                            if event.key in keys:
                                input += keys[event.key]
                    else:
                        input = input[:-1]
                else:
                    if len(input) > 0:
                        if int(input) == maths_tuple[1]:
                            run = False
                            runner.falling = False
                            runner.jumping = False
                        else:
                            end_screen()
                            run = False
                            runner.falling = False
                            runner.jumping = False

        input_render = large_font.render('? = '+input, 1, (255, 255, 255))
        window.blit(input_render, (W / 2 - input_render.get_width() / 2, 130))

        pygame.display.update()

def end_screen():
    global runner, pause, score, speed, obstacles, lives
    runner = Player(50, 175, 64, 64)
    pause = 0
    speed = 30
    obstacles = []
    lives = 3

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.jumping = False

        window.blit(pygame.transform.scale(bg, (int(bg_size[0]), int(bg_size[1]))), (0, 0))
        large_font = game_font(50, bold=True)
        score_font = game_font(30)
        game_over = large_font.render('GAME OVER!', 1, (255, 255, 255))
        current_score = score_font.render('Skoor: ' + str(score), 1, (255, 255, 255))
        window.blit(game_over, (W / 2 - game_over.get_width() / 2, 70))
        window.blit(current_score, (W / 2 - current_score.get_width() / 2, 130))
        pygame.display.update()
    score = 0


def redraw_window():
    life_full = pygame.image.load(os.path.join('images', 'life-full.png'))
    life_empty = pygame.image.load(os.path.join('images', 'life-empty.png'))

    large_font = game_font(30, bold=True)
    window.blit(pygame.transform.scale(bg, (int(bg_size[0]), int(bg_size[1]))), (bgX, 0))
    window.blit(pygame.transform.scale(bg, (int(bg_size[0]), int(bg_size[1]))), (bgX2, 0))
    score_text = large_font.render(str(score), 1, (255, 255, 255))
    runner.draw(window)
    for obstacle in obstacles:
        obstacle.draw(window)

    if lives > 0:
        window.blit(pygame.transform.scale(life_full, (32, 32)), (705, 5))
        if lives > 1:
            window.blit(pygame.transform.scale(life_full, (32, 32)), (670, 5))
            if lives > 2:
                window.blit(pygame.transform.scale(life_full, (32, 32)), (635, 5))
    else:
        window.blit(pygame.transform.scale(life_empty, (32, 32)), (705, 5))

    window.blit(score_text, (15, 3))
    pygame.display.update()

pygame.time.set_timer(USEREVENT + 1, 1500)
pygame.time.set_timer(USEREVENT + 2, 5000)
speed = 30

score = 0

run = True
runner = Player(50, 175, 64, 64)

obstacles = []
scored_obstacles = []
pause = 0
started = False

while run:
    if not started:
        pause = 1
        start_screen()
    if pause == 0:
        for obstacle in obstacles:
            if obstacle.collide(runner.hitbox):
                runner.falling = True
                pause = 1
            else:
                if obstacle.x < runner.x:
                    if obstacle not in scored_obstacles:
                        score += 1
                        scored_obstacles.append(obstacle)

            if obstacle.x < -64:
                obstacles.pop(obstacles.index(obstacle))
            else:
                obstacle.x -= 1.4

        bgX -= 1.4
        bgX2 -= 1.4

        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == USEREVENT + 1:
                speed += 1

            if event.type == USEREVENT + 2:
                obstacles.append(Enemy(710, 175, 64, 64))

        if not runner.falling:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                if not runner.jumping:
                    runner.jumping = True

        clock.tick(speed)
    elif pause == 1:
        if lives > 0:
            maths_tuple = maths(lives)
            maths_screen(maths_tuple)
        else:
            end_screen()

    redraw_window()
