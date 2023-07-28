import neat
import pygame
import time
import random
import os
import sys
from entities.bird import Bird
from entities.pipe import Pipe
from entities.base import Base

pygame.init()
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

size = (WIN_WIDTH,WIN_HEIGHT)
fps = 30
STATS_FONT = pygame.font.SysFont("Cascadia Code", 50)

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
    ]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

#COLORES
BLACK = 0, 0, 0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

bird = Bird(200, 350, BIRD_IMGS)

pipes = [Pipe(600, PIPE_IMG)]

base = Base(730, BASE_IMG)

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #LÓGICA
    #bird.move()
    base.move()

    rem = []
    add_pipe = False
    for pipe in pipes:
        if pipe.collide(bird):
            pass

        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            rem.append(pipe)

        if not pipe.passed and pipe.x < bird.x:
            pipe.passed = True
            add_pipe = True

        pipe.move()
    
    if add_pipe:
        score += 1
        pipes.append(Pipe(700, PIPE_IMG))

    for r in rem:
        pipes.remove(r)

    if bird.y + bird.actual_img.get_height() >= 730:
        pass

    #DIBUJO
    screen.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(screen)

    text = STATS_FONT.render("Score: " + str(score), 1, BLACK)
    screen.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(screen)
    bird.draw(screen)

    pygame.display.flip()
    clock.tick(fps)