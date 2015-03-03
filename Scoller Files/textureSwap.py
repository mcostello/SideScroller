from direct.task import Task

def playTexture(mod, texList, loop, speed, name, seq = None):
    # setup and start an animated texture
    t = taskMgr.doMethodLater(speed, playTex, name)
    t.mod = mod
    t.texList = texList
    t.index = 0
    t.loop = loop
    t.seq = seq
    ## print "setup for texture", name

def playTex(task):
    tex = task.texList[task.index]
    task.mod.setTexture(tex,1)
    if tex == task.texList[-1] and task.loop:
        # if at the end and loop then reset the index to 0 
        task.index = 0 
        return Task.again
    elif tex == task.texList[-1] and not task.loop:
        # if at the end and don't loop then if a sequence was provided 
        # start it and then quit this task
        if task.seq != None:
            task.seq.start()
        return Task.done     
    else:
        # not at the end so increase the index and call again
        task.index += 1
        return Task.again
    
def stopTexture(name):
    # stop the texture from playing by removing the task
    taskMgr.remove(name)
    
    
    
    
## s = Sequence(Wait(2), Func(self.plate.removeNode))  # what to do when the texture gets done playing
        ## playTexture(self.plate, self.plateTex, 0, ANI_SPEED, self.plate.getName() + "tex", s)
        
        ## t = taskMgr.doMethodLater(1, self.playT, "t", extraArgs = [ 0,0], appendTask = True)
                                  
    
    ## def playT(self, mod, index, task):
        ## print index, task.time
        ## index += 1
        ## return Task.again
    
