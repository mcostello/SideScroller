# python specific imports
from random import randint
from random import randrange

# panda specific imports
import direct.directbase.DirectStart                                     
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *


# program specific imports
from config import *
from textureSwap import *
from textureSwap import *
from collisions import *

class EnemyManager(DirectObject): 
    def __init__(self):
        # manage the creation and updating of all enemy ships
        ## self.e = Enemy()
        ## self.e.down = False
        # start a count of how many enemies have been created so each is unique 
        self.count = 0
        
        # store a pointer to each enemy in a dict 
        self.enemies = {}
        
        # load all the textures needed only once
        EngineSTex = []
        EngineRTex = []
        for i in range(1,5):
                EngineSTex.append(loader.loadTexture("Textures/enemy_scout_engine" + str(i).zfill(0) + ".tif"))
                EngineRTex.append(loader.loadTexture("Textures/enemy_raider_engine" + str(i).zfill(0) + ".tif"))
        self.enemyTexs = {"S_engine" :  EngineSTex, "R_engine" :  EngineRTex,
                          "S_mine" : loader.loadTexture("Textures/enemy_scout_mine_scoop.tif"),
                          "S_pulse" : loader.loadTexture("Textures/enemy_scout_pulse_lower.tif"),
                          "S_plasma" : loader.loadTexture("Textures/enemy_scout_plasma.tif"),
                          "R_ship" : loader.loadTexture("Textures/enemy_raider.tif"), 
                          "R_pulseL" : loader.loadTexture("Textures/enemy_raider_pulse_lower.tif"),
                          "R_pulseT" : loader.loadTexture("Textures/enemy_raider_pulse_top.tif"),
                          "R_plasmaL" : loader.loadTexture("Textures/enemy_raider_plasma_lower.tif"),
                          "R_plasmaT" : loader.loadTexture("Textures/enemy_raider_plasma_top.tif") }
        
        # setup message accepts 
        self.accept('destroy_enemy',self.destroyShip)
        
        taskMgr.doMethodLater(E_SPAWN, self.spawnShip, "spawnEnemyShip")
        
        
############### Functions ####################################################
        
    def spawnShip(self, task):
        self.createShip()
        ## self.destroyShip()
        return Task.again
    
    def createShip(self):
        # what type of ship to create
        ship_types = ["scout", "raider"]
        type = ship_types[randint(0,1)]
        # what kind of weapons will it have 
        weapons = ["mine", "pulse", "plasma"]
        weaponT = None
        if type == "scout":
            weaponL = weapons[randint(0,2)]
        else:
            weaponL = weapons[randint(1,2)]     # raiders don't have mine scoops 
            weaponT = weapons[randint(1,2)]     # raiders don't have mine scoops 
        self.enemies["e"+str(self.count)] = Enemy("e"+str(self.count), type, weaponL, weaponT, self.enemyTexs)
        self.count += 1 
        
    def destroyShip(self, name):
        # destroy the instance with the given name
        self.enemies[name].destroyModels()
        self.enemies.pop(name)
        ## print "enemy destroyed", name
    def eBaseWeapons(self):
        weaponL = "Bpulse"
        weaponT = "Bplasma"
        
        
##############################################################################
##############################################################################



class Enemy(DirectObject): 
    def __init__(self, name, type, weaponL, weaponT, enemyTexs, pos = None): 
        # if pos is supplied then it should be a Point3(x,y,z) 
        ## self.down = False
        
        self.name = name
        self.type = type
        self.weaponL_type = weaponL
        self.weaponT_type = weaponT
        self.enemyTexs = enemyTexs
        
        # create the model
        self.model = loader.loadModel("Models/enemy_ship.egg")           # load the model
        self.engines = loader.loadModel("Models/enemy_ship.egg")         # load the model
        self.weaponL = loader.loadModel("Models/enemy_ship.egg")         # load the model
        
        # assign textures based on type
        if self.type == "scout":  
            playTexture(self.engines, self.enemyTexs["S_engine"], 1, ANI_SPEED, self.name + "_engine_" + "tex") # update engine texture    
            if self.weaponL_type == "mine":
                self.weaponL.setTexture(self.enemyTexs["S_mine"], 1)
            elif self.weaponL_type == "pulse":
                self.weaponL.setTexture(self.enemyTexs["S_pulse"], 1)
            elif self.weaponL_type == "plasma":
                self.weaponL.setTexture(self.enemyTexs["S_plasma"], 1)
            
        else:   # self.type == "raider"
            self.model.setTexture(self.enemyTexs["R_ship"],1)  # load the raider texture
            playTexture(self.engines, self.enemyTexs["R_engine"], 1, ANI_SPEED, self.name + "_engine_" + "tex") # update engine texture
            if self.weaponL_type == "pulse":
                self.weaponL.setTexture(self.enemyTexs["R_pulseL"], 1)
            elif self.weaponL_type == "plasma":
                self.weaponL.setTexture(self.enemyTexs["R_plasmaL"], 1)
            self.weaponT = loader.loadModel("Models/enemy_ship.egg")         # load the model
            if self.weaponT_type == "pulse":
                self.weaponT.setTexture(self.enemyTexs["R_pulseT"], 1)
            elif self.weaponT_type == "plasma":
                self.weaponT.setTexture(self.enemyTexs["R_plasmaT"], 1)
                
        
        # Assign parents
        self.model.reparentTo(render)
        self.engines.reparentTo(self.model)
        self.weaponL.reparentTo(self.model)
        if self.type == "raider":
            self.weaponT.reparentTo(self.model)
            
        # position the ship off the right side of the screen
        if pos != None:
            self.model.setPos(pos)
        else: 
            self.model.setPos(ESPAWN_X,-.1,randrange(E_Z_MIN, E_Z_MAX)*.1)
        self.model.setScale(0.1)
        ## self.model.place()
        self.engines.setY(.01)
        self.weaponL.setY(-.01)
        if self.type == "raider":
            self.weaponT.setY(-.01)
            
        # create a collider 
        # create the player collider
        if self.type == "scout":
            self.enemyC = createColSphere(self.model, self.name+"C", 3, show = SHOW_C)
        else: 
            self.enemyC = createColSphere(self.model, self.name+"C", 4, show = SHOW_C)
        setColMask(self.enemyC, -1, type = 'From', allOff = True )  # disallow this type
        setColMask(self.enemyC, 0, type = 'Into' )
        messenger.send('addCollider', [self.enemyC])
        
        # begin the update task
        taskMgr.add(self.update, self.name + '_updateTask')
        # fire weapons
        taskMgr.doMethodLater(EFIRE_DELAY, self.fire, self.name + '_fireTask')
        taskMgr.doMethodLater(.00000000000000001, self.moveShip, "moveShip")
        
