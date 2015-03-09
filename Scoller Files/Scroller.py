""" A  basic Side-Scroller Shooting Game """

import random
import time

import pygame


class DrawableSurface():
    """ A class that wraps a pygame.Surface and a pygame.Rect """
    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        self.surface = surface
        self.rect = rect

    def get_surface(self):
        """ Get the surface """
        return self.surface

    def get_rect(self):
        """ Get the rect """
        return self.rect

class Plane(pygame.sprite.Sprite):
    """ represents the state of the player in the game """
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/biplane.png')
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_y = 0

    def update(self):
        pygame.event.pump()
        self.pos_x += 0
        if (pygame.key.get_pressed()[pygame.K_w]) and self.pos_y > 0:
            self.pos_y -= 1
        if (pygame.key.get_pressed()[pygame.K_a]) and self.pos_x > 0:
            self.pos_x -= 1
        if (pygame.key.get_pressed()[pygame.K_d]) and self.pos_x < 1080:
            self.pos_x += 1
        if (pygame.key.get_pressed()[pygame.K_s]) and self.pos_y < 360:
            self.pos_y += 1

    def get_drawables(self):
        w,h = self.image.get_size()
        return [DrawableSurface(self.image, 
                                pygame.Rect(self.pos_x, self.pos_y, w, h))]

class Bullet(pygame.sprite.Sprite):
    """ represents the state of the player in the game """
    def __init__(self, bpos_x, bpos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.image.set_colorkey((255,255,255))
        self.bpos_x = bpos_x + 200
        self.bpos_y = bpos_y + 50
        
    def update(self):
        """ change to moving the bullet across the screen """
        self.bpos_x += 3

    def get_drawables(self):
        """ return a sprite to draw """
        return DrawableSurface(self.image, pygame.Rect((self.bpos_x, self.bpos_y), self.image.get_size()))

class Background(pygame.sprite.Sprite):
    """ Represents the background (at first just the ground) """
    def __init__(self,pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/background.png')
        self.image.set_colorkey((255,255,255))
        self.pos_x = pos_x
        self.height = 480

    def update(self):
        """ update the background to move at a constant rate"""
        self.pos_x -=2

    def get_drawables(self):
        """ Gets the drawables for the background """
        return DrawableSurface(self.image, pygame.Rect(self.pos_x, self.height - 128, 1024, 128))

class Enemy(pygame.sprite.Sprite):
    """ represents the state of the player in the game """
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/biplane_grey.png')
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self):
        pygame.event.pump()
        self.pos_x -= 1        

    def get_drawables(self):
        w,h = self.image.get_size()
        return [DrawableSurface(self.image, 
                                pygame.Rect(self.pos_x, self.pos_y, w, h))]

class ScrollerModel():
    """ Represents the game state of the scroller """
    def __init__(self, width, height):
        """ Initialize the plane model """
        self.width = width
        self.height = height
        self.plane = Plane(0,200)
        self.enemy = Enemy(1080, 200)
        self.bullets = []
        self.enemies = []
        self.background = [Background(0),Background(1024),Background(2048)]

    def get_plane_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        return self.plane.get_drawables()# + self.background.get_drawables()

    def get_bullet_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        return [bullet.get_drawables() for bullet in self.bullets]# + self.background.get_drawables()

    def get_background_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        return [background.get_drawables() for background in self.background]

    def get_enemy_drawables(self):
        """ gets a list of all enemy drawables"""
        return self.enemy.get_drawables()

    def is_player_dead(self):
        """ Return True if the player is dead the player
            has collided with an obstacle, and false otherwise """
        #We can never die. Until we figure out collisions, at least.
        return 0

    def is_enemy_dead(self):
        """ Return True if the player is dead the player
            has collided with an obstacle, and false otherwise """
        #We can never die. Until we figure out collisions, at least.
        return 0

    def plane_update(self):
        """ Updates the model and its constituent parts """
        self.plane.update()

    def enemy_update(self):
        """ updates enemies"""
        #self.enemy.update()
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    print len(self.enemies)
                    self.enemies.append(Enemy(1080, 200))
        for enemy in self.enemies:
            self.enemy.update()
            if enemy.pos_x < 0:
                self.enemies = self.enemies[1:]

    def bullet_update(self):
        """checks for creation of a bullet. If bullet created, add bullet to
        a list of bullets"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print len(self.bullets)
                    self.bullets.append(Bullet(self.plane.pos_x, self.plane.pos_y))
        for bullet in self.bullets:
            bullet.update()
            if bullet.bpos_x > 1280:
                self.bullets = self.bullets[1:]

    def background_update(self):
        """Updates the background"""
        for background in self.background:
            background.update()
            if background.pos_x < -1023:
                self.background = self.background[1:]
                self.background.append(Background(2048))

class ScrollerView():
    def __init__(self, s_model, width, height):
        """ Initialize the view.  The input model is necessary to find 
            the position of relevant objects to draw. """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        # this is used for figuring out where to draw stuff
        self.game_model = s_model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        # get the new drawables
        self.drawables = (self.game_model.get_plane_drawables() 
                        + self.game_model.get_bullet_drawables() 
                        + self.game_model.get_background_drawables()
                        + self.game_model.get_enemy_drawables())
        for d in self.drawables:
            rect = d.get_rect()
            surf = d.get_surface()
            surf.set_colorkey((255,255,255))
            self.screen.blit(surf, rect)

class SideScroller():
    """ The main SideScroller class """

    def __init__(self):
        """ Initialize the game.  Use SideScroller.run to
            start the game """
        self.game_model = ScrollerModel(1280, 480)
        self.view = ScrollerView(self.game_model, 1280, 480)

    def run(self):
        """ the main runloop... loop until death """
        last_update_time = time.time()
        while not(self.game_model.is_player_dead()):
            self.game_model.plane_update()
            self.game_model.bullet_update()
            self.game_model.background_update()
            self.game_model.enemy_update()
            self.view.draw()
            last_update_time = time.time()
            pygame.display.update()

if __name__ == '__main__':
    Scroller = SideScroller()
    Scroller.run()

