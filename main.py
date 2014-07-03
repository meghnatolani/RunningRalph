from math import pi, sin, cos
 

from gameGuiMgr import gameGUI

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from pandac.PandaModules import CollisionTraverser,CollisionNode
from pandac.PandaModules import CollisionHandlerQueue,CollisionRay , CollisionSphere , CollisionPolygon
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from pandac.PandaModules import Vec3,Vec4,BitMask32 , Point3
import random, sys, os, math
from pandac.PandaModules import Filename
from panda3d.ai import *
from pandac.PandaModules import loadPrcFileData
from direct.gui.DirectGui import *
from pandac.PandaModules import loadPrcFileData , TransparencyAttrib

#Set default settings
loadPrcFileData("", "win-size 700 500")
loadPrcFileData("", "window-title Run Run!")
loadPrcFileData("", "fullscreen #f")
loadPrcFileData("", "interpolate-frames 1")

MYDIR=os.path.abspath(sys.path[0])
MYDIR=Filename.fromOsSpecific(MYDIR).getFullpath()

finishme = 0

class Myclass(ShowBase):
    """docstring for Myclass"""
    def __init__(self):
        ShowBase.__init__(self)

        self.playerGUI = gameGUI()
        self.numObjects = 200;
        self.again = 0
        
        self.setBackgroundColor(.6, .6, 1)
        self.evrn = self.loader.loadModel(MYDIR+"/world/world")
        self.evrn.reparentTo(self.render)
        self.evrn.setScale(3)
        self.evrn.setPos(0,0,0)
        self.evrn.setCollideMask(BitMask32.bit(1))
        
        self.sky = self.loader.loadModel(MYDIR+"/alice-skies--happysky/happysky")
        self.sky.reparentTo(self.render)
        self.sky.setScale(3)
        self.sky.setPos(-10,-50,5)   

        self.house = self.loader.loadModel(MYDIR+"/dojo/dojo")
        self.house.reparentTo(self.evrn)
        self.house.setScale(0.032)
        self.house.setPos(30,30,4)
        self.house.setHpr(90,0,0)

        self.house.setCollideMask(BitMask32.bit(1))
        self.rect = CollisionSphere(0,0,0,300)
        self.rectnode = CollisionNode('houserect')
        self.rectnode.addSolid(self.rect)
        self.rectnode.setCollideMask(BitMask32.bit(1))
        self.houserectad = self.house.attachNewNode(self.rectnode)
        #self.houserectad.show()

        self.placeCollectibles()
        self.loadMenu()
        self.loadcharacter()
        
       
        
    def loadcharacter(self):

        self.ralphstartpos = Point3(-350,-150,9)
        self.player = Character(MYDIR+"/ralph/ralph",MYDIR+"/ralph/ralph-run",MYDIR+"/ralph/ralph-walk",self.ralphstartpos, 1.2,1,self.playerGUI)
        ralph = self.player.getactor()

        self.accept("j", self.player.setControl, ["left",1])
        self.accept("l",  self.player.setControl, ["right",1])
        self.accept("i",  self.player.setControl, ["forward",1])
        self.accept("j-up",  self.player.setControl, ["left",0])
        self.accept("l-up", self.player.setControl, ["right",0])
        self.accept("i-up", self.player.setControl, ["forward",0])

        camera = Camera(self.player.actor)

        self.accept("a-up", camera.setControl, ["left",0])
        self.accept("s-up", camera.setControl, ["right",0])
        self.accept("a", camera.setControl, ["left",1])
        self.accept("s", camera.setControl, ["right",1])
        
        self.dino = Agent(MYDIR+"/trex/trex",MYDIR+"/trex/trex-run",MYDIR+"/trex/trex-run",(-350,120,3),1.2,2,ralph,self.playerGUI)

        

    def placeCollectibles(self):
        self.placeCol = render.attachNewNode("Collectible-Placeholder")
        self.placeCol.setPos(0,0,0)
        
        # Add the health items to the placeCol node
        for i in range(self.numObjects):
            # Load in the health item model
            self.collect = loader.loadModel(MYDIR+"/ball/jack")
            self.collect.setPos(0,0,0)
            self.collect.setH(90)
            self.collect.setScale(2)
            self.collect.reparentTo(self.placeCol)
            
            self.placeItem(self.collect)
            
            # Add spherical collision detection
            colSphere = CollisionSphere(0,0,0,1)
            sphereNode = CollisionNode('colSphere')
            sphereNode.addSolid(colSphere)
            sphereNode.setFromCollideMask(BitMask32.allOff())
            sphereNode.setIntoCollideMask(BitMask32.bit(1))
            sphereNp = self.collect.attachNewNode(sphereNode)
            
    def placeItem(self, item):
        # Add ground collision detector to the health item
        self.cTrav1 = CollisionTraverser()

        self.collectGroundRay = CollisionRay()
        self.collectGroundRay.setOrigin(0,0,300)
        self.collectGroundRay.setDirection(0,0,-1)
        self.collectGroundCol = CollisionNode('colRay')
        self.collectGroundCol.addSolid(self.collectGroundRay)
        self.collectGroundCol.setFromCollideMask(BitMask32.bit(1))
        self.collectGroundCol.setIntoCollideMask(BitMask32.allOff())
        self.collectGroundColNp = item.attachNewNode(self.collectGroundCol)
        self.collectGroundHandler = CollisionHandlerQueue()
        base.cTrav1.addCollider(self.collectGroundColNp, self.collectGroundHandler)
        
        placed = False;
        while placed == False:
            # re-randomize position
            item.setPos(-random.randint(-350,300),-random.randint(-100,150),0)
            
            base.cTrav1.traverse(render)
            
            # Get Z position from terrain collision
            entries = []
            for j in range(self.collectGroundHandler.getNumEntries()):
                entry = self.collectGroundHandler.getEntry(j)
                entries.append(entry)
            entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                         x.getSurfacePoint(render).getZ()))
        
            if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
                item.setZ(entries[0].getSurfacePoint(render).getZ()+4)
                placed = True
                
        # remove placement collider
        #self.collectGroundColNp.removeNode()

    def start(self):
        self.playerGUI.runralph = 1
        self.playerGUI.setgamepausevalue(1)
        taskMgr.add(self.movement, "Movement")
        self.playerGUI.playend()
        self.playerGUI.initTimer()


        #Start music
        #soundMgr.playBG()

    def movement(self,task):
        '''
        taskMgr.add(self.finishGame, "Finish Game")
        Task.again
        '''
        global finishme
        if self.playerGUI.runralph == 1 and finishme == 0:
            return Task.again
        else:
            self.player.getactor().stop()
            self.dino.getactor().stop()
            taskMgr.doMethodLater(2, self.finishGame, "Finish Game")
            return Task.done
        


    def loadMenu(self):
        #Load main menu
        #Add play icon
        click = loader.loadSfx("./sounds/correct.ogg")
        self.playicon = DirectButton(image="./GUI/cloud.png", scale=.3, pos=(-0.38,0,0.21), relief=None, state=DGG.NORMAL, command=self.playGame, clickSound=click)
        self.playicon.setScale(0.3)
        self.playicon.setTransparency(TransparencyAttrib.MAlpha)

        #Play text
        play = TextNode('Play')
        play.setText("\1menu\1 Play! \2")
        self.playNP = aspect2d.attachNewNode(play)
        self.playNP.setScale(0.18)
        self.playNP.setPos(-0.7,0,0.13)

        self.playerGUI.controls()

        #Exit text and icon
        self.exiticon = DirectButton(image="./GUI/cloud.png", scale=.3, pos=(0.48,0,0.21), relief=None, state=DGG.NORMAL, command=exit, clickSound=click)
        self.exiticon.setScale(0.3)
        self.exiticon.setTransparency(TransparencyAttrib.MAlpha)
        exitx = TextNode('Exit')
        exitx.setText("\1menu\1 Exit \2")
        self.exitxNP = aspect2d.attachNewNode(exitx)
        self.exitxNP.setScale(0.18)
        self.exitxNP.setPos(0.22,0,0.13)

    def playGame(self):
        #Unload menu
        
        self.playicon.destroy()
        self.exiticon.destroy()
        self.playNP.removeNode()
        self.exitxNP.removeNode()
        self.playerGUI.controlsleftNP.removeNode()
        self.playerGUI.controlsrightNP.removeNode()
        self.playerGUI.controlsforwardNP.removeNode()
        self.playerGUI.controlscameraaNP.removeNode()
        self.playerGUI.controlscamerasNP.removeNode()
        self.playerGUI.instructions1NP.removeNode()

        if self.again:
            self.playerGUI.reset()
            #self.restartgame()
            self.player.getactor().cleanup()
            self.player.getactor().removeNode()
            self.dino.getactor().cleanup()
            self.dino.getactor().removeNode()

            self.loadcharacter()
            
        #Start game
        self.countdw = 3
        taskMgr.doMethodLater(1, self.countDown, "Count Down")

    def restartgame(self):
        self.numObjects = 200;
        self.player.getactor().setPos(self.ralphstartpos)
        self.dino.getactor().setPos(-350,120,3)
        self.time = 0
        base.camera.setPos(self.player.getactor().getX()-30,self.player.getactor().getY()-10,self.player.getactor().getZ()+7)
        camera.setHpr(-60,0,0)
        #self.placeHealthItems()
        self.placeCollectibles()
        #taskMgr.add(self.move,"moveTask")
        #taskMgr.doMethodLater(0.5, self.healthDec, "healthTask")

    
    def finishGame(self, task):
        global finishme
        #if finishme == 0 and self.playerGUI.runralph == 1:
         # Task.cont
        #check if finish global is 1 toh continue else return task.cont
        #Check if there's a new record
        if self.playerGUI.points > self.playerGUI.record:
            self.playerGUI.setRecord(self.playerGUI.points)
        #else:
            #soundMgr.playSnd("./sounds/opening.ogg",1,False)
        self.again = 1
        self.playerGUI.setgamepausevalue(0)

        #self.player.getactor().stop()
        #self.dino.getactor().stop()

        taskMgr.remove("moveTask")
        taskMgr.remove("AIUpdate")
        taskMgr.remove("cameraMoveTask")
        #taskMgr.remove("TicTac")
        finishme = 0
        self.playerGUI.picked = 0
        self.loadMenu()

    def countDown(self, task):
        #Start countdown
        if self.countdw >= -1:
           if self.countdw == 0:
               self.start()
           self.playerGUI.setCount(self.countdw)
           self.countdw -= 1
           return Task.again
        else:
            return Task.done
    

