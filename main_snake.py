import pygame
import random
from os import path

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (35, 171, 250)

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Snake game")

FPS = 30
snake_block = 30
snake_step = 10

music_dir = path.join(path.dirname(__file__), 'music')
img_dir = path.join(path.dirname(__file__), 'img')


def create_message(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    message = font_style.render(msg, True, color)
    screen.blit(message, (x, y))


def eating_check(xcor, ycor, foodx, foody):
    if foodx - snake_block <= xcor <= foodx + snake_block:
        if foody - snake_block <= ycor <= foody + snake_block:
            return True
        else:
            return False


# Голова змейки
head_snake = [
    pygame.image.load(path.join(img_dir, 'HeadL.png')).convert(),
    pygame.image.load(path.join(img_dir, 'HeadT.png')).convert(),
    pygame.image.load(path.join(img_dir, 'HeadR.png')).convert(),
    pygame.image.load(path.join(img_dir, 'HeadB.png')).convert(),
]


def draw_head(i, snake_list):
    snake_head_img = head_snake[i]
    snake_head = pygame.transform.scale(snake_head_img, (snake_block, snake_block)).convert()
    snake_head.set_colorkey(BLACK)
    snake_head_rect = snake_head.get_rect(x=snake_list[-1][0], y=snake_list[-1][-1])
    screen.blit(snake_head, snake_head_rect)


def game_loop():
    i = 0
    snake_list = []
    xCor = DISPLAY_WIDTH / 2
    yCor = DISPLAY_HEIGHT / 2

    clock = pygame.time.Clock()

    x_change = 0
    y_change = 0
    length = 2
    score = 0

    run_game = True
    game_close = False

    foodX = random.randrange(snake_block, DISPLAY_WIDTH - snake_block)
    foodY = random.randrange(snake_block, DISPLAY_HEIGHT - snake_block)

    pygame.mixer.music.load(path.join(music_dir, 'Intense.mp3'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    am = pygame.mixer.Sound(path.join(music_dir, 'apple_bite.ogg'))
    am.set_volume(0.1)

    hit = pygame.mixer.Sound(path.join(music_dir, 'hit_wall.mp3'))
    hit.set_volume(0.1)


    bg = pygame.image.load(path.join(img_dir, 'Fon_grass4_1.jpg'))
    bg = pygame.transform.scale(bg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    bg_rect = bg.get_rect()

    food = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'f_1.png')).convert(), (snake_block, snake_block))
    food.set_colorkey(WHITE)
    food_rect = food.get_rect(x=foodX, y=foodY)


    while run_game:
        clock.tick(FPS)
        screen.fill(BLUE)
        screen.blit(bg, bg_rect)
        create_message(f"Ваш счёт: {score}", BLACK, 10, 10, "comicsans", 18)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change = -snake_step
                    y_change = 0
                    i = 0
                elif event.key == pygame.K_d:
                    x_change = snake_step
                    y_change = 0
                    i = 2
                elif event.key == pygame.K_w:
                    x_change = 0
                    y_change = -snake_step
                    i = 1
                elif event.key == pygame.K_s:
                    x_change = 0
                    y_change = snake_step
                    i = 3

        xCor += x_change
        yCor += y_change

        if xCor <= 0 or xCor >= DISPLAY_WIDTH or yCor <= 0 or yCor >= DISPLAY_HEIGHT:
            run_game = False
            game_close = True
            pygame.mixer.music.load(path.join(music_dir, 'lose_game.mp3'))
            hit.play()
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.1)

        snake_head = [xCor, yCor]
        snake_list.append(snake_head)

        if len(snake_list) > length:
            del snake_list[0]

        for x in snake_list[1:]:
            snake_img = pygame.image.load(path.join(img_dir, 'body3.png')).convert()
            snake = pygame.transform.scale(snake_img, (snake_block, snake_block))
            snake.set_colorkey(WHITE)
            screen.blit(snake, (x[0], x[1]))
            # pygame.draw.rect(screen, BLACK, (snake[0], snake[1], snake_block, snake_block))

        for snake in snake_list[1:-1]:
            if snake == snake_head:
                run_game = False
                game_close = True
                pygame.mixer.music.load(path.join(music_dir, 'lose_game.mp3'))
                pygame.mixer.music.play()

        # Отрисовка спрайта головы
        draw_head(i, snake_list)
        screen.blit(food, food_rect)
        # draw_tail(i, snake_list)
        # pygame.draw.rect(screen, GREEN, (foodX, foodY, snake_block, snake_block))

        if eating_check(xCor, yCor, foodX, foodY):
            length += 3
            score += 1
            foodX = random.randrange(0, DISPLAY_WIDTH - snake_block)
            foodY = random.randrange(0, DISPLAY_HEIGHT - snake_block)
            food = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'f_1.png')).convert(), (snake_block, snake_block))
            food_rect = food.get_rect(x=foodX, y=foodY)
            food.set_colorkey(WHITE)
            am.play()







        while game_close:
            screen.fill(BLACK)
            create_message("Вы проиграли!", RED, 200, 100, "comicsans", 60)
            create_message(f"Ваш счёт: {score}", RED, 350, 200, "comicsans", 20)
            create_message("Для выхода нажмите \"Q\". Для продолжения нажмите \"R\" ", WHITE, 60, 250, "comicsans", 25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_loop()
                    elif event.key == pygame.K_q:
                        run_game = False
                        game_close = False

            pygame.display.update()

        pygame.display.update()
        pygame.display.flip()


game_loop()

pygame.quit()
quit()
