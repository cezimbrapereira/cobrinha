import pygame
import sys
import random
from pygame.math import Vector2

# todas as imagens nesse jogo foram feitas por mim
# o áudio da mordida https://youtu.be/Haoq2hDGLtQ
# e a música de fundo é um midi que eu modifiquei


class SNAKE:
    def __init__(self):

        self.body = [Vector2(3, 4), Vector2(2, 4), Vector2(1, 4)]  # posição inicial
        # importante ir em ordem x decrescente para que apareça 1 2 3 e não 3 2 1
        # o 3/ primeiro item é a cabeça. a cobra nasce com 3 blocos
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.eat_sound = pygame.mixer.Sound('Sound/nom.mp3')

# partes do corpo dela ^, a maioria dos nomes se explicam, mas tr/tl/br/bl é
# top right, top left, bottom right, bottom left para quando ela muda de direção

# escolhe qual parte da cobra vai em qual lugar v

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                if previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                # compara posições x e y entre partes adjacentes para saber onde conectar ^

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]  # 0 é a cabeça
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down  # método similar ao o anterior,
            # mas em vez de comparar dois, compara si mesmo com apenas um.

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down  # mesma coisa, mas para o rabo

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        # movimento normal (else) joga todos os blocos para a direção escolhida e apaga o último.
        # caso ela tenha comido algo, ele não apaga o último bloco, fazendo a cobra
        # aumentar de tamanho

    def add_block(self):
        self.new_block = True

    def play_eat_sound(self):
        self.eat_sound.play()

    def reset(self):
        self.body = [Vector2(3, 4), Vector2(2, 4), Vector2(1, 4)]
        # quando dá game over ela automaticamente reseta para a posição inicial


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect((int(self.pos.x * cell_size)), (int(self.pos.y * cell_size)), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_horizontal - 1)
        self.y = random.randint(0, cell_vertical - 1)
        self.pos = Vector2(self.x, self.y)  # joga ela num x e y aleatório


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_tiles()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_eat_sound()
            # se a cabeça da cobra acertar a maçã, toca o som
            # de comida, a maçã é jogada em outro lugar
            # a cobra cresce

        for block in self.snake.body[:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
        # se a maçã for nascer no mesmo bloco que a cobra
        # está, ela é re-randomizada

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_horizontal or not 0 <= self.snake.body[0].y < cell_vertical:
            self.game_over()
        # cobra precisa estar dentro da janela. se ela passar um bloco para fora/ bater na parede,
        # o jogo vai dar game over.
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        # se 0 (cabeça) parar no mesmo bloco que qualquer outra parte do corpo (1:), dá gameover
        # infelizmente tem bugs. se mudar ela de direção rápido demais dá gameover
        # mesmo tendo só 3 partes (impossível de colidir), ainda ocorre :/

    def game_over(self):
        self.snake.reset()
        self.snake.direction = Vector2(0, 0)
        # coloca a cobra em posição inicial e tira o movimento que ela estava antes de bater

    def draw_tiles(self):
        tiles_color = (248, 248, 200)
        for row in range(cell_horizontal):
            if row % 2 == 0:
                for col in range(cell_vertical):
                    if col % 2 == 0:
                        tiles_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, tiles_color, tiles_rect)
            else:
                for col in range(cell_horizontal):
                    if col % 2 != 0:
                        tiles_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, tiles_color, tiles_rect)
            # meio complexo, tive que dar uma ajeitada algumas vezes. mas as linhas pares
            # tem blocos amarelos nas colunas pares (2, 4, 6)
            # e nas linhas ímpares, tem blocos amarelos nas colunas ímpares (1, 3, 5)


pygame.init()
pygame.mixer.music.load('Sound/musica.wav')
# sim, é um rickroll disfarçado de lo-fi, beijos.
# link midi https://bitmidi.com/never-gonna-give-you-up-2-mid
pygame.mixer.music.play(-1)
# loop ^
cell_size = 48
# ^ fiz a cobra em 16x16, então usar um múltiplo para o bloco e aumentar a imagem funcionou bem
cell_horizontal = 10
cell_vertical = 9
# ^ mesmo tamanho utilizado pelo menor mapa do jogo da cobra do google
screen = pygame.display.set_mode((cell_horizontal * cell_size, cell_vertical * cell_size))
# ^ tela, x por y
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
# ^ velocidade do jogo. eu gosto de jogar com 100–125, mas deixei
# o projeto em 150.

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            # ^ fecha o jogo
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            # up joga a cobra para cima, down para baixo, etc etc
            # mas a cobra não pode andar dentro dela mesma
            # então ela só pode andar para cima se ela não estiver
            # andando para baixo. eu precisaria mudar ela para um lado
            # e somente depois para cima
            # caso não tivesse esse if, ela entraria nela mesma
            # e daria game over por colisão

    screen.fill((255, 255, 255))
    # branco
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
    # fps