class Character:

    def __init__(self, model, run, walk, startPos, scale,select,saysome):
        
        self.playerGUI = saysome
        print(self.playerGUI.getpausevalue())
        self.controlMap = {"left":0, "right":0, "forward":0}
        self.select = select
        self.actor = Actor(model, {"run":run, "walk":walk})
        self.actor.reparentTo(render)
        self.actor.setScale(scale)
        self.actor.setPos(startPos)
        self.actor.setHpr(90,0,0)

        taskMgr.add(self.move,"moveTask")

        self.prevtime = 0
        self.isMoving = False
        
        self.cTrav = CollisionTraverser()

        self.groundRay = CollisionRay(0,0,1000,0,0,-1)  
        self.groundCol = CollisionNode('ralphRay')
        self.groundCol.addSolid(self.groundRay)
        self.groundCol.setFromCollideMask(BitMask32.bit(1))
        self.groundCol.setIntoCollideMask(BitMask32.allOff())
        self.groundColNp = self.actor.attachNewNode(self.groundCol)
        self.groundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.groundColNp, self.groundHandler)

        self.sphere = CollisionSphere(0,0,0,3)
        self.spherecol = CollisionNode('ralphSphere')
        self.spherecol.addSolid(self.sphere)
        self.spherecol.setFromCollideMask(BitMask32.bit(1))
        self.spherecol.setIntoCollideMask(BitMask32.allOff())
        self.ralphcolhs = self.actor.attachNewNode(self.spherecol)
        self.ralphcolhandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.ralphcolhs , self.ralphcolhandler)

        #self.ralphcolhs.show()

        #self.groundColNp.show()
        #self.cTrav.showCollisions(render)

    def setControl(self, control, value):

        self.controlMap[control] = value


    def move(self, task):
        global finishme
        self.wonagain = 0
        
        elapsed = task.time - self.prevtime
        startpos = self.actor.getPos()
        #print(startpos)
        if self.playerGUI.getpausevalue():
            if(self.select == 1):

                if (self.controlMap["left"]!=0):
                    self.actor.setH(self.actor.getH() + elapsed*300)

                if (self.controlMap["right"]!=0):
                    self.actor.setH(self.actor.getH() - elapsed*300)

                if (self.controlMap["forward"]!=0):
                    backward = self.actor.getNetTransform().getMat().getRow3(1)
                   
                    backward.setZ(0)
                    backward.normalize()
                    
                    self.actor.setPos(self.actor.getPos() - backward*(elapsed*20))
                    #print("pos",self.actor.getPos())

                if (self.controlMap["forward"]!=0) or (self.controlMap["left"]!=0) or (self.controlMap["right"]!=0):
                   
                    if self.isMoving is False:
                        self.actor.loop("run")
                        self.isMoving = True
                else:
                    if self.isMoving:
                        self.actor.stop()
                        self.actor.pose("walk",5)
                        self.isMoving = False


        self.cTrav.traverse(render)
        
        entries = []
        for i in range(self.groundHandler.getNumEntries()):
            entry = self.groundHandler.getEntry(i)
            #print()
            entries.append(entry)
        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))

        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            self.actor.setZ(entries[0].getSurfacePoint(render).getZ())
        else:
            self.actor.setPos(startpos)


        for x in range(self.ralphcolhandler.getNumEntries()):
            ent = self.ralphcolhandler.getEntry(x)
            if(ent.getIntoNode().getName() == "houserect"):
                #print("hurryyyyy")
                self.won = OkDialog(dialogName="YOUR GAME STATUS", text="YOU WON!!!!!",command=self.showDialog1)
                self.playerGUI.playSnd("./sounds/incarnation_mono.ogg",1,False)
                self.wonagain = 1
                finishme = 1
                self.playerGUI.picked = 1

                
            if(ent.getIntoNode().getName() == "dinoSphere"):
                self.playerGUI.playSnd("./sounds/monsterGrowl.ogg",1,False)
                if self.wonagain == 0:
                    self.loss = OkDialog(dialogName="YOUR GAME", text="YOU LOST",command=self.showDialog)
                finishme = 1
                self.playerGUI.picked = 1
                #need to call finish from the above class

            if(ent.getIntoNode().getName() == "colSphere"):
                self.playerGUI.playSnd("./sounds/item_ok.ogg",1,False)
                ent.getIntoNodePath().getParent().removeNode()
                self.playerGUI.addcandy()
                self.playerGUI.addPoints(100)

        # Store the task time and continue.
        self.prevtime = task.time
        return Task.cont

    def showDialog(self,arg):
        self.loss.cleanup()

    def showDialog1(self,arg):
        self.won.cleanup()

    def getactor(self):
        return self.actor


