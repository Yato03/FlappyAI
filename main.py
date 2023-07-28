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
fps = 60
STATS_FONT = pygame.font.SysFont("Cascadia Code", 50)

birds_IMGS = [
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

def main(genomes, config):

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(200, 350, birds_IMGS))
        g.fitness = 0
        ge.append(g)

    pipes = [Pipe(600, PIPE_IMG)]

    base = Base(730, BASE_IMG)

    score = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #if press n next generation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    run = False
                    break

        #LÓGICA
        
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()
        
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600, PIPE_IMG))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.actual_img.get_height() >= 730 or bird.y < 0:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        #DIBUJO
        screen.blit(BG_IMG, (0,0))

        for pipe in pipes:
            pipe.draw(screen)

        text = STATS_FONT.render("Score: " + str(score), 1, BLACK)
        screen.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

        base.draw(screen)
        for bird in birds:
            bird.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)