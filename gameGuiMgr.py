    
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.task.Task import Task
from pandac.PandaModules import TextNode, TextProperties, TextPropertiesManager
from pandac.PandaModules import TransparencyAttrib , Filename
from random import random, choice
import os , sys


class gameGUI(DirectObject):
    def __init__(self):
        self.points = 0
        self.timersecs = 60
        self.duration = 0
        self.ncandy = 0
        self.runralph = 0
        self.gamepause = 0
        self.picked = 0

        self.bg = loader.loadSfx("./sounds/faster_than_all.ogg")
        self.bg.setLoop(True)
        self.bg.setVolume(0.3)
        self.bgcount = loader.loadSfx("./sounds/panic.ogg")
        self.bgcount.setLoop(False)
        self.bgcount.setVolume(1)

        self.playBG()

        butaicon = OnscreenImage(image = './GUI/smiley1.png', pos = (0.66, 0, 0.85))
        butaicon.setScale(0.12,0,0.11)
        butaicon.setTransparency(TransparencyAttrib.MAlpha)

        tpButa = TextProperties()
        tpButa.setTextColor(1,1,1,1)
        butafont = loader.loadFont('./GUI/fonts/butafont.ttf')
        tpButa.setFont(butafont)
        tpButa.setShadow(0.05, 0.05)
        tpButa.setShadowColor(0,0,0,1)
        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpMgr.setProperties("buta", tpButa)
        tpMenu = TextProperties()
        tpMenu.setTextColor(1,0.6,0.75,1)
        tpMenu.setFont(butafont)
        tpMenu.setShadow(0.05, 0.05)
        tpMenu.setShadowColor(1,0.8,0.9,1)
        tpMgr.setProperties("menu", tpMenu)

        #Add candy number
        self.candy = TextNode('Candy Number')
        self.candy.setText("\1buta\1x "+str(self.ncandy)+" \2")
        self.candynumNP = aspect2d.attachNewNode(self.candy)
        self.candynumNP.setScale(0.18)
        self.candynumNP.setPos(0.79, 0, 0.8)

         #Add points number
        self.ptnum = TextNode('Pt Number')
        self.ptnum.setText("\1buta\1Pt. "+str(self.points)+" \2")
        self.ptnumNP = aspect2d.attachNewNode(self.ptnum)
        self.ptnumNP.setScale(0.18)
        self.ptnumNP.setPos(-1.31, 0, 0.8)

         #Add record number
        
        recordfile = open("candyrecord.dat","r")
        self.record = int(recordfile.read())
        recordfile.close()
        self.rcnum = TextNode('Record Number')
        self.rcnum.setText("\1buta\1Record \n"+str(self.record)+" \2")
        self.rcnumNP = aspect2d.attachNewNode(self.rcnum)
        self.rcnumNP.setScale(0.11)
        self.rcnumNP.setPos(-1.38, 0, 0.65)
        self.rcnum.setWordwrap(4.5)

        #Add timer
        self.timer = TextNode('Timer')
        self.timer.setText("\1buta\1 "+str(self.timersecs/60)+":00 \2")
        self.timerNP = aspect2d.attachNewNode(self.timer)
        self.timerNP.setScale(0.18)
        self.timerNP.setPos(0.9,0,-0.93)

        
        self.itemset = {"musicon":loader.loadTexture('./GUI/soundon.png'),"musicoff":loader.loadTexture('./GUI/soundoff.png'),}
        self.itembox = DirectButton(image=self.itemset["musicon"], scale=.10, pos=(-1.19,0,-0.82), relief=None, state=DGG.NORMAL, command=self.changemusic, clickSound=None)
        self.itembox.setScale(0.15)
        self.itembox.setTransparency(TransparencyAttrib.MAlpha)

    def controls(self):
            self.controlsleft = TextNode('controlsleft')
            self.controlsleft.setText("\1buta\1J-Left \2")
            self.controlsleftNP = aspect2d.attachNewNode(self.controlsleft)
            self.controlsleftNP.setScale(0.07)
            self.controlsleftNP.setPos(-1.38, 0, 0.31)

            self.controlsforward = TextNode('controlsforward')
            self.controlsforward.setText("\1buta\1I-Forward \2")
            self.controlsforwardNP = aspect2d.attachNewNode(self.controlsforward)
            self.controlsforwardNP.setScale(0.07)
            self.controlsforwardNP.setPos(-1.38, 0, 0.20)

            self.controlsright = TextNode('controlsright')
            self.controlsright.setText("\1buta\1L-Right \2")
            self.controlsrightNP = aspect2d.attachNewNode(self.controlsright)
            self.controlsrightNP.setScale(0.07)
            self.controlsrightNP.setPos(-1.38, 0, 0.11)

            self.controlscameraa = TextNode('controlscameraa')
            self.controlscameraa.setText("\1buta\1A-Rotate camera left \2")
            self.controlscameraaNP = aspect2d.attachNewNode(self.controlscameraa)
            self.controlscameraaNP.setScale(0.07)
            self.controlscameraaNP.setPos(-1.38, 0, -0.07)

            self.controlscameras = TextNode('controlscameras')
            self.controlscameras.setText("\1buta\1S-Rotate camera right \2")
            self.controlscamerasNP = aspect2d.attachNewNode(self.controlscameras)
            self.controlscamerasNP.setScale(0.07)
            self.controlscamerasNP.setPos(-1.38, 0, -0.16)
            '''
            self.con = TextNode('con')
            self.con.setText("\1buta\1S-Rotate camera right \2")
            self.conNP = aspect2d.attachNewNode(self.con)
            self.conNP.setScale(0.11)
            self.conNP.setPos(-1.38, 0, -0.20)
            '''
            self.instructions1 = TextNode('instructions1')
            self.instructions1.setText("\1buta\1Reach the House in minimum time collect smileys taking care of dinosorus \2")
            self.instructions1NP = aspect2d.attachNewNode(self.instructions1)
            self.instructions1NP.setScale(0.07)
            self.instructions1NP.setPos(-1.38, 0, -0.40)

    def changemusic(self):
        
        if self.itembox["image"] == self.itemset["musicon"]:
            self.itembox["image"] = self.itemset["musicoff"]
            self.stopBG()
            #gamesoundMgr.stopBG()
        else:
            self.itembox["image"] = self.itemset["musicon"]
            #gamesoundMgr.playBG()
            self.playBG()

    def playend(self):
        '''
        self.playpause = {"play":loader.loadTexture('./GUI/play.png'),"pause":loader.loadTexture('./GUI/pause.png'),}
        self.playpauseclick = DirectButton(image=self.playpause["play"], scale=.10, pos=(-.95,0,-0.82), relief=None, state=DGG.NORMAL, command=self.gameplypause, clickSound=None)
        self.playpauseclick.setScale(0.10)
        self.playpauseclick.setTransparency(TransparencyAttrib.MAlpha)
        '''
        self.playexit = DirectButton(image='./GUI/exit.png', scale=.10, pos=(-.95,0,-0.82), relief=None, state=DGG.NORMAL, command=exit, clickSound=None)
        self.playexit.setScale(0.10)
        self.playexit.setTransparency(TransparencyAttrib.MAlpha)


    def gameplypause(self):

        if self.playpauseclick["image"] == self.playpause["play"]:
            self.playpauseclick["image"] = self.playpause["pause"]
            #gamesoundMgr.stopBG()
        else:
            self.playpauseclick["image"] = self.playpause["play"]
            #gamesoundMgr.playBG()

    def gameexit(self):
        taskMgr.exit()

    def setgamepausevalue(self,value):
        self.gamepause = value

    def getpausevalue(self):
        return self.gamepause

    def stopBG(self):
        self.bg.stop()

    def playBG(self):
        self.bg.play()

    def playSnd(self,sound, volume, loop=False):
    #Play sound
        sndfx = loader.loadSfx(sound)
        sndfx.setLoop(loop)
        sndfx.setVolume(volume)
        sndfx.play()

    def playPanic(self,play):
    #Play ghost BG
        if play:
            self.bgcount.play()
        else:
            if self.bgcount.status() == 2:
               self.bgcount.stop()
     
    def initTimer(self):
        #init timer
        taskMgr.doMethodLater(1, self.tacTime, "TicTac")

    def stopTimer(self):
        #stop timer
        taskMgr.remove("TicTac")


    def tacTime(self, task):
        #reduce the time by one second
        self.timersecs -= 1

        if self.picked:
            return Task.done

        if self.timersecs > 0:
             #Start sound if time is 10 seconds
            if self.timersecs == 10: self.playPanic(True)

             #Figure out seconds
            secmod = self.timersecs%60      
              #update GUI
            if secmod < 10:
               self.timerstr = "0"+str(secmod)
            else:
                self.timerstr = str(secmod)
            self.timer.setText("\1buta\1 "+str(self.timersecs/60)+":"+self.timerstr+" \2")

            return Task.again
    #code missing do it later

        else:
            #Time out!
            self.timer.setText("\1buta\1 0:00 \2")
            self.runralph = 0
            self.playSnd("./sounds/stop!.ogg",1,False)
            return Task.done

    def addcandy(self):
        #Add picked pig
        self.ncandy += 1

         #Update GUI
        self.candy.setText("\1buta\1x "+str(self.ncandy)+" \2")

    def addPoints(self, points):
    	self.points += points
    	self.ptnum.setText("\1buta\1Pt. "+str(self.points)+" \2")

    def removePoints(self, points):
    	self.points -= points
        if self.points < 0: self.points = 0

         #Update GUI
        self.ptnum.setText("\1buta\1Pt. "+str(self.points)+" \2")

    #code missing here

    
    def setCount(self, count):
        if count == 3:
           #Start count down!
           self.counter = TextNode('Counter')
           self.counter.setText("\1buta\1Three!\2")
           self.counterNP = aspect2d.attachNewNode(self.counter)
           self.counterNP.setScale(0.2)
           self.counterNP.setPos(-0.32,0,0.77)
           self.playSnd("./sounds/count.ogg",1,False)
            
        if count == 2:
           self.counter.setText("\1buta\1Two!\2")

        if count == 1:
           self.counter.setText("\1buta\1One!\2")

        if count == 0:
           self.counter.setText("\1buta\1GO!\2")

        if count == -1:
           self.counterNP.removeNode()

    def setRecord(self, newrecord):
         #set new record
        self.playSnd("./sounds/new_record!.ogg",1,False)
        recordfile = open("candyrecord.dat","w")
        recordfile.write(str(newrecord))
        recordfile.close()
        self.record = newrecord
        self.rcnum.setText("\1buta\1Record \n"+str(self.record)+" \2")

    def reset(self):
         #State variables
        self.points = 0
        self.ncandy = 0
        self.timersecs = 60
        self.duration = 0
        self.runralph = 0
        self.picked = 0

         #Texts
        self.timer.setText("\1buta\1 "+str(self.timersecs/60)+":00 \2")
        self.rcnum.setText("\1buta\1Record \n"+str(self.record)+" \2")
        self.candy.setText("\1buta\1x "+str(self.ncandy)+" \2")
        self.ptnum.setText("\1buta\1Pt. "+str(self.points)+" \2")