############### Functions ####################################################
    ## def move(self, task):
        ## move_types = ["up", "down", "stay"]
        ## move = move_types[randint(0,2)]
        ## if (self.model.getZ() + SCR_DIST *.5 < MAX_VH and move == 1):
            ## self.model.setZ(self.model.getZ() + SCR_DIST*.55)
            ## print "going up"
            ## self.goingUp = True
        
        ## elif (self.model.getZ() - SCR_DIST *.5 > MIN_VH and move == 2):
            ## self.model.setZ(self.model.getZ() - SCR_DIST*.55)
            ## print "going down"
            ## self.goingDown = True
    ## Task.again()
    
    def moveShip(self, task):
        s = Sequence(LerpPosInterval(self.model, 1, self.model.getPos() + Point3(-4,0,1)), Wait(.01), LerpPosInterval(self.model, 1, self.model.getPos() + Point3(-8,0,-.5)), Wait(.01), LerpPosInterval(self.model, 1, self.model.getPos() + Point3(-15,0,1))).start()
    
    def update(self, task):
        
        # move the ship
        self.model.setX(self.model.getX() - SCR_DIST *.5)
        ## self.move()
        ## if (DOWN != 2 and not self.model.getZ() + SCR_DIST *.5 >= MAX_VH):
            ## self.model.setZ(self.model.getZ() + SCR_DIST *.55)
            ## print "up"
        ## elif self.model.getZ() + SCR_DIST *.5 > MAX_VH:
            ## self.model.setZ(self.model.getZ() - SCR_DIST *.55)
            ## DOWN = 2
            ## print "down"
        ## elif self.model.getZ() + SCR_DIST *.5 < MIN_VH and self.down == False:
            ## self.down = False
        ## move_types = ["up", "down", "stay"]
        ## move = move_types[randint(0,2)]
        ## if (self.model.getZ() + SCR_DIST *.5 < MAX_VH and move == 1):
            ## self.model.setZ(self.model.getZ() + SCR_DIST*.55)
            ## print "going up"
            ## self.goingUp = True
        
        ## elif (self.model.getZ() - SCR_DIST *.5 > MIN_VH and move == 2):
            ## self.model.setZ(self.model.getZ() - SCR_DIST*.55)
            ## print "going down"
            ## self.goingDown = True
            
        ## if (self.model.getZ > 1):
            ## self.model.setZ(self.model.getZ() +.05)
            ## print "going up"
        ## if self.model.getZ < 10:
            ## self.model.setZ(self.model.getZ() -.05)
            ## print "going down"
        # should the ship be destroyed 
        if self.model.getX() < E_X_MIN: 
            messenger.send('destroy_enemy', [self.name])
            return Task.done
        else:
            return Task.cont
        
    def fire(self, task):
        
        if self.type == "scout":
            if self.weaponL_type == "mine":
                messenger.send('fire_bullet', [ "e", "mine", self.model.getPos() + ESBMINE_SPAWN ])
            elif self.weaponL_type == "pulse":
                messenger.send('fire_bullet', [ "e", "pulse", self.model.getPos() + ESBPULSE_SPAWN ])
            elif self.weaponL_type == "plasma":
                messenger.send('fire_bullet', [ "e", "plasma", self.model.getPos() + ESBPLASMA_SPAWN ])
        else: # raider
            if self.weaponL_type == "pulse":
                messenger.send('fire_bullet', [ "e", "pulse", self.model.getPos() + ERBLPULSE_SPAWN ])
            elif self.weaponL_type == "plasma":
                messenger.send('fire_bullet', [ "e", "plasma", self.model.getPos() + ERBLPLASMA_SPAWN ])
            if self.weaponT_type == "pulse":
                messenger.send('fire_bullet', [ "e", "pulse", self.model.getPos() + ERBTPULSE_SPAWN ])
            elif self.weaponT_type == "plasma":
                messenger.send('fire_bullet', [ "e", "plasma", self.model.getPos() + ERBTPLASMA_SPAWN ])
            
        return Task.again
        
    def destroyModels(self):
        # remove the ship and all of its parts 
        taskMgr.remove(self.name + '_updateTask')       # incase it is still running
        taskMgr.remove(self.name + '_fireTask')         # incase it is still running
        if self.type == "raider":
            self.weaponT.removeNode()
        self.weaponL.removeNode()
        stopTexture(self.name + "_engine_" + "tex")
        self.engines.removeNode()
        self.enemyC.removeNode()
        self.model.removeNode()
        

    
    

