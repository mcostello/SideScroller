""" A  basic Side-Scroller Shooting Game """

import random
from random import randint
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

    def update(self):
        """ checks for wasd keypresses, moves player """
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
        """ gets the drawables for the player """
        w,h = self.image.get_size()
        return [DrawableSurface(self.image, 
                                pygame.Rect(self.pos_x, self.pos_y, w, h))]

class Background(pygame.sprite.Sprite):
    """ Represents the background """
    def __init__(self,pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/background.png')
        self.image.set_colorkey((255,255,255))
        self.pos_x = pos_x
        self.height = 480

    def update(self):
        """ update the background to move at a constant rate"""
        self.pos_x -=1

    def get_drawables(self):
        """ Gets the drawables for the background """
        return DrawableSurface(self.image,
                                pygame.Rect((self.pos_x, self.height - 128), self.image.get_size()))

    def collided_with(self, entity):
        """ Returns True if the input drawable surface (entity) has
            collided with the ground """
        drawables = self.get_drawables()
        rectangles = []
        for d in drawables:
            rectangles.append(d.get_rect())
        return entity.get_rect().collidelist(rectangles) != -1

class Bullet(pygame.sprite.Sprite):
    """ represents the state of the bullets in the game """
    def __init__(self, bpos_x, bpos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.image.set_colorkey((255,255,255))
        self.bpos_x = bpos_x + 200
        self.bpos_y = bpos_y + 50
        
    def update(self):
        """ moves the bullet across the screen """
        self.bpos_x += 3

    def get_drawables(self):
        """ returns the drawable sprites for the bullet list """
        return DrawableSurface(self.image, pygame.Rect((self.bpos_x, self.bpos_y), self.image.get_size()))

    def collided_with(self, entity):
        """ Returns True if the input drawable surface (entity) has
            collided with the another surface """
        drawables = self.get_drawables()
        rectangles = []
        for d in drawables:
            rectangles.append(d.get_rect())
        return entity.get_rect().collidelist(rectangles) != -1

class Enemy(pygame.sprite.Sprite):
    """ represents the state of the player in the game """
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/biplane_grey.png')
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self):
        """ move the enemy plane across the screen """
        pygame.event.pump()
        self.pos_x -= 1.5        

    def get_drawables(self):
        """ gets the drawables for each enemy in the list """
        w,h = self.image.get_size()
        return DrawableSurface(self.image, 
                                pygame.Rect(self.pos_x, self.pos_y, w, h))

    def collided_with(self, entity):
        """ Returns True if the input drawable surface (entity) has
            collided with the ground """
        d_rect = self.get_drawables().get_rect()
        return entity.colliderect(d_rect)

    def is_dead(self, bullet_list):
        """ checks for collisions between enemies and bullets """
        enemy_rect = self.get_drawables().get_rect()
        bullet_rects = [bullet.get_drawables().get_rect() for bullet in bullet_list]
        for bullet in bullet_rects:
            if enemy_rect.collidelist([bullet]) == 0 and len(bullet_list)>0:
                return ((enemy_rect.collidelist(bullet_rects) != -1),bullet)
        
class ScrollerModel():
    """ Represents the game state of the scroller """
    def __init__(self, width, height):
        """ Initialize the plane model """
        self.width = width
        self.height = height
        self.plane = Plane(0,200)
        self.background = [Background(0),Background(1024),Background(2048)]
        self.bullets = []
        self.enemies = [Enemy(1080, randint(100,356))]

    def update(self):
        """ updates all aspects of the game """
        events = pygame.event.get()
        self.plane_update()
        self.bullet_update(events)
        self.background_update()
        self.enemy_update(events)

    def get_plane_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        return self.plane.get_drawables()

    def get_bullet_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        return [bullet.get_drawables() for bullet in self.bullets]

    def get_enemy_drawables(self):
        """ gets a list of all enemy drawables"""
        return [enemy.get_drawables() for enemy in self.enemies]

    def get_background_drawables(self):
        """ gets a list of all enemy drawables"""
        return [background.get_drawables() for background in self.background]

    def is_player_dead(self):
        """ Return True if the player is dead (having collided with an enemy)
        and false otherwise """
        player_rect = self.plane.get_drawables()[0].get_rect()
        for enemy in self.enemies:
            if enemy.collided_with(player_rect):
                return True

    def is_bullet_dead(self):
        """ Return True if the bullet is dead (having collided with a wall
            or plane) and false otherwise """
        bullet_rect = self.bullets.get_drawables()[0].get_rect()
        return self.enemies.collided_with(bullet_rect)

    def is_enemy_dead(self):
        """ Return True if an enemy in list self.enemies is dead
            (having collided with a bullet) and false otherwise """
        enemy_rect = self.enemy.get_drawables()[0]
        return self.enemy.collided_with(player_rect)

    def plane_update(self):
        """ Updates the plane and its constituent parts """
        self.plane.update()

    def enemy_update(self, events):
        """ Updates and checks for death for each enemy in self.enemies """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    self.enemies.append(Enemy(1080, randint(0,256)))
        for enemy in self.enemies:
            enemy.update()
            if enemy.pos_x < 0:
                self.enemies = self.enemies[1:]
            elif enemy.is_dead(self.bullets):
                self.enemies = self.enemies[1:]
            if len(self.enemies) == 0:
                self.enemies.append(Enemy(1280, randint(100,356)))

    def bullet_update(self, events):
        """checks for creation of a bullet. If bullet created, add bullet to
        a list of bullets"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(self.plane.pos_x, self.plane.pos_y))
        for bullet in self.bullets:
            bullet.update()
        if len(self.bullets) > 0 and self.bullets[0].bpos_x > 1280:
            self.bullets = self.bullets[1:]

    def background_update(self):
        """Updates the background"""
        for background in self.background:
            background.update()
            if background.pos_x < -1023:
                self.background = self.background[1:]
                self.background.append(Background(2048))

class ScrollerView():
    def __init__(self, g_model, width, height):
        """ Initialize the view. The input model is necessary to find 
            the position of relevant objects to draw. """
        pygame.init()
        #determine where to draw
        self.screen = pygame.display.set_mode((width, height))
        self.game_model = g_model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        # get the new drawables
        self.drawables = (self.game_model.get_background_drawables()
                        + self.game_model.get_plane_drawables()
                        + self.game_model.get_bullet_drawables()
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
            self.game_model.update()
            self.view.draw()
            last_update_time = time.time()
            pygame.display.update()

if __name__ == '__main__':
    Scroller = SideScroller()
    Scroller.run()