class Camera:
    def __init__(self,actor):

        self.actor = actor
        self.prevtime = 0
        self.controlMap = {"left":0, "right":0}

        taskMgr.add(self.move,"cameraMoveTask")
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        base.disableMouse()
        #base.camera.setPos(self.actor.getX(),self.actor.getY()+10,2)
        base.camera.setPos(self.actor.getX()-30,self.actor.getY()-10,self.actor.getZ()+7)
        camera.setHpr(-60,0,0)

        self.cTrav = CollisionTraverser()
        self.groundRay = CollisionRay()
        self.groundRay.setOrigin(0,0,1000)
        self.groundRay.setDirection(0,0,-1)
        self.groundCol = CollisionNode('camRay')
        self.groundCol.addSolid(self.groundRay)
        self.groundCol.setFromCollideMask(BitMask32.bit(1))
        self.groundCol.setIntoCollideMask(BitMask32.allOff())
        self.groundColNp = base.camera.attachNewNode(self.groundCol)
        self.groundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.groundColNp, self.groundHandler)

        self.groundColNp.show()

    def move(self,task):
        elapsed = task.time - self.prevtime

        base.camera.lookAt(self.actor)
        camright = base.camera.getNetTransform().getMat().getRow3(0)
        camright.normalize()
        if (self.controlMap["left"]!=0):
            base.camera.setPos(base.camera.getPos() - camright*(elapsed*50))
        if (self.controlMap["right"]!=0):
            base.camera.setPos(base.camera.getPos() + camright*(elapsed*50))


        camvec = self.actor.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        #print(camdist)
        camvec.normalize()
        if (camdist > 30.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-30))
            camdist = 30.0
        if (camdist < 15.0):
            base.camera.setPos(base.camera.getPos() - camvec*(15-camdist))
            camdist = 15.0

        self.cTrav.traverse(render)

        entries = []
        for i in range(self.groundHandler.getNumEntries()):
            entry = self.groundHandler.getEntry(i)
            entries.append(entry)
            #print(entry)

        entries.sort(lambda x,y: cmp(y.getSurfacePoint(render).getZ(),
                                     x.getSurfacePoint(render).getZ()))
        if (len(entries)>0) and (entries[0].getIntoNode().getName() == "terrain"):
            base.camera.setZ(entries[0].getSurfacePoint(render).getZ()+4.0)
        if (base.camera.getZ() < self.actor.getZ() + 8.0):
            base.camera.setZ(self.actor.getZ() + 8.0)

        self.floater.setPos(self.actor.getPos())
        self.floater.setZ(self.actor.getZ() + 8.0)

        base.camera.lookAt(self.floater)
        #print("camer1" ,camera.getHpr())
        self.prevtime = task.time
        return Task.cont

    def setControl(self, control, value):

        self.controlMap[control] = value

