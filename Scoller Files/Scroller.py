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

class Plane():
    """ represents the state of the player in the game """
    def __init__(self, pos_x, pos_y):
        self.image = pygame.image.load('images/biplane.png')
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_y = 0

    def update(self):
        pygame.event.pump()
        self.pos_x += 0
        if (pygame.key.get_pressed()[pygame.K_w]):
            self.pos_y -= 1
        if (pygame.key.get_pressed()[pygame.K_a]):
            self.pos_x -= 1
        if (pygame.key.get_pressed()[pygame.K_d]):
            self.pos_x += 1
        if (pygame.key.get_pressed()[pygame.K_s]):
            self.pos_y += 1

    def get_drawables(self):
        w,h = self.image.get_size()
        return [DrawableSurface(self.image, 
                                pygame.Rect(self.pos_x, self.pos_y, w, h))]

class Background():
    """ Represents the background (at first just the ground) """
    def __init__(self,width,height):
        self.image = pygame.image.load('images/background.png')
        self.image.set_colorkey((255,255,255))
        self.height = height

    def get_drawables(self):
        """ Gets the drawables for the background """
        drawables = []
        for i in range(100):
            drawables.append(DrawableSurface(self.image,
                                             pygame.Rect(i*1024,self.height - 128,1024,128)))
        return drawables

    def collided_with(self, entity):
        """ Returns True iff the input drawable surface (entity) has
            collided with the ground """
        drawables = self.get_drawables()
        rectangles = []
        for d in drawables:
            rectangles.append(d.get_rect())
        return entity.get_rect().collidelist(rectangles) != -1

class Bullet():
    """ represents the state of the player in the game """
    def __init__(self, bpos_x, bpos_y):
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

class Enemy():
    pass
    #     """ represents the states of the enemies in the game """
    #     def __init__(self, pos_x, pos_y):
    #         self.image = pygame.image.load('images/biplane_grey.png')
    #         self.pos_x = pos_x
    #         self.pos_y = pos_y
    #         self.vel_y = 0

    #     def update(self):

class ScrollerModel():
    """ Represents the game state of the scroller """
    def __init__(self, width, height):
        """ Initialize the plane model """
        self.width = width
        self.height = height
        # self.plane_model = Plane
        self.background = Background(width, height)
        self.plane = Plane(0,200)
        self.background = Background(width, height)
        self.bullets = []
        self.bullets.append(Bullet(self.plane.pos_x,self.plane.pos_y))

    def get_plane_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        return self.plane.get_drawables() + self.background.get_drawables()

    def get_bullet_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        return [bullet.get_drawables() for bullet in self.bullets] + self.background.get_drawables()

    def is_player_dead(self):
        """ Return True if the player is dead (for instance) the player
            has collided with an obstacle, and false otherwise """
        player_rect = self.get_bullet_drawables()[0]
        return self.background.collided_with(player_rect)

    def is_bullet_dead(self):
        """ Return True if the player is dead (for instance) the players
            has collided with an obstacle, and false otherwise """
        bullet_rect = self.bullet.get_drawables()[0]
        return self.background.collided_with(bullet_rect)

    def plane_update(self):
        """ Updates the model and its constituent parts """
        self.plane.update()

    def bullet_update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print len(self.bullets)
                    self.bullets.append(Bullet(self.plane.pos_x, self.plane.pos_y))
        for bullet in self.bullets:
            bullet.update()

class ScrollerView():
    def __init__(self, s_model, width, height):
        """ Initialize the view.  The input model is necessary to find 
            the position of relevant objects to draw. """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        # this is used for figuring out where to draw stuff
        self.game_model = s_model
        # self.bullet_model = b_model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        # get the new drawables
        self.drawables = self.game_model.get_plane_drawables() + self.game_model.get_bullet_drawables()
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
        # self.bullet_model = BulletModel(20, 20, self.game_model.bird)
        self.view = ScrollerView(self.game_model, 1280, 480)

    def run(self):
        """ the main runloop... loop until death """
        last_update_time = time.time()
        while not(self.game_model.is_player_dead()):
            self.game_model.plane_update()
            self.game_model.bullet_update()
            self.view.draw()
            last_update_time = time.time()
            pygame.display.update()

if __name__ == '__main__':
    Scroller = SideScroller()
    Scroller.run()

