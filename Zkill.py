#!/usr/bin/python2

from __future__ import division
import pygame, sys, os, math, operator
from pygame.locals import *
from pygame.compat import geterror

size = (800, 600)
game_dir = "./"
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

def coord_to_angle(player_coord, crosshair_coord):
    #This function will get the player rotation from the aim position.
    #First we subtract the player coords from the crosshair coords, to simulate a 0,0 axis:
    #TODO: clean up this mess!
    #I guess for now this is here to stay...
    player_coord[1] = -player_coord[1]
    relative_coords = map(operator.sub,crosshair_coord, player_coord)
    relative_coords[1] = -relative_coords[1]
    #Then we calculate the angle from the new coord set:
    if relative_coords[1] == 0 and relative_coords[0] > 0:
        angle = -90
    elif relative_coords[1] == 0 and relative_coords[0] < 0:
        angle = 90
    else:
        if relative_coords[1] > 0:
            angle = -math.degrees(math.atan(relative_coords[0]/relative_coords[1]))
        else:
            angle = -math.degrees(math.atan(relative_coords[0]/relative_coords[1])) -180

    return angle

def main():
    pygame.init()
    pygame.mouse.set_visible(0) # Sets mouse cursor invisible

    background= pygame.image.load("images/Building01.png").convert()
    background = pygame.transform.scale(background,size)
    screen.blit(background, (0,0))
    clock = pygame.time.Clock()
    h_position = 400
    v_position = -305
    rotation = 0
    speed = 3

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

        #h_position += (keystate[K_RIGHT] - keystate[K_LEFT]) * speed
        #v_position += (keystate[K_UP] - keystate[K_DOWN]) * speed

        rotation = coord_to_angle([h_position,v_position], pygame.mouse.get_pos())

        h_position += math.cos(math.radians(rotation+90)) * (keystate[K_UP]) * speed
        v_position += math.sin(math.radians(rotation+90)) * (keystate[K_UP]) * speed 
        h_position += math.cos(math.radians(rotation+90)) * (keystate[K_DOWN]) * -speed
        v_position += math.sin(math.radians(rotation+90)) * (keystate[K_DOWN]) * -speed 
        h_position += math.cos(math.radians(rotation)) * (keystate[K_RIGHT]) * speed
        v_position += math.sin(math.radians(rotation)) * (keystate[K_RIGHT]) * speed 
        h_position += math.cos(math.radians(rotation+180)) * (keystate[K_LEFT]) * speed
        v_position += math.sin(math.radians(rotation+180)) * (keystate[K_LEFT]) * speed 

        player1.move(h_position,v_position)
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

main()
