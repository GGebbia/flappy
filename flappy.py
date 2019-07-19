import pygame, sys
from pygame.locals import *
import random

FPS = 15
WINDOWWIDTH = 600
WINDOWHEIGHT = 500

# R G B
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DARKGREEN = ( 0, 155, 0)
DARKGRAY = ( 40, 40, 40)
BGCOLOR = BLACK


#Initialization
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Floppy Jwen')


#Images (Player, Background, Pipes)
player = pygame.image.load('flappy.png').convert_alpha()
player.set_colorkey((0,0,0))

pipes = pygame.image.load('pipes.png').convert_alpha()
pipes.set_colorkey((0,0,0))

# Creating the Poles Generator class
class PolesGenerator:
    poles = []
    color_poles = []

    def update(self):
        self.spawner()
        self.move(vel=5)
        self.show()

    def create_pole(self):
        heightPoleU = random.randint(50, WINDOWHEIGHT)
        c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        poleD = pygame.Rect((WINDOWWIDTH, heightPoleU, 20, WINDOWHEIGHT - heightPoleU))

        poleU = pygame.Rect((WINDOWWIDTH, 0, 20, heightPoleU - 100))

        self.poles.append(poleD)
        self.color_poles.append(c)
        self.poles.append(poleU)
        self.color_poles.append(c)

    # distance between two poles. set the new spawn to 200
    dist_poles = 50
    spawn_new = 50

    # if the distance from last pole created is 200  then create another pole.
    # Otherwise increase 1 to the distance between the pole and the wall (spawn_new += 1)
    def spawner(self):
        if self.spawn_new == self.dist_poles:
            self.create_pole()
            self.spawn_new = 0
        self.spawn_new += 1

    def move(self, vel):
        for pole in self.poles:
            pole[0] -= vel

    def show(self):
        for i, pole in enumerate(self.poles):
            pygame.draw.rect(DISPLAYSURF, self.color_poles[i], pole)


class Bird:

    def __init__(self):
        self.width = 2 * 20
        self.height = 2 * 15
        self.bird = pygame.transform.scale(player, (self.width, self.height))
        self.birdrect = self.bird.get_rect()
        self.x = 10
        self.y = int(WINDOWHEIGHT / 2) - self.bird.get_height() / 2
        self.speed = 5
        self.jump = False
        self.jumpCount = 10

    def update(self):
        self.movement()
        if self.collision() != -1:
            GameOverScreen()


    def collision(self):

        return (self.birdrect).collidelist(PolesGenerator.poles)



    def movement(self):
        keys = pygame.key.get_pressed()

        if not self.jump:

            if keys[pygame.K_UP] and self.y > self.speed:
                self.y -= self.speed
            if keys[pygame.K_DOWN] and self.y < WINDOWHEIGHT - self.bird.get_height() - self.speed:
                self.y += self.speed
            if keys[pygame.K_SPACE]:
                self.jump = True
                self.sign = 1
            if keys[pygame.K_SPACE] and keys[pygame.K_DOWN]:
                self.jump = True
                self.sign = -1
        else:
            if self.y < self.jumpCount ** 2 / 2 + 5 and self.sign == 1:
                self.jump = False
                self.jumpCount = 10
                self.y = 5

            elif self.y > WINDOWHEIGHT - self.bird.get_height() - self.jumpCount ** 2 / 2 and self.sign == -1:
                self.jump = False
                self.jumpCount = 10
                self.y = WINDOWHEIGHT - self.bird.get_height() - 5

            elif self.jumpCount > 0:
                self.y -= self.sign * self.jumpCount ** 2 / 2
                self.jumpCount -= 1
            else:
                self.jump = False
                self.jumpCount = 10

        self.birdrect[0] = self.x
        self.birdrect[1] = self.y

    def show(self):
        DISPLAYSURF.blit(self.bird, (self.x, self.y))


def main():
    poles = PolesGenerator()
    bird = Bird()

    while True:
        pygame.time.delay(20)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill((0, 0, 0))
        bird.update()
        poles.update()
        bird.show()
        pygame.display.update()

def StartScreen():
    textFont = pygame.font.Font('freesansbold.ttf', 120)
    flappySurf = textFont.render('Flappy', True, DARKGREEN)
    flappyRect = flappySurf.get_rect()
    birdSurf = textFont.render('Jwen', True, DARKGREEN)
    birdRect = flappySurf.get_rect()
    flappyRect.midtop = (WINDOWWIDTH / 2, 10)
    birdRect.midtop = (WINDOWWIDTH / 2, flappyRect.height + 10 + 25)

def GameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, RED)
    overSurf = gameOverFont.render('Over', True, RED)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    PressAnyKeyMessage()
    pygame.display.update()
    pygame.time.wait(50)
    KeyPress()  # clear out any key presses in the event queue

    while True:
        if KeyPress():
            pygame.event.get()  # clear event queue
            return


def PressAnyKeyMessage():
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    pressKeySurf = BASICFONT.render('Press any key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def KeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        pygame.quit()
        sys.exit()
    keyupevent = pygame.event.get(KEYUP)
    if len(keyupevent) == 0:
        return None
    if keyupevent[0].key == K_ESCAPE:
        pygame.quit()
        sys.exit()
    return keyupevent[0].key

main()