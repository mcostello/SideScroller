# setup the window
from pandac.PandaModules import loadPrcFileData
from config import *
loadPrcFileData("", ORIGIN)
loadPrcFileData("", SIZE) 
loadPrcFileData("", TITLE)

# python specific imports
import sys
from random import randint

# panda specific imports
import direct.directbase.DirectStart                                     
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.gui.DirectGui import *


# program specific imports
from textureSwap import *
from enemy import *
from collisions import *
from bullet import *


class World(DirectObject): 
    def __init__(self): 
        
        # set up the camera
        base.disableMouse()
        base.camera.setPos(0, -14.4, 0)
        base.camLens.setFar(10000)
        base.setBackgroundColor( .5, .5, .5 )
        
        # Extra code in case you want to see the whole thing from a 
        # different angle to visualize how it's all done easier.
        ## base.camera.place()
        ## base.camera.setPosHpr(-19,-9,0,290,0,0)
       
         ## create a start screen
        self.startScreen = loader.loadModel("Models/startScreen.egg")         # load the model
        self.startScreen.reparentTo(render)                             # link to render so the camera sees it
        self.startScreen.setScale(0.1)                             # size it
        # place a texture on the startScreen   
        startScreenTex = loader.loadTexture("Textures/start_screen.jpg")       # load the texture
        self.startScreen.setTexture(startScreenTex, 1)                  # assign the texture
        self.endScreenTex = loader.loadTexture("Textures/end_screen.jpg")       # load the texture - while we are here
        
        # set up accepts    
        self.accept('escape', self.quit)
        self.accept('space', self.clickToContinue)
        
    
