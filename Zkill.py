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

def coord_to_angle(source_coord, target_coord):
    #This function will get the player player_rotation from the aim position.
    #First we subtract the player coords from the crosshair coords, to simulate a 0,0 axis:
    #TODO: clean up this mess!
    #I guess for now this is here to stay...
    source_coord[1] = -source_coord[1]
    relative_coords = map(operator.sub,target_coord, source_coord)
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
    z_h_position = h_position - 300
    z_v_position = v_position + 200
    base_speed = 3

    while True:
        clock.tick(60)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.update()
        crosshair = Crosshair()
        player1 = Player()
        zombie = Zombie()
        #shot = Handgun()
        allsprites = pygame.sprite.RenderPlain(crosshair,player1,zombie)
        keystate = pygame.key.get_pressed()
        
        #Define PLayer movement
        player_rotation = coord_to_angle([h_position,v_position], pygame.mouse.get_pos())

        speed = base_speed + 0

        h_position += math.cos(math.radians(player_rotation+90)) * (keystate[K_UP]) * speed 
        v_position += math.sin(math.radians(player_rotation+90)) * (keystate[K_UP]) * speed 
        h_position += math.cos(math.radians(player_rotation+90)) * (keystate[K_DOWN]) * -speed 
        v_position += math.sin(math.radians(player_rotation+90)) * (keystate[K_DOWN]) * -speed 
        h_position += math.cos(math.radians(player_rotation)) * (keystate[K_RIGHT]) * speed 
        v_position += math.sin(math.radians(player_rotation)) * (keystate[K_RIGHT]) * speed 
        h_position += math.cos(math.radians(player_rotation+180)) * (keystate[K_LEFT]) * speed 
        v_position += math.sin(math.radians(player_rotation+180)) * (keystate[K_LEFT]) * speed 

        player1.move(h_position,v_position)
        player1.rotate(player_rotation)


        #Define Zombie movement:

        zombie_speed = 2
        zombie_rotation = coord_to_angle([z_h_position,z_v_position], [h_position,-v_position])

        z_h_position += math.cos(math.radians(zombie_rotation+90)) * zombie_speed
        z_v_position += math.sin(math.radians(zombie_rotation+90)) * zombie_speed
        zombie.move(z_h_position,z_v_position)
        zombie.rotate(zombie_rotation)

        ##Define bullet movement
        #bullet_speed = 10
        #b_h_position += h_position + math.cos(math.radians(player_rotation+90)) * bullet_speed
        #b_v_position += v_position + math.sin(math.radians(player_rotation+90)) * bullet_speed

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
#    def temp_boosts(self, extra_speed):
#        self.extra_speed = extra_speed
#        return extra_speed

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("images/Zombie.png",-1)
    def move(self, z_h_position, z_v_position):
        self.rect.move_ip(z_h_position, -z_v_position)
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)

class Handgun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("image/HG_bullet.png",-1)
    def move(self, h_position, v_position):
        self.rect.move_ip(h_position, -v_position)

main()
