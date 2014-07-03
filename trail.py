from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from pandac.PandaModules import CollisionTraverser,CollisionNode
from pandac.PandaModules import CollisionHandlerQueue,CollisionRay
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode

from direct.task.Task import Task
from pandac.PandaModules import Vec3,Vec4,BitMask32
import random, sys, os, math


class Myclass(ShowBase):
    """docstring for Myclass"""
    def __init__(self):
        ShowBase.__init__(self)

        self.setBackgroundColor(.6, .6, 1)
        self.evrn = self.loader.loadModel("my my/my game/world/world")
        self.evrn.reparentTo(self.render)
        self.evrn.setScale(3)
        self.evrn.setPos(0,0,0)
        

        #print(BitMask32.bit(1))
        #print(self.evrn.find("**/start_point").getPos())

        self.house = self.loader.loadModel("my my/my game/dojo/dojo")
        self.house.reparentTo(self.evrn)
        self.house.setScale(0.032)
        self.house.setPos(30,30,6)
        self.house.setHpr(90,0,0)
        player = Character("my my/my game/ralph/ralph","my my/my game/ralph/ralph-run","my my/my game/ralph/ralph-walk",(-350,-150,9), 1.2)

        camera = Camera(player.actor)

class Character:

    def __init__(self, model, run, walk, startPos, scale):

    	self.actor = Actor(model, {"run":run, "walk":walk})
        self.actor.reparentTo(render)
        self.actor.setScale(scale)
        self.actor.setPos(startPos)
        self.actor.setHpr(90,0,0)

class Camera:
    def __init__(self,actor):

        self.actor = actor

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        
        base.disableMouse()
        base.camera.setPos(self.actor.getX()-30,self.actor.getY()-10,self.actor.getZ()+7)
        camera.setHpr(-60,0,0)

w = Myclass()
w.run()

'''
import direct.directbase.DirectStart
from pandac.PandaModules import CollisionTraverser,CollisionNode
from pandac.PandaModules import CollisionHandlerQueue,CollisionRay
from pandac.PandaModules import Filename
from pandac.PandaModules import PandaNode,NodePath,Camera,TextNode
from pandac.PandaModules import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math

# Figure out what directory this program is in.
MYDIR=os.path.abspath(sys.path[0])
MYDIR=Filename.fromOsSpecific(MYDIR).getFullpath()

class Camera:

    def __init__(self,actor):

        self.actor = actor
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)        

        # Set up the camera.

        base.disableMouse()
        base.camera.setPos(self.actor.getX(),self.actor.getY()+10,2)

class Character:

    def __init__(self, model, run, walk, startPos, scale):

        self.actor = Actor(model, {"run":run, "walk":walk})
        self.actor.reparentTo(render)
        self.actor.setScale(scale)
        self.actor.setPos(startPos)


class Game(DirectObject):

    def __init__(self):

        #environ = loader.loadModel(MYDIR+"/models/world/world")
        environ = loader.loadModel("my my/my game/world/world")
        environ.reparentTo(render)
        environ.setPos(0,0,0)
        player = Character("my my/my game/ralph/ralph","my my/my game/ralph/ralph-run","my my/my game/ralph/ralph-walk",environ.find("**/start_point").getPos(),.2)
        camera = Camera(player.actor)
if __name__ == "__main__":        
    
    game = Game()
    run()
'''