############### Functions ####################################################
    ## def startGame(self, reset):
    #moves the screen along to the instructions page
    def clickToContinue(self):
        self.startScreenTex2 = loader.loadTexture("Textures/instruction_page2EDIT.jpg")
        self.startScreen.setTexture(self.startScreenTex2, 1)
        self.accept('space', self.startGame)
    #starts the game
    def startGame(self):
        # start the game - 
        self.startScreen.hide()                 # hide the start screen - use it later
        self.ignore('space')                    # stop accepting keyboard clicks
        self.createEnviro()                     # Create the environment
        self.mountains = []
        self.enemiesRemaining = 50
        self.basePresent = False
        self.firing = False
        self.shipsCollide = False
        # setup keyboard control
        # WASD Movement, K AND L fire weapons
        self.keys = {'w':False, 'a':False, 's':False, 'd':False, 'k':False, 'l':False}
        ## self.accept('q-up', self.returnHealth)
        #make the final score text for later
        self.scoreFinal = OnscreenText(text="You Scored " + str(self.score) + " Points", 
                                       style=1, fg=(1,.7,0,1), pos=(0,0,0), scale = .1)
        self.scoreFinal.hide()
        self.score = 0
        #set up the goal to end the game via text with enemies remaining
        self.enemiesText = OnscreenText(text="Enemies Remaining: " + str(self.enemiesRemaining), 
                                       style=1, fg=(1,.7,0,1), pos=(0,.77,0), scale = .085)
        ## self.enemiesText.show()
        #set up the score
        self.scoreText = OnscreenText(text= str(self.score), style=1, fg=(1,1,1,1), pos=(.60,.85,0), scale = .07)
        #set up all three lives
        self.l = loader.loadModel("Models/player_ship" + ".egg")# load the model
        self.l.reparentTo(render)                    #Reparent to render    
        self.l.setScale(0.05)                        #Adjust scale
        self.l.setPos(-3.9,-.2,3.2)
        
        self.l2 = loader.loadModel("Models/player_ship" + ".egg")# load the model
        self.l2.reparentTo(render)                    #Reparent to render    
        self.l2.setScale(0.05)                        #Adjust scale
        self.l2.setPos(-3.45,-.2,3.2)
        
        self.l3 = loader.loadModel("Models/player_ship" + ".egg")# load the model
        self.l3.reparentTo(render)                    #Reparent to render    
        self.l3.setScale(0.05)                        #Adjust scale
        self.l3.setPos(-3.0,-.2,3.2)
        #set them all to true for later diferentiation
        self.life1 = True
        self.life2 = True
        self.life3 = True
        
        #initialize the shield, plasma, and pulse amounts
        self.pShield = 100
        self.pPlasma = 100
        self.pPulse = 100
       #get the keys ready
        def onKey(key, pressed): 
                self.keys[key] = pressed 
                
        self.accept('w', onKey, ['w', True])
        self.accept('a', onKey, ['a', True])
        self.accept('s', onKey, ['s', True])
        self.accept('d', onKey, ['d', True])
        self.accept('k', onKey, ['k', True])
        self.accept('l', onKey, ['l', True])
        self.accept('w-up', onKey, ['w', False])
        self.accept('a-up', onKey, ['a', False])
        self.accept('s-up', onKey, ['s', False])
        self.accept('d-up', onKey, ['d', False])
        self.accept('k-up', onKey, ['k', False])
        self.accept('l-up', onKey, ['l', False])
        
        # setup collisions - 
        # create the traverser and handler 
        base.cTrav = CollisionTraverser()               
        if SHOW_C: base.cTrav.showCollisions(render)                          
        self.CollisionHandler = CollisionHandlerEvent()
        self.CollisionHandler.addInPattern('HitAnything')
        self.CollisionHandler.addAgainPattern('HitAnything')
        #add the player collider to the traverser 
        base.cTrav.addCollider(self.playerC, self.CollisionHandler)
        # setup collision accepts
        self.accept('HitAnything', self.hitSomething)
        self.accept("addCollider", self.addCollider)
        
        # begin the update task
        taskMgr.add(self.update, 'updateTask')
        
        
        # SEE BULLET AND ENEMY files
            # start the enemy manager
            # start the bullet manager
        self.BManager = BulletManager()
        
        self.EManager = EnemyManager()
        
        ## self.EManager.destroyShip()
        ## self.BManager.destroyBullet()        # fire delay to prevent streams of bullets
        #make it so the player can start of able to fire
        self.canFire = True
        ## self.resetCanFire()
        
        #set up the task manager
        taskMgr.doMethodLater(MNT_DELAY, self.createMountain, "createMountain")
        
        taskMgr.doMethodLater(.01, self.scrollMountains, "scrollMountain")
        
        taskMgr.doMethodLater(.01, self.scrollBackDrop1, "scrollBackDrop1")
        
        taskMgr.doMethodLater(.01, self.scrollBackDrop2, "scrollBackDrop2")
        
        taskMgr.doMethodLater(1.2, self.regenPlasma, "regneratePlasma")
        
        taskMgr.doMethodLater(1.2, self.regenPulse, "regeneratePulse")
        
        ## taskMgr.doMethodLater(.5, self.eBaseFire, "eBaseFire")
        
        
        ## taskMgr.doMethodLater(.1, self.makeEBase, "makeEBase")
        
    
     #gets the player position   
    def getPPos(self):
        return self.player.getPos()
     
    #updates all tasks    
    def update(self, task):
        self.scoreText["text"] = str(self.score)
        self.enemiesText["text"] = "Enemies Remaining: " + str(self.enemiesRemaining)
        # check for player verticle movement 
        # check for player horizontal movement
        if (self.keys['w'] and self.player.getZ() + SCR_DIST *.5 < MAX_VH):
            self.player.setZ(self.player.getZ() + SCR_DIST*.55)
        if (self.keys['s'] and self.player.getZ() - SCR_DIST *.5 > MIN_VH):
            self.player.setZ(self.player.getZ() - SCR_DIST*.55)
        if (self.keys['a'] and self.player.getX() - SCR_DIST *.5 > MIN_HW):
            self.player.setX(self.player.getX() - SCR_DIST*.55)
        if (self.keys['d'] and self.player.getX() + SCR_DIST *.5 < MAX_HW):
            self.player.setX(self.player.getX() + SCR_DIST*.55)
        # fire control
        if self.keys['k'] and self.canFire == True and self.pPulse != 0:
            self.canFire = False
            ## self.createBullet = createBullet()
            ## self.createBullet(self.player, "pulse", self.getPPos())
            self.BManager.createBullet("p", "pulse", self.player.getPos() + PBPULSE_SPAWN)
            

            # fire a pulse blast    
            print "Fired Pulse!"
            self.pPulse -= 5
            self.f2 = Func(self.resetCanFire)
            s = Sequence(Wait(0.35), self.f2).start()
            ## self.resetCanFire()
        if self.keys['l'] and self.canFire == True and self.pPlasma != 0:
            self.canFire = False
            ## self.createBullet(self.player, "plasma", self.getPPos())
            # fire a plasma blast     
            print "Fired Plasma!"
            self.pPlasma -= 5
            self.BManager.createBullet("p", "plasma", self.player.getPos() + PBPLASMA_SPAWN)
            self.f2 = Func(self.resetCanFire)
            s = Sequence(Wait(0.35), self.f2).start()
            ## self.resetCanFire()

        # update the ui
        self.healthBar["value"] = self.pHealth
        if self.pHealth > MAXH*.25:
            self.healthBar["barColor"] = Vec4(0,1,0,1)
        else : 
            self.healthBar["barColor"] = Vec4(1,0,0,1)  # danger - low health
        
        
        #removes lives    
        if self.pHealth <= 0 and self.lives != 0 and self.life1 == True:
            self.life1 = False
            self.l3.hide()
            self.lives = 2
            self.resetPlayer()
            print "lost life 1"
        elif self.pHealth <= 0 and self.lives != 0 and self.life1 == False and self.life2 == True:
            self.life2 = False
            self.l2.hide()
            self.lives = 1
            self.resetPlayer()
            print "lost life 2"
        elif self.pHealth <= 0 and self.lives != 0 and self.life1 == False and self.life2 == False and self.life3 == True:
            self.life3 = False
            self.l.hide()
            self.lives = 0
            print "lost life 3"
            self.gameOver()
        ## self.energyBar["value"] = self.pEnergy
        ## self.scoreTitle["text"] = str(self.score)
        ## for i in range(NUM_LIVES):
            ## if i < self.lives:
                ## self.livesMods[i].show()
            ## else:
                ## self.livesMods[i].hide()
       #more shield setup
        self.shieldBar["value"] = self.pShield
        if self.pShield <= 0:
            self.shieldMod.hide()
        #ends the game when objective completed
        if self.enemiesRemaining <= 0:
            self.gameOver()
        
        #initializes bars
        self.pulseBar["value"] = self.pPulse
        self.plasmaBar["value"] = self.pPlasma
        ## self.enemiesText = OnscreenText(text="Enemies Remaining: " + str(self.enemiesRemaining), 
                                       ## style=1, fg=(1,.7,0,1), pos=(0,0,1), scale = .1)
        ## self.enemiesText["text"] = str(self.enemiesRemaining)
        #Continue the task so it will update continuously
        return Task.cont
    #this was an attempt at fixing the collision glitch where when a bullet was colliding with an enemy at the same time as the player,
    #the game would try to remove the enemy twice, resulting in a crash. i could
    #not find a working method of fixing this.
    def pHitE(self):
        self.EManager.destroyShip(self.Coll3)
    def pbHitsE(self):
        self.EManager.destroyShip(self.Coll2)
    
    def resetShipsCollide(self):
        self.shipsCollide = False
    #sets all collisions
    def hitSomething(self, collEntry):
        ## print "COLLSION", collEntry.getFromNode().getName(), collEntry.getIntoNode().getName()
        ## if (collEntry.getFromNode().getName() == 'pC') and ("mountain" in collEntry.getIntoNode().getName()):
            ## self.pHealth -= 1
        #If player hits mountain
            # hit a mountain - damage the player
        if (collEntry.getFromNode().getName()[0] == 'p') and ("m" in collEntry.getIntoNode().getName()[0]):
            self.pShield -= 1
            self.pHealth -= 1   
            print "hit mountain" 
        #elif player and enemy ships hit each other
            # hit an enemy ship - damage the player, destroy the enemy
            #working
        if (collEntry.getIntoNode().getName()[0] == 'e') and (collEntry.getFromNode().getName()[0] == 'p') and not ((collEntry.getFromNode().getName()[1] == "p") and ("e" in collEntry.getIntoNode().getName()[0])):
            ## self.Coll3 = collEntry.getIntoNode().getName().strip("C")
            ## a = Sequence(Wait(.00001), Func(self.pHitE)).start()
            self.EManager.destroyShip(collEntry.getIntoNode().getName().strip("C"))
            self.enemiesRemaining -= 1
            if self.pShield <= 0:
                self.pHealth -= 10
            else:
                self.pShield -= 20
            print "ships collide" 
            self.shipsCollide = True
            s = Sequence(Wait(.01), Func(self.resetShipsCollide)).start()
             #fix idea: self.shipsCollide = True, s = Sequence(Wait(.01), Func(self.resetShipsCollide)).start(), if self.shipsCollide != True:
        #elif player_bullet hits the enemy ship
            # player bullet hits an enemy ship - destroy the enemy, destroy the bullet, gain score
            #working
           
        if (collEntry.getFromNode().getName()[1] == "p") and ("e" in collEntry.getIntoNode().getName()[0]) and not ((collEntry.getIntoNode().getName()[0] == 'e') and (collEntry.getFromNode().getName()[0] == 'p')) and (self.shipsCollide != True):
            ## Coll1 = collEntry.getFromNode().getName().strip("C")
            ## self.Coll2 = collEntry.getIntoNode().getName().strip("C")
            self.EManager.destroyShip(collEntry.getIntoNode().getName().strip("C"))
            ## s = Sequence(Wait(.000000001), Func(self.pbHitsE)).start()
            self.BManager.destroyBullet(collEntry.getFromNode().getName().strip("C"))
            self.score += 10
            self.enemiesRemaining -= 1
            print "enemy hit"
        #elif player bullet hits a mountain just destroy the bullet
            # player bullet hits a mountain - destroy the bullet 
            #working
        if (collEntry.getFromNode().getName()[1] == 'p') and ("m" in collEntry.getIntoNode().getName()):
            self.BManager.destroyBullet(collEntry.getFromNode().getName().strip("C"))
            print "pbullet hit mountain"
        #elif player ship is hit by an enemy bullet
            # enemy bullet hit player ship - damage the player, destroy the bullet
            #working
        if (collEntry.getIntoNode().getName() == 'pC') and ("be" in collEntry.getFromNode().getName()):
            self.BManager.destroyBullet(collEntry.getFromNode().getName().strip("C"))
            if self.pShield <= 0:
                self.pHealth -= 5
            else:
                self.pShield -= 10
            print "player hit"
        #elif player bullet hits an enemy bullet
            # player bullet hits enemy bullet - destroy both bullet
            #working
        if ('p' in collEntry.getIntoNode().getName()[1]) and ("e" in collEntry.getFromNode().getName()[1]):
            ## self.Coll4 = collEntry.getIntoNode().getName().strip("C")
            ## b = Sequence(Wait(.001), Func(self.pbHitEb)).start()
            self.BManager.destroyBullet(collEntry.getIntoNode().getName().strip("C"))
            self.BManager.destroyBullet(collEntry.getFromNode().getName().strip("C"))
            print "inair bullet collision"
            ## self.Coll5 = collEntry.getFromNode().getName().strip("C")
            ## c = Sequence(Wait(.01), Func(self.ebHitPb)).start()
            ## ## self.BManager.destroyBullet(collEntry.getIntoNode().getName().strip("C"))
            ## self.BManager.destroyBullet(collEntry.getFromNode().getName().strip("C"))
            ## print "inair bullet collision"
    # This will be useful for when we need to create new enemies and bullets
    # Adding them to the traverser and handler will let them interact
    # with the player
    def pbHitEb(self):
        self.BManager.destroyBullet(self.Coll4)
    
    def addCollider(self, col):
        # add the provided collider to the collision handler
        base.cTrav.addCollider(col, self.CollisionHandler)
        
    def createEnviro(self):
        self.m = loader.loadModel("Models/mountain1.egg")
        # load the back drops
            # load the model
            # shift all but the first to the right
        
        # start the back drops scrolling left
            #USE A TASK to run self.scroll backdrop
            
        # load in the mountains  
        ## self.mountains = []
        ## m = loader.loadModel("Models/mountain1.egg")         # create one to get all the info from
        ## m.reparentTo(render)
        ## m.setScale(0.1)
        ## m.place()
        #Tasks to create mountains
        #and then to scroll them, just like backdrop
        self.backDrop1 = loader.loadModel("Models/backDrop.egg")
        self.backDrop1.reparentTo(render)
        self.backDrop1.setScale(.1)
        
        self.backDrop2 = loader.loadModel("Models/backDrop.egg")
        self.backDrop2.reparentTo(render)
        self.backDrop2.setScale(.1)
        self.backDrop2.setX(20)
        # create the player ship
        self.player = loader.loadModel("Models/player_ship.egg")         # load the model
        self.player.reparentTo(render)                 #Parent to render
        self.player.setScale(0.1)                      #Set scale
        self.lives = NUM_LIVES                         #Set lives
        self.score = 0                                 #Score set to 0
         
                                    #Reset the player pos
        ## self.player.place()
        
        # create the player assessories 
        self.playerEngines = loader.loadModel("Models/player_ship.egg")         # load the model
        self.playerEngines.reparentTo(self.player)
        self.playerEngines.setY(-.01)
        self.pEngineTex = []
        for i in range(1,5):
            self.pEngineTex.append(loader.loadTexture("Textures/player_engine" + str(i).zfill(0) + ".tif"))
        playTexture(self.playerEngines, self.pEngineTex, 1, ANI_SPEED, self.playerEngines.getName() + "tex")
        
        #more shield related mods
        self.shieldMod = loader.loadModel("Models/player_ship.egg")
        self.shieldMod.reparentTo(self.player)
        self.shieldMod.setY(-.01)
        self.shieldTex1 = loader.loadTexture("Textures/player_shield.tif")
        self.shieldMod.setTexture(self.shieldTex1, 1)
        self.resetPlayer()
        
        
        
        
        # load and setup the UI
        self.ui = loader.loadModel("Models/ui.egg")
        self.ui.reparentTo(render)
        self.ui.setPos(0,-.1,3.3)
        self.ui.setScale(.1)
            # load the model
            # reparent to render
            # set the scale to .1
            # adjust position and rotation 
        
        
        # Set up health/ shield/ pulse/ plasma/ score title/ life models
        self.healthBar  = DirectWaitBar(text = "", value = MAXH, pos = (-.85,0,.93), scale = .2,  range = MAXH, barColor = Vec4(0,1,0,1))
        self.shieldBar  = DirectWaitBar(text = "", value = MAXH, pos = (1.2,0,.94), scale = .1,  range = MAXH, barColor = Vec4(0,0,1,1))
        self.pulseBar  = DirectWaitBar(text = "", value = MAXH, pos = (1.2,0,.88), scale = .1,  range = MAXH, barColor = Vec4(1,0,0,1))
        self.plasmaBar  = DirectWaitBar(text = "", value = MAXH, pos = (1.2,0,.82), scale = .1,  range = MAXH, barColor = Vec4(.5,0,1,1))
        ## self.healthBar["value"] = self.pHealth
        ## if self.pHealth > MAXH*.25:
            ## self.healthBar["barColor"] = Vec4(0,1,0,1)
        ## else : 
            ## self.healthBar["barColor"] = Vec4(1,0,0,1)  # danger - low health
        ## self.energyBar["value"] = self.pEnergy
        ## self.scoreTitle["text"] = str(self.score)
        ## for i in range(NUM_LIVES):
            ## if i < self.lives:
                ## self.livesMods[i].show()
            ## else:
                ## self.livesMods[i].hide() 
                
        

        # create the player collider
        self.playerC = createColSphere(self.player, "pC", 3, show = SHOW_C)
        setColMask(self.playerC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.playerC, 0, type = 'Into' )
        return Task.cont
     #makes enemy bases appear 33 1/3 percent of the time when the 3rd mountain type spawns   
    #this is the function I used to rise to your challenge of making a base.
    #I hope it is to your satisfaction.
    def makeEBase(self):
        if (self.r == 2):
            r = randint(0,2)
            if r == 1:
                #purpose of this if statement is to prevent a recurring error during endgame due to trying to remove an already
                #removed task from the manager.
                if self.enemiesRemaining >= 10:
                    self.eBase = loader.loadModel("Models/mountain3.egg")
                    self.eBase.reparentTo(self.m2)
                    self.eBase.setY(-.02)
                    self.eBase.setZ(-6.5)
                    self.eBase.setX(-7)
                    self.eBase.setScale(.1)
                    self.eBaseTex = loader.loadTexture("Textures/bases2.tif")
                    self.eBase.setTexture(self.eBaseTex, 1)
                    print "making a base"
                    ## self.basePresent = True
                    ## ## self.eBaseFire()
                    taskMgr.doMethodLater(1.2, self.eBaseFire, "eBaseFire")
                    s = Sequence(Wait(2), Func(self.eBaseCanFire)).start()
    #the actual firing mechanism for the base.
    def eBaseFire(self, task):
        self.BManager.createBullet("e", "Bpulse", self.m2.getPos() + Point3(-.1,0,-.8))
        # fire a pulse blast    
        ## print "Fired Enemy Pulse!"

        # fire a plasma blast     
        ## print "Fired Enemy Plasma!"
        self.BManager.createBullet("e", "Bplasma", self.m2.getPos() + Point3(-.05,0,.8))
        return Task.again
    #used to regulate firing capacity
    def eBaseCanFire(self):
        self.firing = True
        ## if self.enemiesRemaining <= 0:
            ## self.gameOver()
   #scrolls the backdrop
    def scrollBackDrop1(self,task):
        ## print "Scrolling Backdrop"
        ## i = 0
        ## while i <= 2:
        self.backDrop1.setX(self.backDrop1.getX() - SCR_SPEED)
        if self.backDrop1.getX() <= -20:
                self.backDrop1.setX(20)
        # move the back drops to the left 
            #If the backdrop moves far enough to the left,
            # flip back to the right so it looks like it
            # is continuously scrolling
        #Rerun task
        return Task.again
    def scrollBackDrop2(self,task):
        ## print "scrolling second mountains"
        self.backDrop2.setX(self.backDrop2.getX() - SCR_SPEED)
        if self.backDrop2.getX() <= -20:
                self.backDrop2.setX(20)
        return Task.again
    #scrolls the mountains
    def scrollMountains(self,task):
        ## print "Scrolling Mountains"
        num = len(self.mountains)
        i = 0
        while i < num:
            self.mountains[i].setX(self.mountains[i].getX() - SCR_SPEED)
            if self.mountains[i].getX() <= -10:
                self.mountains[i].removeNode()
                self.mountains.pop(i)
                i -= 1
                num = len(self.mountains)
                if self.firing == True:
                    taskMgr.remove("eBaseFire")
                    self.firing = False
                    print "firing reset"
            i += 1
        return Task.again
        
        # move the mountains to the left 
        # When the model is too far to the left
            # delete the model
            # remove the pointer from the list
                # this will change the index of the array
            # readjust the index so that it is correct
            # go to the next index
        #Rerun task
    
    

    def createMountain(self,task):
        # Create a random mountain and append it to the mountain list
        self.r = randint(0,2)        #Random Mountain Selection Variable
        print self.r
        if self.r == 2:
            self.m2 = loader.loadModel("Models/mountain3.egg")
            self.m2.reparentTo(render)
            self.m2.setScale(0.08)                        #Adjust scale
            self.m2.setPosHpr(8,-.1,-2.38,  0,-1,0)       #Adjust positioning
        
                        #ASSUMING YOU HAVE YOUR MOUNTAINS IN THE ARRAY CALLED: self.mountains
            self.mountains.append(self.m2)                #Append it to the mountains array
            self.makeEBase()
            # Rerun the task
            return Task.again
            #used m2 to differentiate between the right mountain for the base to be placed on.
            return self.m2
        else:
            self.makeEBase()
            self.m = loader.loadModel("Models/mountain" + str(self.r+1) + ".egg")# load the model
            self.m.reparentTo(render)                    #Reparent to render    
            self.m.setScale(0.08)                        #Adjust scale
            self.m.setPosHpr(8,-.1,-2.38,  0,-1,0)       #Adjust positioning
            
            #ASSUMING YOU HAVE YOUR MOUNTAINS IN THE ARRAY CALLED: self.mountains
            self.mountains.append(self.m)                #Append it to the mountains array
            
            # Rerun the task
            return Task.again
            return self.m
    
    ## def createLives(self):
        ## l = loader.loadModel("Models/playerShip" + ".egg")# load the model
        ## l.reparentTo(render)                    #Reparent to render    
        ## l.setScale(0.08)                        #Adjust scale
        l.setPosHpr(8,-.1,-2.38,  0,-1,0) 
    #idle function, thought it would help with something at some point.
    ## def returnHealth(self):
        ## return self.pHealth
        ## print self.pHealth
    #used to help with hiding the final score which did not hide correctly before
    def preStart(self):
        self.scoreFinal.hide()
        self.startGame()
    
    #regenerates plasma and pulse over time
    def regenPlasma(self, task):
        if self.pPlasma <= 100:
            self.pPlasma += 10
        return Task.again
    
    def regenPulse(self, task):
        if self.pPulse <= 100:
            self.pPulse += 10
        return Task.again
    
    #ends the game
    def gameOver(self):
        
        #Stop updating the game.
        taskMgr.remove("updateTask")
        
        
        # Remove the enemy bullets
        self.BManager.ignore('fire_bullet') #Ignore messages
        self.BManager.ignore('destroy_bullet')
        
        #Loop through the dictionary of created bullets
        # and remove the models for each
        ## for k,v in self.bulletManager.bullets.iteritems():
            ## self.bulletManager.bullets[k].destroyModels()
            ## print "key", k
            ## print "value", v
        
        
        #Stop spawning enemy ships
        #ends the manager
        taskMgr.remove("spawnEnemyShip")
        taskMgr.remove("scrollMountain")
        taskMgr.remove("createMountain")
        taskMgr.remove("scrollBackDrop1")
        taskMgr.remove("scrollBackDrop2")
        taskMgr.remove("regeneratePlasma")
        taskMgr.remove("regeneratePulse")
        ## if self.firing == True:
            ## tskMgr.remove("eBaseFire")
        ## self.mountains.removeNode()
        self.backDrop1.removeNode()
        self.backDrop2.removeNode()
        
        ## for i in range(len(self.mountains)):
            ## self.mountains[i] = None
            
        for i in range(len(self.mountains)):
            self.mountains[i].removeNode()
            
        for name,data in self.EManager.enemies.iteritems():
            self.EManager.enemies[name].destroyModels()
        
        for name,data in self.BManager.bullets.iteritems():
            self.BManager.bullets[name].destroyModels()
            
        #Loop through the dictionary of created enemies
        # Remove existing enemy ships
        self.EManager.ignore('destroy_enemy')
        ## for k,v in self.enemyManager.enemies.iteritems():
            ## self.enemyManager.enemies[k].destroyModels()
            ## print "key", k
            ## print "value", v
        
        #Remove the player model and collider
        self.playerC.removeNode()
        self.player.removeNode()
        
        #Clear and remove the collision handler
        self.CollisionHandler.clear()
        self.collisionHandler = None
        
        
        #Clear the colliders and reset the variable
        base.cTrav.clearColliders()
        base.Ctrav = None
        

        #Remove the mountain tasks
        #Remove the mountains models

        
        #Remove the backdrop task
        #Remove the backdrop
            
                    
        # Get rid of screen/ui nodes
        self.healthBar.hide()
        self.ui.hide()
        self.shieldBar.hide()
        self.plasmaBar.hide()
        self.pulseBar.hide()
        #Display end message and wait for player to make a decision
        #Move the score to the center of the screen for the player to see
        self.scoreFinal = OnscreenText(text="You Scored " + str(self.score) + " Points", 
                                       style=1, fg=(1,.7,0,1), pos=(0,0,0), scale = .1)
        self.scoreFinal.show()
        self.startScreen.setTexture(self.endScreenTex,1)
        self.startScreen.show()
        # Restart game when Space is pressed
        self.accept('space', self.preStart)
        self.scoreText.hide()
        self.enemiesText.hide()
        self.l.hide()
        self.l2.hide()
        self.l3.hide()
    
    def resetPlayer(self):
        # move the player to the spawn point, reset health and energy levels
        self.player.setPos(PSPAWN)
        self.pHealth = MAXH
        self.pShield = 100
        self.pPulse = 100
        self.pPlasma = 100
        self.shieldMod.show()
    def resetCanFire(self):
        # reset the can fire variable
        ## self.f2 = Func(self.resetFire)
        ## s = Sequence(Wait(1), self.f2)
        self.canFire = True
        print "reset can fire"
    
    def resetFire(self):
        self.canFire = True
        print "resetFire"
##############################################################################        
                
    def quit(self):
        # exit out of the game 
        print "good bye"
        sys.exit()
        
##############################################################################



w = World()  # create an instance of class World and assign "it" to variable w
run()