import pygame, sys, os, random, math
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

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

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

    def collided(self, target):
        for alien in target:
            if self.rect.colliderect(alien.rect) and alien.get_collided() == False:
                alien.set_collided(True)
                return True


class Basic_alien(pygame.sprite.Sprite):

    def __init__(self, scr_width, scr_height, ship):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('ufo1.png', -1)
        self.scr_width = scr_width
        self.scr_height = scr_height
        self.pos_x = random.randint(self.image.get_width(), scr_width - self.image.get_width())
        self.pos_y = 50 #starting y position
        self.rect.midtop = (self.pos_x, self.pos_y)
        self.dx = 0
        self.dy = 0
        self.speed = 0
        self.max_speed = random.randint(5, 7)
        self.timer = random.randint(200, 300)
        self.ship = ship
        self.collided = False

    def update(self):
        self.move()

        self.rect.midtop = (self.pos_x, self.pos_y)
        if self.pos_y > self.scr_height:
            self.rebuild()

    def move(self):
        enemy_x = self.ship.get_x()
        if self.timer > 0:
            self.timer -= 1
            if enemy_x > self.pos_x:
                self.pos_x += .5
            elif enemy_x < self.pos_x:
                self.pos_x -= .5

        if self.timer == 0 and self.speed < self.max_speed:
            self.speed += .02

        self.pos_y += self.speed

    def rebuild(self):
        self.pos_x = random.randint(self.image.get_width(), self.scr_width - self.image.get_width())
        self.pos_y = 50 #starting y position
        self.rect.midtop = (self.pos_x, self.pos_y)
        self.dx = 0
        self.dy = 0
        self.speed = 0
        self.max_speed = random.randint(5, 7)
        self.timer = random.randint(200, 300)
        self.collided = False

    def get_collided(self):
        return self.collided

    def set_collided(self, hit):
        self.collided = True

def show_explosions(explosions, screen):
    WHITE = (240, 233, 240)
    for explosion in explosions:
        pos_x = explosion[0]
        pos_y = explosion[1]
        pygame.draw.circle(screen, WHITE, (pos_x, pos_y), explosion[2], 3)
        if explosion[2] < 30:
            explosion[2] += 2
        if explosion[2] > 30:
            explosions.remove(explosion)






SCR_WIDTH = 800
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
aliens = []
for x in range(3):
    aliens.append(Basic_alien(SCR_WIDTH, SCR_HEIGHT, ship))
allsprites = pygame.sprite.RenderPlain((ship, aliens))

explosions = []

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

    if ship.collided(aliens):
        #make explosions a bit random
        x = random.randint(math.floor(ship.get_x()) - 20, math.floor(ship.get_x()) +20)
        y = random.randint(math.floor(ship.get_y()) - 20, math.floor(ship.get_y()) +20)
        explosions.append([x, y, 3])

    allsprites.update()
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    show_explosions(explosions, screen)
    pygame.display.flip()