class Agent:
    def __init__(self, model, run, walk, startPos, scale, select,ralph,saysome):

        self.actor = Actor(model, {"run":run, "walk":walk})
        self.actor.reparentTo(render)
        self.actor.setScale(scale)
        self.actor.setPos(startPos)
        self.actor.setHpr(90,0,0)
        self.playerGUI = saysome
        self.myralph = ralph
        self.setAI()

        self.cTrav = CollisionTraverser()

        self.groundRay = CollisionRay(0,0,1000,0,0,-1)  
        self.groundCol = CollisionNode('dinoRay')
        self.groundCol.addSolid(self.groundRay)
        self.groundCol.setFromCollideMask(BitMask32.bit(1))
        self.groundCol.setIntoCollideMask(BitMask32.allOff())
        self.groundColNp = self.actor.attachNewNode(self.groundCol)
        self.groundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.groundColNp, self.groundHandler)

        self.sphere = CollisionSphere(0,0,5,13)
        self.spherecol = CollisionNode('dinoSphere')
        self.spherecol.addSolid(self.sphere)
        self.spherecol.setCollideMask(BitMask32.bit(1))
        self.dinocolhs = self.actor.attachNewNode(self.spherecol)

        #self.dinocolhs.show()
        #self.groundColNp.show()
        #self.cTrav.showCollisions(render)

    def setAI(self):
        #Creating AI World
        self.AIworld = AIWorld(render)
 
        self.AIchar = AICharacter("seeker",self.actor, 380, 50, 250)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()  
        self.AIbehaviors.pursue(self.myralph)

        self.actor.loop('run')
        
        #AI World update        
        taskMgr.add(self.AIUpdate,"AIUpdate")
        
    #to update the AIWorld    
    def AIUpdate(self,task):
        if self.playerGUI.getpausevalue():
            self.AIworld.update()            
        return Task.cont

    def setControl(self, control, value):
        self.controlMap[control] = value

    def getactor(self):
        return self.actor



w = Myclass()
w.run()

