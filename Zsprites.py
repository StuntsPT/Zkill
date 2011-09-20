#!/usr/bin/python2

import pygame, os, sys
from pygame.locals import *

game_dir = "./"

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

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Calls sprite initializer
        self.image, self.rect = load_image("images/Aim.png",-1)
    def update(self):
        # Move the crosshair based on mouse position
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        return self.rect

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("images/Player_Head.png",-1)
    def move(self,h_position,v_position):
        self.rect.move_ip(h_position, -v_position)
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

Crosshair()
Player()
