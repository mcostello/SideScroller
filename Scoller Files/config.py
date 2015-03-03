from pandac.PandaModules import *
# constants
DOWN = 1
ANI_SPEED = .03 # in seconds, how long to wait between texture frames 
SCR_SPEED = .1 # how fast should the back drop scroll
SCR_DIST = 0.1  # how far should the back drop scroll in a given step
MNT_DELAY = 1   # every n seconds create a random mountain
PSPAWN = Point3(-4,-.2,0)       # spawning point for the player ship
MAXH = 100      # the max number of health points
MAXE = 100      # the max number of energy points
NUM_LIVES = 3   # the number of lives the player gets
MAX_VH = 2.6    # the highest the player ship can move vertically
MIN_VH = -3.4   # the lowest the player ship can move vertically
MAX_HW = 4.5    # the farthest right the player ship can move horizontally
MIN_HW = -4.5   # the farthest left the player ship can move horizontally
ESPAWN_X = 6    # the enemy ships spawning x coordinate
E_Z_MAX = 18    # the enemy ships spawning max z coordinate -- mult by .1
E_Z_MIN = -3    # the enemy ships spawning min z coordinate -- mult by .1
E_X_MIN = -6    # destroy any enemy ships who's x coordinate is less then this
E_X_MAX = 5     # destroy any bullet who's x coordinate is less then this
E_SPAWN = .8     # spawn an enemy ship every n seconds
MT_DAM = 1      # how much damage the player takes from hitting a mountain
ES_DAM = 10     # how much damage the player takes from hitting an enemy ship
EB_DAM = 5      # how much damage the player takes from hitting an enemy bullet
FIRE_DELAY = 1  # how many seconds between firing 
PBPULSE_SPAWN = Point3(.54,0,-.26)       # spawning point for the player pulse bullet
PBPLASMA_SPAWN = Point3(.55,0,-.27)      # spawning point for the player plasma bullet
SCORE_E = 10    # how many points you receieve for destroying an enemy ship 
EFIRE_DELAY = 1  # how long between firing for enemy ships
ESBPULSE_SPAWN = Point3(-.51,0,-.39)      # spawning point for the enemy scout pulse bullet
ESBPLASMA_SPAWN = Point3(-.77,0,-.17)     # spawning point for the enemy scout plasma bullet
ESBMINE_SPAWN = Point3(.2,-.01,-.3)       # spawning point for the enemy scout mine 
ERBLPULSE_SPAWN = Point3(-.47,0,-.56)     # spawning point for the enemy raider lower pulse bullet
ERBTPULSE_SPAWN = Point3(-.47,0,.56)      # spawning point for the enemy raider top pulse bullet
ERBLPLASMA_SPAWN = Point3(-.72,0,-.35)     # spawning point for the enemy raider lower plasma bullet
ERBTPLASMA_SPAWN = Point3(-.72,0,.35)     # spawning point for the enemy raider top plasma bullet
BSCR_SPEED = .5

# debug constants
SHOW_C = False   # show colliders

# Panda window placement 
ORIGIN = "win-origin 10 25"
SIZE = "win-size 1024 768"
TITLE = "window-title Moon Command"

