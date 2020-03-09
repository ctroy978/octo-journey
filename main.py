import pygame, sys, os
from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as msg:
        print('Cannot load image: ', msg)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Ship(pygame.sprite.Sprite):
    def __init__(self, scr_width, scr_height):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('ship.png', -1)
        self.scr_width = scr_width
        self.pos_x = scr_width // 2 #starting x position
        self.pos_y = scr_height - self.image.get_height() #starting y position
        self.rect.midtop = (self.pos_x, self.pos_y)
        self.dx = 0
        self.speed = 0
        self.direction = 'stop'

    def update(self):
        """move the ship"""
        self.accelerate()
        if self.pos_x > self.image.get_width()//2 and self.dx < 0:
            self.pos_x += self.dx
        if self.pos_x < self.scr_width - self.image.get_width()//2 and self.dx > 0:
            self.pos_x += self.dx

        self.rect.midtop = (self.pos_x, self.pos_y)

    def move(self, direction):
        """declare the direction based on key presses"""
        self.direction = direction

    def accelerate(self):
        """change self.speed based on direction"""
        if self.direction == 'stop' and self.speed != 0:
            if self.speed > 0:
                self.speed -= .02
            elif self.speed < 0:
                self.speed += .02
        if self.direction == 'right' and self.speed < 7:
            self.speed += .02
        if self.direction == 'left' and self.speed > -7:
            self.speed -= .02
        """if we are on the edge, zero out speed because we've stopped"""
        if self.pos_x > self.scr_width - self.image.get_width()//2 and self.dx > 0:
            self.speed = 0
        if self.pos_x < self.image.get_width()//2 and self.dx < 0:
            self.speed = 0
        self.dx = self.speed




SCR_WIDTH = 600
SCR_HEIGHT = 600
BLACK = (0, 0, 0)
SHIP_SPEED = 2

pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Alien Invader')
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)

#build screen while loading
screen.blit(background, (0, 0))
pygame.display.flip()

ship = Ship(SCR_WIDTH, SCR_HEIGHT)
allsprites = pygame.sprite.RenderPlain((ship))


while True:
    clock.tick(60)
    screen.blit(background, (0, 0))


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                ship.move('right')
            if event.key == K_LEFT:
                ship.move('left')
        elif event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_LEFT:
                ship.move('stop')

    allsprites.update()
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()





