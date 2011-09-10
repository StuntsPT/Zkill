#!/usr/bin/python2

import pygame, sys, os
from pygame.locals import *
from pygame.compat import geterror

#Title goes here

size = (800, 600)
game_dir = "/home/diogo/Dropbox/Share_Francisco/Zkill/"
player_speed = [200,200]
screen = pygame.display.set_mode(size)

def load_image(name, colorkey=None):
    fullname = os.path.join(game_dir, name)
    try:
        image =pygame.image.load(fullname)
    except pygame.error:
        print ("Cannot load image... canalha!: ", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def main():
    pygame.init()
    pygame.mouse.set_visible(0) # Sets mouse cursor invisible

    background= pygame.image.load("Building01.png").convert()
    background = pygame.transform.scale(background,size)
    screen.blit(background, (0,0))
    clock = pygame.time.Clock()
    h_direction = 133
    v_direction = -100
    rotation = 0

    while True:
        clock.tick(60)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.update()
        crosshair = Crosshair()
        player1 = Player()
        allsprites = pygame.sprite.RenderPlain(crosshair,player1)
        keystate = pygame.key.get_pressed()

        h_direction += keystate[K_RIGHT] - keystate[K_LEFT]
        v_direction += keystate[K_UP] - keystate[K_DOWN]

        if rotation >= 360 or rotation <= -360:
            rotation = 0
        else:
            rotation += keystate[K_q] - keystate[K_e]

        player1.move(h_direction,v_direction)
        player1.rotate(rotation)

        screen.blit(background, (0,0))
        # Draws everything (order matters)
        allsprites.update()
        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()


class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Calls sprite initializer
        self.image, self.rect = load_image("Aim.png",-1)
    def update(self):
        # Move the crosshair based on mouse position
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        return self.rect

class Player(pygame.sprite.Sprite):
    speed = 3
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("Player.png",-1)
    def move(self,h_direction,v_direction):
        self.rect.move_ip(h_direction*self.speed,0)
        self.rect.move_ip(0, -v_direction*self.speed)
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

main()
