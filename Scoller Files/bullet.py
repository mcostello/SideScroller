# python specific imports

# panda specific imports
import direct.directbase.DirectStart                                     
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.task import Task


# program specific imports
from config import *
from collisions import *

class BulletManager(DirectObject): 
    def __init__(self):
        # manage the creation and updating of all bullets with the enemy and player
        
        # start a count of how many bullets have been created so each is unique 
        self.count = 0
        
        # store a pointer to each bullet in a dict 
        self.bullets = {}
        
        # load all the textures needed only once
        self.bulletTexs = {"P_pulse" :  loader.loadTexture("Textures/player_pulse_bullet.tif"),
                           "P_plasma" : loader.loadTexture("Textures/player_plasma_bullet.tif"),
                           "E_pulse" : loader.loadTexture("Textures/enemy_pulse_bullet.tif"),
                           "E_plasma" : loader.loadTexture("Textures/enemy_plasma_bullet.tif"),
                           "E_mine" : loader.loadTexture("Textures/enemy_mine.tif") }
        
        # setup message accepts 
        self.accept('fire_bullet',self.createBullet)    # called from the enemy ships
        self.accept('destroy_bullet',self.destroyBullet)
        
        
############### Functions ####################################################
    
    def createBullet(self, who, type, pos):
        self.bullets["b"+who+str(self.count)] = Bullet("b"+who+str(self.count), who, type, pos, self.bulletTexs)
        self.count += 1 
        
    def destroyBullet(self, name):
        # destroy the instance with the given name
        self.bullets[name].destroyModels()
        self.bullets.pop(name)
        
        print "bullet destroyed", name
        
        
##############################################################################
##############################################################################



class Bullet(DirectObject): 
    def __init__(self, name, who, type, pos, bulletTexs): 
        # pos should be a Point3(x,y,z) 
        ## print "Making a bullet: ", name
        self.name = name
        self.who = who
        self.type = type
        self.bulletTexs = bulletTexs
        
        # create the model
        if self.type == "mine":
            self.model = loader.loadModel("Models/mine.egg")           # load the model
        else:
            self.model = loader.loadModel("Models/bullet.egg")           # load the model
        
        # assign textures based on type
        if who == "p":
            if self.type == "pulse":  
                self.model.setTexture(self.bulletTexs["P_pulse"], 1)
            elif self.type == "plasma":
                self.model.setTexture(self.bulletTexs["P_plasma"], 1)
            self.dir = 1        # move to the right
            
        else:   # who == "e"
            if self.type == "pulse":  
                self.model.setTexture(self.bulletTexs["E_pulse"], 1)
            elif self.type == "plasma":
                self.model.setTexture(self.bulletTexs["E_plasma"], 1)
            elif self.type == "mine":
                self.model.setTexture(self.bulletTexs["E_mine"], 1)
            elif self.type == "Bpulse":
                self.model.setTexture(self.bulletTexs["E_pulse"], 1)
                ## self.model.reparentTo(render)
            elif self.type == "Bplasma":
                self.model.setTexture(self.bulletTexs["E_plasma"], 1)
                ## self.model.reparentTo(render)
            self.dir = -1       # move to the left
                
        
        # Assign parents
        self.model.reparentTo(render)
            
        # position the bullet 
        self.model.setPos(pos)
        self.model.setScale(0.1)
        ## self.model.place()
            
        # create a collider 
        # create the collider
        self.bulletC = createColSphere(self.model, self.name+"C", 1, show = SHOW_C)
        ## setColMask(self.bulletC, -1, type = 'From', allOff = True )  # disallow this type
        setColMask(self.bulletC, 0, type = 'From' )
        setColMask(self.bulletC, 0, type = 'Into' )
        messenger.send('addCollider', [self.bulletC])
        
        # begin the update task
        taskMgr.add(self.update, self.name + '_updateTask')
    
############### Functions ####################################################
        
    def update(self, task):
        
        # move the bullet
        if self.type == "mine":
            self.model.setX(self.model.getX() + SCR_DIST *.25 *self.dir)        # moves slower
        elif self.type == "Bpulse" or self.type == "Bplasma":
            self.model.setZ(self.model.getZ() + SCR_DIST *.5 *1)
            ## self.model.setY(-.03)
            ## print "accepting new"
        else:
            ## self.model.setX(self.model.getX() + SCR_DIST *.75 *self.dir)        # moves faster than ships
             self.model.setX(self.model.getX() + SCR_DIST *.75 *self.dir)
        # should the bullet be destroyed 
        if self.model.getX() < E_X_MIN or self.model.getX() > E_X_MAX or self.model.getZ() > 8: 
            messenger.send('destroy_bullet', [self.name])
            return Task.done
        else:
            return Task.cont
        
    def destroyModels(self):
        ## print "Destroying a bullet!", self.name
        # remove the bullet  
        taskMgr.remove(self.name + '_updateTask')       # incase it is still running
        self.bulletC.removeNode()
        self.model.removeNode()
        
        
    
    

